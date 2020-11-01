from flask import Flask
from service import BaseException, ProductNotFound
from products import products_blueprint
from flask.json import jsonify
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.errorhandler(BaseException)
def handle_invalid_usage(error):
    response = jsonify(error.message)
    response.status_code = error.status_code
    return response
    

app.register_blueprint(products_blueprint)

app.run()

