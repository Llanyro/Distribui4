let fileuploaded = undefined;
let credenciales = undefined;

function fun1(e) { e.stopPropagation(); e.preventDefault(); }
function drop(e) { fun1(e); getFileContent(e.dataTransfer.files[0]); }
function getFile() { getFileContent(this.files[0]); }
function getFileContent(file) {
    if(file !== undefined) {
        fileuploaded = file;
        document.getElementById("label_priv").innerHTML = file.name;
    }
    else console.log('No file is selected');
}
window.onload = function() {
    let dropbox = document.getElementById("dropbox");
    dropbox.addEventListener("dragenter", fun1, false);
    dropbox.addEventListener("dragover", fun1, false);
    dropbox.addEventListener("drop", drop, false);
    document.getElementById("file").addEventListener("change", getFile);
    getCredentials();
}
function getCredentials() {
  try {
      apigClient.subirGet({}, {}, {})
          .then(function(result) {
            console.log(result);
            credenciales = result.data;
          }).catch( function(result) {
              console.log(result);
          });
  }
  catch(e) {console.log(e);}
}
function subirVideoDB() {
    var params = {
        peticion: "",
        cookie: "",
        nombreVideo: "",
        etiquetas: "",
        visualizacion: "",
        size: ""
    };
    var body = {
        peticion: "subirVideo",
        cookie: getCookie("AWS")[0],
        nombreVideo: document.getElementById("nombreVideo").value,
        etiquetas: document.getElementById("etiquetas").value,
        visualizacion: document.getElementById("visualizacion").value,
        size: fileuploaded.size
    };
    var additionalParams = {};
    
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    // Subir video al s3
                    subirVideoS3(result.data.name);
                }
                else {
                    console.log("Algo ha petado en la DB, por lo que no se ha subido nada");
                    console.log(result);
                }
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function subirVideoS3(name) {
    let formulario = new FormData();
    formulario.append("X-Amz-Credential", credenciales.xAmzCredential);
    formulario.append("X-Amz-Date", credenciales.amzDate);
    formulario.append("Policy", credenciales.stringToSign);
    formulario.append("X-Amz-Signature", credenciales.stringSigned);
    formulario.append("acl", "public-read");
    formulario.append("success_action_redirect", "http://distribui4.s3-website-us-east-1.amazonaws.com/success.html");
    formulario.append("X-Amz-Algorithm", "AWS4-HMAC-SHA256");
    formulario.append("X-Amz-Security-Token", credenciales.securityToken);
    formulario.append("key", name + ".mp4");
    formulario.append("file", fileuploaded);
    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: "http://distribui4.s3.us-east-1.amazonaws.com/",
        data: formulario,
        processData: false,
        contentType: false,
        cache: false,
        timeout: 600000,
        success: function (data) {
            if(data === "Fichero subido") {
                alert("Video subido con exito!");
                window.location.href='./perfil.html';
            }
            else {
                alert("Ha habido un error al subur el video!");
                window.location.href='./subir_video.html';
            }
            console.log(data);
        },
        error: function (e) {
            console.log(e);
        }
    });
}