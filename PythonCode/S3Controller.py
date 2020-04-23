#import boto3
import hashlib
from Singleton import variableCorrecta
import ControladorBaseDatos
from enum import Enum
import uuid

local = "192.168.0.107"


class EnumType(Enum):
    Public = "public-read"
    Private = 2
    EnlaceOnly = 3


class BucketObject:
    __bucketname: str = 'distribui4'
    __s3 = None  # boto3.resource("s3")
    __bucket = None

    def __init__(self, bucketname: str):
        self.__bucketname = bucketname
        # self.__bucket = self.__s3.Bucket(self.__bucketname)

    def saveFile(self, path: str, content, visualizacion: EnumType):
        encode_content: str = content.encode('utf8')
        self.__bucket.put_object(Key=path, Body=encode_content, ACL=visualizacion)
        return None


class ResolutorSolicitudes:
    __dbController = None
    __numIntentos: int = 3
    __bucketObject: BucketObject = None

    def __init__(self):
        self.__dbController = ControladorBaseDatos.ControladorBaseDatos(local)
        self.__bucketObject = BucketObject("distribui4")

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
            if res_login is False:
                intentos = self.__dbController.getIntentos(usuario)
                if intentos is not None:
                    if intentos >= self.__numIntentos:
                        self.__dbController.deleteUsuario(usuario)
                    else:
                        self.__dbController.setIntentos(usuario, int(intentos) + 1)
            else:
                self.__dbController.setIntentos(usuario, 0)
            resultado = {"resultado": 69, "statusCode": "OK", "accesoConcedido": res_login}
        return resultado

    # """
    # {
    #   "peticion": "signin",
    #   "nombre": "Pato",
    #   "apellido": "",
    #   "usuario": "Pato",
    #   "correo": "Pato@Pato.pato",
    #   "password": "Pato",
    #   "color": "Red"
    # }
    # nombre, apellido, usuario, correo, passwd, color
    # """
    def __resolverSignin(self, datos: dict):
        nombre = datos.get("nombre")
        apellido = datos.get("apellido")
        usuario = datos.get("usuario")
        correo = datos.get("correo")
        passwd = datos.get("password")
        color = datos.get("color")
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
        elif variableCorrecta(color) is False:
            resultado = {"resultado": 7, "statusCode": "color null"}
        else:
            resultado = {"resultado": 69, "statusCode": "OK",
                         "accesoConcedido": self.__dbController.singin(nombre, apellido, usuario, correo, passwd, color)
                         }
        return resultado

    # {
    #     "peticion": "recupPass",
    #     "usuario": "Pato",
    #     "color": "Red",
    #     "correo": "Pato@Pato.pato"
    # }
    def __resolverRecuperarPassword(self, datos: dict):
        usuario = datos.get("usuario")
        color = datos.get("color")
        correo = datos.get("correo")
        if variableCorrecta(usuario) is False:
            resultado = {"resultado": 7, "statusCode": "usuario null"}
        elif variableCorrecta(color) is False:
            resultado = {"resultado": 7, "statusCode": "color null"}
        elif variableCorrecta(correo) is False:
            resultado = {"resultado": 7, "statusCode": "correo null"}
        else:
            if self.__dbController.getRespuestaValida(usuario, correo, color) is True:
                newpass = str(uuid.uuid4())
                self.__dbController.cambiarpasswd(usuario, newpass)
                resultado = {"resultado": 69, "statusCode": "OK", "color": newpass}
            else:
                resultado = {"resultado": 7, "statusCode": "respuesta erronea", "color": None}
        return resultado

    # {
    #     "peticion": "cambiarPass",
    #     "usuario": "Pato",
    #     "password": "Pato",
    #     "newpass": "Pato2"
    # }
    def __resolverCambiarPassword(self, datos:dict):
        usuario = datos.get("usuario")
        passwd = datos.get("password")
        newpass = datos.get("newpass")
        if variableCorrecta(usuario) is False:
            resultado = {"resultado": 7, "statusCode": "usuario null"}
        elif variableCorrecta(passwd) is False:
            resultado = {"resultado": 7, "statusCode": "passwd null"}
        elif variableCorrecta(newpass) is False:
            resultado = {"resultado": 7, "statusCode": "newpass null"}
        else:
            resultado = {"resultado": 7, "statusCode": "OK",
                         "cambioPass": self.__dbController.cambiarpasswdWEB(usuario, passwd, newpass)}
        return resultado

    # endregion
    # region Videos
    # {
    #     "peticion": "subirVideo",
    #     "usuariovideo": "Pato",
    #     "nombrevideo": "Video de Pato",
    #     "etiquetas": "tuputamadre.jpg#hashtag",
    #     "size": "0",
    #     "ruta": "ruta"
    # }
    def __resolverSubirVideo(self, datos: dict):
        usuariovideo = datos.get("usuariovideo")
        nombrevideo = datos.get("nombrevideo")
        etiquetas = datos.get("etiquetas")
        size = datos.get("size")
        ruta = usuariovideo + "/" + nombrevideo
        if variableCorrecta(usuariovideo) is False:
            resultado = {"resultado": 7, "statusCode": "usuariovideo null"}
        elif variableCorrecta(nombrevideo) is False:
            resultado = {"resultado": 7, "statusCode": "nombrevideo null"}
        elif variableCorrecta(etiquetas) is False:
            resultado = {"resultado": 7, "statusCode": "etiquetas null"}
        elif variableCorrecta(size) is False:
            resultado = {"resultado": 7, "statusCode": "size null"}
        else:
            self.__dbController.subirVideo(usuariovideo, nombrevideo, etiquetas, size, ruta)



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
            elif peticion == "subirVideo":
                resultado = self.__resolverSubirVideo(datos)
            else:
                resultado = {"resultado": 5, "statusCode": "Peticion invalida"}
        return resultado


res = ResolutorSolicitudes()
# print(res.resolverSolicitud({"peticion": "login", "usuario": "Pato", "password": "Pato"}))
# print(res.resolverSolicitud({"peticion": "signin", "nombre": "Pato", "apellido": "Pato", "usuario": "Pato",
#                              "correo": "Pato@Pato.pato", "password": "Pato", "color": "Red"}))
# print(res.resolverSolicitud({"peticion": "recup", "usuario": "Pato", "color": "Red", "correo": "Pato@Pato.pato"}))
# print(res.resolverSolicitud({"peticion": "cambiarPass", "usuario": "Pato", "password": "Pato", "newpass": "Pato"}))

