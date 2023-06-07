from wtforms import ValidationError

from business_logic.portfolio_generator import PortfolioGenerator
from webapp import app, socketio
from flask import render_template, request
from webapp.forms import GenerateForm


@socketio.on('connect', namespace='/portfolio_generation')
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = GenerateForm()
    show_results_modal = False

    if request.method == "POST":
        validate_generate_form_data(form)
        tickers = form.tickers.data if form.tickers.data != '' else form.tickers_num.data

        generator = PortfolioGenerator(form.start_date.data, form.end_date.data)
        thread = socketio.start_background_task(target=generator.generate_portfolio,
                                                tickers=tickers, gen_num=1000)
        show_results_modal = True

    return render_template('home.html', form=form, show_results_modal=show_results_modal)


def validate_generate_form_data(form):
    if form.tickers.data != '' and form.tickers_num.data is not None:
        raise ValidationError('Can only pass the tickers as a string or a number, not both')
    if form.start_date.data > form.end_date.data:
        raise ValidationError('Start date cannot be later than end date')
