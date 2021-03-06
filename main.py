# from __future__ import print_function
from flask import Flask, request, render_template, jsonify, url_for, redirect
import pypyodbc
# import sys

APP = Flask(__name__)

CONNECTION = pypyodbc.connect('Driver={SQL Server}; Server=titan.csse.rose-hulman.edu;'
                              'Database=ICE_Project; Uid=introvertGuest; Pwd=introvertPassword')

def remove_sql_comments(toRemove):
    output = toRemove.replace("--", " ")
    output = output.replace("/*", " ")
    return output.strip()

def clean_user_input(toClean):
    if toClean is not None:
        return toClean.replace("'", "''")
    else:
        return toClean

@APP.route('/')
@APP.route('/Welcome')
def hello_world():
    return render_template('Welcome.html')

#-----------MENU----------------#


@APP.route('/Menu',methods=['GET', 'POST'])
def menu_page():
    method = request.form.get('_method')
    if method == 'POST':
        recipename = clean_user_input(request.form.get('name'))
        price = clean_user_input(request.form.get('price'))
        time = clean_user_input(request.form.get('time'))
        info = clean_user_input(request.form.get('calorie'))
        des = clean_user_input(request.form.get('description'))
        rate = clean_user_input(request.form.get('rate'))
        img = clean_user_input(request.form.get('img'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddRecipe " + \
            "'"+str(recipename) + "' , '" + str(price) + \
            "' , '" + str(time) + "' , '" + str(info) + "', '" + str(des) +"', '" + str(rate) + "', '" + str(img) + "' "
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        recipename = clean_user_input(request.form.get('name'))
        price = clean_user_input(request.form.get('price'))
        time = clean_user_input(request.form.get('time'))
        info = clean_user_input(request.form.get('calorie'))
        des = clean_user_input(request.form.get('description'))
        rate = clean_user_input(request.form.get('rate'))
        img = clean_user_input(request.form.get('img'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdateDish " + \
            "'"+str(recipename) + "' , '" + price + \
            "' , '" + time + "' , '" + str(info) + "', '" + str(des) +"', '" + rate + "', '" + str(img) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        recipename = clean_user_input(request.form.get('delname'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec delDish '" + recipename + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    cursor = CONNECTION.cursor()
    squery = ("SELECT RecipeName, Price, Rating FROM Recipe")
    squery = remove_sql_comments(squery)
    cursor.execute(squery)
    results = cursor.fetchall()
    rows = []
    for row in results:
        rows.append(row)
    return render_template("Menu.html", menu=rows)

#---------------RECIPE-------------------#


@APP.route('/Recipe')
def recipe_page():
    name = request.args.get('name')
    cursor = CONNECTION.cursor()
    squery = "SELECT RecipeName, Description, NutritionalInfo, CookTime, PictureURL " \
        "FROM Recipe " \
        "WHERE RecipeName = '" + name + "'"
    squery = remove_sql_comments(squery)
    cursor.execute(squery)
    result = cursor.fetchone()
    return render_template('Recipe.html', recipe=result)


#-----ORDERS------#


@APP.route('/OrderList', methods=['GET', 'POST'])
def orderList_page():
    method = request.form.get('_method')
    if method == 'POST':
        guestnumber = clean_user_input(request.form.get('guest'))
        tablenumber = clean_user_input(request.form.get('table'))
        username = clean_user_input(request.form.get('username'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddCheck " + \
            str(guestnumber) + " , '', '" + str(username) + \
            "', " + str(tablenumber)
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        guestnumber = clean_user_input(request.form.get('guest'))
        tablenumber = clean_user_input(request.form.get('table'))
        username = clean_user_input(request.form.get('username'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdateBill " + \
            str(guestnumber) + " , '', '" + str(username) + \
            "', " + str(tablenumber)
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        guestnumber = clean_user_input(request.form.get('guest'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec delBill '" + \
            str(guestnumber) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    cursor = CONNECTION.cursor()
    squery = ("SELECT * FROM [Check] LEFT OUTER JOIN Bill ON [Check].GuestNumber=Bill.Guest")
    squery = remove_sql_comments(squery)
    cursor.execute(squery)
    results = cursor.fetchall()
    rows = []
    for row in results:
        rows.append(row)
    return render_template("OrderList.html", orderlist=rows)


@APP.route('/Order', methods=['GET', 'POST'])
def order_page():
    method = request.form.get('_method')
    if method == 'POST':
        guestnumber = clean_user_input(request.args.get('guestnumber', ''))
        recipename = clean_user_input(request.form.get('name'))
        quantity = clean_user_input(request.form.get('quantity'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddOrder " + \
            (guestnumber) + " , [" + str(recipename) + \
            "], " + str(quantity) + " , '' "
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        guestnumber = clean_user_input(request.args.get('guestnumber', ''))
        recipename = clean_user_input(request.form.get('name'))
        quantity = clean_user_input(request.form.get('quantity'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdateBuy [" + \
            (guestnumber) + "] , [" + str(recipename) + \
            "] , [" + str(quantity) + "] , '' "
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        guestnumber = clean_user_input(request.args.get('guestnumber', ''))
        recipename = clean_user_input(request.form.get('delname'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec delBuy [" + \
            (guestnumber) + "] , [" + recipename + "]"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()


    guestnumber = clean_user_input(request.args.get('guestnumber', ''))
    cursor = CONNECTION.cursor()
    squery = "Select Orders.RecipeName, Quantity, (Price*Quantity) as Price " \
        "From [Check], Orders, Recipe " \
        "Where [Check].GuestNumber = Orders.GuestNumber " \
        "And Orders.RecipeName = Recipe.RecipeName " \
        "AND [Check].GuestNumber = " + guestnumber

    squery2 = "Select Orders.GuestNumber, [Date/Time], TableNumber, Cost "  \
        "From [Check], Orders, Bill " \
        "Where [Check].GuestNumber = Orders.GuestNumber AND Orders.GuestNumber=Bill.Guest " \
        "AND [Check].GuestNumber = " + guestnumber

    squery = remove_sql_comments(squery)
    squery2 = remove_sql_comments(squery2)

    cursor.execute(squery)
    recipesOrdered = cursor.fetchall()

    cursor.execute(squery2)
    checkInfo = cursor.fetchone()
    return render_template('Order.html', orderInfo=recipesOrdered, checkInfo=checkInfo)


#-----CUSTOMERS----------#


@APP.route('/CustomerList',methods=['GET', 'POST'])

def customerList_page():
    method = request.form.get('_method')
    if method == 'POST':
        name = clean_user_input(request.form.get('fname'))
        username = clean_user_input(request.form.get('username'))
        password = clean_user_input(request.form.get('password'))
        balance = clean_user_input(request.form.get('balance'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddAccount '" + \
            str(username) + "' , '" + str(password) + \
            "', " + balance + " , '" + str(name) +"'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        name = clean_user_input(request.form.get('fname'))
        username = clean_user_input(request.form.get('username'))
        password = clean_user_input(request.form.get('password'))
        new = clean_user_input(request.form.get('newpassword'))
        balance = clean_user_input(request.form.get('balance'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdateUser '" + \
            str(username) + "' , '" + str(password) + \
            "', '" + str(new) +"' , '" + str(balance) + "', '" + str(name) +"'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        username = clean_user_input(request.form.get('delname'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec delUser [" + username + "]"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    cursor = CONNECTION.cursor()
    squery = ("SELECT Username, Balance, FullName FROM Account")
    squery = remove_sql_comments(squery)
    cursor.execute(squery)
    results = cursor.fetchall()
    rows = []
    for row in results:
        rows.append(row)
    return render_template("CustomerList.html", customer=rows)


@APP.route('/Customer', methods=['POST','GET'])
def customer_page():
    if(request.method=='POST'):
        username = request.args.get('user')
        fav = clean_user_input(request.form.get('favorite'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddFavorite '" + str(username) + "' , '" + str(fav) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    username = request.args.get('user')
    cursor = CONNECTION.cursor()
    squery1 = ("SELECT * FROM Account WHERE Username=" + "'" + username + "'")
    squery2 = ("SELECT * FROM [CHECK], Bill WHERE [Check].GuestNumber=Bill.Guest AND Username=" + "'" + username + "'")
    squery3 = ("SELECT * FROM Favorite WHERE Username=" + "'" + username + "'")

    squery1 = remove_sql_comments(squery1)
    squery2 = remove_sql_comments(squery2)
    squery3 = remove_sql_comments(squery3)

    cursor.execute(squery1)
    result1 = cursor.fetchall()
    cursor.execute(squery2)
    result2 = cursor.fetchall()
    cursor.execute(squery3)
    if cursor.rowcount == 0:
        temp = ['', "None"]
        return render_template('Customer.html', customer=result1[0],hisorder=result2,fav=temp)
    result3 = cursor.fetchall()
    return render_template('Customer.html', customer=result1[0],hisorder=result2,fav=result3[0])

#-------INGREDIENTS----------#


@APP.route('/IngredientList', methods=['POST', 'GET'])
def ingredientList_page():
    method = request.form.get('_method')

    if method == 'POST':
        nameofingredient = clean_user_input(request.form.get('name', ''))
        nutriinfo = clean_user_input(request.form.get('nutrinfo'))
        unitsize = clean_user_input(request.form.get('UnitSize'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddIngredient '" + str(nameofingredient) + "' , '" \
            + str(nutriinfo) + "' , '" + str(unitsize) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        nameofingredient = clean_user_input(request.form.get('name', ''))
        nutriinfo = clean_user_input(request.form.get('nutrinfo'))
        unitsize = clean_user_input(request.form.get('UnitSize'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdatePart '" + str(nameofingredient) + "' , '" \
            + str(nutriinfo) + "' , '" + str(unitsize) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        nameofingredient = clean_user_input(request.form.get('delname', ''))
        sqlquer = "exec delPart '" + str(nameofingredient) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor = CONNECTION.cursor()
        cursor.execute(sqlquer)
        CONNECTION.commit()

    cursor = CONNECTION.cursor()
    squery = "SELECT Ingredient.IngredientName, IngredientReadout.Stocked, Units " \
        "FROM Ingredient LEFT JOIN IngredientReadout " \
        "ON Ingredient.IngredientName=IngredientReadout.IngredientName;"
    squery = remove_sql_comments(squery)
    cursor.execute(squery)
    results = cursor.fetchall()
    rows = []
    for row in results:
        rows.append(row)
    return render_template('IngredientList.html', ingredientlist=rows)


@APP.route('/Ingredient',methods=["GET","POST"])
def ingredient_page():
    method = request.form.get('_method')

    if method == 'POST':
        nameofingredient = request.args.get('name')
        shipno = clean_user_input(request.form.get('shipno'))
        exp = clean_user_input(request.form.get('exp'))
        quantity = clean_user_input(request.form.get('quantity'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec AddStock '" + str(shipno) + "' , '" \
            + str(quantity) + "' , '" + str(exp) + "', '" + str(nameofingredient) +"'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'PUT':
        nameofingredient = request.args.get('name')
        shipno = clean_user_input(request.form.get('shipno'))
        exp = clean_user_input(request.form.get('exp'))
        quantity = clean_user_input(request.form.get('quantity'))
        cursor = CONNECTION.cursor()
        sqlquer = "exec UpdateStuff '" + str(shipno) + "' , '" \
            + str(quantity) + "' , '" + str(exp) + "', '" + str(nameofingredient) +"'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor.execute(sqlquer)
        CONNECTION.commit()

    if method == 'DELETE':
        shipno = clean_user_input(request.form.get('delnum', ''))
        sqlquer = "exec delStuff '" + str(shipno) + "'"
        sqlquer = remove_sql_comments(sqlquer)
        cursor = CONNECTION.cursor()
        cursor.execute(sqlquer)
        CONNECTION.commit()

    iname = request.args.get('name')
    cursor = CONNECTION.cursor()
    squery1 = ("SELECT * FROM Ingredient WHERE IngredientName=" + "'" + iname + "'")
    squery2 = ("SELECT * FROM Stock WHERE IngredientName=" + "'" + iname + "'")
    squery1 = remove_sql_comments(squery1)
    squery2 = remove_sql_comments(squery2)
    cursor.execute(squery1)
    result1 = cursor.fetchall()
    cursor.execute(squery2)
    result2 = cursor.fetchall()
    return render_template('Ingredient.html', info=result1[0], serial=result2)

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8080, debug=True)
