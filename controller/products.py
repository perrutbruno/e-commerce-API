from flask import Flask,Blueprint, request
from service.service import ProductService, ProdAttribService, ProdBarcodeService
from utils.errorhandler import ProductNotFound
from flask.json import jsonify


products_blueprint = Blueprint('products', __name__)

#Instancia os objetos das services para manipulação de dados do banco
product_service = ProductService()
product_attrib_service = ProdAttribService()
product_barcode_service = ProdBarcodeService()

@products_blueprint.route('/api/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def products_by_id(product_id):
    if request.method == "GET":
        #product é o produto retornado do banco, caso exista
        product = product_service.get_product_by_id(product_id)
        #Tenta serializar em dict o produto para mais tarde, retornar um json do mesmo
        serialized_product = product_service.serialize_product_dict(product)

        #attributes são os atributos do produto referenciado pelo id retornado do banco, caso exista
        attributes = product_attrib_service.get_prod_attrib_by_id(product_id)
        #Serializa esse retorno para dicionário
        serialized_attributes = product_attrib_service.serialize_productattrib_dict(attributes)
        
        #Barcode é o valor de barcodes do produto referenciado pelo id
        barcode = product_barcode_service.get_prod_barcode_by_id(product_id)
        #Serializa esse retorno para dicionário
        serialized_barcode = product_barcode_service.serialize_productbarcode_dict(barcode)
        
        #o dicionário serialized_product recebe a chave attributes com os atributos retornados acima como valores
        serialized_product['attributes'] = serialized_attributes
        
        #O mesmo que acima, porém com barcodes
        serialized_product['barcodes'] = serialized_barcode
        
        #Retorna o dicionário como json
        return jsonify(serialized_product)

    elif request.method == "PUT":
        #Tenta dar um get no produto pelo id, para checar se ele já existe
        product_service.get_product_by_id(product_id)

        #Inicia um dicionário vazio para encaixar os parâmetros enviados no JSON
        params_dict = {}
        
        #Variável que guarda a requisição JSON recebida
        req_data = request.get_json()

        #Para cada parâmetro enviado na requisição, adiciona no dic. params_dict
        for param in req_data:
            params_dict[param] = req_data[param]

        #Atualiza o produto
        product_service.update_product_by_id(product_id, params_dict)

        #Atualiza o atributo de produto
        product_attrib_service.update_prodattrib(req_data, product_id)

        #Atualiza o barcode
        product_barcode_service.update_prodbarcode(req_data, product_id)
        
        return str(True)

    elif request.method == "DELETE":
        #Utiliza do service delete_product que comunica com os repositórios e deleta os registros do product_id
        product_service.delete_product(product_id)
        return str('true')


@products_blueprint.route('/api/products', methods=['POST','GET'])
def products():
    
        #Caso o método enviado seja POST, entra no bloco do try:
    if request.method == "POST":
        try:
            req_data = request.get_json()
                
            title = req_data['title']
            sku = req_data['sku']

            for barcodes in req_data['barcodes']:
                barcode = barcodes

            description = req_data['description'] or "NULL"

            attributes = req_data['attributes']
            price = req_data['price']

            #Cria o produto e retorna o id do mesmo
            created_product = product_service.create_product(title, sku, barcode, attributes, price, description)

            #Para cada atributo passado na requisição JSON, desempacota os mesmos e cria o atributo do produto no banco com insert.
            for attribute in attributes:
                name = attribute['name']
                value = attribute['value']
                    
                #Usa do id retornado na função create_product para vincular ao product attribute e cria na tabela o registro
                product_attrib_service.insert_prod_attrib(created_product, name, value)

            #Usa do id retornado na função create_product para vincular ao product barcode e cria na tabela o registro
            product_barcode_service.insert_prod_barcode(created_product, barcode)
                
            return "45", 200
                
        except KeyError as missing_param:
            return 'Todos os parâmetros devem ser preenchidos. Consulte a documentação para mais detalhes!',400
        
        #Caso requisição seja GET, entra no bloco abaixo
    if request.method == "GET":

        #Pega os valores passados na query string
        start = request.args['start']
        num = request.args['num']
        fields = request.args['fields']

        #Declara fields_dict como dicionário auxiliar e o return_products para alocar os valores
        fields_dict = dict()
        return_products = dict()

        #Caso tenha attributes como parâmetro, pega os valores de attributes no banco, remove-o de fields (que são os parâmetros de query string) e aloca o mesmo no dicionário de retorno
        if 'attributes' in fields:
            param_fields = { "fields": ["name, value"], "where": { }}
            prod_attributes = product_service.get_all_products(param_fields, start, num, 'product_attribute')
            fields = fields.replace('attributes,','')
            fields = fields.replace(',attributes','')
            return_products['attributes'] = prod_attributes

        #O mesmo que acima, porém para barcodes
        if 'barcodes' in fields:
            param_fields = { "fields": ["barcode"], "where": { }}
            barcodes = product_service.get_all_products(param_fields, start, num, 'product_barcode')

            fields = fields.replace('barcodes,','')
            fields = fields.replace(',barcodes','')
            return_products['barcodes'] = barcodes
            
        #Separa a query sttring por , alocando os parâmetros numa lista
        fields_list = fields.split(",")

        #Para cada parâmetro, adiciona-o em fields_dict dicionário com o valor 1, para que a função get_all_products monte a query usando os parâmetros passados
        for field in fields_list:
            fields_dict[field] = 1

        result_product = product_service.get_all_products({ "fields": fields_dict, "where": { }}, start, num)

        #Adiciona na chave items os itens retornados do banco e totalCount como a quantidade de items encontrados com o parâmetro passado na query string
        return_products['items'] = result_product
        return_products['totalCount'] = len(result_product)

        return jsonify(return_products)


