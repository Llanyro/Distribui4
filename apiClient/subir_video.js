let fileuploaded = undefined;
let filecontent = undefined;

function fun1(e) { e.stopPropagation(); e.preventDefault(); }
function drop(e) { fun1(e); getFileContent(e.dataTransfer.files[0]); }
function getFile() { getFileContent(this.files[0]); }
function getFileContent(file) {
    fileuploaded = file;
    document.getElementById("filename").innerText = file.name;
    if (file === undefined) {
        console.log('No file is selected');
        return;
    }
    else {
        var reader = new FileReader();
        reader.onload = function() {
            let arrayBuffer = this.result;
            array = new Uint8Array(arrayBuffer);
            filecontent = String.fromCharCode.apply(null, array);
            console.log(filecontent);
        };
        reader.readAsArrayBuffer(file);
    }
}
function subirVideo() {
    let continuar = true;
    var params = {
        peticion: "",
        cookie: "",
        nombreVideo: "",
        etiquetas: "",
        visualizacion: "",
        file: ""
    };
    var body = {
        peticion: "subirVideo",
        cookie: getCookie("AWS")[0],
        nombreVideo: document.getElementById("nombre").value,
        etiquetas: document.getElementById("etiquetas").value,
        visualizacion: document.getElementById("mySelect").value,
        file: filecontent
    };
    console.log(body);
    var additionalParams = {};

    if(body.nombreVideo === undefined) {
        alert("Introduce el nombre del video");
        document.getElementById("nombre").focus();
        continuar = false;
    }
    if(body.file === undefined) {
        alert("Introduce el video");
        continuar = false;
    }
    
    if(continuar) {
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                    let code = result.data.resultado;
                    if (code === 69) {
                        if(result.data.filesubido) 
                            alert("El video se ha subido con exito!");
                        else
                            alert("Ha habido un problema al subir el video.");
                        window.location.href='./perfil.html';
                    }
                    else {
                        console.log("Algo ha petado");
                        console.log(result);
                    }
                }).catch( function(result) {
                    console.log(result);
                });
        }
        catch(e) {console.log(e);}
    }
}
window.onload = function() {
    let dropbox = document.getElementById("dropbox");
    dropbox.addEventListener("dragenter", fun1, false);
    dropbox.addEventListener("dragover", fun1, false);
    dropbox.addEventListener("drop", drop, false);
    document.getElementById("inputGroupFile01").addEventListener("change", getFile);
}