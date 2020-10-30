from flask import Flask,Blueprint, request
from service.service import ProductService, ProdAttribService, ProdBarcodeService
from utils.errorhandler import ProductNotFound


products_blueprint = Blueprint('products', __name__)

#Instancia os objetos das services para manipulação de dados do banco
product_service = ProductService()
product_attrib_service = ProdAttribService()
product_barcode_service = ProdBarcodeService()

@products_blueprint.route('/api/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
def products_by_id(product_id):
    if request.method == "GET":
        return str(product_service.get_product_by_id(product_id))

    elif request.method == "PUT":
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


@products_blueprint.route('/api/products', methods=['POST'])
def products():
    if request.is_json:
        try:
            req_data = request.get_json()
            
            title = req_data['title']
            sku = req_data['sku']

            for barcodes in req_data['barcodes']:
                barcode = barcodes

            description = req_data['barcodes'] or "NULL"
            attributes = req_data['attributes']
            price = req_data['price']

            #Cria o produto e retorna o id do mesmo
            created_product = product_service.create_product(title, sku, barcode, attributes, price)

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

