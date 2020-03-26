class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance


def variableCorrecta(var: str):
    if var is None:
        resultado = False
    elif var.__len__() == 0:
        resultado = False
    else:
        resultado = True
    return resultado


def variableCorrectaInt(var: int):
    if var is None:
        resultado = False
    elif var < 0:
        resultado = False
    else:
        resultado = True
    return resultado
