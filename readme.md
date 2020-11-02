# challenge-delta

API com CRUD.

  - Inclui manifestos kubernetes para deploy do projeto e banco de dados
  - Inclui testes unitários em cima de algumas rotas da API, checando status code de retorno
  - Inclui API

# Detalhes de arquitetura

  - A API foi moldada no design pattern Repository.
  - O manuseador de conexão do banco é feito conforme o design pattern Singleton
  - A API usa normas de padronização de nomes de classes, variáveis e etc conforme PEP8

### Tech
 *Libs/frameworks utilizados:*
  - FLASK, que por ser um micro-framework, segue a determinação do desafio de que quanto menos frameworks, melhor. 
  - Driver de conexão com o mysql pymysql-connector
  - Pytest para assert dos testes
  - Módulo requests
  - Libs default do python (os, datetime )

### Deploy
Projeto escrito em python3+.

Instale as dependências conforme o padrão a seguir:

```sh
- Dentro da pasta do projeto (git clone):
$ cd kubernetes/
$ kubectl apply -f .
```
- Você deve configurar o banco para que consiga utilizar a API. Em futuras releases iremos adicionar a tag command com o script de criação de banco de dados e liberação do login do root no deployment do mysql! :-)
```sh
- Dentro do pod do mysql:
$ mysql -u root -p
$ CREATE TABLE hurb_test_assignment.....
$ GRANT ALL PRIVILEGES ON . TO 'root'@'%' IDENTIFIED BY 'hurb';
```

(O PROJETO RODA NA PORTA 5000 DO POD)
### Exemplos de requisições
```GET /api/products```
* Na rota *GET* /api/products?start=0&num=2&fields=productId,title a requisição é feita com método GET, onde em fields podemos passar todos os parâmetros, por exemplo:
* /api/products?start=0&num=2&fields=productId,title,attributes

Retorno SUCESSO:
{
"totalCount"​: <int>​,
"items"​: [​<product>​]
}

```GET /api/products/<product_id>```

* Nessa rota *GET* você deve requisitar com a query string acima passando o id do produto após products/, por exemplo http://url_api.hurb/api/products/25

```GET /api/products/<product_id>```

O retorno de sucesso é um json
```
{
    "product_id": 25,
    "title": "Peruca",
    "sku": "['SOC-1020']",
    "description": 'Este pode ser um campo null também',
    "price": 225.0,
    "created": 1604087330,
    "lastUpdated": 1604087330,
    "attributes": [
        {
            "name": "color",
            "value": "blue"
        },
        {
            "name": "size",
            "value": "big"
        }
    ],
    "barcodes": [
        "9292929"
    ]
}
```

```POST​ /api/products```

- O parâmetro é um JSON, que deve ser passado como body e deve ser passado conforme a seguir:
```
{
​"title": "Awesome socks"​,
"sku"​: "SCK-4511"​,
"barcodes"​: [​"7410852096307"​],
​"description"​: null​,
​"attributes"​: [
        {
​
            "name"​: "color"​,
            "value"​: "Red"​,
        },
        {
​            "name": "size"​,
            "value"​: "39-41"​,
        },
    ],
    ​"price"​: "89.00"​,
}
```
- O retorno de sucesso é um int com o número do id do produto criado

```DELETE​/ /api/products/{productId}```

- Basta passar o product_id após o products/ e voi'la :-)

```PUT /api/products/{productId}```
- Você deve passar um JSON com os dados do produto que você quer alterar
- 
```
{
	"sku": "SKU-111121",
	"barcodes": ["01020304"],
	"description": "",
	"attributes": [
        {

            "name": "color",
            "value": "new color"
        },
        {
            "name": "size",
            "value": "new size"
        },
        {
            "name": "style",
            "value": "swag"
        }        
    ],
}
```

## Todas as requisições possuem cobertura das exceptions

### A fazer
*Infelizmente, algumas coisas ficaram faltando, a seguir detalho o que ainda não foi feito:*

- Ingress para fazer o balanceamento da aplicação
- Configuração de número de requests para HPA

