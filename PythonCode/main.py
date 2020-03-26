import sys
import hashlib
from Singleton import Singleton, variableCorrecta
import pymysql


class DBObject:
    __metaclass__ = Singleton
    connector = None
    __host: str = "192.168.1.41"
    __user: str = "monty"
    __passwd: str = "some_pass"
    __dbname: str = "serv"
    __iniciado: bool = False

    def __init__(self):
        try:
            self.connector = pymysql.connect(host=self.__host, port=3306, user=self.__user, passwd=self.__passwd, db=self.__dbname)
            self.__iniciado = True
        except pymysql.MySQLError as e:
            self.__iniciado = False
            print(e)
            sys.exit()

    def login(self, username: str, passwd: str):
        if variableCorrecta(username) is False or variableCorrecta(passwd) is False:
            resultado = False
        else:
            try:
                with self.connector.cursor() as cursor:
                    pss = hashlib.sha3_256(passwd.encode()).hexdigest()
                    command = "SELECT * FROM USERS where username='" + username + "' and password='" + pss + "'"
                    print(command)
                    cursor.execute(command)
                    if cursor.rowcount == 1:
                        resultado = True
                    elif cursor.rowcount == 0:
                        resultado = False
                    else:
                        sys.exit()
            except pymysql.MySQLError as e:
                print(e)
                resultado = False
        return resultado

    def singin(self, username: str, passwd: str):
        if variableCorrecta(username) is False or variableCorrecta(passwd) is False:
            resultado = False
        else:
            try:
                with self.connector.cursor() as cursor:
                    pss = hashlib.sha3_256(passwd.encode()).hexdigest()
                    command = "insert into USERS values ( '" + username + "' , '" + pss + "' )"
                    print(command)
                    cursor.execute(command)
                    self.connector.commit()
                    resultado = True
            except pymysql.MySQLError as e:
                print(e)
                resultado = False
        return resultado

    def showUsers(self):
        usuarios: list = []
        cur = self.connector.cursor()
        cur.execute("select * from USERS")
        for row in cur:
            usuarios.append(row[0])
        return usuarios

    def isIniciado(self):
        return self.__iniciado


conector = DBObject()


def resolverLogin(datos: dict):
    usuario = datos.get("username")
    pss = datos.get("password")
    if usuario is None:
        resultado = "{\"resultado\":6,\"status\":\"username null\"}"
    elif pss is None:
        resultado = "{\"resultado\":7,\"status\":\"password null\"}"
    else:
        resultado = "{\"resultado\":69,\"status\":\"OK\",\"accesoConcedido\":" + str(conector.login(usuario, pss)) +\
                    "}"
    return resultado


def resolverSignin(datos: dict):
    usuario = datos.get("username")
    pss = datos.get("password")
    if usuario is None:
        resultado = "{\"resultado\":6,\"status\":\"username null\"}"
    elif pss is None:
        resultado = "{\"resultado\":7,\"status\":\"password null\"}"
    else:
        resultado = "{\"resultado\":69,\"status\":\"OK\",\"accesoConcedido\":" + str(conector.singin(usuario, pss)) +\
                    "}"
    return resultado


def resolverSolicitud(datos: dict):
    size = len(datos)
    if size == 3:
        peticion = datos.get("peticion")
        if peticion is None:
            resultado = "{\"resultado\":2,\"status\":\"Tipo de peticion vacia\"}"
        else:
            if peticion == "login":
                resultado = resolverLogin(datos)
            elif peticion == "signin":
                resultado = resolverSignin(datos)
            else:
                resultado = "{\"resultado\":5,\"status\":\"Peticion invalida\"}"
    elif size > 3:
        resultado = "{\"resultado\":3,\"status\":\"Demasiados argumentos\"}"
    else:
        resultado = "{\"resultado\":4,\"status\":\"Faltan argumentos\"}"
    return resultado


def lambda_handler(event, context):
    datos = event.get("query")
    if datos is None:
        resultado = "{\"resultado\":0,\"status\":\"No hay query\"}"
    elif conector.isIniciado() is False:
        resultado = "{\"resultado\":1,\"status\":\"Conecxion a la db no correcta\"}"
    else:
        resultado = resolverSolicitud(datos)
    return resultado


dicc: dict = {"username": "Pato", "password": "Pato", "peticion": "login"}
print(lambda_handler({"query": dicc}, None))

"""
0: No hay query
1: Conecxion a la db no correcta
2: Tipo de peticion vacia
3: Demasiados argumentos
4: Faltan argumentos
5: Peticion invalida
6: username null-
7: password null

69: OK
"""
