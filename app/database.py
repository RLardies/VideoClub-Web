# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
#db_table_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)

def db_listOfMovies1949():
    try:
        db_conn = None
        db_conn = db_engine.connect()

        # Seleccionar las peliculas del anno 1949
        db_movies_1949 = select([db_table_movies]).where(text("year = '1949'"))
        db_result = db_conn.execute(db_movies_1949)
        #db_result = db_conn.execute("Select * from imdb_movies where year = '1949'")
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

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

        db_film = f"select movietitle, year, price, directorname, language_name, genre_name, country_name "
        db_film += f"from imdb_movies as m,languages as l,imdb_movielanguages as il, genres as g, imdb_moviegenres as ig, "
        db_film += f"imdb_directors as d,imdb_directormovies as dm, imdb_moviecountries as ic, countries as c, products as p "
        db_film += f"where p.movieid = m.movieid and l.language_id = il.language and m.movieid = il.movieid and g.genre_id = ig.genre "
        db_film += f"and ig.movieid = m.movieid and d.directorid = dm.directorid and m.movieid = dm.movieid and ic.movieid = m.movieid " 
        db_film += f"and ic.country = c.country_id and p.prod_id = '{film}'"
        
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

        db_cat = f"select m.movieid, movietitle from imdb_movies as m, imdb_moviegenres as ig, genres as g "
        db_cat += f"where m.movieid = ig.movieid and ig.genre = g.genre_id and genre_name = '{cat}'"
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

        #falta comprobar si hay stock
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
            db_update = f"update orderdetail set quantity = quantity + 1 where prod_id = {movieid} and orderid = {result3[0][0]}"
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

        db_getprods = f"select prod_id, orders.orderid, quantity from orders natural join orderdetail"
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

        return list(db_result)

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

        return list(db_result)

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
        print(quantity)

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

        return list(db_result)

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

        #faltaria por comprobar si hay stock para añadirla ??

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