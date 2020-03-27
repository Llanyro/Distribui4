import sys
import hashlib
from Singleton import Singleton, variableCorrecta
import pymysql


class DBObject:
    __metaclass__ = Singleton
    connector = None
    __host: str = "3.92.173.228"
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


# """
# {
#   "peticion": "login",
#   "username": "Pato",
#   "password": "Pato"
# }
# """
def resolverLogin(datos: dict):
    usuario = datos.get("username")
    pss = datos.get("password")
    if usuario is None:
        resultado = {"resultado": 6, "statusCode": "username null"}
    elif pss is None:
        resultado = {"resultado": 7, "statusCode": "password null"}
    else:
        resultado = {"resultado": 69, "statusCode": "OK", "accesoConcedido": str(conector.login(usuario, pss))}
    return resultado


# """
# {
#   "peticion": "signin",
#   "username": "Pato",
#   "password": "Pato"
# }
# """
def resolverSignin(datos: dict):
    usuario = datos.get("username")
    pss = datos.get("password")
    if usuario is None:
        resultado = {"resultado": 6, "statusCode": "username null"}
    elif pss is None:
        resultado = {"resultado": 7, "statusCode": "password null"}
    else:
        resultado = {"resultado": 69, "statusCode": "OK", "accesoConcedido": str(conector.singin(usuario, pss))}
    return resultado


def resolverSolicitud(datos: dict):
    size = len(datos)
    if size == 3:
        peticion = datos.get("peticion")
        if peticion is None:
            resultado = {"resultado": 2, "statusCode": "Tipo de peticion vacia"}
        else:
            if peticion == "login":
                resultado = resolverLogin(datos)
            elif peticion == "signin":
                resultado = resolverSignin(datos)
            else:
                resultado = {"resultado": 5, "statusCode": "Peticion invalida"}
    elif size > 3:
        resultado = {"resultado": 3, "statusCode": "Demasiados argumentos"}
    else:
        resultado = {"resultado": 4, "statusCode": "Faltan argumentos"}
    return resultado


def lambda_handler(event, context):
    if event is None:
        resultado = {"resultado": "0", "statusCode": "No hay query"}
    elif conector.isIniciado() is False:
        resultado = {"resultado": 1, "statusCode": "Conecxion a la db no correcta"}
    else:
        resultado = resolverSolicitud(event)
    return resultado


dicc: dict = {"username": "Pato", "password": "Pato", "peticion": "signin"}
print(lambda_handler(dicc, None))

"""
0: No hay query
1: Conecxion a la db no correcta
2: Tipo de peticion vacia
3: Demasiados argumentos
4: Faltan argumentos
5: Peticion invalida
6: username null
7: password null

69: OK
"""
