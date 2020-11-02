import mysql.connector, os

#Classe modelo singleton do manuseador do banco de dados
class DBHandler(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBHandler, cls).__new__(cls)
            db_host = os.getenv("DB_HOST")
            #Pega variaveis de ambiente para manusear a conexao com o db
            cls.__db = mysql.connector.connect(
                    host=db_host,
                    user="root",
                    database="hurb_test_assignment",
                    password="hurb"
                )
        return cls.instance

#Método de retorno da conexão do db criada em __new__ quando instanciamos o objeto
    def db_connection(self):
        return self.__db


