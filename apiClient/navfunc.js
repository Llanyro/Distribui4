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