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
        reader.onload = function(event) {
            filecontent = event.target.result;
        };
        reader.readAsText(file);
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
        filecontent: "",
    };

    var body = {
        peticion: "subirVideo",
        cookie: getCookie("AWS")[0],
        nombreVideo: document.getElementById("nombre").value,
        etiquetas: document.getElementById("etiquetas").value,
        visualizacion: document.getElementById("mySelect").value,
        filecontent: filecontent,
    };
    console.log(body);
    var additionalParams = {};

    if(body.nombreVideo === undefined) {
        alert("Introduce el nombre del video");
        document.getElementById("nombre").focus();
        continuar = false;
    }
    if(body.filecontent === undefined) {
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