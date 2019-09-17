from flask import Flask, url_for

app = Flask(__name__)
app.secret_key = 'secret'

from app import views
