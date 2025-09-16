# ================================
# python.py - Sistema de Rutas + EventBus
# ================================

from collections import deque

# ========= EVENTBUS (Observer en Python) =========
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, handler):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    def publish(self, topic, data):
        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                handler(data)

# Ejemplo de servicios suscriptores
class Logger:
    @staticmethod
    def registrar(evento):
        print(f"📝 [LOG] {evento}")

class Notificador:
    @staticmethod
    def enviar(evento):
        print(f"🔔 [NOTIFICACIÓN] {evento}")

# Instanciamos un EventBus global
bus = EventBus()
bus.subscribe("ruta_calculada", Logger.registrar)
bus.subscribe("ruta_calculada", Notificador.enviar)

# ========= ALGORITMO DE BÚSQUEDA BIDIRECCIONAL =========
def bidirectional_search(grafo, inicio, fin):
    if inicio == fin:
        return [inicio]

    visitados_inicio = {inicio: None}
    visitados_fin = {fin: None}

    cola_inicio = deque([inicio])
    cola_fin = deque([fin])

    while cola_inicio and cola_fin:
        # Expansión desde inicio
        if cola_inicio:
            nodo = cola_inicio.popleft()
            for vecino in grafo.get(nodo, []):
                if vecino not in visitados_inicio:
                    visitados_inicio[vecino] = nodo
                    cola_inicio.append(vecino)
                    if vecino in visitados_fin:
                        return construir_camino(visitados_inicio, visitados_fin, vecino)

        # Expansión desde fin
        if cola_fin:
            nodo = cola_fin.popleft()
            for vecino in grafo.get(nodo, []):
                if vecino not in visitados_fin:
                    visitados_fin[vecino] = nodo
                    cola_fin.append(vecino)
                    if vecino in visitados_inicio:
                        return construir_camino(visitados_inicio, visitados_fin, vecino)
    return None

def construir_camino(visitados_inicio, visitados_fin, encuentro):
    camino = []
    nodo = encuentro
    while nodo is not None:
        camino.append(nodo)
        nodo = visitados_inicio[nodo]
    camino.reverse()

    nodo = visitados_fin[encuentro]
    while nodo is not None:
        camino.append(nodo)
        nodo = visitados_fin[nodo]

    return camino

# ========= EJEMPLO DE USO =========
if __name__ == "__main__":
    # Grafo que representa calles del conjunto
    grafo = {
        "Entrada": ["A", "B"],
        "A": ["Entrada", "C"],
        "B": ["Entrada", "D"],
        "C": ["A", "E"],
        "D": ["B", "E"],
        "E": ["C", "D", "Casa1", "Casa2"],
        "Casa1": ["E"],
        "Casa2": ["E"]
    }

    inicio = "Entrada"
    destino = "Casa1"

    ruta = bidirectional_search(grafo, inicio, destino)

    if ruta:
        mensaje = f"Ruta calculada desde {inicio} hasta {destino}: {' -> '.join(ruta)}"
        print(mensaje)
        # Publicamos evento en el EventBus
        bus.publish("ruta_calculada", mensaje)
    else:
        print("No se encontró ruta disponible")
