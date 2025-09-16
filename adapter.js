// adapter.js
class IReconocedorPlacas {
    reconocer(frame) {
        throw "Método abstracto";
    }
}

// Implementación local
class ReconocedorLocal extends IReconocedorPlacas {
    reconocer(frame) {
        return "ABC123"; // simulación
    }
}

// SDK externo ficticio
class SDKExterno {
    detectarMatricula(frame) {
        return { placa: "XYZ987", confianza: 0.95 };
    }
}

// Adapter para el SDK externo
class AdapterReconocedorExterno extends IReconocedorPlacas {
    constructor(sdk) {
        super();
        this.sdk = sdk;
    }
    reconocer(frame) {
        const resultado = this.sdk.detectarMatricula(frame);
        return resultado.placa;
    }
}

// Ejemplo de uso:
const sdk = new SDKExterno();
const adapter = new AdapterReconocedorExterno(sdk);
console.log("Placa detectada:", adapter.reconocer("frameImagen"));
