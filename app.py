import os
from form import AddForm, DelForm
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Aroma_Mocha')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    orderID = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text)
    orderStatus = db.Column(db.Text)
    def __init__(self, username, orderStatus):
        self.username = username
        self.orderStatus = orderStatus

class OrderDetail(db.Model):
    __tablename__ = 'orderDetails'
    orderDetailID = db.Column(db.Integer, primary_key = True, autoincrement = True)
    orderID = db.Column(db.Integer)
    products = db.Column(db.Text)
    quantity = db.Column(db.Text)
    price = db.Column(db.Text)
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
    return render_template('login_customer.html')

@app.route('/val', methods = ['GET', 'POST'])
def val():
    email = request.form.get("email2")
    pwd = request.form.get("pwd2")
    print(email)
    print(pwd)
    user = Users.query.get(email)
    if(user is not None and user.password == pwd and user.userType == 'C'):
        fail = False
        print('success')
        return render_template('placeOrder.html', email = email, pwd = pwd, fail = fail)
    else:
        fail = True
        print('fail')
        return render_template('login_customer.html', fail = fail)

@app.route('/sign-out', methods = ['GET', 'POST'])
def sign_out():
    return render_template('sign_out.html')

@app.route('/employee/signup', methods = ['GET'])
def employee_sign_up():
    return render_template('register_employee.html')

@app.route('/employee/signup', methods = ['POST'])
def employee_sign_up_post():
    email = request.form.get("email")
    pwd = request.form.get("pwd")
    user = Users(email, pwd, 'E')
    fail = False
    user_email = Users.query.get(email)
    if user_email is None:
        db.session.add(user)
        db.session.commit()
        return render_template('login_employee.html')
    else:
        fail = True
        error_message = "Username already exists"
        return render_template('register_employee.html', error_message = error_message, fail = fail)

@app.route('/employee/login', methods = ['GET', 'POST'])
def employee_login():
    return render_template('login_employee.html')

@app.route('/employee/val', methods = ['GET', 'POST'])
def employee_val():
    email = request.form.get("email2")
    pwd = request.form.get("pwd2")
    print(email)
    print(pwd)
    user = Users.query.get(email)
    if(user is not None and user.password == pwd and user.userType == 'E'):
        fail = False
        print('success')
        return render_template('viewOrder.html', email = email, pwd = pwd)
    else:
        fail = True
        print('fail')
        return render_template('login_employee.html', fail = fail)

@app.route('/placeOrder', methods = ['GET'])
def placeOrder():
    return render_template('placeOrder.html')

@app.route('/orderSubmitted', methods = ['GET', 'POST'])
def orderSubmitted(list):
    print(list)
    return render_template('orderSubmitted.html', list = list)

@app.route('/viewOrder', methods = ['GET', 'POST'])
def viewOrder():
    list = []
    orderList = []
    form = AddForm()
    allProducts = ["Cookies", "Cookies&Cream", "Chocolate Cake", "Chocolate Fudge Brownies", "Blueberry Drink", "Mango & Raspberry Drink", "The Tropical Drink"]
    userName = ""
    status = "Pending"
    order = Order(userName, status)
    db.session.add(order)
    db.session.commit()
    for i in range(0, len(allProducts) - 1):
        if(request.args.get(allProducts[i]) == 'on'):
            quantity = 1
            price = 10
            orderDetail = OrderDetail(order.orderID, allProducts[i], quantity, price, quantity * price)
            orderList.append(orderDetail)
            db.session.add(orderDetail)
    db.session.commit()
    length = len(allProducts)
    print(list)
    return render_template('viewOrder.html', list = list, orderList = orderList, length = length)

@app.route('/employee/viewOrderDetail', methods = ['GET'])
def viewOrderDetail():
    orderID = request.args.get("orderID")
    orderDetails = db.session.query(OrderDetail).filter_by(orderID = orderID).all()
    length = len(orderDetails)
    return render_template('viewOrderDetail.html', orderList = orderDetails, length = length)

@app.route('/employee/viewAllOrders', methods = ['GET'])
def viewAllOrders():
    orders = db.session.query(Order).all()
    length = len(orders)
    return render_template('viewAllOrders.html', orderList = orders, length = length)

@app.route('/changeStatus')
def changeStatus():
    return render_template('changeStatus.html')

if __name__ == "__main__":
    app.run()