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
                        document.cookie = setCookie("AWS",result.data.cookie);
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
                        document.cookie = setCookie("AWS",result.data.cookie);
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
    if (document.getElementById("passwordNueva1") === document.getElementById("passwordNueva2")) {
        var params = {
            peticion: "",
            cookie: "",
            password: "",
            newPassword: ""
        };
        var body = {
            peticion: "getPerfil",
            cookie: document.cookie,
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
        peticion: "getPerfil",
        cookie: document.cookie
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                let code = result.data.resultado;
                if (code === 69) {
                    document.cookie = deleteCookie("AWS");
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

function setCookie(key, newValue) {
    let cookies = ("; " + document.cookie).split("; ");
    let newCookieList = "";

    for (let i = 1; i < cookies.length; i++) {
        let spl = cookies[i].split('=');
        if(spl.length == 2) {
            if(spl[0] == key && i == 1)
                newCookieList += spl[0] + "=" + newValue;
            else if(spl[0] == key)
                newCookieList += "; " + spl[0] + "=" + newValue;
            else if(i == 1)
                newCookieList += spl[0] + "=" + spl[1];
            else
                newCookieList += "; " + spl[0] + "=" + spl[1];
        }
    }
    return newCookieList;
}

function getCookie(key){
    let coo = "; " + document.cookie;
    let cookielist = coo.split("; ");
    let val = [];
    for(let i = 0; i < cookielist.length; i++){
        let spl = cookielist[i].split('=');
        if(spl.length == 2 && spl[0] == key)
            val.push(spl[1]);
    }
    return val;
}

function deleteCookie(key) {
    let cookies = ("; " + document.cookie).split("; ");
    let newCookieList = "";
    for (let i = 1; i < cookies.length; i++) {
        let spl = cookies[i].split('=');
        if(spl.length == 2)
            if (spl[0] != key) {
                if(i == 1)
                newCookieList += spl[0] + "=" + spl[1];
                else
                    newCookieList += "; " + spl[0] + "=" + spl[1];
            }
    }
    return newCookieList;
}