"""Generates and secures form in the index.html page"""
from email.policy import default
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class QueryForm(FlaskForm):
    search = StringField('Enter your search', validators=[DataRequired()])
    content = SelectField('Content type', choices=[('video', 'Video'), ('book', 'Book'), ('article', 'Article')], default='video')
    submit = SubmitField('recommend')