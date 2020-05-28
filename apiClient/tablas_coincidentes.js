let url = "http://distribui4.s3-website-us-east-1.amazonaws.com/";
function rellenar_tabla(array, admin, nombrepagina) {
    let table = crear_tabla();
    let row_header = undefined;
    if(admin)
        row_header = crear_header(
            ['Nombre','Usuario','Etiquetas', "Fecha", "Visualizacion", "Size", "Video", '']);
    else
        row_header = crear_header(
            ['Nombre','Usuario','Etiquetas', "Fecha", "Visualizacion", "Size", "Video"]);
    row_header.setAttribute("class", "cabecera_tabla");
    table.appendChild(row_header);

    console.log(array.length);
    for(let i = 0; i < array.length; i++) {
        let ruta = array[i].Usuario + "/" + array[i].Nombre;
        let row = document.createElement('tr');
        row.onclick= function() {window.location.href = url + 'apiClient/ver_video.html?ruta=' + ruta;}
        table.appendChild(row);

        let nombre = document.createElement('td');
        let usuario = document.createElement('td');
        let etiquetas = document.createElement('td');
        let fecha = document.createElement('td');
        let visualizacion = document.createElement('td');
        let size = document.createElement('td');
        
        let contenidiNombre = document.createElement('p');
        let contenidiUsuario = document.createElement('p');
        let contenidiEtiquetas = document.createElement('p');
        let contenidiFecha = document.createElement('p');
        let contenidiVisualizacion = document.createElement('p');
        let contenidiSize = document.createElement('p');

        contenidiNombre.innerText = array[i].Nombre;
        contenidiUsuario.innerText = array[i].Usuario;
        contenidiEtiquetas.innerText = array[i].Etiquetas;
        contenidiFecha.innerText = array[i].Fecha;
        contenidiVisualizacion.innerText = array[i].Visualizacion;
        contenidiSize.innerText = array[i].Size;

        let viewSrc = document.createElement("video");
        viewSrc.setAttribute("preload", "auto");
        viewSrc.setAttribute("controls", "");
        viewSrc.setAttribute("loop", "loop");
        viewSrc.src = url + ruta + ".mp4";

        nombre.appendChild(contenidiNombre);
        usuario.appendChild(contenidiUsuario);
        etiquetas.appendChild(contenidiEtiquetas);
        fecha.appendChild(contenidiFecha);
        visualizacion.appendChild(contenidiVisualizacion);
        size.appendChild(contenidiSize);

        row.appendChild(nombre);
        row.appendChild(usuario);
        row.appendChild(etiquetas);
        row.appendChild(fecha);
        row.appendChild(visualizacion);
        row.appendChild(size);
        row.appendChild(viewSrc);

        if(admin) {
            let del = document.createElement('td');

            let a = document.createElement("button");
            a.setAttribute("class", "btn btn-secondary");
            a.id = array[i].Nombre;
            a.onclick=function(){eliminar(this, nombrepagina)};

            let btn = document.createElement('i');
            btn.setAttribute('class','fa fa-trash');
            btn.setAttribute('aria-hidden',"true");
    
            a.appendChild(btn);
            del.appendChild(a);
            row.appendChild(del);
        }
    }
}
function crear_header(master) {
    let row_header = document.createElement('tr');
    master.forEach((h) => {
        let header = document.createElement('th');
        header.innerHTML = h;
        row_header.appendChild(header);
    });
    return row_header;
}
function crear_tabla() {
    let body = document.getElementById('videocontainer');
    
    let tabla = document.getElementsByTagName('table');
    if(tabla.length > 0)
        for (let index = 0; index < tabla.length; index++)
            tabla[index].remove();

    let table = document.createElement('table');
    //table.setAttribute('border', 1);
    table.setAttribute("class", "table table-striped");
    body.appendChild(table);
    return table;
}
function eliminar(btn, nombrepagina){
    if(confirm("Seguro que quieres eliminar el fichero: " + btn.id + "\n Recuerda que esto no se puede revertir.") === true) {
        var params = { peticion: "", cookie: "", nombreVideo: "" };
        var body = { peticion: "eliminarVideo", cookie: getCookie("AWS")[0], nombreVideo: btn.id };
        var additionalParams = {};
        try {
            apigClient.rootPost(params, body, additionalParams)
                .then(function(result) {
                console.log(result);
                if(result.data.resultado === 69){
                    alert("El video ha sido eliminado con exito!");
                }
                else {
                    alert("Internal server error aws?");
                }
                  window.location.href='./' + nombrepagina + ".html";
                }).catch( function(result) {
                    console.log(result);
                });
        }
        catch(e) {console.log(e);}
    }
}
