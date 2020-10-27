import mysql.connector

#Classe modelo singleton do manuseador do banco de dados
class DBHandler(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBHandler, cls).__new__(cls)
            cls.__db = mysql.connector.connect(
                    host="127.0.0.1",
                    user="bruno",
                    database="hurb_test_assignment",
                    password="bruno"
                )
        return cls.instance

#Método de retorno da conexão do db criada em __new__ quando instanciamos o objeto
    def db_connection(self):
        return self.__db


