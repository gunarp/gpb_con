import pandas as pd
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from flask import Flask, request, render_template, redirect, url_for, flash
from app.crunch import ups_rates, fedex_rates

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('usa.html', response=None, title='home')
    else:
        params = request.form.to_dict().values()
        ups = ups_rates(params)
        fed = fedex_rates(params)
        if isinstance(ups, pd.DataFrame) and isinstance(fed, pd.DataFrame):
            rates = ups.append(fed)
            rate_table = rates.to_html(classes='data', header='true')
            return render_template('usa.html', rates=[rate_table], title='results')
        else:
            flash("UPS Request Returned: " + str(ups))
            flash("FedEx Request Returned: " + str(fed))
            return render_template('usa.html', response=None, title='error - try again')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
