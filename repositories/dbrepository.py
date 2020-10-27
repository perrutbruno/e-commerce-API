from repositories.db import DBHandler

class BaseRepository:
    def __init__(self, table):
        self.table = table
        self._db = DBHandler()
        self.db_conn = self._db.db_connection()
 
    def raw_select(self, query):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()

        #Executa a query no banco com o cursor aberto
        cursor.execute(query)

        #Aloca o resultado da query na variável result para expor o resultado
        result = cursor.fetchall()
        
        #Fecha o cursor
        cursor.close()

        #Retorna o resultado da query
        return result
 
 
    def select(self, fields = "*"):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()
 
        field_masks = []
 
        #Adiciona na lista field_masks declarada acima cada parametro passado no método select para montagem da query de select
        for field in fields:
            field_masks.append(field)

        #Formata a lista field masks adicionando um , após cada string para montagem da query.
        field_masks_format = ', '.join(field_masks) 

        query = "SELECT {0} FROM {1};".format(field_masks_format,self.table)

        #Executa no db query acima com os valores substituídos pelos valores das variáveis no format.
        cursor.execute(query)

        #Aloca em uma var todos os resultados da query passada
        query_result = cursor.fetchall()

        #Fecha cursor aberto para manipulação dos dados do db, liberando o mesmo.
        cursor.close()

        #Retorna os resultados da query
        return query_result
 
    def update(self, fieldsValues, whereClause):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()

        values_masks = []
        values_where_masks = []

        #Converte o valor em string para encaixe na query
        for field in fieldsValues:
            values_masks.append(f"{field} = \"{fieldsValues[field]}\"")
        for key, value in whereClause.items():
            if self.get_type(value) == '%s':
                values_where_masks.append(f"{key} = \"{value}\"")

        #Monta a query com os parametros formatados
        query = "UPDATE {0} SET {1} WHERE {2}".format(self.table, ', '.join(values_masks), ' AND '.join(values_where_masks))

        #Executa no db query acima com os valores substituídos pelos valores das variáveis no format.
        cursor.execute(query)

        #Faz o commit pro banco para executar as mudanças
        self.db_conn.commit()

        #Aloca numa var o valor de rows afetadas pela alteração para explicitar no retorno
        af_rows = str(cursor.rowcount)

        #Fecha cursor aberto para manipulação dos dados do db, liberando o mesmo.
        cursor.close()

        #Retorna o valor de mudanças no banco
        return af_rows + ' affected rows no banco'
 
    def get_type(self, variable):
        if type(variable) is int:
            return "%i"
        elif type(variable) is str:
            return "%s"
        elif type(variable) is float:
            return "%f"
 
class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__('product')
 
    def get_all(self):
        self.raw_select("SELECT * FROM product")
 
    def get_by_product_id(self, product_id):
        query_result =  self.raw_select(("SELECT * FROM product WHERE product_id = %s") % (product_id))

        return query_result 

    def get_by_barcodes(self, barcodes):
        query_result =  self.raw_select(("SELECT * FROM product WHERE barcodes = %s") % (barcodes))   

        return query_result

    def get_by_sku(self, sku):
        query_result =  self.raw_select(("SELECT * FROM product WHERE sku = %s") % (sku))   

        return query_result

    def select_by_fields(self, params = {}, start = 0, num = 10):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor(dictionary=True)

        fields = ["*"]
        where = {}

        if 'fields' in params:
            fields = params['fields']

        if 'where' in params:
            where = params['where']

        #Monta a query conforme variáveis e converte o fields adicionando , dentre os índices na lista
        query = "SELECT {} FROM {}".format(', '.join(fields), self.table)

        if where != {}:
            query += self.__generate_where(where, start, num)

        print(query)
        #Executa no db query acima com os valores substituídos pelos valores das variáveis no format.
        cursor.execute(query)

        #Aloca em result todos os resultados da query no banco
        result = cursor.fetchall()

        #Fecha o cursor de manipulação do db
        cursor.close()

        #Retorna o resultado
        return result

    def __generate_where(self, where, start, num):
        where_clause = []

        for column in where:
            where_clause.append("{} = \"{}\"".format(column, where[column]))
                    
        return " WHERE {} AND product_id >= {} ORDER BY product_id LIMIT {};".format(" AND ".join(where_clause), start, num)

#dbzada = DBHandler()
# cursor = dbzada.db_connection().cursor()

# cursor.execute("SELECT * FROM product;")
# rows = cursor.fetchall()

# for r in rows:
#     print(r)

product_repository = ProductRepository()

# print(product_repository.get_by_fields({'1'}))

# #print(product_repository.select())

# print(product_repository.select_by_fields({
#     "title": "titles",
#     "product_id": "1",
#    "coluna2": 2
# },
#{
    #"product_id":'1',
    # "sku":"BOT-1234"
#}
#))

# print(product_repository.select_by_fields({
#    "fields": ["product_id", "sku", "title"], 
#    "where": {
#       "product_id": 1,
#       "sku": "BOT-1234",
#    }
# }))
 
#product_repository.get_all()

#product_repository.get_by_product_id("12345")