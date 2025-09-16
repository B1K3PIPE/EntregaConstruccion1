import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

# Inicializa la aplicación Flask
app = Flask(__name__)
# Habilita CORS para permitir que tu HTML (frontend) se comunique con esta API
CORS(app)

# --- Configuración de la Base de Datos ---
DB_NAME = "seguridad_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_db_connection():
    """Establece y retorna la conexión a la base de datos."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# --- Endpoint para el Historial de Accesos (GET) ---
@app.route('/api/accesos', methods=['GET'])
def get_accesos():
    print("📢 [GET] Solicitud para obtener el historial de accesos")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT marca, placa, propietario, fecha FROM accesos ORDER BY fecha DESC;")
        registros = cursor.fetchall()
        lista_registros = [
            {"marca": r[0], "placa": r[1], "propietario": r[2], "fecha": r[3].strftime('%Y-%m-%d %H:%M:%S')}
            for r in registros
        ]
        return jsonify(lista_registros)
    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")
        return jsonify({"error": "Error al obtener datos"}), 500
    finally:
        if conn:
            conn.close()

# --- Endpoint para Registrar un Vehículo (POST) ---
@app.route('/api/registrar-vehiculo', methods=['POST'])
def registrar_vehiculo():
    print("📢 [POST] Solicitud para registrar un vehículo")
    data = request.json
    marca, placa, propietario = data.get('marca'), data.get('placa'), data.get('propietario')
    
    if not all([marca, placa, propietario]):
        print("❌ Datos incompletos")
        return jsonify({"error": "Faltan datos en la solicitud"}), 400
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accesos (marca, placa, propietario) VALUES (%s, %s, %s);",
            (marca, placa, propietario)
        )
        conn.commit()
        print(f"✅ Nuevo vehículo registrado: {placa}")
        return jsonify({"mensaje": "Vehículo registrado exitosamente"}), 201
    except psycopg2.IntegrityError:
        conn.rollback()
        print(f"❌ Error: La placa {placa} ya existe.")
        return jsonify({"error": "La placa ya está registrada."}), 409
    except Exception as e:
        conn.rollback()
        print(f"❌ Error de BD: {e}")
        return jsonify({"error": f"Error al registrar: {e}"}), 500
    finally:
        if conn:
            conn.close()

# --- Endpoint para Verificar Acceso (GET) ---
@app.route('/api/verificar-acceso/<placa>', methods=['GET'])
def verificar_acceso(placa):
    print(f"📢 [GET] Solicitud para verificar acceso de la placa: {placa}")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT propietario FROM accesos WHERE placa = %s;", (placa,))
        resultado = cursor.fetchone()
        
        if resultado:
            print(f"✅ Acceso autorizado para la placa {placa}")
            return jsonify({"autorizado": True, "propietario": resultado[0]})
        else:
            print(f"❌ Acceso denegado para la placa {placa}")
            return jsonify({"autorizado": False})
    except Exception as e:
        print(f"❌ Error al verificar acceso: {e}")
        return jsonify({"error": "Error al verificar acceso"}), 500
    finally:
        if conn:
            conn.close()

# --- NUEVO Endpoint para Residentes ---
@app.route('/api/residentes', methods=['GET'])
def get_residentes():
    print("📢 [GET] Solicitud para obtener el listado de residentes")
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Error de conexión a la BD"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apartamento, email, telefono FROM residentes;")
        residentes = cursor.fetchall()
        lista_residentes = [
            {"nombre": r[0], "apartamento": r[1], "email": r[2], "telefono": r[3]}
            for r in residentes
        ]
        return jsonify(lista_residentes)
    except Exception as e:
        print(f"❌ Error al obtener residentes: {e}")
        return jsonify({"error": "Error al obtener residentes"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)