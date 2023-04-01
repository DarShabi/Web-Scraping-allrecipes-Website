import pymysql


def build_database():
    # Connect to MySQL server
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rootroot'
    )

    # Create database
    cursor = connection.cursor()
    cursor.execute('CREATE DATABASE recipes')

    # Create the recipes table
    cursor.execute('''
        CREATE TABLE recipes (
            id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            link VARCHAR(150),
            title VARCHAR(50),
            num_reviews INT,
            rating INT,
            date_published DATETIME
        )
    ''')


    # Create the ingredients table
    cursor.execute("""
        CREATE TABLE ingredients (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            ingredient VARCHAR(100),
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    cursor.execute('''
        CREATE TABLE recipe_details (
            recipe_id INT PRIMARY KEY,
            prep_time_mins INT,
            cook_time_mins INT,
            total_time_mins INT,
            servings INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE nutrition_facts (
            recipe_id INT PRIMARY KEY,
            calories INT,
            fat_g INT,
            carbs_g INT,
            protein_g INT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    ''')


    # Create the categories table
    cursor.execute("""
        CREATE TABLE categories (
            id INT NOT NULL AUTO_INCREMENT,
            category VARCHAR(50),
            PRIMARY KEY (id)
        )
    """)

    # Create the instructions table
    cursor.execute("""
        CREATE TABLE instructions (
            id INT NOT NULL AUTO_INCREMENT,
            recipe_id INT,
            step INT,
            description TEXT,
            PRIMARY KEY (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    # Create the recipe_category table
    cursor.execute("""
        CREATE TABLE relationship (
            category_id INT,
            recipe_id INT,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id)
        )
    """)

    # commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
