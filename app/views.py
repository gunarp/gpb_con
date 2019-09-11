import pandas as pd
from app import app
from flask import Flask, request, render_template
from app.crunch import ups_rates

@app.route('/')
@app.route('/usa')
def index():
    return render_template('usa.html', response=None)

@app.route('/', methods=['POST'])
def get_rate():
    ups = ups_rates(request.form.to_dict().values())
    return render_template('usa.html', rates=[ups.to_html(classes='data', header='true')])
