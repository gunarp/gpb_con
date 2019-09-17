import pandas as pd
from app import app
from flask import Flask, request, render_template, \
                  flash, redirect, url_for
from app.crunch import ups_rates

@app.route('/', methods=['GET', 'POST'])
def get_rate():
    if request.method == 'GET':
        return render_template('index.html', response=None)
    else:
        ups = ups_rates(request.form.to_dict().values())
        print(ups)
        if isinstance(ups, pd.DataFrame):
            ups_table = ups.to_html(classes='data', header='true')
            return render_template('usa.html', rates=[ups_table])
        else:
            flash(ups)
            return render_template('usa.html', response=None)
