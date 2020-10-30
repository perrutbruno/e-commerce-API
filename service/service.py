import json 
from repositories.dbrepository import BaseRepository, ProductRepository, ProdBarcodeRepository, ProdAttribRepository
from utils.errorhandler import BaseException, ProductIdNotInteger, ProductDoesntExist, ProductNotFound, ProductParamNull, SkuAlreadyExists

# -*- coding: utf-8 -*-

#product Service
class ProductService:
    def __init__(self):
        self.db_repo = ProductRepository()

    def get_sku(self, product_id):
        
        query = "SELECT sku from product where product_id = {0}".format(product_id)

        query_result = self.db_repo.raw_select(query)

        return query_result

    def delete_product(self, product_id):
        
        #Aloca na var abaixo o retorno da função get_by_product_id proveniente do repositório.
        query_result = self.db_repo.get_by_product_id(product_id)

        #Verifica com early return se o retorno da função foi negativo ou vazio (quando não acha o dado no banco) e caso tenha sido, da throw na exception
        if not query_result:
            raise ProductDoesntExist(product_id)

        self.db_repo.raw_delete('product',f'product_id = \"{product_id}\";')

        self.db_repo.raw_delete('product_attribute',f'product_id = \"{product_id}\";')

        self.db_repo.raw_delete('product_barcode',f'product_id = \"{product_id}\";')

        #Caso não tenha problemas com o dado, retorna o mesmo
        return query_result
    
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
    
    def update_product_by_id(self, product_id, params_dict):

        params_list_converted = []

        params_list_values_converted = []

        converted_params = {}

        if 'sku' not in params_dict.keys():
            raise ProductParamNull('sku')

        #Aloca o valor de SKU da requisição na var abaixo
        sku = params_dict['sku']

        #pega o valor da sku do product_id referido
        actual_sku = self.get_sku(product_id)[0][0]

        #Compara em early return se a sku é diferente da sku do projeto para fazer a checagem se a SKU já existe em outro produto
        if sku != actual_sku:
            existant_sku = self.check_if_sku_exists(sku)

        #Checa se existe o parâmetro atributos no dicionário de parâmetros e aloca o mesmo em uma var à parte e o retira do dict
        if 'attributes' in params_dict.keys():
            attributes = params_dict['attributes']
            params_dict.pop('attributes')
        
        #Checa se existe o parâmetro barcode no dicionário de parâmetros e aloca o mesmo em uma var à parte e o retira do dict
        if 'barcodes' in params_dict.keys():
            barcodes = params_dict['barcodes']
            params_dict.pop('barcodes')

        #Para cada índice de chaves do dicionário de parâmetros, aloca o mesmo em uma lista à parte só com os keys do dict
        for param in params_dict.keys():
            params_list_converted.append(param)

        #Mesma coisa que a func acima, porém só com os valores
        for value in params_dict.values():
            params_list_values_converted.append(value)
        
        #Adiciona numa lista as chaves e valores em formato de dicionário em um outro dicionário "limpo".
        for index in range(0, len(params_list_converted)):
            converted_params[params_list_converted[index]] = params_list_values_converted[index]

        where_param = {'product_id':product_id}
        
        update_product = self.db_repo.update(converted_params, where_param)

        return 'Produto alterado com sucesso'
    
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

    def check_if_sku_exists(self, sku):
        query_result = self.db_repo.get_by_sku(sku)

        if query_result:
            raise SkuAlreadyExists(sku)
        
        return query_result
    
    def create_product(self, title, sku, barcodes, attributes, price, description = "NULL"):

        #Checa se a SKU já existe. As SKUS são únicas, então se a mesma já existir, retorna uma exception de erro com o {errortext:"SKU já existe...""} de retorno ao usuário
        sku_check = self.check_if_sku_exists(sku)
        
        #Query padrão com o campo description com "" para inserção da string
        query = f"""INSERT INTO product (title, sku, description, price, created, last_updated) VALUES (\"{title}\", \"{sku}\", \"{description}\", \"{price}\", now(), now());"""
        
        #Caso não tenha sido passada a description, a query deve mudar, para que insira o tipo NULL no lugar da description no banco
        if description == "NULL":
            query = f"""INSERT INTO product (title, sku, description, price, created, last_updated) VALUES (\"{title}\", \"{sku}\", {description}, \"{price}\", now(), now());"""

        #Aloca na variável o resultado do insert
        create_prod_query_result = self.db_repo.insert_into_product(query)

        #Monta a query para o select com o parametro sku preenchido com a var.
        select_query = f"""SELECT product_id FROM product WHERE sku = \"{sku}\";"""

        #Aloca na var abaixo o resultado desempacotado das tuplas que o mySql retorna, retornando somente o valor do id propriamente
        created_products_id = self.db_repo.raw_select(select_query)[0][0]

        return created_products_id
    
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
        
        #Checa em early return se o resultado foi vazio, caso tenha retornado vazio, o produto não foi encontrado e então a service retorna o json de erro
        if not query_result:
            return error_return

        return query_result

#product_attribute Service
class ProdAttribService:
    def __init__(self):
        self.db_repo = ProdAttribRepository()

    def update_prodattrib(self, req_data, product_id):
        #Se o parâmetro de atributos estiver preenchido, entra no bloco
        if 'attributes' in req_data.keys():

            #Deleta todos os atributos do produto. Escolhi deletá-los e readicioná-los para que o usuário consiga alterar valores escritos errados, como "colo" no lugar de "color", por exemplo.
            self.delete_prod_attrib(product_id)

            #Para cada parâmetro na lista de atributos passados em JSON, insere na tabela novamente.
            for attribute in req_data['attributes']:
                #Insere o atributo no product_id referenciado
                self.insert_prod_attrib(product_id, attribute['name'], attribute['value'])

        return True
    
    def delete_prod_attrib(self, product_id):
        #Utiliza do método delete_prod_attrib do repositório para enviar o parâmetro de product_id para montagem da query e delete dos registros no banco de dados
        query_result = self.db_repo.delete_product_attributes(product_id)

        return query_result

    def insert_prod_attrib(self, product_id = None, name = None, value = None ):
        #Checa em early return se algum dos parâmetros está vazio, todos são mandatórios.
        #Poderia ter usado: if product_id == None or value == None or name == None, porém preciso testá-los individualmente para retornar o valor certo para a Exception
        if product_id == None:
            raise ProductParamNull('product_id')
        elif value == None:
            raise ProductParamNull('value')
        elif name == None:
            raise ProductParamNull('name')

        #Cria o atributo com o product id, com o método insert do repositório de atributo de produto
        query = self.db_repo.insert_attribute(product_id, name, value)

        #Caso não tenha problemas com inserção do dado, retorna mensagem de sucesso
        return 'product attribute criado com sucesso'
    
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

    def update_prodbarcode(self, req_data, product_id):
        if 'barcodes' in req_data.keys():
            #Deleta todos os atributos do produto. Escolhi deletá-los e readicioná-los para que o usuário consiga alterar valores escritos errados, como "colo" no lugar de "color", por exemplo.
            self.delete_prod_barcode(product_id)
            for barcode in req_data['barcodes']:
                #Para cada barcode passado na lista, insere o mesmo no banco no product_id enviado.
                self.insert_prod_barcode(product_id, str(barcode))
        
        return True

        
    def delete_prod_barcode(self, product_id):
        #Utiliza do método delete_prod_barcode do repositório para enviar o parâmetro de product_id para montagem da query e delete dos registros no banco de dados
        query_result = self.db_repo.delete_product_barcodes(product_id)

        return query_result

    def insert_prod_barcode(self, product_id = None, barcode = None):
        #Checa em early return se algum dos parâmetros está vazio, todos são mandatórios.
        if product_id == None:
            raise ProductParamNull('product_id')
        elif barcode == None:
            raise ProductParamNull('barcode')

        #Aloca na var abaixo o retorno da função proveniente do repositório.
        query_result = self.db_repo.insert_barcode(product_id, barcode)

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
            