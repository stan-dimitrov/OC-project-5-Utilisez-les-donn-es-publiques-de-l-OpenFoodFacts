import mysql.connector

class Database:

    def __init__(self, host, pwd, user, name):
        self.name = name
        self.pwd = pwd
        self.user = user
        self.host = host
        self.connection = mysql.connector.connect(user=user, password=pwd, host=host, database=name)
        self.connection.connect()

    def clear(self):
        self.connection.execute("""DROP TABLE Category, Food, Substitute""")

    def create_db(self):
        self.connection._execute_query("""
    		CREATE TABLE Category (
            idCategory INT AUTO_INCREMENT NOT NULL,
            category VARCHAR(1000) NOT NULL,
            PRIMARY KEY (idCategory)
            );
            """)

        self.connection._execute_query("""
            CREATE TABLE Substitute (
            id INT AUTO_INCREMENT NOT NULL,
            idCategory INT NOT NULL,
            category VARCHAR(200) NOT NULL,
            subcategory VARCHAR(200),
            ingredient VARCHAR(5000),
            nutriscore CHAR(10),
            label VARCHAR(1000),
            additive VARCHAR(1000),
            nutrient VARCHAR(1000),
            store VARCHAR(1000),
            bar_code BIGINT,
            link VARCHAR(1000),
            PRIMARY KEY (id, idCategory)
            );
            """)

        self.connection._execute_query("""
            CREATE TABLE Food (
            id INT AUTO_INCREMENT NOT NULL,
            idCategory INT NOT NULL,
            category VARCHAR(200) NOT NULL,
            food VARCHAR(400) NOT NULL,
            ingredient VARCHAR(5000),
            additive VARCHAR(1000),
            nutriscore CHAR(10),
            nutrient VARCHAR(1000),
            label VARCHAR(1000),
            store VARCHAR(1000),
            bar_code BIGINT,
            link VARCHAR(1000),
            PRIMARY KEY (id, idCategory)
            );
            """)

        self.connection._execute_query("""
            ALTER TABLE Food ADD CONSTRAINT category_food_fk
            FOREIGN KEY (idCategory)
            REFERENCES Category (idCategory)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION;
            """)

        self.connection._execute_query("""
            ALTER TABLE Substitute ADD CONSTRAINT category_substitute_fk
            FOREIGN KEY (idCategory)
            REFERENCES Category (idCategory)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION;
            """)
        return print("Database Created!")