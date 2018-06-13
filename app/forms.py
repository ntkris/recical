from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please enter a different username.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Email address taken. Please enter a different email address.')

class PurchasesForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    ingredient_type = SelectField('Ingredient type', choices=[('Protein', 'Protein'), ('Fat', 'Fat'),
                                                   ('Seasoning', 'Seasoning'), ('Produce', 'Produce')],
                       validators = [DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    units = SelectField('Units', choices=[('GMS', 'Grams'), ('Units', 'Units')],
                       validators = [DataRequired()])
    submit = SubmitField('Submit')
