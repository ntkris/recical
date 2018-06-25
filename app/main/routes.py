from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_login import login_required


from app import db
from app.main.forms import PurchasesForm, EditProfileForm
from app.models import User, Purchases
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods = ['GET', 'POST'])
@bp.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title = 'Home')


@bp.route('/purchases', methods = ['GET', 'POST'])
@login_required
def purchases():
    form = PurchasesForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        purchases = Purchases(ingredient = form.ingredient.data, ingredient_type = form.ingredient_type.data,
                              units = form.units.type, quantity = form.quantity.data, user_id = user.id, expiration_date = form.expiration_date.data)
        db.session.add(purchases)
        db.session.commit()
        flash('Thank you for recording your purchases!')
        return redirect(url_for('main.index'))
    return render_template('purchases.html', title='Purchases', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.route('/kitchen', methods=['GET', 'POST'])
@login_required
def kitchen():
    user = User.query.filter_by(username=current_user.username).first()
    user_id = user.id
    purchases = Purchases.query.filter_by(user_id=user_id).all()
    return render_template('kitchen.html', title ='Kitchen', user=user, purchases=purchases)