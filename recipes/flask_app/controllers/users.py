from flask_app import app 
from flask import render_template, redirect, session, request, flash 
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/registration', methods=["POST"])
def registration():
    if not User.is_valid_registration(request.form):
        return redirect('/')
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save_user(data) 
    session['user_id'] = user_id
    return redirect('/recipes') 

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form) 
    if not user:
        flash('Wrong email or password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong email or password', 'login')
        return redirect('/')
    session['user_id'] = user.id  
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 

# Show an user page 
@app.route('/user/<int:user_id>')
def show_user(user_id):
    data = {
        'user_id':user_id
    }
    user = User.get_one_user(data)
    return render_template('show_user.html', user=user)