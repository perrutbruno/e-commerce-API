import json 
from repositories.dbrepository import BaseRepository, ProductRepository

# -*- coding: utf-8 -*-

class ProductService:
    def __init__(self):
        self.db_repo = ProductRepository()
    
    def get_product_by_id(self, productid):
        query_result = self.db_repo.get_by_product_id(productid)

        if query_result == []:
            query_result = {"errorText":"Can’t find product {0}".format(product_id)}
            return json.dumps(query_result)
        else:
            return query_result
    
    def get_by_barcodes(self, barcodes):
        query_result = self.db_repo.get_by_barcodes(barcodes)

        if query_result == []:
            query_result = {"errorText":"Can’t find product {0}".format(barcodes)}
            return json.dumps(query_result)
        else:
            return query_result
    
    def get_by_sku(self, sku):
        query_result = self.db_repo.get_by_sku(sku)

        if query_result == []:
            query_result = {"errorText":"Can’t find product {0}".format(sku)}
            return json.dumps(query_result)
        else:
            return query_result
    
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



service = ProductService()

#print(service.get_by_fields(['product_id', 'sku', 'title'],{"product_id": 1, "sku": "BOT-1234"}))

print(service.get_by_fields(['product_id', 'sku', 'title']))

