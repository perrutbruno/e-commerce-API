class BaseRepository:
    def __init__(self):
        return
 
    def raw_select(self, query, fields = []):
        #cursor.execute(query, fields)
        #result = cursor.fetchall()
        #cursor.close()
        #return result
 
        print(query)
 
 
    def select(self, fields = "*"):
        fields_string = ""
 
        field_masks = []
 
        for field in fields:
            field_masks.append("%s")
 
        query = f"SELECT {', '.join(field_masks)} FROM {self.table}"
 
    def update(self, fieldsValues):
        values_masks = []
        values = []
 
        for field in fieldsValues:
            value_type = self.get_type(fieldsValues[field])
            values_masks.append(f"\"{field}\" = {value_type}")
            values.append(fieldsValues[field])
 
        query = f"UPDATE {self.table} SET {', '.join(values_masks)}"
 
    def get_type(self, variable):
        if type(variable) is int:
            return "%i"
        if type(variable) is str:
            return "%s"
 
class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__()
 
    def get_all(self):
        self.raw_select("SELECT * FROM product")
 
 
    def get_by_product_id(self, product_id):
        self.raw_select(f"SELECT * FROM product WHERE product_id = {product_id}")
 
    def get_by_fields(self, start = 0, num = 10, fields):
        values_masks = []
        values = []
 
        for field in fields:
            value_type = self.get_type(fieldsValues[field])
            values_masks.append(f"\"{field}\" = {value_type}")
            values.append(fieldsValues[field])
 
        query = f"SELECT 'productId', 'title' FROM product WHERE {', '.join(values_masks)} AND product_id >= {start} ORDER BY product_id LIMIT {num}"
        self.raw_select(query, values) 
 
 
 
 
product_repository = ProductRepository()
#product_repository.select()
#product_repository.update({
#    "coluna": "valor",
#    "coluna1": "valor1",
#    "coluna2": 2
#})
 
product_repository.get_all()
product_repository.get_by_product_id("12345")