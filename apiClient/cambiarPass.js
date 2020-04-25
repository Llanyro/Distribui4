function cambiarPass() {
    if (document.getElementById("passwordNueva1") === document.getElementById("passwordNueva2")) {
        var params = {
            peticion: "",
            cookie: "",
            password: "",
            newPassword: ""
        };
        var body = {
            peticion: "cambiarPass",
            cookie: getCookie("AWS")[0],
            password: document.getElementById("passwordActual"),
            newPassword: document.getElementById("passwordNueva1")
        };
        var additionalParams = {};
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                    let code = result.data.resultado;
                    if (code === 69) {
                        alert("Contraseña actualizada con éxito!");
                        window.location.href='/apiClient/perfil.html';
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

    else {
        alert("Las contraseñas no coinciden");
        location.reload();
    }   
}