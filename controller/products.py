from flask import Flask,Blueprint, request
from service.service import ProductService, ProdAttribService
from utils.errorhandler import ProductNotFound


products_blueprint = Blueprint('products', __name__)

product_service = ProductService()

@products_blueprint.route('/api/products/<product_id>', methods=['GET'])
def products_by_id(product_id):
    return str(product_service.get_product_by_id(product_id))

@products_blueprint.route('/api/products', methods=['POST'])
def create_products():
    if request.is_json:
        try:
            attributes_list = []
            req_data = request.get_json()
            
            title = req_data['title']
            sku = req_data['sku']

            for barcode in req_data['barcodes']:
                barcodes = req_data['barcodes']

            description = req_data['barcodes'] or "NULL"
            attributes = req_data['attributes']
            price = req_data['price']

            return str(product_service.create_product(title, sku, barcode, attributes, price))


            return "45", 200
        except KeyError as missing_param:
            return 'KEYERROR'

