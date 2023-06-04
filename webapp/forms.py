from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class GenerateForm(FlaskForm):
    rdo_gen_strategy = RadioField('', choices=[('Choose', 'Choose your tickers'), ('Random', 'Random choice')],
                                  validators=[DataRequired()])
    tickers = StringField(label='Tickers:', validators=[Optional()])
    tickers_num = IntegerField(label='Tickers:', validators=[NumberRange(min=0), Optional()])

    submit = SubmitField(label='Generate')
