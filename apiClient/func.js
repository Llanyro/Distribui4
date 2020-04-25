var credentials = {
    accessKey: "ASIAVY64N4P5DQKHMTPV",
    secretKey: "leva/3zWPMc2VHVMHpPqw9d78rHXzB7YiG1Aceb2",
    region: "us-east-1"
};
var apigClient = apigClientFactory.newClient(credentials);

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
                        window.location.href='/apiClient/perfil.html'
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
                console.log(result);
                let code = result.data.resultado;
                if (code === 69) {
                    if(result.data.accesoConcedido === true){
                        setCookie("AWS",result.data.cookie);
                        window.location.href='/apiClient/perfil.html'
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

function logout() {
    var params = {
        peticion: "",
        cookie: ""
    };
    var body = {
        peticion: "logout",
        cookie: getCookie("AWS")[0]
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    deleteCookie("AWS");
                    window.location.href='/apiClient/index.html';
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

function setCookie(key, newValue) {
    document.cookie = key + "=" + newValue + "; expires=Thu, 01 Jan 2050 00:00:00 UTC; path=/;"
}

function getCookie(key){
    let cookies = document.cookie.replace(" ", "").split(";");
    let val = [];
    for(let i = 0; i < cookies.length; i++){
        let spl = cookies[i].split('=');
        if(spl.length == 2 && spl[0] == key)
            val.push(spl[1]);
    }
    return val;
}

function deleteCookie(key) {
    document.cookie = key + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
}


function subirVideo() {
    if (document.getElementById("passwordNueva1") === document.getElementById("passwordNueva2")) {
        var params = {
            peticion: "",
            cookie: "",
            nombre: "",
            etiquetas: "",
            estado: ""
        };
        var body = {
            peticion: "cambiarPass",
            cookie: getCookie("AWS")[0],
            nombre: document.getElementById("nombre"),
            etiquetas: document.getElementById("etiquetas"),
            estado: document.getElementById("mySelect").options[document.getElementById("mySelect").selectedIndex].value,
        };
        var additionalParams = {};
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                    let code = result.data.resultado;
                    if (code === 69) {
                        alert("Contraseña actualizada con éxito!");
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