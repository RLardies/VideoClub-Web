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
        print("entro aqui")
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
        db_film += f"and ic.country = c.country_id and m.movieid = '{film}'"
        
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