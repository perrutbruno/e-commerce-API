from flask import Flask,Blueprint, request
from service.service import ProductService

products_blueprint = Blueprint('products', __name__)

product_service = ProductService()

@products_blueprint.route('/api/products/<productid>', methods=['GET'])
def products_by_id(productid):
    # product_service.
    return productid

