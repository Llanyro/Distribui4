window.onload = function() {
    var params = { peticion: "" };
    var body = { peticion: "getVideos"};
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                console.log(result);
                let videos = JSON.parse(result.data.listaVideo);
                if(videos !== null)
                  rellenar_tabla(videos.videos, false, "videos_publicos");
                else
                  rellenar_tabla([], false, "videos_publicos");
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}
function getVideosLike() {
    var params = { peticion: "", like: "" };
    var body = {
        peticion: "getVideosLike",
        like: document.getElementById("srch-term").value
    };
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
                console.log(result);
                let videos = JSON.parse(result.data.listaVideo);
                if(videos !== null)
                  rellenar_tabla(videos.videos, false, "videos_publicos");
                else
                  rellenar_tabla([], false, "videos_publicos");
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}