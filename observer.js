// observer.js
class EventBus {
    constructor() {
        this.subscribers = {};
    }
    subscribe(topic, handler) {
        if (!this.subscribers[topic]) this.subscribers[topic] = [];
        this.subscribers[topic].push(handler);
    }
    publish(topic, data) {
        if (this.subscribers[topic]) {
            this.subscribers[topic].forEach(h => h(data));
        }
    }
}

// Servicios suscriptores
class NotificacionService {
    enviarNotificacion(evento) {
        console.log("📢 Notificación enviada:", evento);
    }
}
class Logger {
    registrarAcceso(evento) {
        console.log("📝 Log registrado:", evento);
    }
}

// Ejemplo de uso
const bus = new EventBus();
const notificador = new NotificacionService();
const logger = new Logger();

// Suscribimos servicios
bus.subscribe("acceso_detectado", (e) => notificador.enviarNotificacion(e));
bus.subscribe("acceso_detectado", (e) => logger.registrarAcceso(e));

// Publicamos evento
bus.publish("acceso_detectado", { placa: "ABC123", estado: "Autorizado" });
