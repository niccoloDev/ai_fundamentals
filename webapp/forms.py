from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional


class GenerateForm(FlaskForm):
    rdo_gen_strategy = RadioField('', choices=[('Choose', 'Choose your tickers'), ('Random', 'Random choice')],
                                  validators=[DataRequired()], default='Choose')
    tickers = StringField(label='Tickers:', validators=[Optional()])
    tickers_num = IntegerField(label='Tickers:', validators=[NumberRange(min=0), Optional()])
    start_date = DateField(label='Start date:', format='%Y-%m-%d')
    end_date = DateField('End date:', format='%Y-%m-%d')

    submit = SubmitField(label='Generate')
