from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user 

class Recipe:
    db = 'recipes_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}

    @classmethod
    def create_recipe(cls, data): 
        query = "INSERT INTO recipes (name, description, instruction, under30, date_made, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instruction)s, %(under30)s, %(date_made)s, %(user_id)s, NOW(), NOW())"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results 
        
    @classmethod
    def get_recipes_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            recipe.user = user.User(user_data)
            recipes.append(recipe)
        return recipes
    
    @classmethod 
    def get_one_recipe(cls, data):
        query = "SELECT * from recipes LEFT JOIN user ON user_id = users.id WHERE recipes.id = %(recipe_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        recipe = cls(results[0])
        user_data = {
            'id': results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        recipe.user = user.User(user_data)
        return recipe

    @classmethod
    def update_recipe_info(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under30 = %(under30)s, date_made = %(date_made)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(recipe_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    
    @classmethod
    def delete_one_recipe(cls, data):
        query = "DELETE from recipes WHERE id = %(recipe_id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
    
    @staticmethod
    def is_valid(recipe):
        is_valid = True
        if recipe['name'] == '':
            is_valid = False
            flash('Name Required')
        if recipe['description'] == '':
            is_valid = False
            flash('Description Required') 
        if recipe['instruction'] == '':
            is_valid = False
            flash('Instructions Required')
        if recipe['date_made'] == '':
            is_valid = False
            flash('Please enter a date') 
        return is_valid