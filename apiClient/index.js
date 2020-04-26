function logIn(){
    var params = {
        peticion: "",
        usuario: "",
        password: ""
    };
    var body = {
        peticion: "login",
        usuario: document.getElementsByName("username")[0].value,
        password: document.getElementsByName("password")[0].value
    };
    var additionalParams = {};
    
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    if(result.data.accesoConcedido === true){
                        setCookie("AWS",result.data.cookie);
                        window.location.href='./perfil.html';
                    }
                    else
                        alert("El usuario no existe o la contraseña es incorrecta");
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