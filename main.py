# from __future__ import print_function
from flask import Flask, request, render_template, jsonify
import pypyodbc
# import sys

APP = Flask(__name__)

CONNECTION = pypyodbc.connect('Driver={SQL Server}; Server=titan.csse.rose-hulman.edu;'
                              'Database=ICE_Project; Uid=introvertGuest; Pwd=introvertPassword')


@APP.route('/')
@APP.route('/Welcome')
def hello_world():
    return render_template('Welcome.html')


@APP.route('/Menu')
def menu_page():
    cursor = CONNECTION.cursor()
    squery = ("SELECT RecipeName, Price, Rating FROM Recipe")
    cursor.execute(squery)
    results = cursor.fetchall()
    rows = []
    for row in results:
        rows.append(row)
    return render_template("Menu.html", menu=rows)

@APP.route('/Recipe')
def recipe_page():
    recipename=request.args.get('name')
    cursor = CONNECTION.cursor()
    squery1 = ("SELECT* FROM Recipe WHERE RecipeName="+ "'"+recipename+"'")
    cursor.execute(squery1)
    result1 = cursor.fetchall()
    return render_template('Recipe.html',recipe=result1[0])

#-----ORDERS------#


@APP.route('/OrderList')
def orderList_page():
    return render_template("OrderList.html")


@APP.route('/Order')
def order_page():
    return render_template('Order.html')

#-----CUSTOMERS----------#


@APP.route('/CustomerList')
def customerList_page():
    cursor = CONNECTION.cursor()
    squery = ("SELECT Username, Balance FROM Account")
    cursor.execute(squery)
    results = cursor.fetchall()
    #('dante', )
    rows = []
    for row in results:
        rows.append(row)
    return render_template("CustomerList.html", customer=rows)


@APP.route('/Customer')
def customer_page():
    username=request.args.get('user')
    cursor = CONNECTION.cursor()
    squery1 = ("SELECT* FROM Account WHERE Username="+ "'"+username+"'")
    cursor.execute(squery1)
    result1 = cursor.fetchall()
    return render_template('Customer.html',customer=result1[0])

#-------INGREDIENTS----------#


@APP.route('/IngredientList')
def ingredientList_page():
    return render_template('IngredientList.html')


@APP.route('/Ingredient')
def ingredient_page():
    return render_template('Ingredient.html')

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8080, debug=True)
