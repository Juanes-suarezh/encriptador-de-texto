
function validarMinusculas(texto) {
    const regex = /^[a-z\s]*$/;
    if (!regex.test(texto)) {
        alert("Solo letras minúsculas y sin acentos");
        return false;
    }
    return true;
}

function encriptar() {
    let texto = document.getElementById("texto").value;
    if (!validarMinusculas(texto)) return;

    let tituloMensaje = document.getElementById("titulo-mensaje");
    let parrafo = document.getElementById("parrafo");
    let mensajeEncriptado = document.getElementById("mensaje-encriptado");

    let textoCifrado = texto
        .replace(/e/gi, "enter")
        .replace(/i/gi, "imes")
        .replace(/a/gi, "ai")
        .replace(/o/gi, "ober")
        .replace(/u/gi, "ufat");

    tituloMensaje.textContent = "Texto encriptado con éxito";
    parrafo.textContent = textoCifrado;
    mensajeEncriptado.style.display = "block";
}

function desencriptar() {
    let texto = document.getElementById("texto").value;
    if (!validarMinusculas(texto)) return;

    let tituloMensaje = document.getElementById("titulo-mensaje");
    let parrafo = document.getElementById("parrafo");
    let mensajeEncriptado = document.getElementById("mensaje-encriptado");

    let textoCifrado = texto
        .replace(/enter/gi, "e")
        .replace(/imes/gi, "i")
        .replace(/ai/gi, "a")
        .replace(/ober/gi, "o")
        .replace(/ufat/gi, "u");

    tituloMensaje.textContent = "Texto desencriptado con éxito";
    parrafo.textContent = textoCifrado;
    mensajeEncriptado.style.display = "block";
}

function copiarTexto() {
    let parrafo = document.getElementById("parrafo");
    let textoACopiar = parrafo.textContent;

    navigator.clipboard.writeText(textoACopiar).then(() => {
        alert("Texto copiado al portapapeles");
    }, () => {
        alert("Error al copiar el texto");
    });
}


function borrarTexto() {
    // Borrar el contenido del textarea
    document.getElementById("texto").value = "";

    // Reiniciar el contenido del div encriptado
    let tituloMensaje = document.getElementById("titulo-mensaje");
    let parrafo = document.getElementById("parrafo");

    tituloMensaje.textContent = "Ningún mensaje fue encontrado";
    parrafo.textContent = "";

    // Opcional: Ocultar el div encriptado si es necesario
    // document.getElementById("mensaje-encriptado").style.display = "none";
}



