import mysql.connector

#Classe modelo singleton do manuseador do banco de dados
class DBHandler(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(DBHandler, self).__new__(self)
            self.__db = mysql.connector.connect(
                    host="localhost",
                    user="bruno",
                    database="hurb_test_assignment",
                    password="bruno"
                )
        return self.instance

#Método de retorno da conexão do db criada em __new__ quando instanciamos o objeto
    def db_connection(self):
        return self.__db


dbzada = DBHandler()
cursor = dbzada.db_connection().cursor()

cursor.execute("SELECT * FROM product;")
rows = cursor.fetchall()

for r in rows:
    print(r)