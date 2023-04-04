import logging
import sql_connection as sq


def write_to_database(scraped_data):
    """
    Write recipe data to the database.
    :param:scraped_data (dict): A dictionary containing information about a recipe.
    :return: None
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()

    # insert recipe data into recipes table
    sql = "INSERT INTO recipes (link, title, num_reviews, rating, date_published) VALUES (%s, %s, %s, %s, %s)"
    values = (scraped_data['link'], scraped_data['title'], scraped_data['reviews'], scraped_data['rating'],
              scraped_data['published'])
    execute_sql(cursor, sql, values)

    # get the recipe ID from the newly inserted row
    recipe_id = cursor.lastrowid

    # insert recipe details into recipe_details table
    details_not_checked = scraped_data['details']
    details = check_if_keys_exist(details_not_checked, ['Prep Time:', 'Cook Time:', 'Total Time:', 'Servings:'])
    sql = "INSERT INTO recipe_details (recipe_id, prep_time_mins, cook_time_mins, total_time_mins, servings) " \
          "VALUES (%s, %s, %s, %s, %s)"
    values = (recipe_id, details['Prep Time:'], details['Cook Time:'], details['Total Time:'], details['Servings:'])
    execute_sql(cursor, sql, values)

    # insert nutrition facts into nutrition_facts table
    nutrition = scraped_data['nutrition']
    sql = "INSERT INTO nutrition_facts (recipe_id, calories, fat_g, carbs_g, protein_g) VALUES (%s, %s, %s, %s, %s)"
    values = (recipe_id, nutrition['Calories'], nutrition['Fat'], nutrition['Carbs'], nutrition['Protein'])
    execute_sql(cursor, sql, values)

    # insert categories into categories table and relationship into relationship table
    categories = scraped_data['category']
    for category in categories:
        sql = "INSERT INTO categories (category) VALUES (%s)"
        values = (category,)
        execute_sql(cursor, sql, values)
        category_id = cursor.lastrowid
        sql = "INSERT INTO relationship (category_id, recipe_id) VALUES (%s, %s)"
        values = (category_id, recipe_id)
        execute_sql(cursor, sql, values)

    # insert ingredients into ingredients table
    ingredients = scraped_data['ingredients']
    for ingredient in ingredients:
        sql = "INSERT INTO ingredients (recipe_id, ingredient) VALUES (%s, %s)"
        values = (recipe_id, ingredient)
        execute_sql(cursor, sql, values)

    # insert instructions into instructions table
    instructions = scraped_data['instructions']
    for step, description in instructions.items():
        sql = "INSERT INTO instructions (recipe_id, description) VALUES (%s, %s)"
        values = (recipe_id, description)
        execute_sql(cursor, sql, values)

    # commit changes to the database
    connection.commit()
    connection.close()


def get_recipe_by_title(title):
    """
    Retrieve recipe data from the database by recipe title.
    :param title: (str) Title of the recipe to retrieve.
    :return: (tuple) A tuple containing information about the recipe, or None if not found.
    """
    connection = sq.sql_connector()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE title=%s", (title,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result


def execute_sql(cursor, sql, values):
    """
    Executes an SQL query with the given cursor, SQL statement and values.
    If an error occurs during execution, a KeyError is raised with the error message.
    :param: cursor: (cursor object) The cursor to use for executing the SQL query.
            sql: (str) The SQL statement to execute.
            values: (tuple) The values to use for the placeholders in the SQL statement.
    :return: None
    :raises KeyError: If an error occurs during execution.
    """
    try:
        cursor.execute(sql, values)
    except KeyError as ex:
        raise KeyError(f'Error executing SQL: {ex}')


def check_if_keys_exist(dict_to_check, keys_to_check):
    """
    Checks if a dictionary contains all the specified keys. If any of the keys are missing,
    they are added to the dictionary with a value of None.
    :param: dict_to_check: (dict) The dictionary to check.
            keys_to_check: (list) The list of keys to check for in the dictionary.
    :return: (dict) The dictionary with all the specified keys, with any missing keys added with a value of None.
    """
    for key in keys_to_check:
        if key not in dict_to_check:
            dict_to_check[key] = None
    return dict_to_check
