import os
from form import AddForm, DelForm
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Aroma_Mocha')
app.config['SQLALCHEMY+TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class Users(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.Text, primary_key = True)
    password = db.Column(db.Text)
    userType = db.Column(db.Text)

    def __init__(self, username, password, userType):
        self.username = username
        self.password = password
        self.userType = userType

    def __repr__(self):
        return f"User name: {self.username} {self.password} {self.userType}"
    
class Order(db.Model):
    __tablename__ = 'orders'
    oderID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text)
    orderStatus = db.Column(db.Text)
    def __init__(self, username, oderStatus):
        self.username = username
        self.oderStatus = oderStatus

class OderDetail(db.Model):
    __tablename__ = 'oderDetails'
    oderDetailID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    oderID = db.Column(db.Integer)
    products = db.Column(db.Text)
    quantity = db.Column(db.Text)
    price = db.column(db.Text)
    amount = db.Column(db.Text)
    def __init__(self, orderID, products, quantity, price, amount):
        self.orderID = orderID
        self.products = products
        self.quantity = quantity
        self.price = price
        self.amount = amount

@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

@app.route('/signup', methods = ['GET'])
def sign_up():
    return render_template('register_customer.html')

@app.route('/signup', methods =  ['POST'])
def sign_up_post():
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    user = Users(email, pwd, 'C')
    user_email = Users.query.get(email)
    fail = False
    if user_email is None:
        db.session.add(user)
        db.session.commit()
        return render_template('login_customer.html', fail = fail)
    else:
        fail = True
        error_message = "Username already exists"
        return render_template('register_customer.html', error_message = error_message, fail = fail)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    render_template('login_customer.html')

@app.route('/val', methods = ['GET', 'POST'])
def val():
    email = request.form.get("email2")
    pwd = request.form.get("pwd2")
    print(email)
    print(pwd)