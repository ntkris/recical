from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, TextAreaField, DateField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class PurchasesForm(FlaskForm):
    ingredient = StringField('Ingredient', validators=[DataRequired()])
    ingredient_type = SelectField('Ingredient type', choices=[('Protein', 'Protein'), ('Fat', 'Fat'),
                                                   ('Seasoning', 'Seasoning'), ('Produce', 'Produce')],
                       validators = [DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    units = SelectField('Units', choices=[('GMS', 'Grams'), ('Units', 'Units')],
                       validators = [DataRequired()])
    expiration_date = DateField('Expiry date')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max = 140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')