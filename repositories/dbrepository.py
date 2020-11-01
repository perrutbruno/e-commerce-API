from db import DBHandler

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
    
    def raw_delete(self, table, statement):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()

        query = "DELETE FROM {0} where {1}".format(table,statement)
        
        #Executa a query no banco com o cursor aberto
        cursor.execute(query)

        #Faz o commit pro banco para executar as mudanças
        self.db_conn.commit()

        return 'OK'

    def raw_insert(self, query):
        """ Método da classe pai BaseRepository que todas as classes filhas herdam em que faz um insert no banco. """
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()

        try:
            #Executa a query no banco com o cursor aberto
            cursor.execute(query)

            #Faz o commit pro banco para executar as mudanças
            self.db_conn.commit()
        
        except:
            #Caso algo dê errado, faz rollback no banco para o estado anterior da execução dessa query
            self.db_conn.rollback()
        
        #Fecha o cursor
        cursor.close()

        #Retorna o resultado da query
        return 'OK'
 
 
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
 
    def update(self, fieldsValues, whereClause, table = 'product'):
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor()

        values_masks = []
        values_where_masks = []

        #Converte o valor em string para encaixe na query
        for field in fieldsValues:
            values_masks.append(f"{field} = \"{fieldsValues[field]}\"")
        for key, value in whereClause.items():
            value = str(value)
            if self.get_type(value) == '%s':
                values_where_masks.append(f"{key} = \"{value}\"")

        #Monta a query com os parametros formatados
        query = "UPDATE {0} SET {1}, last_updated = now() WHERE {2};".format(table, ', '.join(values_masks), ' AND '.join(values_where_masks))

        #Em early return, checa se está dando update em outra tabela e caso sim, altera a query, retirando o parametro last_updated
        if table != 'product':
            query = "UPDATE {0} SET {1} WHERE {2};".format(table, ', '.join(values_masks), ' AND '.join(values_where_masks))

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
 
#product Repository
class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__('product')
 
    def get_all(self):
        self.raw_select("SELECT * FROM product")
 
    def get_by_product_id(self, product_id):
        query_result =  self.raw_select(("SELECT * FROM product WHERE product_id = %s;") % (product_id))

        return query_result
    
    def insert_into_product(self,query):
        query_result = self.raw_insert(query)

        return query_result

    def get_by_barcodes(self, barcodes):
        query_result =  self.raw_select(("SELECT * FROM product WHERE barcodes = %s;") % (barcodes))   

        return query_result

    def get_by_sku(self, sku, value = "*"):
        query_result =  self.raw_select((f"SELECT {value} FROM product WHERE sku = \"%s\";") % (sku))   

        return query_result

    def select_all_by_fields(self, params = {}, start = 0, num = 10, table = 'product'):
        """ Praticamente uma sobrecarga do select_by_fields porém sem a parte em que eu valido se o where está vazio, para que consiga gerar o where corretamente na query"""
        #Utiliza do atributo da classe BaseRepository para abertura de cursor com o banco e manipulação dos dados.
        cursor = self.db_conn.cursor(dictionary=True)

        fields = ["*"]
        where = {}

        if 'fields' in params:
            fields = params['fields']

        if 'where' in params:
            where = params['where']

        #Monta a query conforme variáveis e converte o fields adicionando , dentre os índices na lista
        query = "SELECT {} FROM {}".format(', '.join(fields), table)

        #Concatena o where na query
        query += self.__generate_where_statement(start, num)

        #Executa no db query acima com os valores substituídos pelos valores das variáveis no format.
        cursor.execute(query)

        #Aloca em result todos os resultados da query no banco
        result = cursor.fetchall()

        #Fecha o cursor de manipulação do db
        cursor.close()

        #Retorna o resultado
        return result


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

        #Executa no db query acima com os valores substituídos pelos valores das variáveis no format.
        cursor.execute(query)

        #Aloca em result todos os resultados da query no banco
        result = cursor.fetchall()

        #Fecha o cursor de manipulação do db
        cursor.close()

        #Retorna o resultado
        return result

    def __generate_where_statement(self, start, num):
        where_clause = []
 
        return " WHERE product_id >= {} ORDER BY product_id LIMIT {};".format(start, num)


    def __generate_where(self, where, start, num):
        """ Sobrecarga do método acima, praticamente, em que eu encaixo parâmetros específicos de where na query """
        where_clause = []

        for column in where:
            where_clause.append("{} = \"{}\"".format(column, where[column]))
                    
        return " WHERE {} AND product_id >= {} ORDER BY product_id LIMIT {};".format(" AND ".join(where_clause), start, num)

#product_attribute Repository
class ProdAttribRepository(BaseRepository):
    def __init__(self):
        super().__init__('product_attribute')

    def insert_attribute(self, product_id, name, value):
        query_result = self.raw_insert("""INSERT INTO product_attribute (product_id, name, value) VALUES ("{0}", "{1}", "{2}");""".format(product_id, name, value))
        return """INSERT INTO product_attribute (product_id, name, value) VALUES ("{0}", "{1}", "{2}");""".format(product_id, name, value)
        
    def get_all(self):
        query_result = self.raw_select("SELECT * FROM product_attribute")

        return query_result
 
    def delete_product_attributes(self, product_id):

        statement = "product_id = \"{0}\";".format(product_id)

        query_result = self.raw_delete('product_attribute', statement)

        return query_result

    def get_by_product_id(self, product_id):
        query_result =  self.raw_select(("SELECT * FROM product_attribute WHERE product_id = %s;") % (product_id))

        return query_result

    def get_by_name(self, name):
        query_result =  self.raw_select(("SELECT * FROM product_attribute WHERE name = \"%s\";") % (name))   

        return query_result

    def get_by_value(self, value):
        query_result =  self.raw_select(("SELECT * FROM product_attribute WHERE value = \"%s\";") % (value))   

        return query_result

#product_barcode Repository
class ProdBarcodeRepository(BaseRepository):
    def __init__(self):
        super().__init__('product_barcode')

    def delete_product_barcodes(self, product_id):

        statement = "product_id = \"{0}\";".format(product_id)

        query_result = self.raw_delete('product_barcode', statement)

        return query_result

    def insert_barcode(self, product_id, barcode):
        query_result = self.raw_insert("""INSERT INTO product_barcode ( product_id, barcode ) VALUES ("{0}", "{1}");""".format(product_id, barcode))
        
        return query_result
        
    def get_all(self):
        self.raw_select("SELECT * FROM product_barcode")
 
    def get_by_product_id(self, product_id):
        query_result =  self.raw_select(("SELECT * FROM product_barcode WHERE product_id = %s;") % (product_id))

        return query_result

    def get_by_barcode(self, barcode):
        query_result =  self.raw_select(("SELECT * FROM product_barcode WHERE barcode = \"%s\";") % (barcode))   

        return query_result
