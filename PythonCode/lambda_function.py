def lambda_handler(event, context):
    if event is None:
        resultado = {"resultado": "0", "statusCode": "No hay query"}
    elif conector.isIniciado() is False:
        resultado = {"resultado": 1, "statusCode": "Conecxion a la db no correcta"}
    else:
        resultado = None
    return resultado


conector = None

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
