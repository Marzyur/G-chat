from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class UserInputForm(FlaskForm):
    user_input=StringField('input',validators=[DataRequired()])
    submit=SubmitField('Submit')
