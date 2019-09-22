import requests
import mysql.connector

class OpenFood:

    def __init__(self, host, pwd, user, name):
        self.name = name
        self.pwd = pwd
        self.user = user
        self.host = host
        self.db = mysql.connector.connect(user=user, password=pwd, host=host, database=name)
        self.cursor = self.db.cursor()

    def list_categories(self):
        '''get categories from the URL API'''
        self.cursor.execute("delete from Substitute")

        self.cursor.execute("delete from Food")

        self.cursor.execute("delete from Category")

        r_cat = requests.get('https://fr.openfoodfacts.org/categories&json=1')
        data_json = r_cat.json()
        data_tags = data_json.get('tags')
        data_cat = [d.get('name', 'None').replace('\'', '') for d in data_tags]
        i = 0
        while i < 10:
            self.cursor = self.db.cursor()
            add_category = ("INSERT INTO Category" "(category)" "VALUES('{}')".format(data_cat[i]))
            self.cursor.execute(add_category)
            self.db.commit()
            self.cursor.close()
            i = i + 1

        cursor = self.db.cursor(buffered=True)
        list_category_query = ("SELECT idcategory, category FROM Category")
        cursor.execute(list_category_query)
        list_category_array = cursor.fetchall()
        for item in list_category_array:
            print(item)

    def list_foods(self, id_category):
        cursor = self.db.cursor(buffered=True)
        selec_cat = ("SELECT category FROM Category WHERE idCategory = " + str(id_category))
        cursor.execute(selec_cat)
        category = str(cursor.fetchone()[0])
        payload = {
            'action': 'process',
            'tagtype_0': 'categories',  # which subject is selected (categories)
            'tag_contains_0': 'contains',  # contains or not
            'tag_0': '{}'.format(category),  # parameters to choose
            'sort_by': 'unique_scans_n',
            'page_size': '{}'.format(10),
            'countries': 'France',
            'json': 1,
            'page': 1



        }
        r_food = requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=payload)
        food_json = r_food.json()
        test2 = food_json.get('products')

        for x in range(10):
            prod_name_saved = [d.get('product_name_fr') for d in test2]  # get product name in french
            prod_name = str(prod_name_saved[x])
            ingrdts_saved = [d.get('ingredients_text_fr') for d in test2]  # get ingredients list in french
            ingrdts = str(ingrdts_saved[x])
            nutri_grd_saved = [d.get('nutrition_grade_fr') for d in test2]  # get nutrigrade
            nutri_grd = str(nutri_grd_saved[x])
            bar_code_saved = [d.get('id') for d in test2]  # get barcode
            bar_code = bar_code_saved[x]
            add_food = (
                "INSERT INTO Food"
                "(idCategory, category, food, ingredient, nutriscore, bar_code)"
                "VALUES (%s, %s, %s, %s, %s, %s)")
            data = (id_category, category, prod_name, ingrdts, nutri_grd, bar_code)
            cursor.execute(add_food, data)
            self.db.commit()

        list_food_query = ("SELECT id, food, nutriscore FROM Food")
        cursor.execute(list_food_query)
        list_food_array = cursor.fetchall()
        for item in list_food_array:
            print(item)

    def select_food(self, id_food):
        cursor = self.db.cursor(buffered=True)
        select_food = ("SELECT category, food, ingredient, nutriscore, bar_code FROM Food WHERE id = " + str(id_food))
        cursor.execute(select_food)
        data = cursor.fetchone()

        food_category = data[0]
        food_name = data[1]
        food_ingredients = data[2]
        food_nutri_score = data[3]
        food_bar_code = data[4]


        existing_substitutes_query = (
                    "SELECT * FROM Food WHERE nutriscore <= " + "'" + food_nutri_score + "' and id != " + str(
                id_food))
        cursor.execute(existing_substitutes_query)
        if cursor.rowcount == 0:
            return False

        print("category: " + food_category)
        print("Food: " + food_name)
        print("Ingredients: " + food_ingredients)
        print("Nutri Score: " + food_nutri_score)
        print("bar_code: " + str(food_bar_code))


        return True

    def find_substitute(self, id_food):
        cursor = self.db.cursor(buffered=True)
        old_nutri_score_query = ("SELECT nutriscore FROM Food WHERE id = " + str(id_food))
        cursor.execute(old_nutri_score_query)
        old_nutri_score = str(cursor.fetchone()[0])

        new_nutri_score_query = ("SELECT category, food, ingredient, nutriscore, bar_code FROM Food WHERE nutriscore <= " + "'" + old_nutri_score + "' and id != " + str(id_food))
        cursor.execute(new_nutri_score_query)

        new_food = cursor.fetchone()

        food_category = new_food[0]
        food_name = new_food[1]
        food_ingredients = new_food[2]
        food_nutri_score = new_food[3]
        food_bar_code = new_food[4]

        print("\nYour substitute:")
        print("category:" + food_category)
        print("Food: " + food_name)
        print("Ingredients: " + food_ingredients)
        print("Nutri Score: " + food_nutri_score)
        print("bar_code" + str(food_bar_code))

    def save_substitute(self, id_food):
        cursor = self.db.cursor(buffered=True)
        substitute_select_query = (
            "INSERT INTO Substitute (idCategory, category, subcategory, ingredient, nutriscore," +
                                     "label, additive, nutrient, store, bar_code) " +
            "SELECT idCategory, category, food, ingredient, nutriscore, label, additive, nutrient, store, bar_code " +
            "FROM Food " +
            "WHERE id = " + str(id_food))

        cursor.execute(substitute_select_query)

        self.db.commit()

        print("\nYour substitute is now saved. Thank you for using our services!")