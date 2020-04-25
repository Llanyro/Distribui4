function signIn() {
    var params = {
        peticion: "",
        usuario: "",
        password: "",
        nombre: "",
        apellido: "",
        correo: "",
        pregunta: "",
        respuesta: ""
    };
    var body = {
        peticion: "signin",
        usuario: document.getElementsByName("username")[0].value,
        password: document.getElementsByName("password")[0].value,
        nombre: document.getElementsByName("nombre")[0].value,
        apellido: document.getElementsByName("apellidos")[0].value,
        correo: document.getElementsByName("correo")[0].value,
        pregunta: document.getElementById("mySelect").options[document.getElementById("mySelect").selectedIndex].value,
        respuesta: document.getElementsByName("respuesta")[0].value
    };
    var additionalParams = {};
    
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    if(result.data.accesoConcedido === true){
                        setCookie("AWS", result.data.cookie);
                        window.location.href='./apiClient/perfil.html';
                    }
                    else
                        alert("El usuario o el correo ya existen en la base de datos");
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