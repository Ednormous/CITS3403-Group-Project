from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class searchForm(FlaskForm):
    searched = StringField('searched', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')