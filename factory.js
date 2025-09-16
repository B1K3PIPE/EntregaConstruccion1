// factory.js
class Usuario {
    constructor(usuario, contrasena) {
        this.usuario = usuario;
        this.contrasena = contrasena;
    }
}

class Administrador extends Usuario {
    gestionarRegistros() { console.log("Gestionando registros..."); }
}

class Celador extends Usuario {
    verificarAcceso() { console.log("Verificando acceso..."); }
}

class OperadorSeguridad extends Usuario {
    monitorearCCTV() { console.log("Monitoreando cámaras..."); }
}

class Residente extends Usuario {
    revisarGrabaciones() { console.log("Revisando grabaciones..."); }
}

// Factory Method
class UsuarioFactory {
    static crearUsuario(tipo, usuario, contrasena) {
        switch (tipo) {
            case "Administrador": return new Administrador(usuario, contrasena);
            case "Celador": return new Celador(usuario, contrasena);
            case "Operador": return new OperadorSeguridad(usuario, contrasena);
            case "Residente": return new Residente(usuario, contrasena);
            default: throw new Error("Tipo de usuario no válido");
        }
    }
}

// Ejemplo de uso:
const admin = UsuarioFactory.crearUsuario("Administrador", "admin", "1234");
admin.gestionarRegistros();
