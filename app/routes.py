from app import app
from flask import Flask, request, render_template
from app.access.ups.SoapRate import get_rates

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def get_rate():
    input = request.form['text']
    return str(get_rates())
