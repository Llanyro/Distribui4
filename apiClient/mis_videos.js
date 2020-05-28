window.onload = function() {
    var params = { peticion: "", cookie: "" };
    var body = { peticion: "getMisVideos", cookie: getCookie("AWS")[0]};
    var additionalParams = {};
    try {
        apigClient.rootPost(params, body, additionalParams)
            .then(function(result) {
              console.log(result);
              let videos = JSON.parse(result.data.listaVideo);
              if(videos !== null)
                rellenar_tabla(videos.videos, true, "mis_videos");
              else
                rellenar_tabla([], true, "mis_videos");
            }).catch( function(result) {
                console.log(result);
            });
    }
    catch(e) {console.log(e);}
}