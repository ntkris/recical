from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, PurchasesForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app import db
from app.models import User, Purchases
from werkzeug.urls import url_parse
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username of password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a Recical user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/purchases', methods = ['GET', 'POST'])
@login_required
def purchases():
    form = PurchasesForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        purchases = Purchases(ingredient = form.ingredient.data, ingredient_type = form.ingredient_type.data,
                              units = form.units.type, quantity = form.quantity.data, user_id = user.id)
        db.session.add(purchases)
        db.session.commit()
        flash('Thank you for recording your purchases!')
        return redirect(url_for('index'))
    return render_template('purchases.html', title='Purchases', form=form)