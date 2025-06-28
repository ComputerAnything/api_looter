from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ApiCallForm(FlaskForm):
    api_key = StringField('API Key', validators=[DataRequired()])
    parameters = TextAreaField('Parameters', validators=[DataRequired()])
    submit = SubmitField('Make API Call')
