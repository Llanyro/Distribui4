import sys
import hashlib
from sql import BaseDatos
from Singleton import variableCorrectaList
import datetime


class ControladorBaseDatos(BaseDatos):
    __tabaUsuarios: str = "USUARIO"
    __tablaComentarios: str = "COMENTARIO"
    __tablaVideos: str = "VIDEO"
    __tablaVoto: str = "VOTO"

    def __init__(self, hostname: str):
        super().__init__(3306, "AWS", hostname, "monty", "some_pass", 1)
        self.__debudMode = True
        self.connect()

    # region Usuarios
    # Muestra todos los usuarios de la DB
    def showUsers(self):
        return self.select("select * from " + self.__tabaUsuarios, {})

    # Crea un nuevo usuario en la base de datos
    def singin(self, nombre: str, apellido: str, usuario: str, correo: str, passwd: str, color: str):
        if variableCorrectaList([nombre, apellido, usuario, correo, passwd, color]) is False:
            resultado = False
        else:
            command = "insert into " + self.__tabaUsuarios + " values ( " \
                      + "%(nombre)s, " + "%(apellido)s, " \
                      + "%(usuario)s, " + "%(correo)s, " \
                      + "%(passhash)s, " + "%(color)s, " + "0 )"
            passhash = hashlib.sha3_256(passwd.encode()).hexdigest()
            dicc = {'nombre': nombre, "apellido": apellido, "usuario": usuario, "correo": correo,
                    "passhash": passhash, "color": color}
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
            command = "SELECT usuario FROM " + self.__tabaUsuarios + \
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
            resultado = -1
        else:
            command = "select intento from " + self.__tabaUsuarios + " where usuario= %(usuario)s"
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
            command = "update " + self.__tabaUsuarios + " set intento= %(intentos)s where usuario= %(usuario)s"
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
            command = "delete from " + self.__tabaUsuarios + " where usuario=%(usuario)s"
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
            command = "delete from " + self.__tabaUsuarios + " where usuario=%(usuario)s and password=%(passhash)s"
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
            command = "update " + self.__tabaUsuarios + \
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
            command = "update " + self.__tabaUsuarios + \
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
    def getRespuestaValida(self, usuario: str, correo: str, color: str):
        if variableCorrectaList([usuario, color, correo]) is False:
            resultado = -1
        else:
            command = "select color from " + self.__tabaUsuarios + " where usuario= %(usuario)s " \
                                                                   "and color=%(color)s and " \
                                                                   "correo=%(correo)s"
            result = self.selectCount(command, {"usuario": usuario, "color": color, "correo": correo})
            if result == 1:
                resultado = True
            elif result == 0:
                resultado = False
            else:
                sys.exit()
        return resultado

    # endregion
    # region Videos
    # Sube un video a la base de datos
    def subirVideo(self, usuariovideo: str, nombrevideo: str, etiquetas: str, size: str, ruta: str):
        if variableCorrectaList([usuariovideo, nombrevideo, etiquetas, size, ruta]) is False:
            resultado = False
        else:
            command = "insert into " + self.__tablaVideos + " values ( " \
                      + "%(usuariovideo)s, " + "%(nombrevideo)s, " \
                      + "%(etiquetas)s, " + "%(size)s, " \
                      + "%(ruta)s, " + "%(date)s )"
            dicc = {'usuariovideo': usuariovideo, "nombrevideo": nombrevideo,
                    "etiquetas": etiquetas, "size": size,
                    "ruta": ruta, "date": datetime.datetime.now()}
            cambios = self.update(command, dicc)
            if cambios == 0:
                resultado = False
            elif cambios == 1:
                resultado = True
            else:
                sys.exit()
        return resultado

    # endregion


local = "192.168.0.107"

# controlador = ControladorBaseDatos("192.168.1.41")
controlador = ControladorBaseDatos(local)
# print(controlador.getRespuestaValida("Pata", "Rojo"))
# print(controlador.deleteUsuarioWEB("PaTo4", "Password1"))
# print(controlador.deleteUsuario("Pato"))
# print(controlador.cambiarpasswdWEB("Pato", "Pato2", "Pato"))
# print(controlador.incrementarIntentos("Pato"))
# print(controlador.setIntentos("Pato", 10))
# print(controlador.singin("Pato", "Pato", "Pato", "aaa", "Password1", "Rojo"))
# print(controlador.showUsers())
# print(controlador.login("Pato4", "Password1"))
# print(controlador.getIntentos("Pat1o"))
"c84f13b8cb9cbcda1ee1b7703db954f57ae07835b8421fd00c46fc407f2ddcef"
print(controlador.subirVideo("Pato", "Video de Pato", "#tuputamadre.jpg#hashtag", "0", "Pato/Video de Pato"))
