let rutavideo = undefined;

window.onload = function() {
    rutavideo = decodeURIComponent(document.URL.split("\?")[1].split("=")[1]);
    this.document.getElementsByTagName("title")[0].innerHTML = rutavideo.split("/")[0];
    console.log(rutavideo);
    let video = document.getElementById("video");
    video.src = "http://distribui4.s3-website-us-east-1.amazonaws.com/" + rutavideo + ".mp4";
    actualizarVotos();
    getComentarios();
}
function actualizarVotos() {
    var params = { peticion: "", ruta: "" };
    var body = { peticion: "verVotos", ruta: rutavideo};
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
              console.log(result);
              if(result.data.resultado === 69) {
                document.getElementById("voteup").innerHTML = result.data.votos[1];
                document.getElementById("votedown").innerHTML = result.data.votos[0];
              }
              else {
                  alert("Error de peticion?");
              }
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function votar(value) {
    var params = { peticion: "", cookie: "", decision: "", ruta: "" };
    var body = { peticion: "voto", cookie: getCookie("AWS")[0], decision: value, ruta: rutavideo};
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
              console.log(result);
              if(result.data.resultado === 69) {
                actualizarVotos();
              }
              else {
                  alert("Error de peticion?");
              }
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function getComentarios() {
    var params = { peticion: "", ruta: "" };
    var body = { peticion: "getComentarios", ruta: rutavideo};
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
              console.log(result);
              if(result.data.resultado === 69) {
                  printComentarios(result.data.comentarios);
              }
              else {
                  alert("Error de peticion?");
              }
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function postComentario() {
    var params = { peticion: "", cookie: "", comentario: "", ruta: "" };
    var body = { 
        peticion: "addComentario", 
        cookie: getCookie("AWS")[0], 
        comentario: document.getElementById("comment").value, 
        ruta: rutavideo
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
              console.log(result);
              if(result.data.resultado === 69) {
                document.getElementById("comment").innerHTML = "";
              }
              else {
                  alert("Error de peticion?");
              }
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function printComentarios(array) {
    let zonaComentariosPadre = document.getElementById("zonaComentariosPadre");
    let rowlist = document.getElementById("zonaComentarios");
    if(rowlist !== undefined)
        rowlist.remove();
    let row = document.createElement("div");

    for (let index = 0; index < array.length; index++) {
        const element = array[index];
        
        let divpadre = generarDiv();
        let divmedio = document.createElement("div");
        divmedio.setAttribute("class", "media-body");

        let nombre = document.createElement("h4");
        nombre.setAttribute("class", "media-heading");
        nombre.setAttribute("id", "usuario");
        nombre.innerHTML = element[0];

        let comentario = document.createElement("p");
        comentario.innerHTML = element[1];

        divmedio.appendChild(nombre);
        divmedio.appendChild(comentario);
        divpadre.appendChild(divmedio);
        row.appendChild(divpadre);
    }
    zonaComentariosPadre.appendChild(row);
}
function generarDiv() {
    let divpadre = document.createElement("div");
    divpadre.setAttribute("class", "media comment-box");

    let divimg = document.createElement("div");
    divimg.setAttribute("class", "media-left");

    let img = document.createElement("img");
    img.setAttribute("class", "img-responsive user-photo");
    img.setAttribute("width","30%");
    img.src = "https://ssl.gstatic.com/accounts/ui/avatar_2x.png";

    divimg.appendChild(img);
    divpadre.appendChild(divimg);
    return divpadre;
}