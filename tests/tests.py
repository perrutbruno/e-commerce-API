import requests, random, os

class TestHandler():
    #Método para enviar json em POST na api para criar usuário (sku gerado aleatoriamente)
    def create_new_user(self):
        db_host = os.environ["DB_HOST"]
        url = f"http://127.0.0.1:5000/api/products"
        number = random.randint(1000,9999)
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
        return r.status_code
    
    #Verifica se o retorno da API foi HTTP 200
    def test_create_new_user(self):
        assert 200 == self.create_new_user()

    def select_by_fields(self):
        db_host = os.environ["DB_HOST"]
        #Declara number como um valor aleatório de 1 a 7 para manipulaçao do query string num e de seleção de fields para envio do get
        number = random.randint(1,7)
        #Dicionário que depende da var number, para que o teste gere um número aleatório de parâmetros para enviar na requisição, evitando com que o teste realize sempre a mesma requisição
        fields = {1:'product_id',
                  2: 'title',
                  3: 'attributes',
                  4: 'description',
                  5: 'barcodes',
                  6: 'sku',
                  7: 'price'}
        #Lista para alocar os valores
        fields_params = []
        
        #Loop para alocar na lista um valor aleatório de number para envio na requisição GET
        for i in range(1, number + 1):
            fields_params.append(fields[i])
        
        #Transforma em string e remove os traços do tipo lista da string ('[' , ']')
        str_fields_params = str(fields_params)

        str_fields_params = str_fields_params.replace('[','')
        str_fields_params = str_fields_params.replace(']','')
        str_fields_params = str_fields_params.replace("'","")
        str_fields_params = str_fields_params.replace(" ","")
        
        url = f"http://127.0.0.1:5000/api/products?start=0&num={number}&fields={str_fields_params}"
      
        r = requests.get(url)
        return r.status_code

    #Testa a func select_by_fields, checando o código de retorno http
    def test_select_by_fields(self):
        assert 200 == self.select_by_fields()

    def select_by_id(self):
        db_host = os.environ["DB_HOST"]
        
        number = random.randint(1,10)
        print(number)
        url = f"http://127.0.0.1:5000/api/products/{number}"
        r = requests.get(url)
        return r.status_code

    def test_select_by_fields(self):
        assert 200 == self.select_by_id()
    