import sys
import hashlib
from Singleton import Singleton, variableCorrecta
import pymysql


class DBObject:
    __metaclass__ = Singleton
    connector = None
    __host: str = "52.55.253.67"
    __user: str = "monty"
    __passwd: str = "some_pass"
    __dbname: str = "serv"
    __iniciado: bool = False

    def __init__(self):
        try:
            self.connector = pymysql.connect(host=self.__host, port=3306, user=self.__user, passwd=self.__passwd, db=self.__dbname, connect_timeout=2)
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


def mat_mult(a, b):
    result = []
    result1 = []
    while len(a) > 0:
        d = 0
        a1 = a[:1:]
        c = True
        while d < len(a1):
            for x in b:
                for x1 in x:
                    result.append(x1 * a1[0][d])
                d = d + 1
        a.pop(0)
    result = [result[i:i + len(b[0])] for i in range(0, len(result), len(b[0]))]
    sum2 = 0
    while len(result) > 0:

        for X in range(len(result[0])):
            for Y in range(len(b)):
                sum2 = sum2 + result[Y][X]
            result1.append(sum2)
            sum2 = 0
        for s in range(len(b)):
            result.pop(0)
    result1 = [result1[i:i + len(b[0])] for i in range(0, len(result1), len(b[0]))]
    return result1


def resolverMatriz4x4(datos: dict):
    matriz1 = datos.get("matriz1")
    matriz2 = datos.get("matriz2")
    if matriz1 is None:
        resultado = {"resultado": 8, "statusCode": "matriz 1 null"}
    elif matriz2 is None:
        resultado = {"resultado": 9, "statusCode": "matriz 2 null"}
    else:
        resultado = {"resultado": 69, "statusCode": "OK", "result": mat_mult(matriz1, matriz2)}
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
            elif peticion == "matriz4x4":
                resultado = resolverMatriz4x4(datos)
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


# dicc: dict = {"username": "Pato", "password": "Pato", "peticion": "login"}
# print(lambda_handler(dicc, None))
"""
matriz1 = [[1, 2, 4, 6], [2, 3, 5, 1], [2, 3, 1, 2], [12, 3, 23, 4]]
matriz2 = [[1, 2, 2, 6], [2, 3, 5, 22], [3, 3, 1, 4], [2, 3, 3, 12]]
dicc: dict = {
    "peticion": "matriz4x4",
    "matriz1": matriz1,
    "matriz2": matriz2
}
print(lambda_handler(dicc, None))

{
    "peticion": "login",
    "username": "Pato",
    "password": "Pato"
}


0: No hay query
1: Conecxion a la db no correcta
2: Tipo de peticion vacia
3: Demasiados argumentos
4: Faltan argumentos
5: Peticion invalida
6: username null
7: password null
8: matriz 1 null
9: matriz 2 null


69: OK
"""
