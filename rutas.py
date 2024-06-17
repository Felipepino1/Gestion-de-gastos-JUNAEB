from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from conectar import app, db, bcrypt
from forms import RegistrationForm, LoginForm
from models.user import User

@app.route('/index')
def index():
    servicios = list(db.service.find())
    return render_template('index.html', servicios=servicios)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password
        }

        db.users.insert_one(user_data)
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('index'))

    return render_template('registro.html', title='Registro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user_data = db.users.find_one({"username": username})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Inicio de sesión fallido. Verifica tu nombre de usuario y contraseña', 'danger')
    
    return render_template('login.html', title='Iniciar sesión', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('login'))
