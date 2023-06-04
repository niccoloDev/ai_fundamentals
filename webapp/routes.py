from wtforms import ValidationError

from business_logic.portfolio_generator import PortfolioGenerator
from webapp import app, socketio
from flask import render_template
from webapp.forms import GenerateForm


@socketio.on('connect', namespace='/portfolio_generation')
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    form = GenerateForm()
    show_results_modal = False

    if form.validate_on_submit():
        print(form.tickers.data)
        print(form.tickers_num.data)
        if form.tickers.data is not '' and form.tickers_num.data is not None:
            raise ValidationError('Can only pass the tickers as a string or a number, not both')
        tickers = form.tickers.data if form.tickers.data is not '' else form.tickers_num.data

        generator = PortfolioGenerator('2022-06-03', '2023-06-03')
        thread = socketio.start_background_task(target=generator.generate_portfolio,
                                                start_date='2022-06-03',
                                                end_date='2023-06-03',
                                                tickers=tickers, gen_num=100)
        show_results_modal = True

    return render_template('home.html', form=form, show_results_modal=show_results_modal)
