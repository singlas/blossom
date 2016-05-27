import os
from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import stripe

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.secret_key =" "

mysql = MySQLConnector('restfulroutespython')

# @app.route("/")
# def index():
# 	users = mysql.fetch("SELECT id, first_name, last_name, email, created_at FROM users")
# 	return render_template("index.html", users=users)

@app.route("/edit/<id>")
def edit(id):
	query = "SELECT id, first_name, last_name, email, created_at FROM users WHERE id = '{}'".format(id)
	info = mysql.fetch(query)
	return render_template("edit.html", users=info)

@app.route("/update/<id>", methods=['POST'])
def update(id):
	mysql.run_mysql_query("UPDATE users SET first_name='{}', last_name = '{}', email = '{}' WHERE id = '{}'".format(request.form['first_name'], request.form['last_name'], request.form['email'], id))
	return redirect("/")

@app.route('/add')
def add():
	return render_template("new.html")

@app.route('/payment')
def payment():
	return render_template("payment.html", key=stripe_keys['publishable_key'])

@app.route("/create", methods=['POST'])
def create():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	email = request.form['email']
	comment = request.form['comment']

	query = "INSERT INTO users (first_name, last_name, email, comment, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(first_name, last_name, email, comment)
	mysql.run_mysql_query(query)
	return redirect('/')

@app.route("/show/<id>")
def show(id):
	query = "SELECT id, first_name, last_name, email, created_at FROM users WHERE id = '{}'".format(id)
	info = mysql.fetch(query)
	return render_template("show.html", users=info)

@app.route("/destroy/<id>")
def destroy(id):
	mysql.run_mysql_query(("DELETE FROM users WHERE id = '{}'").format(id))
	return redirect('/')

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 4999

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)

if __name__ == '__main__':

	app.run(debug=True)