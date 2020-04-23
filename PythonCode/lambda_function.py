import sys
import hashlib
from Singleton import Singleton, variableCorrecta
import pymysql
#import boto3
from enum import Enum


class EnumType(Enum):
    Public = 1
    Private = 2
    EnlaceOnly = 3


class BucketObject:
    __bucketname: str = 'distribui4'
    __s3 = None  # boto3.resource("s3")

    def __init__(self, bucketname: str):
        self.__bucketname = bucketname

    def saveFile(self, path: str, content, ):
        return None


# """
# {
#   "peticion": "login",
#   "usuario": "Pato",
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
#   "nombre": "Pato",
#   "apellido": "",
#   "usuario": "Pato",
#   "correo": "Pato@Pato.pato",
#   "password": "Pato",
#   "color": "Red"
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
        matr = mat_mult(matriz1, matriz2)
        encoded_string = str(matr).encode('utf8')
        path = 'result.txt'
        s3 = boto3.resource("s3")
        s3.Bucket(BUCKET_NAME).put_object(Key=path, Body=encoded_string, ACL="public-read")
        resultado = {"resultado": 69, "statusCode": "OK", "result": "http://distribui4.s3-website-us-east-1.amazonaws.com/" + path}
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


conector = DBObject("18.234.24.37", True)

print(conector.singin("Pato2", "Pato2", "Pato2", "Pato2", "Pato2", "Red"))
# print(conector.login("Pato", "Pato2"))
# print(conector.getIntentos("Pato"))
# print(conector.setIntentos("Pato", 0))
# print(conector.getIntentos("Pato"))
# print(conector.incrementoIntentos("Paa"))
# print(conector.deleteUsuario("Pato"))
# print(conector.deleteUsuarioWEB("Pato", "Pato"))
print(conector.showUsers())
# print(conector.cambiarpasswd("Pato", "Pato", "Pato2"))



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
