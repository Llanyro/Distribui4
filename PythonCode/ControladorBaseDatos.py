import sys
import hashlib
from sql import BaseDatos
from Singleton import variableCorrectaList
import datetime
from enum import Enum


class EnumType(Enum):
    Public = "public-read"
    Private = "private"
    EnlaceOnly = 3


def impVideos(videos: list):
    if videos.__len__() == 0:
        print("No hay videos disponibles")
    else:
        for vid in videos:
            print("Nombre Video: " + vid[1])
            print("Usuario: " + vid[0])
            print("Etiquetas: " + vid[2])
            print("Visualizacion: " + vid[5])
            print("Pecha Pub: " + str(vid[6]))
            print("")


class ControladorBaseDatos(BaseDatos):
    __tablaUsuarios: str = "USUARIO"
    __tablaComentarios: str = "COMENTARIO"
    __tablaVideos: str = "VIDEO"
    __tablaVoto: str = "VOTO"
    __tablaCookies: str = "COOKIE"

    def __init__(self, hostname: str):
        super().__init__(3306, "AWS", hostname, "monty", "some_pass", 1)
        self.__debudMode = True
        self.connect()

    # region Usuarios
    # Muestra todos los usuarios de la DB
    def showUsers(self):
        return self.select("select * from " + self.__tablaUsuarios, {})

    # Crea un nuevo usuario en la base de datos
    def singin(self, nombre: str, apellido: str, usuario: str, correo: str, passwd: str, pregunta: str, respuesta: str):
        if variableCorrectaList([nombre, apellido, usuario, correo, passwd, pregunta, respuesta]) is False:
            resultado = False
        else:
            command = "insert into " + self.__tablaUsuarios + " values ( " \
                      + "%(nombre)s, %(apellido)s, %(usuario)s, %(correo)s, " \
                      + "%(passhash)s, %(pregunta)s, %(respuesta)s, 0 )"
            passhash = hashlib.sha3_256(passwd.encode()).hexdigest()
            dicc = {'nombre': nombre, "apellido": apellido, "usuario": usuario, "correo": correo,
                    "passhash": passhash, "pregunta": pregunta, "respuesta": respuesta}
            cambios = self.update(command, dicc)
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Devuelve si el usuario y la contraseña coinciden en la DB
    def login(self, usuario: str, passwd: str):
        if variableCorrectaList([usuario, passwd]) is False:
            resultado = False
        else:
            passhash = hashlib.sha3_256(passwd.encode()).hexdigest()
            command = "SELECT usuario FROM " + self.__tablaUsuarios + \
                      " where usuario= %(usuario)s and password= %(passhash)s"
            dicc = {'usuario': usuario, 'passhash': passhash}
            result = self.selectCount(command, dicc)
            if result == 1:
                # Seteamos los intentos del usuario a 0
                resultado = True
            elif result == 0:
                # Añadimos intento al usuario
                resultado = False
            else:
                sys.exit()
        return resultado

    # Devuelve los intentos de solicitar la pass a un usuario
    def getIntentos(self, usuario):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select intento from " + self.__tablaUsuarios + " where usuario= %(usuario)s"
            resultado = self.select(command, {"usuario": usuario})
            if resultado.__len__() == 1:
                if resultado[0].__len__() == 1:
                    resultado = resultado[0][0]
                else:
                    resultado = None
            else:
                resultado = None
        return resultado

    # Cambia el valor de intentos de un usuario (Password)
    def setIntentos(self, usuario: str, intentos: int):
        if variableCorrectaList([usuario, str(intentos)]) is False:
            resultado = False
        else:
            command = "update " + self.__tablaUsuarios + " set intento= %(intentos)s where usuario= %(usuario)s"
            dicc = {"usuario": usuario, "intentos": intentos}
            cambios = self.update(command, dicc)
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Incrementa en 1 el numero de intentos de un usuario
    def incrementarIntentos(self, usuario: str):
        intactuales = self.getIntentos(usuario)
        if intactuales is None:
            resultado = intactuales
        else:
            intentos = int(intactuales) + 1
            resultado = self.setIntentos(usuario, intentos)
        return resultado

    # Elimina un usuario solo con su nombre de usuario (Funciones internas del servidor)
    def deleteUsuario(self, usuario: str):
        if variableCorrectaList([usuario]) is False:
            resultado = False
        else:
            command = "delete from " + self.__tablaUsuarios + " where usuario=%(usuario)s"
            cambios = self.update(command, {"usuario": usuario})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Elimina un usuario pidiendo el usuario y la contraseña (WEB)
    def deleteUsuarioWEB(self, usuario: str, passwd: str):
        if variableCorrectaList([usuario, passwd]) is False:
            resultado = False
        else:
            command = "delete from " + self.__tablaUsuarios + " where usuario=%(usuario)s and password=%(passhash)s"
            passhash = hashlib.sha3_256(passwd.encode()).hexdigest()
            cambios = self.update(command, {"usuario": usuario, "passhash": passhash})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Cambia la contraseña de un usuario recibiendo el usaurio ademas de la nueva contraseña
    def cambiarpasswd(self, usuario: str, newpasswd: str):
        if variableCorrectaList([usuario, newpasswd]) is False:
            resultado = False
        else:
            command = "update " + self.__tablaUsuarios + \
                      " set password=%(newpasshash)s where usuario=%(usuario)s"
            newpasshash = hashlib.sha3_256(newpasswd.encode()).hexdigest()
            cambios = self.update(command, {"usuario": usuario, "newpasshash": newpasshash})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Cambia la contraseña de un usuario recibiendo el usaurio y contraseña actual ademas de la nueva contraseña (WEB)
    def cambiarpasswdWEB(self, usuario: str, passwd: str, newpasswd: str):
        if variableCorrectaList([usuario, passwd, newpasswd]) is False:
            resultado = False
        else:
            command = "update " + self.__tablaUsuarios + \
                      " set password=%(newpasshash)s where usuario=%(usuario)s and password=%(passhash)s"
            passhash = hashlib.sha3_256(passwd.encode()).hexdigest()
            newpasshash = hashlib.sha3_256(newpasswd.encode()).hexdigest()
            cambios = self.update(command, {"usuario": usuario, "passhash": passhash, "newpasshash": newpasshash})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Devuelve si un usuario respondio o no a la pregunta secreta la respuesta indicada
    def getRespuestaValida(self, usuario: str, correo: str, pregunta: str, respuesta: str):
        if variableCorrectaList([usuario, pregunta, correo, respuesta]) is False:
            resultado = -1
        else:
            command = "select * from " + self.__tablaUsuarios + " where usuario= %(usuario)s " \
                                                                   "and pregunta=%(pregunta)s and " \
                                                                   "correo=%(correo)s and respuesta=%(respuesta)s"
            result = self.selectCount(command, {"usuario": usuario, "respuesta": respuesta,
                                                "correo": correo, "pregunta": pregunta})
            if result == 1:
                resultado = True
            elif result == 0:
                resultado = False
            else:
                sys.exit()
        return resultado

    # Devuelve el perfil de un usuario, None si no existe
    def getPerfil(self, usuario: str):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select nombre, apellido, usuario, correo, pregunta, respuesta from " + self.__tablaUsuarios + \
                      " where usuario=%(usuario)s"
            result = self.select(command, {"usuario": usuario})
            if result.__len__() > 0:
                if result[0].__len__() > 0:
                    resultado = {"nombre": result[0][0], "apellido": result[0][1], "respuesta": result[0][5],
                                 "usuario": result[0][2], "correo": result[0][3], "pregunta": result[0][4]}
                else:
                    resultado = None
            else:
                resultado = None
        return resultado

    # endregion
    # region Videos
    # Sube un video a la DB, si visualizacion es un valor null o 0 se guarda como private
    def subirVideo(self, usuariovideo: str, nombrevideo: str, etiquetas: str, size: str, ruta: str, visualizacion: str):
        if variableCorrectaList([usuariovideo, nombrevideo, etiquetas, ruta]) is False and size != 0:
            resultado = False
        else:
            command = "insert into " + self.__tablaVideos + " values ( " \
                      + "%(usuariovideo)s, %(nombrevideo)s, %(etiquetas)s, %(size)s, " \
                      + "%(ruta)s , %(visualizacion)s , %(date)s )"
            dicc = {'usuariovideo': usuariovideo, "nombrevideo": nombrevideo,
                    "etiquetas": etiquetas, "size": size, "ruta": ruta, "date": datetime.datetime.now()}
            if variableCorrectaList([visualizacion]) is False:
                dicc.update({"visualizacion": EnumType.Private})
            else:
                dicc.update({"visualizacion": visualizacion})
            cambios = self.update(command, dicc)
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Borra un video de un usuario (el creador) dato el usaurio y el nombre del video
    def deleteVideo(self, usuariovideo: str, nombrevideo: str):
        if variableCorrectaList([usuariovideo, nombrevideo]) is False:
            resultado = False
        else:
            command = "delete from " + self.__tablaVideos + " where usuarioVideo=%(usuario)s and nombreVideo=%(nombre)s"
            cambios = self.update(command, {"usuario": usuariovideo, "nombre": nombrevideo})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # Devuelve una lista de videos con limite
    def getVideosLim(self, usuario: str, lim: int):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select * from " + self.__tablaVideos + " where usuarioVideo=%(usuario)s " \
                                                              "or estado=%(visualizacion)s limit %(lim)s, 20"
            resultado = self.select(command, {"usuario": usuario, "lim": lim, "visualizacion": EnumType.Public.value})
        return resultado

    # Devuelve una lista de videos
    def getVideos(self, usuario: str):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select * from " + self.__tablaVideos + " where usuarioVideo=%(usuario)s " \
                                                              "or estado=%(visualizacion)s"
            resultado = self.select(command, {"usuario": usuario, "visualizacion": EnumType.Public.value})
        return resultado

    # Devuelve los videos subidos por un usuario con un limite
    def getMyVideosLim(self, usuario: str, lim: int):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select * from " + self.__tablaVideos + " where usuarioVideo=%(usuario)s limit %(lim)s, 20"
            resultado = self.select(command, {"usuario": usuario, "lim": lim})
        return resultado

    # Devuelve los videos subidos por un usuario
    def getMyVideos(self, usuario: str):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select * from " + self.__tablaVideos + " where usuarioVideo=%(usuario)s"
            resultado = self.select(command, {"usuario": usuario})
        return resultado

    # endregion
    # region Cookies
    def showCookies(self):
        return self.select("select * from " + self.__tablaCookies, {})

    def getCookie(self, usuario: str):
        if variableCorrectaList([usuario]) is False:
            resultado = None
        else:
            command = "select cookie from " + self.__tablaCookies + " where usuario=%(usuario)s"
            resultado = self.select(command, {"usuario": usuario})
            if resultado.__len__() == 1:
                if resultado[0].__len__() == 1:
                    resultado = resultado[0][0]
                else:
                    resultado = None
            else:
                resultado = None
        return resultado

    def getUsername(self, cookie: str):
        if variableCorrectaList([cookie]) is False:
            resultado = None
        else:
            command = "select usuario from " + self.__tablaCookies + " where cookie=%(cookie)s"
            resultado = self.select(command, {"cookie": cookie})
            if resultado == -1 or resultado == -2:
                resultado = None
            else:
                if resultado.__len__() == 1:
                    if resultado[0].__len__() == 1:
                        resultado = resultado[0][0]
                    else:
                        resultado = None
                else:
                    resultado = None
        return resultado

    def addCookie(self, usuario: str, cookie: str):
        if variableCorrectaList([usuario, cookie]) is False:
            resultado = False
        else:
            command = "insert into " + self.__tablaCookies + " values ( %(cookie)s, %(usuario)s )"
            cambios = self.update(command, {"usuario": usuario, "cookie": cookie})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    def deleteCookie(self, cookie: str):
        if variableCorrectaList([cookie]) is False:
            resultado = False
        else:
            command = "delete from " + self.__tablaCookies + " where cookie=%(cookie)s"
            cambios = self.update(command, {"cookie": cookie})
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # endregion


local = "192.168.0.107"
juinja = "192.168.1.41"

# controlador = ControladorBaseDatos(juinja)
# print(controlador.getRespuestaValida("Pata", "Rojo"))
# print(controlador.deleteUsuarioWEB("PaTo4", "Password1"))
# print(controlador.deleteUsuario("Pato"))
# print(controlador.cambiarpasswdWEB("Pato", "Pato2", "Pato"))
# print(controlador.incrementarIntentos("Pato"))
# print(controlador.setIntentos("Pato", 10))
# print(controlador.singin("Pato", "Pato", "Pato", "aaa", "Password1", "Rojo"))
# print(controlador.showUsers())
# print(controlador.showCookies())
# impVideos(controlador.getVideos("Pato"))
# print(controlador.getPerfil("Pato2"))
# print(controlador.login("Pato4", "Password1"))
# print(controlador.getIntentos("Pat1o"))
# print(controlador.deleteVideo("Pato", "Video 1 de pato.mp1"))
# print(controlador.subirVideo("Pato", "Video de Pato", "#tuputamadre.jpg#hashtag", "0", "Pato/Video de Pato"))


