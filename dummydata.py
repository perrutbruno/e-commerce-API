import requests, os
from db import *

db_host = os.environ["DB_HOST"]

url = f"http://127.0.0.1:5000/api/products"

def send_post(number):
    json = {
        "title": "dummy title",
        "sku": f"SKU-{number}",
        "barcodes": [f"0000{number}"],
        "description": "dummy description",
        "attributes": [
            {

                "name": "color",
                "value": "blue"
            },
            {
                "name": "size",
                "value": "large"
            }
        ],
        "price": f"2{number}.00"
    }
    r = requests.post(url, json=json)
    print(r.status_code)

#Altere a variável abaixo para alterar o número de dados inseridos no banco
numero_de_dados = 20

for i in range(0, numero_de_dados):
    send_post(i)


