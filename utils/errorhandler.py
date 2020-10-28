from flask import jsonify, app

#Classe base para lançamento de exceções
class BaseException(Exception):
    status_code = 500
 
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = { "errorText": message }
        if status_code is not None:
            self.status_code = status_code

##Product Exceptions##

#Informa que o produto não foi encontrado
class ProductNotFound(BaseException):
    def __init__(self, product_id):
       super().__init__(f"Can't find product ({product_id})", 404)

#Informa que o SKU já existe
class SkuAlreadyExists(BaseException):
    def __init__(self, sku):
       super().__init__(f"SKU '{sku}' already exists", 400)

#Informa que o product_id precisa ser do tipo integer
class ProductIdNotInteger(BaseException):
    def __init__(self):
       super().__init__(f"Product id must be an integer", 400)



##General API exceptions##

#Informa que os parâmetros devem ser preenchidos
class ProductParamNull(BaseException):
    def __init__(self, table):
       super().__init__(f"{table} fields must not be null", 400)

