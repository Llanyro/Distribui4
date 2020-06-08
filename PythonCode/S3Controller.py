import boto3
from Singleton import variableCorrecta, variableCorrectaInt
from ControladorBaseDatos import ControladorBaseDatos, EnumType, impVideos
import uuid
import codecs


class BucketObject:
    __bucketname: str = 'distribui4'
    __s3 = boto3.resource("s3")
    __bucket = None

    def __init__(self, bucketname: str):
        self.__bucketname = bucketname
        self.__bucket = self.__s3.Bucket(self.__bucketname)

    def deleteFile(self, path: str):
        self.__s3.Object(self.__bucketname, path + ".mp4").delete()
        return None

    @staticmethod
    def filepath(usuariovideo: str, filename: str):
        return usuariovideo + "/" + filename


class ResolutorSolicitudes:
    __dbController = None
    __numIntentos: int = 3
    __bucketObject: BucketObject = None

    __cookieInvalida: str = "cookie invalida"
    __ok: str = "OK"

    def __init__(self, host: str, bucket: str):
        self.__dbController = ControladorBaseDatos(host)
        self.__bucketObject = BucketObject(bucket)

    def dbconnected(self):
        return self.__dbController.getIniciadaConexion()

    def __getCookie(self, usuario: str):
        repetir = True
        cookie: str = self.__dbController.getCookie(usuario)
        if cookie is None:
            while repetir is True:
                cookie = str(uuid.uuid4())
                result = self.__dbController.addCookie(usuario, cookie)
                if result is True:
                    repetir = False
        return cookie

    # region Usuarios
    # """
    # {
    #   "peticion": "login",
    #   "usuario": "Pato",
    #   "password": "Pato"
    # }
    # """
    def __resolverLogin(self, datos: dict):
        usuario = datos.get("usuario")
        passwd = datos.get("password")
        if usuario is None:
            resultado = {"resultado": 6, "statusCode": "username null"}
        elif passwd is None:
            resultado = {"resultado": 7, "statusCode": "password null"}
        else:
            res_login = self.__dbController.login(usuario, passwd)
            resultado = {"resultado": 69, "statusCode": self.__ok, "accesoConcedido": res_login}
            if res_login is False:
                intentos = self.__dbController.getIntentos(usuario)
                if intentos is not None:
                    if intentos >= self.__numIntentos:
                        self.__dbController.deleteUsuario(usuario)
                    else:
                        self.__dbController.setIntentos(usuario, int(intentos) + 1)
            else:
                self.__dbController.setIntentos(usuario, 0)
                resultado.update({"cookie": self.__getCookie(usuario)})
        return resultado

    # """
    # {
    #   "peticion": "signin",
    #   "nombre": "Pato",
    #   "apellido": "",
    #   "usuario": "Pato",
    #   "correo": "Pato@Pato.pato",
    #   "password": "Pato",
    #   "pregunta": "Red",
    #   "respuesta": "Red"
    # }
    # """
    def __resolverSignin(self, datos: dict):
        nombre = datos.get("nombre")
        apellido = datos.get("apellido")
        usuario = datos.get("usuario")
        correo = datos.get("correo")
        passwd = datos.get("password")
        pregunta = datos.get("pregunta")
        respuesta = datos.get("respuesta")
        if variableCorrecta(nombre) is False:
            resultado = {"resultado": 6, "statusCode": "nombre null"}
        elif variableCorrecta(apellido) is False:
            resultado = {"resultado": 7, "statusCode": "apellido null"}
        elif variableCorrecta(correo) is False:
            resultado = {"resultado": 7, "statusCode": "correo null"}
        elif variableCorrecta(usuario) is False:
            resultado = {"resultado": 7, "statusCode": "usuario null"}
        elif variableCorrecta(passwd) is False:
            resultado = {"resultado": 7, "statusCode": "password null"}
        elif variableCorrecta(pregunta) is False:
            resultado = {"resultado": 7, "statusCode": "pregunta null"}
        elif variableCorrecta(respuesta) is False:
            resultado = {"resultado": 7, "statusCode": "respuesta null"}
        else:
            res_signin = self.__dbController.singin(nombre, apellido, usuario, correo, passwd, pregunta, respuesta)
            resultado = {"resultado": 69, "statusCode": self.__ok, "accesoConcedido": res_signin}
            if res_signin is True:
                resultado.update({"cookie": self.__getCookie(usuario)})
        return resultado

    # {
    #     "peticion": "recupPass",
    #     "usuario": "Pato",
    #     "pregunta": "Red",
    #     "respuesta": "Red"
    #     "correo": "Pato@Pato.pato"
    # }
    def __resolverRecuperarPassword(self, datos: dict):
        usuario = datos.get("usuario")
        pregunta = datos.get("pregunta")
        respuesta = datos.get("respuesta")
        correo = datos.get("correo")
        if variableCorrecta(usuario) is False:
            resultado = {"resultado": 7, "statusCode": "usuario null"}
        elif variableCorrecta(respuesta) is False:
            resultado = {"resultado": 7, "statusCode": "respuesta null"}
        elif variableCorrecta(pregunta) is False:
            resultado = {"resultado": 7, "statusCode": "pregunta null"}
        elif variableCorrecta(correo) is False:
            resultado = {"resultado": 7, "statusCode": "correo null"}
        else:
            if self.__dbController.getRespuestaValida(usuario, correo, pregunta, respuesta) is True:
                newpass = str(uuid.uuid4())
                self.__dbController.cambiarpasswd(usuario, newpass)
                resultado = {"resultado": 69, "statusCode": self.__ok, "color": newpass}
            else:
                resultado = {"resultado": 7, "statusCode": "respuesta erronea", "color": None}
        return resultado

    # {
    #     "peticion": "cambiarPass",
    #     "cookie": "b6156e8b-5029-49b1-8af4-e5afc6f46114",
    #     "password": "Pato",
    #     "newpass": "Pato2"
    # }
    def __resolverCambiarPassword(self, datos:dict):
        cookie = datos.get("cookie")
        passwd = datos.get("password")
        newpass = datos.get("newpass")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        elif variableCorrecta(passwd) is False:
            resultado = {"resultado": 7, "statusCode": "password null"}
        elif variableCorrecta(newpass) is False:
            resultado = {"resultado": 7, "statusCode": "newpass null"}
        else:
            usuario = self.__dbController.getUsername(cookie)
            if variableCorrecta(usuario) is False:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                resul = self.__dbController.cambiarpasswdWEB(usuario, passwd, newpass)
                resultado = {"resultado": 69, "statusCode": self.__ok, "cambioPass": resul}
        return resultado

    # {
    #     "peticion": "getPerfil",
    #     "cookie": "b6156e8b-5029-49b1-8af4-e5afc6f46114",
    # }
    def __resolverGetPerfil(self, datos: dict):
        cookie = datos.get("cookie")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        else:
            usuario = self.__dbController.getUsername(cookie)
            if variableCorrecta(usuario) is False:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                perfil = self.__dbController.getPerfil(usuario)
                if perfil is None:
                    resultado = {"resultado": 7, "statusCode": "error interno?"}
                else:
                    resultado = {"resultado": 69, "statusCode": self.__ok, "perfil": perfil}
        return resultado

    # {
    #     "peticion": "logout",
    #     "cookie": "f51744b3-ce25-412f-aa06-24e08360f876"
    # }
    def __resolverLogout(self, datos: dict):
        cookie = datos.get("cookie")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        else:
            resultado = {"resultado": 69, "statusCode": self.__ok,
                         "logout": self.__dbController.deleteCookie(cookie)}
        return resultado

    # endregion
    # region Ficheros
    # {
    #     "peticion": "subirVideo",
    #     "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
    #     "nombreVideo": "Video de Pato",
    #     "etiquetas": "tuputamadre.jpg#hashtag",
    #     "visualizacion": "public",
    #     "size": "0"
    # }
    def __resolverSubirVideo(self, datos: dict):
        cookie = datos.get("cookie")
        nombrevideo = datos.get("nombreVideo")
        etiquetas = datos.get("etiquetas")
        visualizacion = datos.get("visualizacion")
        size = datos.get("size")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        elif variableCorrecta(nombrevideo) is False:
            resultado = {"resultado": 7, "statusCode": "nombreVideo null"}
        elif variableCorrecta(etiquetas) is False:
            resultado = {"resultado": 7, "statusCode": "etiquetas null"}
        elif variableCorrectaInt(size) is None:
            resultado = {"resultado": 7, "statusCode": "file null"}
        else:
            usuariovideo = self.__dbController.getUsername(cookie)
            if usuariovideo is None:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                ruta = self.__bucketObject.filepath(usuariovideo, nombrevideo)
                if visualizacion is None:
                    visualizacion = EnumType.Private.value
                result = self.__dbController.subirVideo(usuariovideo, nombrevideo,
                                                        etiquetas, str(size), ruta, visualizacion)
                resultado = {"resultado": 69, "statusCode": self.__ok, "filesubido": result, "name": ruta}
        return resultado

    # {
    #     "peticion": "getMisVideos",
    #     "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
    # }
    def __resolverGetMisVideos(self, datos: dict):
        cookie = datos.get("cookie")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        else:
            usuariovideo = self.__dbController.getUsername(cookie)
            if usuariovideo is None:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                result = self.__dbController.getMyVideos(usuariovideo)
                resultado = {"resultado": 69, "statusCode": self.__ok, "listaVideo": result}
        return resultado

    # {
    #     "peticion": "getVideos"
    # }
    def __resolverGetVideos(self, datos: dict):
        result = self.__dbController.getVideos()
        return {"resultado": 69, "statusCode": self.__ok, "listaVideo": result}

    # {
    #     "peticion": "nombreVideo",
    #     "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
    #     "nombrevideo": "Video 0 de pato.mp1"
    # }
    def __resolverEliminarVideo(self, datos: dict):
        cookie = datos.get("cookie")
        nombrevideo = datos.get("nombreVideo")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        elif variableCorrecta(nombrevideo) is False:
            resultado = {"resultado": 7, "statusCode": "nombreVideo null"}
        else:
            usuariovideo = self.__dbController.getUsername(cookie)
            if usuariovideo is None:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                result = self.__dbController.deleteVideo(usuariovideo, nombrevideo)
                if result:
                    self.__bucketObject.deleteFile(self.__bucketObject.filepath(usuariovideo, nombrevideo))
                resultado = {"resultado": 69, "statusCode": self.__ok, "fileEliminado": result}
        return resultado

    # {
    #     "peticion": "getVideosLike",
    #     "like": "asdf"
    # }
    def __resolverGetVideosLike(self, datos: dict):
        like = datos.get("like")
        if variableCorrecta(like) is False:
            like = ""
        result = self.__dbController.getVideosLike(like)
        resultado = {"resultado": 69, "statusCode": self.__ok, "listaVideo": result}
        return resultado

    # endregion
    # region Votos
    # {
    #     "peticion": "voto",
    #     "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
    #     "ruta": "Fian/asdf",
    #     "decision": 0
    # }
    def __resolverVoto(self, datos: dict):
        cookie = datos.get("cookie")
        ruta = datos.get("ruta")
        decision = datos.get("decision")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        elif variableCorrecta(ruta) is False:
            resultado = {"resultado": 7, "statusCode": "ruta null"}
        elif variableCorrectaInt(decision) is False:
            resultado = {"resultado": 7, "statusCode": "decision null"}
        else:
            usuario = self.__dbController.getUsername(cookie)
            if usuario is None:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                result = self.__dbController.insertarVoto(ruta, usuario, decision)
                resultado = {"resultado": 69, "statusCode": self.__ok, "votoRealizado": result}
        return resultado

    # {
    #     "peticion": "verVotos",
    #     "ruta": "Fian/asdf"
    # }
    def __resolverVerVotos(self, datos: dict):
        ruta = datos.get("ruta")
        if variableCorrecta(ruta) is False:
            resultado = {"resultado": 7, "statusCode": "ruta null"}
        else:
            result = self.__dbController.verVotosVideo(ruta)
            resultado = {"resultado": 69, "statusCode": self.__ok, "votos": result}
        return resultado

    # endregion
    # region Comentarios
    # {
    #     "peticion": "addComentario",
    #     "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
    #     "ruta": "Fian/asdf",
    #     "comentario": "asdf"
    # }
    def __resolverAddComentario(self, datos: dict):
        cookie = datos.get("cookie")
        ruta = datos.get("ruta")
        comentario = datos.get("comentario")
        if variableCorrecta(cookie) is False:
            resultado = {"resultado": 7, "statusCode": "cookie null"}
        elif variableCorrecta(ruta) is False:
            resultado = {"resultado": 7, "statusCode": "ruta null"}
        elif variableCorrecta(comentario) is False:
            resultado = {"resultado": 7, "statusCode": "comentario null"}
        else:
            usuario = self.__dbController.getUsername(cookie)
            if usuario is None:
                resultado = {"resultado": 7, "statusCode": self.__cookieInvalida}
            else:
                result = self.__dbController.addComentario(ruta, usuario, comentario)
                resultado = {"resultado": 69, "statusCode": self.__ok, "comentarioRealizado": result}
        return resultado

    # {
    #     "peticion": "getComentarios",
    #     "ruta": "Fian/asdf"
    # }
    def __resolverGetComentarios(self, datos: dict):
        ruta = datos.get("ruta")
        if variableCorrecta(ruta) is False:
            resultado = {"resultado": 7, "statusCode": "ruta null"}
        else:
            result = self.__dbController.getComentarios(ruta)
            resultado = {"resultado": 69, "statusCode": self.__ok, "comentarios": result}
        return resultado

    # endregion
    def resolverSolicitud(self, datos: dict):
        peticion = datos.get("peticion")
        if peticion is None:
            resultado = {"resultado": 2, "statusCode": "Tipo de peticion vacia"}
        else:
            if peticion == "login":
                resultado = self.__resolverLogin(datos)
            elif peticion == "signin":
                resultado = self.__resolverSignin(datos)
            elif peticion == "recupPass":
                resultado = self.__resolverRecuperarPassword(datos)
            elif peticion == "cambiarPass":
                resultado = self.__resolverCambiarPassword(datos)
            elif peticion == "logout":
                resultado = self.__resolverLogout(datos)
            elif peticion == "getPerfil":
                resultado = self.__resolverGetPerfil(datos)

            elif peticion == "subirVideo":
                resultado = self.__resolverSubirVideo(datos)
            elif peticion == "getMisVideos":
                resultado = self.__resolverGetMisVideos(datos)
            elif peticion == "getVideos":
                resultado = self.__resolverGetVideos(datos)
            elif peticion == "getVideosLike":
                resultado = self.__resolverGetVideosLike(datos)
            elif peticion == "eliminarVideo":
                resultado = self.__resolverEliminarVideo(datos)

            elif peticion == "voto":
                resultado = self.__resolverVoto(datos)
            elif peticion == "verVotos":
                resultado = self.__resolverVerVotos(datos)

            elif peticion == "addComentario":
                resultado = self.__resolverAddComentario(datos)
            elif peticion == "getComentarios":
                resultado = self.__resolverGetComentarios(datos)

            else:
                resultado = {"resultado": 5, "statusCode": "Peticion invalida"}
        return resultado

# res = ResolutorSolicitudes()
# print(res.resolverSolicitud({"peticion": "login", "usuario": "Pato", "password": "Pato"}))
# print(res.resolverSolicitud({"peticion": "signin", "nombre": "Pato2", "apellido": "Pato2", "usuario": "Pato2",
#                              "correo": "Pato@Pato.pato2", "password": "Pato2",
#                              "pregunta": "Red", "respuesta": "Red"}))
# print(res.resolverSolicitud({"peticion": "recup", "usuario": "Pato", "color": "Red", "correo": "Pato@Pato.pato"}))
# print(res.resolverSolicitud({"peticion": "cambiarPass",
# "cookie": "81f978e9-d793-474f-b8da-aba550bb573d", "password": "Pato", "newpass": "Pato2"}))
# print(res.resolverSolicitud({"peticion": "logout", "cookie": "b6156e8b-5029-49b1-8af4-e5afc6f46114"}))
# print(res.resolverSolicitud({"peticion": "getPerfil", "cookie": "81f978e9-d793-474f-b8da-aba550bb573d"}))
# print(res.resolverSolicitud({"peticion": "subirVideo", "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
#                              "nombreVideo": "Video 1 de pato.mp1",
#                              "etiquetas": "#Pato#PatoPutoAmo#PrimerVideo#PrimerUsuario", "size": "0"}))
# di: dict = res.resolverSolicitud({"peticion": "getVideos", "cookie": "81f978e9-d793-474f-b8da-aba550bb573d"})
# di: dict = res.resolverSolicitud({"peticion": "getVideos", "cookie": "332b893e-c940-4959-bd2b-0b5c96a04426"})
# impVideos(di["listaVideo"])

# print(res.resolverSolicitud({"peticion": "eliminarVideo", "cookie": "332b893e-c940-4959-bd2b-0b5c96a04426", "nombrevideo": "Video 0 de pato.mp1"}))
# print(res.resolverSolicitud({"peticion": "eliminarVideo", "cookie": "81f978e9-d793-474f-b8da-aba550bb573d", "nombrevideo": "Video 0 de pato.mp1"}))
"""for i in range(0, 10):
    print(res.resolverSolicitud({"peticion": "subirVideo", "cookie": "81f978e9-d793-474f-b8da-aba550bb573d",
                                 "nombreVideo": "Video " + str(i) + " de pato.mp1",
                                 "visualizacion": EnumType.Private.value,
                                 "etiquetas": "#Pato#PatoPutoAmo#PrimerVideo#PrimerUsuario", "size": "0"}))"""
"81f978e9-d793-474f-b8da-aba550bb573d"
"1970796d-b103-4eda-bf19-8a325d766d4c"
"332b893e-c940-4959-bd2b-0b5c96a04426"

