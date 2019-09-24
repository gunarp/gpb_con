import pandas as pd
from app import app, db
from app.models import User, UPS, Fedex
from app.forms import LoginForm, RegistrationForm, EditFedex, EditUps
from flask_login import current_user, login_user, logout_user, login_required
from flask import Flask, request, render_template, redirect, url_for, flash
from app.crunch import ups_rates, fedex_rates

@app.route('/', methods=['GET', 'POST'])
def usa():
    if request.method == 'GET':
        return render_template('usa.html', response=None, title='home')
    else:
        params = request.form.to_dict().values()
        ups = ups_rates(current_user, params)
        fed = fedex_rates(current_user, params)
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
        return redirect(url_for('usa'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('usa'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('usa'))

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    ups_form = EditUps()
    fdx_form = EditFedex()    

    return render_template('edit_user.html', user=user, ups=ups_form, fedex=fdx_form)

@app.route('/edit_ups', methods=['POST'])
def edit_ups():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    ups_form = EditUps()
    fdx_form = EditFedex()

    if ups_form.validate_on_submit():
        user.ups = [UPS(username=ups_form.username.data,
                        password=ups_form.password.data,
                        api_key=ups_form.api_key.data,
                        ship_num=ups_form.ship_num.data,
                        user_id=user.id)]
        db.session.commit()
        flash('UPS Settings Updated!')
    
    return render_template('edit_user.html', user=user, ups=ups_form, fedex=fdx_form)

@app.route('/edit_fdx', methods=['POST'])
def edit_fdx():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    ups_form = EditUps()
    fdx_form = EditFedex()

    if fdx_form.validate_on_submit():
        user.fedex = [Fedex(password=fdx_form.password.data,
                            api_key=fdx_form.api_key.data,
                            ship_num=fdx_form.ship_num.data,
                            meter_num=fdx_form.meter_num.data,
                            user_id=user.id)]
        db.session.commit()
        flash('FedEx Settings Updated!')

    return render_template('edit_user.html', user=user, ups=ups_form, fedex=fdx_form)
