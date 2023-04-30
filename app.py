from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
from datetime import datetime
from datetime import date

app = Flask(__name__)
app.secret_key = 'xyzsdf'


# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Soha7120&",
    database="petkingdom"
)

# Define a route to display the home page


@app.route('/')
def home():
    return render_template('home.html')

# Define a route to display the signup page


@app.route('/signup')
def signup():
    return render_template('signup.html')

# Define a route to handle the signup form submission


@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user_type = request.form['user_type']
    mycursor = mydb.cursor()
    sql = "INSERT INTO Users (name, email, password, type) VALUES (%s, %s, %s, %s)"
    val = (name, email, password, user_type)
    mycursor.execute(sql, val)
    mydb.commit()
    return render_template('signupsuccess.html')


@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']
    mycursor = mydb.cursor()
    # sql = "SELECT user_id, email, password, type FROM Users WHERE email = %s AND password = %s"
    # mycursor.execute(sql, (email, password))

    mycursor.callproc("get_user_EP", [email, password])

    # user = mycursor.fetchone()
    results = mycursor.stored_results()
    procedure_result = []
    for result in results:
        rows = result.fetchall()
     # Get the columns from the result object
        procedure_result.extend(rows)

    user = procedure_result[0]

    if user:
        session['user_id'] = user[0]
        session['user_email'] = user[1]
        return redirect('/user/{}'.format(user[0]))

    else:
        error = "Invalid email or password. Please try again"
        return render_template('login.html', error=error)


@app.route('/user/<int:user_id>')
def user_page(user_id):
    mycursor = mydb.cursor()
    if 'user_id' in session and session['user_id'] == user_id:
        # query = "SELECT name, type FROM Users WHERE user_id = %s"
        # mycursor.execute(query, (user_id,))
        mycursor.callproc("UserType", [user_id])
        results = mycursor.stored_results()
        procedure_result = []
        for result in results:
            rows = result.fetchone()
            procedure_result.extend(rows)

        user = procedure_result
        # user = mycursor.fetchone()

        if user[1] == 'customer':
            # query = "SELECT order_id, order_date, product_name, quantity, total_price FROM Orders WHERE user_id = %s"
            # mycursor.execute(query, (user_id,))
            mycursor.callproc("GetOrders", [user_id])
            results = mycursor.stored_results()
            procedure_result = []
            for result in results:
                rows = result.fetchall()
            # Get the columns from the result object
                procedure_result.extend(rows)
            # rows = mycursor.fetchall()
            # user_info = rows
            user_info = procedure_result

        if user[1] == 'admin':
            query = "SELECT sales_date, amount FROM sales"
            mycursor.execute(query)
            rows = mycursor.fetchall()
            user_info = rows

            query_favourites = "SELECT user_id, product_name FROM UserFavourites LEFT JOIN Products USING (product_id)"
            mycursor.execute(query_favourites)
            favs = mycursor.fetchall()

        if user[1] == 'supplier':
            query_payment_details = "SELECT * FROM payment"
            mycursor.execute(query_payment_details)
            details = mycursor.fetchall()

            query = "SELECT product_id, product_name, stock_quantity FROM Products"
            mycursor.execute(query)
            rows = mycursor.fetchall()
            user_info = rows

        if user[1] == 'supplier':
            return render_template('user.html', user=user, user_info=user_info, user_id=user_id, details=details)
        elif user[1] == 'admin':
            return render_template('user.html', user=user, user_info=user_info, user_id=user_id, favs=favs)

        else:
            return render_template('user.html', user=user, user_info=user_info, user_id=user_id)

    else:
        return render_template('login.html')


@app.route('/signupform')
def signupform():
    return render_template('signup.html')


@app.route('/')
def homepage():
    return redirect(url_for('signupform'))


@app.route('/')
def returnhome():
    return render_template('home.html')


@app.route('/')
def returnhomepage():
    return redirect(url_for('returnhome'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login')
def loginpage():
    return redirect(url_for('login'))


@app.route('/user/<int:user_id>/order')
def order(user_id):
    mycursor = mydb.cursor()
    query = "SELECT product_name, description, price, expiration_date, material, color FROM Products p LEFT JOIN Food f USING(product_id) LEFT JOIN Toys t USING(product_id) LEFT JOIN Accessories a USING(product_id)"
    mycursor.execute(query)
    prod = mycursor.fetchall()
    return render_template('order.html', user_id=user_id, prod=prod)


@app.route('/user/<int:user_id>/order')
def orderpage(user_id):
    return redirect(url_for('order', user_id=user_id))


@app.route('/user/<int:user_id>/order/placeorder')
def placeorder(user_id):
    mycursor = mydb.cursor()
    query = "SELECT product_name, description, price, expiration_date, material, color FROM Products p LEFT JOIN Food f USING(product_id) LEFT JOIN Toys t USING(product_id) LEFT JOIN Accessories a USING(product_id)"
    mycursor.execute(query)
    prod = mycursor.fetchall()
    return render_template('placeorder.html', user_id=user_id, prod=prod)


@app.route('/user/<int:user_id>/order/placeorder')
def placeorderorderpage(user_id):
    return redirect(url_for('placeorder', user_id=user_id))


@app.route('/receipt', methods=['POST'])
def receipt_submit():
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    user_id = request.form['user_id']
    total_price = float(request.form['total_price'])

    # Generate today's date
    today_date = date.today()
    order_date = today_date
    mycursor = mydb.cursor()
    mycursor.callproc(
        "insert_order", [order_date, user_id, product_name, quantity, total_price])

    mydb.commit()
    return render_template('receipt.html', product_name=product_name, quantity=quantity, user_id=user_id, total_price=total_price)


@app.route('/payment', methods=['POST'])
def payment():
    mycursor = mydb.cursor()
    product_name = request.form['product_name']
    quantity = request.form['quantity']
    user_id = request.form['user_id']
    total_price = float(request.form['total_price'])
    addressline = request.form['addressline']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    zipcode = request.form['zipcode']
    payment_method = request.form['payment_method']

    # mycursor.callproc(
    #     "insert_order", [order_date, user_id, product_name, quantity, total_price])
    query = "INSERT INTO payment (user_id, addressline, city, state, country, zipcode, payment_method) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, (user_id, addressline, city,
                     state, country, zipcode, payment_method))
    mydb.commit()
    return render_template('payment.html', product_name=product_name, quantity=quantity, user_id=user_id, total_price=total_price, addressline=addressline, city=city, state=state, country=country, zipcode=zipcode, payment_method=payment_method)


@app.route('/user/<int:user_id>/get_total_orders', methods=['POST'])
def get_total_orders(user_id):
    customer_id = request.form['customer_id']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT fn_get_customer_order_count(%s)", (customer_id,))
    total_orders = mycursor.fetchone()

    # query = "SELECT name, type FROM Users WHERE user_id = %s"
    # mycursor.execute(query, (user_id,))
    # user = mycursor.fetchone()
    mycursor.callproc("UserType", [user_id])
    results = mycursor.stored_results()
    procedure_result = []
    for result in results:
        rows = result.fetchone()
        procedure_result.extend(rows)
    user = procedure_result

    query = "SELECT sales_date, amount FROM sales"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    user_info = rows
    return render_template('user.html', total_orders=total_orders, user=user, user_id=user_id, user_info=user_info)


@app.route('/user/<int:user_id>/update_stock_quantity', methods=['POST'])
def update_stock_quantity(user_id):
    product_id = request.form['product_id']
    stock_quantity = request.form['stock_quantity']
    mycursor = mydb.cursor()
    mycursor.execute(
        "UPDATE Products SET stock_quantity = %s WHERE product_id = %s", (stock_quantity, product_id,))
    mydb.commit()
    msg = "Stock updated!"

    query_payment_details = "SELECT * FROM payment"
    mycursor.execute(query_payment_details)
    details = mycursor.fetchall()

    query = "SELECT product_id, product_name, stock_quantity FROM Products"
    mycursor.execute(query)
    updated_data = mycursor.fetchall()
    mycursor.callproc("UserType", [user_id])
    results = mycursor.stored_results()
    procedure_result = []
    for result in results:
        rows = result.fetchone()
        procedure_result.extend(rows)
    user = procedure_result

    return render_template('user.html', msg=msg, user=user, user_id=user_id, user_info=updated_data, details=details)


@app.route('/user/<int:user_id>/delete_product', methods=['POST'])
def delete_product(user_id):
    product_id = request.form['product_id']
    mycursor = mydb.cursor()
    mycursor.execute(
        "DELETE FROM Products WHERE product_id = %s", (product_id,))
    mydb.commit()
    msg = "Product Deleted!"

    # Query the updated data from the database
    query = "SELECT product_id, product_name, stock_quantity FROM Products"
    mycursor.execute(query)
    after_delete = mycursor.fetchall()

    # query = "SELECT name, type FROM Users WHERE user_id = %s"
    # mycursor.execute(query, (user_id,))
    # user = mycursor.fetchone()

    query_payment_details = "SELECT * FROM payment"
    mycursor.execute(query_payment_details)
    details = mycursor.fetchall()

    mycursor.callproc("UserType", [user_id])
    results = mycursor.stored_results()
    procedure_result = []
    for result in results:
        rows = result.fetchone()
        procedure_result.extend(rows)
    user = procedure_result

    return render_template('user.html', msg=msg, user=user, user_id=user_id, user_info=after_delete, details=details)


@app.route('/user/<int:user_id>/user_favourite')
def user_favourite(user_id):
    # mycursor = mydb.cursor()
    # query = "SELECT DISTINCT product_name FROM Orders WHERE user_id = %s"
    # mycursor.execute(query, (user_id,))
    # prod = mycursor.fetchall()

    mycursor = mydb.cursor()
    query = "SELECT DISTINCT product_name, product_id FROM Products p INNER JOIN Orders o USING (product_name) WHERE user_id = %s"
    mycursor.execute(query, (user_id,))
    prod = mycursor.fetchall()
    return render_template('user_favourite.html', user_id=user_id, prod=prod)


@app.route('/user/<int:user_id>/user_favourite')
def userfavouritepage(user_id):
    return redirect(url_for('user_favourite', user_id=user_id))


def get_product_id(product_name):
    mycursor = mydb.cursor()
    query = "SELECT product_id FROM Products WHERE product_name = %s"
    mycursor.execute(query, (product_name,))
    product_id = mycursor.fetchone()[0]
    return product_id


@app.route('/user/<int:user_id>/favourite', methods=['POST'])
def favourite(user_id):
    mycursor = mydb.cursor()
    product_name = request.form['product_name']
    product_id = get_product_id(product_name)

    mycursor.execute(
        "INSERT INTO UserFavourites VALUES (%s, %s)", (user_id, product_id,))
    mydb.commit()
    msg = "Marked as favorite!"

    return render_template('user_favourite.html', msg=msg, user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
