
window.onload = function() { getPerfil(); }

function getPerfil() {
    var params = {
        peticion: "",
        cookie: ""
    };
    var body = {
        peticion: "getPerfil",
        cookie: getCookie("AWS")[0]
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
        .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    let perfil = result.data.perfil;
                    console.log(perfil);
                    document.getElementById("nombre").innerHTML = perfil.nombre;
                    document.getElementById("apellidos").innerHTML = perfil.apellido;
                    document.getElementById("pregunta").innerHTML = perfil.pregunta;
                    document.getElementById("respuesta").innerHTML = perfil.respuesta;
                    document.getElementById("correo").innerHTML = perfil.correo;
                    document.getElementById("usuario").innerHTML = perfil.usuario;
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
window.onload = function() { getPerfil(); }
