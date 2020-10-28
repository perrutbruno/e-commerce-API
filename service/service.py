import json 
from repositories.dbrepository import BaseRepository, ProductRepository, ProdBarcodeRepository, ProdAttribRepository
from utils.errorhandler import BaseException, ProductIdNotInteger, ProductNotFound, ProductParamNull, SkuAlreadyExists

# -*- coding: utf-8 -*-

#product Service
class ProductService:
    def __init__(self):
        self.db_repo = ProductRepository()
    
    def get_product_by_id(self, product_id):
        #Tenta converter o product_id para o tipo integer e caso não consiga, da throw numa exception que retorna que o tipo de valor está errado.
        try:
            int(product_id)
        except ValueError as wrong_value_type:
            raise ProductIdNotInteger()

        #Aloca na var abaixo o retorno da função get_by_product_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(product_id)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(product_id)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result
    
    def get_by_barcodes(self, barcodes):
        #Aloca na var abaixo o retorno da função get_by_barcodes proveniente do repositório.
        query_result = self.db_repo.get_by_barcodes(barcodes)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(barcodes)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result
    
    def get_by_sku(self, sku):
        query_result = self.db_repo.get_by_sku(sku)

        if not query_result:
            raise ProductNotFound(sku)
        
        return query_result
    
    def create_product(self, title, sku, barcodes, attributes, price, description = "NULL"):

        try:
            sku_check = self.get_by_sku(sku)
        except ProductNotFound:
            raise SkuAlreadyExists(sku)

        return 0
    
    def get_by_fields(self, fields_values = [], where_dict_values = {}, start = 0, num = 10):
        query_result = []

        #Declara uma variável para padronizar o retorno em caso de erro
        error_return = json.dumps({"errorText":"Can’t find product with these params {0}".format(fields_values)})
            
        try:
            params = {"fields": fields_values, "where": where_dict_values}
            
            #Exemplo de chamada do método no repositório
            #query_result = self.get_by_fields({"fields": ["product_id", "sku", "title"], "where": {"product_id": 1,"sku": "BOT-1234",})
            query_result = self.db_repo.select_by_fields(params, start, num)
 
        except Exception as exc:
            return error_return
        
        #Checa se o resultado foi vazio, caso tenha retornado vazio, o produto não foi encontrado e então a service retorna o json de erro
        if query_result == []:
            return error_return
        else:
            return query_result

#product_attribute Service
class ProdAttribService:
    def __init__(self):
        self.db_repo = ProdAttribRepository()

    def insert_prod_attrib(self, product_id = None, name = None, value = None):
        #Checa em early return se algum dos parâmetros está vazio, todos são mandatórios.
        if product_id == None or name == None or value == None:
            raise ProductParamNull('product_attribute')

        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.insert(product_id, name, value)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result
    
    def get_prod_attrib_by_id(self, product_id):
        #Tenta converter o product_id para o tipo integer e caso não consiga, da throw numa exception que retorna que o tipo de valor está errado.
        try:
            int(product_id)
        except ValueError as wrong_value_type:
            raise ProductIdNotInteger()
        
        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(product_id)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(product_id)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result

    def get_prod_attrib_by_name(self, name):
        
        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(name)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(name)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result

    def get_prod_attrib_by_value(self, value):
        
        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.get_by_value(value)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(value)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result


#product_barcode Service
class ProdBarcodeService:
    def __init__(self):
        self.db_repo = ProdBarcodeRepository()

    def insert_prod_barcode(self, product_id = None, barcode = None):
        #Checa em early return se algum dos parâmetros está vazio, todos são mandatórios.
        if product_id == None or barcode == None:
            raise ProductParamNull('product_barcode')

        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.insert(product_id, barcode)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result

    def get_prod_barcode_by_id(self, product_id):
        #Tenta converter o product_id para o tipo integer e caso não consiga, da throw numa exception que retorna que o tipo de valor está errado.
        try:
            int(product_id)
        except ValueError as wrong_value_type:
            raise ProductIdNotInteger()
        
        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(product_id)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(product_id)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result

    def get_prod_attrib_by_barcode(self, barcode):
        
        #Aloca na var abaixo o retorno da função get_by_prudct_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(barcode)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductNotFound(barcode)

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result

            
        



# service = ProductService()

# service.create_product('abc', 'BOT-123k4', 'SSSS', 'AA', '10.90')

# #print(service.get_by_fields(['product_id', 'sku', 'title'],{"product_id": 1, "sku": "BOT-1234"}))

# print(service.get_by_fields(['product_id', 'sku', 'title']))

