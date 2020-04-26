function recuperar(){
    var params = {
        peticion: "",
        usuario: "",
        correo: "",
        pregunta: "",
        respuesta: ""
    };
    var body = {
        peticion: "recupPass",
        usuario: document.getElementsByName("username")[0].value,
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
                    alert("Nueva contraseña temporal: " + result.data.color);
                    window.location.href='./index.html';
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