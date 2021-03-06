# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db_mongo = myclient["si1"]

#registra el usuario en nuestra base de datos
def db_register(data):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_customer_register = f"insert into customers(firstname, lastname, email, creditcard," 
        db_customer_register += f"username, password, gender) values ('{data['firstname']}','{data['lastname']}',"
        db_customer_register += f"'{data['email']}','{data['creditcard']}','{data['username']}', '{data['pwd']}',"
        db_customer_register += f" '{data['gender']}')"

        db_result = db_conn.execute(db_customer_register)
        db_conn.close()

        return True

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False
    
#necesitamos una funcion con una query que nos diga si el usuario está registrado ya

def db_alreadyregistered(data):
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_customer_exists =  f"select username from customers where username = '{data['username']}'"
        db_result = db_conn.execute(db_customer_exists)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_login(username, pwd):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_login =  f"select * from customers where username = '{username}' and password = '{pwd}'"
        db_result = db_conn.execute(db_login)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_filmdescription(film):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_film = f"select movietitle, year, price, directorname, language, genre, country "
        db_film += f"from imdb_movies as m, imdb_movielanguages as il, imdb_moviegenres as ig, "
        db_film += f"imdb_directors as d,imdb_directormovies as dm, imdb_moviecountries as ic, products as p "
        db_film += f"where p.movieid = m.movieid and m.movieid = il.movieid "
        db_film += f"and ig.movieid = m.movieid and d.directorid = dm.directorid and m.movieid = dm.movieid and ic.movieid = m.movieid " 
        db_film += f"and m.movieid = '{film}'"
        
        db_result = db_conn.execute(db_film)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_search(search):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_search = f"select movieid, movietitle from imdb_movies where movietitle ~* '{search}'"
        
        db_result = db_conn.execute(db_search)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_category(cat):
    if cat == 'Accion':
        cat = 'Action'
    elif cat == 'Aventura':
        cat = 'Adventure'
    elif cat == 'Ciencia Ficcion':
        cat = 'Sci-Fi'

    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_cat = f"select m.movieid, movietitle from imdb_movies as m, imdb_moviegenres as ig "
        db_cat += f"where m.movieid = ig.movieid and genre = '{cat}'"
        db_cat += f" fetch first 3 rows only"
        
        db_result = db_conn.execute(db_cat)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_aumentarSaldo(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_cat = f"update customers set saldo = saldo + 20 where customers.customerid = {userid}" 
        
        db_result = db_conn.execute(db_cat)
        db_conn.close()

        return True

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_obtenerSaldo(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_cat = f"select saldo from customers where customers.customerid = {userid}" 
        
        db_result = db_conn.execute(db_cat)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_comprar(userid, movieid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # si esta query no devuelve nada es que no hay order aun creado
        db_order = f"select * from orders where status is null and customerid = {userid}" 
        
        db_result = db_conn.execute(db_order)

        result = list(db_result)

        db_price = f"select price from products where movieid = {movieid}"
        db_result2 = db_conn.execute(db_price)

        result2 = list(db_result2)

        if result == []:
            db_insert = f"insert into orders (orderdate, customerid, tax) values (current_date, {userid}, 15)"
            db_result3 = db_conn.execute(db_insert)

        #una vez insertado obtenemos el id del pedido para insertarlo en orderdetail

        db_idorder = f"select orderid from orders where status is null and customerid = {userid}"
        db_result3 = db_conn.execute(db_idorder)

        result3 = list(db_result3)

        db_getprodid = f"select prod_id from products where movieid = {movieid}"
        db_prodid = db_conn.execute(db_getprodid)

        prodid = list(db_prodid)
        #veamos si esta ya el pedido en orderdetail

        db_orderdetail = f"select * from orderdetail where orderid = {result3[0][0]} and prod_id = {prodid[0][0]}"
        db_result4 = db_conn.execute(db_orderdetail)

        result4 = list(db_result4)

        #si esta vacia es porque el id no está en orderdetail, es decir es un order nuevo
        if result4 == []:
            db_insert2 = f"insert into orderdetail (orderid, prod_id, price, quantity) values ({result3[0][0]}, {prodid[0][0]}, {result2[0][0]}, 1)"
            db_result5 = db_conn.execute(db_insert2)

        else:
            db_update = f"update orderdetail set quantity = quantity + 1 where prod_id = {prodid[0][0]} and orderid = {result3[0][0]}"
            db_result5 = db_conn.execute(db_update)

        db_conn.close()

        return True

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_getorders(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getorders = f"select prod_id, orders.orderid, quantity from orders natural join orderdetail"
        db_getorders += f" where status is null and customerid = {userid}" 
        
        db_result = db_conn.execute(db_getorders)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_finpedido(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getpedido = f"select * from orders where status is null and customerid = {userid}"
        
        db_result = db_conn.execute(db_getpedido)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def db_getproductos(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getprods = f"select movieid, orders.orderid, quantity from orders natural join orderdetail natural join products"
        db_getprods += f" where status is null and customerid = {userid}"

        db_result = db_conn.execute(db_getprods)
        
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def db_setstatus(orderid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_setStatus = f"update orders set status = 'Paid' where orderid = {orderid}"
        
        db_result = db_conn.execute(db_setStatus)
        db_conn.close()

        return

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_setsaldo(userid, precio):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_setsaldo = f"update customers set saldo = saldo - {precio} where customerid = {userid}"
        
        db_result = db_conn.execute(db_setsaldo)
        db_conn.close()

        return

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_getmovieid(prodid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getmovieid = f"select movieid from products where prod_id = {prodid}"
        
        db_result = db_conn.execute(db_getmovieid)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False   

def db_getprodid(movieid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getprodid = f"select prod_id from products where movieid = {movieid}"
        
        db_result = db_conn.execute(db_getprodid)
        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False   


def db_eliminar(userid, movie_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        prodid = db_getprodid(movie_id)

        db_getorders = f"select * from orders natural join orderdetail where customerid = {userid} and prod_id = {prodid[0][0]}"
        db_result = db_conn.execute(db_getorders)
        
        orders = list(db_result)

        if orders == []:
            print ("Error")
            return False

        db_setquantity = f"update orderdetail set quantity = quantity - 1 where prod_id = {prodid[0][0]} and orderid = {orders[0][0]}"
        db_result = db_conn.execute(db_setquantity)

        db_comprobar = f"select quantity from orderdetail where prod_id = {prodid[0][0]} and orderid = {orders[0][0]}"
        db_result = db_conn.execute(db_comprobar)

        quantity = list(db_result)

        if quantity[0][0] <= 0:
            db_sacarfila = f"delete from orderdetail where prod_id = {prodid[0][0]} and orderid = {orders[0][0]}"
            db_result = db_conn.execute(db_sacarfila)

        db_comprobar2 = f"select prod_id from orderdetail where orderid = {orders[0][0]}"
        db_result = db_conn.execute(db_comprobar2)

        lista = list(db_result)
        if lista == []:
            db_sacarfila2 = f"delete from orders where orderid = {orders[0][0]}"
            db_result = db_conn.execute(db_sacarfila2)

        db_conn.close()

        return

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False    

def db_añadir(userid, movie_id):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        prodid = db_getprodid(movie_id)

        db_getorders = f"select * from orders natural join orderdetail where customerid = {userid} and prod_id = {prodid[0][0]}"
        db_result = db_conn.execute(db_getorders)
        
        orders = list(db_result)

        if orders == []:
            print ("Error")
            return False

        db_setquantity = f"update orderdetail set quantity = quantity + 1 where prod_id = {prodid[0][0]} and orderid = {orders[0][0]}"
        db_result = db_conn.execute(db_setquantity)

        db_conn.close()

        return 

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False 

def db_gethistorial(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_gethistorial = f"select prod_id, orders.orderid, quantity, orderdate from orders natural join orderdetail"
        db_gethistorial += f" where status = 'Paid' and customerid = {userid}" 
        db_result = db_conn.execute(db_gethistorial)

        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_getfechas(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getfechas = f"select distinct orderdate from orders natural join orderdetail"
        db_getfechas += f" where status = 'Paid' and customerid = {userid}" 
        db_result = db_conn.execute(db_getfechas)

        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


'''def db_topventas():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getTopVentas = f"select * from getTopVentas(2017, 2020)"
        db_result = db_conn.execute(db_getTopVentas)

        db_conn.close()

        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False'''

def db_getstock(prodid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getstock = f"select stock from products where prod_id = {prodid}"
        
        db_result = db_conn.execute(db_getstock)
        db_conn.close()

        stock = list(db_result)
        return stock[0][0]

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_getnumitems(userid):
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_getnumitems = f"select sum(quantity) from orderdetail, orders"
        db_getnumitems += f" where orders.orderid = orderdetail.orderid and orders.status is null"
        db_getnumitems += f" and orders.customerid = {userid}"
        
        db_result = db_conn.execute(db_getnumitems)
        db_conn.close()

        items = list(db_result)
        if items[0][0] == None:
            return 0

        return items[0][0]

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def db_topUSAfirstTable():


    col = db_mongo["topUSA"]
    query = { "year" : "1997", "title" : { "$regex" : "(?i).*?\\blife.*?\\b"}, 'genres':{ "$in": ["Comedy"]}}
    topUSA = col.find(query)

    top = []

    for movie in topUSA:

        peli = {}

        peli["title"] = movie["title"]
        peli["year"] = movie["year"]
        top.append(peli)

    return top

def db_topUSAsecondTable():

    col = db_mongo["topUSA"]
    query = {  "year" : { "$gte" : "1990"}, "year" : {"$lte": "1999"},'directors':{ "$in": ["Allen, Woody"]}}
    topUSA = col.find(query)

    top = []
    for movie in topUSA:

        peli = {}

        peli["title"] = movie["title"]
        peli["year"] = movie["year"]
        peli["directores"] = movie["directors"]

        top.append(peli)

    return top

def db_topUSAthirdTable():

    col = db_mongo["topUSA"]
    query = {"actors": {"$all": ["Galecki, Johnny", "Parsons, Jim (II)"]}}
    topUSA = col.find(query)

    top = []
    for movie in topUSA:

        peli = {}

        peli["title"] = movie["title"]
        peli["year"] = movie["year"]
        peli["actors"] = movie["actors"]

        top.append(peli)

    return top




    