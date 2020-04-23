var credentials = {
    accessKey: "ASIAVY64N4P5MEVIAVYN",
    secretKey: "ZoMUyi2qJSu13OD+0IDA6TuD64Mcc/xWRGPIRIkJ",
    region: "us-east-1"
};
var apigClient = apigClientFactory.newClient(credentials);

function logIn(){
    var params = {
        peticion: "",
        username: "",
        password: ""
    };
    var body = {
        peticion: "login",
        username: document.getElementsByName("username")[0].value,
        password: document.getElementsByName("password")[0].value
    };
    var additionalParams = {};
    
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    if(result.data.accesoConcedido === "True"){
                        window.location.href='/apiClient/matriz.html'
                    }
                    else {
                        alert("El usuario no existe o la contraseña es incorrecta");
                    }
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

function signIn() {
    var params = {
        peticion: "",
        username: "",
        password: "",
        nombre = "",
        apellidos = "",
        correo = "",
        pregunta = "",
        respuesta = ""
    };
    var body = {
        peticion: "signin",
        username: document.getElementsByName("username")[0].value,
        password: document.getElementsByName("password")[0].value,
        nombre: document.getElementsByName("nombre")[0].value,
        apellidos: document.getElementsByName("apellidos")[0].value,
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
                    if(result.data.accesoConcedido === "True"){
                        window.location.href='/apiClient/index.html'
                    }
                    else {
                        alert("El usuario o el correo ya existen en la base de datos");
                    }
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

function recuperar(){
    var params = {
        peticion: "",
        username: "",
        correo = "",
        pregunta = "",
        respuesta = ""
    };
    var body = {
        peticion: "recupPass",
        username: document.getElementsByName("username")[0].value,
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
                    if(result.data.accesoConcedido === "True"){
                        alert(result.data.color);
                        window.location.href='/apiClient/index.html';
                    }
                    else {
                        alert("Los datos proporcionados no son correctos");
                    }
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

function getPerfil() {
    var params = {
        peticion: "",
        cookie: ""
    };
    var body = {
        peticion: "getPerfil",
        cookie: document.cookie
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    let perfil = result.data.perfil;
                    document.getElementById("nombre") = perfil.nombre;
                    document.getElementById("apellidos") = perfil.apellidos;
                    document.getElementById("pregunta") = perfil.pregunta;
                    document.getElementById("respuesta") = perfil.respuesta;
                    document.getElementById("correo") = perfil.correo;
                    document.getElementById("usuario") = perfil.usuario;
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

function cambiarPass() {
    var params = {
        peticion: "",
        cookie: "",
        password: "",
        newPassword: ""
    };
    var body = {
        peticion: "getPerfil",
        cookie: document.cookie
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    let perfil = result.data.perfil;
                    
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

function logout() {
    alert("siii")
    var params = {
        peticion: "",
        cookie: ""
    };
    var body = {
        peticion: "getPerfil",
        cookie: document.cookie
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    let perfil = result.data.perfil;
                    
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