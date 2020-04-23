from Singleton import Singleton
import pymysql
from enum import Enum


class BaseDatos:
    # region Variables de la clase
    __metaclass__ = Singleton
    __port: int = 3306
    __database: str = ""
    __hostaname: str = ""
    __usuario: str = ""
    __password: str = ""
    __connect_time_out: int = 5

    __url: str = ""
    __connector = None
    __iniciado: bool = False
    __debudMode: bool = True

    __notconected: str = "Conecxion con la base de datos no realizada"
    # endregion

    # Constructor base
    def __init__(self, port: int, database: str, hostname: str, usuario: str, password: str, connect_timeout: int):
        self.__port = port
        self.__database = database
        self.__hostaname = hostname
        self.__usuario = usuario
        self.__password = password
        self.__connect_time_out = connect_timeout
        self.__debudMode = False
        self.__connector = None

    def __printf(self, something):
        if self.__debudMode:
            print(something)

    # Intenta conectarse a la DB solicitada y devuelve si esta conectado
    def connect(self):
        if self.__iniciado is False:
            try:
                self.__connector = pymysql.connect(host=self.__hostaname, port=3306, user=self.__usuario,
                                                   passwd=self.__password, db=self.__database,
                                                   connect_timeout=self.__connect_time_out)
                self.__iniciado = True
            except pymysql.MySQLError as e:
                self.__iniciado = False
                print(e)
        return self.__iniciado

    def getIniciadaConexion(self):
        return self.__iniciado

    def update(self, consulta: str, parametros: dict):
        self.__printf(consulta)
        self.__printf(parametros)
        if self.__iniciado:
            with self.__connector.cursor() as cursor:
                try:
                    resultado = cursor.execute(consulta, parametros)
                    self.__connector.commit()
                except pymysql.MySQLError as m:
                    print(m)
                    resultado = -1
        else:
            resultado = -2
            print(self.__notconected)
        return resultado

    def selectCount(self, consulta: str, parametros: dict):
        self.__printf(consulta)
        self.__printf(parametros)
        if self.__iniciado:
            with self.__connector.cursor() as cursor:
                try:
                    cursor.execute(consulta, parametros)
                    resultado = cursor.rowcount
                except pymysql.MySQLError as m:
                    print(m)
                    resultado = -1
        else:
            resultado = -2
            print(self.__notconected)
        return resultado

    def select(self, consulta: str, parametros: dict):
        self.__printf(consulta)
        self.__printf(parametros)
        if self.__iniciado:
            with self.__connector.cursor() as cursor:
                try:
                    cursor.execute(consulta, parametros)
                    resultado = []
                    for row in cursor:
                        res = []
                        for colum in row:
                            res.append(colum)
                        resultado.append(res)
                except pymysql.MySQLError as m:
                    print(m)
                    resultado = -1
        else:
            resultado = -2
            print(self.__notconected)
        return resultado
