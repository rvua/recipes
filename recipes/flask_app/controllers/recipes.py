from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def recipe_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    all_recipes = Recipe.get_recipes_with_users()
    return render_template('list_recipe.html', all_recipes=all_recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    users = User.get_users()
    return render_template('new_recipe.html', users=users)

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if Recipe.is_valid(request.form):
        data = {
            'name':request.form['name'],
            'description':request.form['description'],
            'instruction':request.form['instruction'],
            'under30':request.form['under30'],
            'date_made':request.form['date_made'],
            'user_id':session['user_id']
        }
        Recipe.create_recipe(data)
        return redirect('/recipes') 
    else:
        return redirect('/recipes/new')

@app.route('/recipes/<int:recipe_id>')
def show_recipre(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'recipe_id':recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template('show_recipe.html', recipe=recipe)

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    users = User.get_users()
    data = {
        'recipe_id':recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template('edit_recipe.html', users = users, recipe=recipe)

@app.route('/update_recipe/<int:recipe_id>', methods=['POST']) 
def update_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    if Recipe.is_valid(request.form):
        data = {
            'recipe_id':recipe_id,
            'name':request.form['name'],
            'description':request.form['description'],
            'instruction':request.form['instruction'],
            'under30':request.form['under30'],
            'date_made':request.form['date_made'],
            'user_id':session['user_id']
        }
        Recipe.update_recipe_info(data)
        return redirect('/recipes')
    else:
        return redirect(f'/recipes/{recipe_id}/edit') 

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'recipe_id':recipe_id
    }
    Recipe.delete_one_recipe(data)
    return redirect('/recipes') 