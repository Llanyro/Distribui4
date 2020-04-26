function cambiarPass() {
    if (document.getElementById("passwordNueva1").value === document.getElementById("passwordNueva2").value) {
        var params = { peticion: "", cookie: "", password: "", newpass: "" };
        var body = {
            peticion: "cambiarPass",
            cookie: getCookie("AWS")[0],
            password: document.getElementById("passwordActual").value,
            newpass: document.getElementById("passwordNueva1").value
        };
        var additionalParams = {};
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                    let code = result.data.resultado;
                    if (code === 69) {
                        alert("Contraseña actualizada con éxito!");
                        window.location.href='./perfil.html';
                    }
                    else {
                        console.log("Algo ha petado");
                        console.log(result);
                    }
                }).catch( function(result) { console.log(result); });
        }
        catch(e) {console.log(e);}
    }
    else {
        alert("Las contraseñas no coinciden");
        location.reload();
    }   
}