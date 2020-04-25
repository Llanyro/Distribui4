let fileuploaded = undefined;
let filecontent = "";

function fun1(e) { e.stopPropagation(); e.preventDefault(); }
function drop(e) { fun1(e); getFileContent(e.dataTransfer.files[0]); }
function getFile() { getFileContent(this.files[0]); }
function getFileContent(file) {
    fileuploaded = file;
    document.getElementById("filename").innerText = file.name;
    if (file === undefined) {
        console.log('No file is selected');
        return;
    }
    else {
        var reader = new FileReader();
        reader.onload = function(event) {
            filecontent = event.target.result;
        };
        reader.readAsText(file);
    }
}
function subirVideo() { alert("Funcionalidad incompleta"); }
window.onload = function() {
    let dropbox = document.getElementById("dropbox");
    dropbox.addEventListener("dragenter", fun1, false);
    dropbox.addEventListener("dragover", fun1, false);
    dropbox.addEventListener("drop", drop, false);
    document.getElementById("inputGroupFile01").addEventListener("change", getFile);
}