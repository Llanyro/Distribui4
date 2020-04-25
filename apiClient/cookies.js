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