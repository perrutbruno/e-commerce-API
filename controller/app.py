from flask import Flask
from controller.products import products_blueprint
app = Flask(__name__)

app.register_blueprint(products_blueprint)

app.run()
