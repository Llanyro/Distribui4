var credentials = {
    accessKey: "ASIAVY64N4P5OEQTKSZM",
    secretKey: "V7CYN2YSyCB9xyQynJoRacJk8WTTkJA70OU7lD6M",
    region: "us-east-1"
};
var apigClient = apigClientFactory.newClient(credentials);


function enviar(varibale) {
    var params = {
        peticion: "",
        username: "",
        password: ""
    };
    var body = {
        peticion: varibale,
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
                        if(varibale === 'login')
                            window.location.href='/apiClient/matriz.html'
                        else if(varibale === 'signin')
                            window.location.href='/apiClient/index.html'
                    }
                    else {
                        if(varibale === 'login')
                            alert("El usuario no existe o la contraseña es incorrecta");
                        else if(varibale === 'signin')
                            alert("El usuario ya existe en la base de datos");
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

function recibirMatriz(objmatriz, nombrematriz) {
    let matriz = undefined;
    temp = objmatriz.value.split(" ");
    if (temp.length < 16)
        alert("No hay suficientes elmentos en la matriz " + nombrematriz)
    else if(temp.length > 16)
        alert("Demasiados elmentos en la matriz " + nombrematriz)
    else {
        matriz = [];
        let newlist = [];
        for (let i = 0; i < temp.length; i++) {
            newlist.push(parseInt(temp[i]));
            if(i % 4 == 3){
                matriz.push(newlist);
                newlist = [];
            }
        }
        matriz1completada = true;
    }
    return matriz;
}

//1 2 3 4 5 6 7 8 9 0 11 12 13 14 15 16
function multiplicarMatrices() {
    let matrizlist = document.getElementsByName("matriz");
    let objMatriz1 = matrizlist[0];
    let objMatriz2 = matrizlist[1];

    let matriz1res = recibirMatriz(objMatriz1, "1");
    let matriz2res = recibirMatriz(objMatriz2, "2");

    if(matriz1res !== undefined && matriz2res !== undefined){
        var params = {
            peticion: "",
            matriz1: "",
            matriz2: ""
        };
        var body = {
            peticion: "matriz4x4",
            matriz1: matriz1res,
            matriz2: matriz2res
        };
        var additionalParams = {};
        
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                    let code = result.data.resultado;
                    if (code === 69)
                        alert(result.data.result);
                    else
                        console.log(result);
                }).catch( function(result) {
                    console.log("Algo ha petado");
                    console.log(result);
                });
        }
        catch(e) {
            console.log("Algo ha petado");
            console.log(e);
        }
    }
}