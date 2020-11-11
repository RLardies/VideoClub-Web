#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request
from flask import url_for, redirect, session, make_response
import json
import os
import sys
import hashlib
from random import randint
import itertools
import time
import traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

# obtenemos todas las peliculas de catalogue.json

def getMovies():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    return catalogue['peliculas']

# obtenemos todas las categorias de catalogue.json


def getCategories():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    categories = []

    for movie in catalogue['peliculas']:
        if movie['categoria'] not in categories:
            categories.append(movie['categoria'])
    return categories


@app.route('/')
@app.route('/home')
def home():
    print(url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # inicializamos algunas de las variables de session
    if 'num_items' not in session:
        session['num_items'] = 0

    if 'carrito' not in session:
        session['carrito'] = []

    if 'precio' not in session:
        session['precio'] = 0

    return render_template('home.html',
                           title="Home",
                           movies=catalogue['peliculas'],
                           categories=getCategories())


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'username' in request.form:

        username = request.form['username']
        pwd = request.form['password']

        result = database.db_login(username, pwd)

        if result:
            session['userid'] = result[0][0]
            response = make_response(redirect(url_for('home')))
            response.set_cookie('usuario', request.form['username'])
            session['usuario'] = request.form['username']
            session.modified = True

            return response

        else:
            return render_template('login.html',
                                       title="Sign In",
                                       categories=getCategories(), msg = "Login incorrect")

    else:
        nombre = request.cookies.get('usuario')
        # se puede guardar la pagina desde la que se invoca
        session['url_origen'] = request.referrer
        session.modified = True
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print(request.referrer, file=sys.stderr)
        return render_template('login.html',
                               title="Sign In",
                               nombre=nombre,
                               categories=getCategories())


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['usuario'] = None
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.pop('precio', None)
    session.pop('num_productos_car', 0)
    session.pop('num_items', 0)
    session.modified = True

    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if 'username' in request.form:

        data = {}
        data['username'] = request.form['username']
        data['pwd'] = request.form['pwd']
        data['email'] = request.form['email']
        data['creditcard'] = request.form['creditcard']
        data['gender'] = request.form['gender']
        data['firstname'] = request.form['firstname']
        data['lastname'] = request.form['lastname']

        result = database.db_alreadyregistered(data)
        if result:
            return render_template('signup.html', title="Sign Up", msg = "User already exists")
                
        else:
            r = database.db_register(data)
            if r:
                return render_template('home.html',
                                   movies=getMovies(),
                                   categories=getCategories())
            else:
                return render_template('signup.html', title="Sign Up", msg = "Something went wrong") 
        
    else:
       return render_template('signup.html', title="Sign Up", )

def filmdescriptionAux(movieid):

    result = database.db_filmdescription(movieid)
    print("RESULTADO")
    print(result)

    if result != False:
        item = {}
        item['id'] = movieid
        item['titulo'] = result[0][0]
        item['director'] = result[0][3]
        item['precio'] = result[0][2]
        item['categoria'] = result[0][5]
        item['año'] = result[0][1]
        item['pais'] = result[0][6]
        item['idioma'] = result[0][4]

        return item
    else:
        return None

@app.route('/filmdescription', methods=['GET', 'POST'])
def filmdescription():

    #catalogue_data = open(os.path.join(
    #    app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    #catalogue = json.loads(catalogue_data)

    # obtenemos el id de la pelicula requerida y la buscamos en el catalogo
    movie_id = request.args.get('movie_id')
    prodid = database.getprodid(movie_id)

    #for item in catalogue['peliculas']:
    #    if item['id'] == int(movie_id):
    #        break
 
    item = filmdescriptionAux(prodid[0][0])

    if item is None:
        return render_template('home.html',
                           movies=getMovies(),
                           categories=getCategories())

    return render_template('filmdescription.html',
                           title=item['titulo'],
                           movie=item,
                           categories=getCategories())


@app.route('/filmdescription/<movie_id>_buy', methods=['GET', 'POST'])
def comprar(movie_id):

    if 'userid' not in session:
        return render_template('login.html',
                                title="Sign In",
                                categories=getCategories())
    userid = session['userid']
    result = database.db_comprar(userid, movie_id)

    if 'num_items' not in session:
        session['num_items'] = 0

    session['num_items'] += 1
    session.modified=True

    return redirect(url_for('filmdescription', movie_id=movie_id))


@app.route('/category', methods=['GET', 'POST'])
def category():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    movies = []
    # Obtenemos el nombre de la categoria que se ha solicitado
    cat = request.args.get('nombre')

    result = database.db_category(cat)
    if result:
        for item in result:
            movie = {}
            movie['id'] = item[0]
            movie['titulo'] = item[1]
            movie['poster'] = ""
            movies.append(movie)

    

    # Añadimos las peliculas de esa categoria
    #for movie in catalogue['peliculas']:
    #    if movie['categoria'] == cat:
    #        movies.append(movie)

        return render_template('category.html',
                           title=cat,
                           movies=movies,
                           categories=getCategories())
    else:
        return render_template('home.html',
                           title="Home",
                           movies=catalogue['peliculas'],
                           categories=getCategories())


@app.route('/historial', methods=['GET', 'POST'])
def historial():
    # FALTA POR INTEGRAR EL HISTORIAL
    userid = session['userid']

    # Comprobamos que el usuario este loggeado
    if session['usuario'] is not None:
        result = database.db_obtenerSaldo(userid)
        saldo = float(result[0][0])
        saldo = "{0:.2f}".format(saldo)

        #result = database.db_gethistorial(userid)

        return render_template('historial.html',
                                    title='Historial de Compra',
                                    msg="Aún no hay nada aquí",
                                    categories=getCategories(), saldo=saldo)

    else:
        return redirect(url_for('home'))


@app.route('/historial/aumentar_saldo', methods=['GET', 'POST'])
def aumentarSaldo():

    userid = session['userid']
    result = database.db_aumentarSaldo(userid)

    return redirect(url_for('historial'))


@app.route('/search', methods=['GET', 'POST'])
def search():

    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # Texto que se va a buscar
    search = request.args.get('search')

    movies = []
    msg = None

    if request.form['search'] != "":

        search = request.form['search']

        result = database.db_search(search)
        if result:
            for item in result:
                movie = {}
                movie['id'] = item[0]
                movie['titulo'] = item[1]
                movie['poster'] = ""
                movies.append(movie)
            
            return render_template('search.html', title="Búsqueda",
                           movies=movies, categories=getCategories(), msg=msg)
        
        else:
            msg = "No hay peliculas asociadas a la busqueda '" + search + "'"

            return render_template('search.html', title="Búsqueda",
                           movies=movies, categories=getCategories(), msg=msg)

    else:
         return render_template('home.html',
                           title="Home",
                           movies=catalogue['peliculas'],
                           categories=getCategories())

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():

    if 'carrito' not in session:
        session['carrito'] = []

    if 'precio' not in session:
        session['precio'] = 0

    if 'num_productos_car' not in session:
        session['num_productos_car'] = []

    userid = session['userid']
    result = database.db_getorders(userid)
    lista = []
    precio = 0

    if result != False:
        for item in result:
            result = database.db_getmovieid(item[0])
            movie = filmdescriptionAux(result[0][0])
            movie['cantidad'] = item[2]
            precio += movie['precio']*item[2]
            lista.append(movie)

        session['precio'] = precio

    return render_template('carrito.html', title="Carrito",
                           lista_carrito=lista,
                           precio="{0:.2f}".format(session['precio']),
                           categories=getCategories(),  msg="")


@app.route('/carrito/<movie_id>_removed', methods=['GET', 'POST'])
def eliminar(movie_id):
    userid = session['userid']

    result = database.db_eliminar(userid, movie_id)
    if session['num_items'] > 0:
        session['num_items'] -= 1
    session.modified = True

    return redirect(url_for('carrito'))


@app.route('/carrito/<movie_id>_added', methods=['GET', 'POST'])
def añadir(movie_id):
    userid = session['userid']

    result = database.db_añadir(userid, movie_id)
    session['num_items'] += 1
    session.modified = True

    return redirect(url_for('carrito'))


@app.route('/finpedido', methods=['GET', 'POST'])
def realizar_pedido():

    if 'usuario' in session:
        userid = session['userid']

        result = database.db_finpedido(userid)
        result2= database.db_obtenerSaldo(userid)
        saldo = result2[0][0]
        print(saldo)

        # Si el precio es mayor que el saldo mostramnos mensaje de error
        if float(saldo) < float(session['precio']):

            lista = []

            pedido = database.db_getproductos(userid)

            for item in pedido:
                movie = filmdescriptionAux(item[0])
                movie['cantidad'] = item[2]
                lista.append(movie)

            msg = "Saldo insuficiente"
            return render_template('carrito.html', title="Carrito",
                                   lista_carrito=lista,
                                   precio="{0:.2f}".format(session['precio']),
                                   categories=getCategories(), msg=msg)
        
        else:
            result3 = database.db_setstatus(result[0][0])
            result4 = database.db_setsaldo(userid, session['precio'])
            session['num_items'] = 0
            session.modified=True

            return redirect(url_for('carrito'))

    else:

        return redirect(url_for('login'))


@app.route('/connected_users')
def connected_user():

    # Tomamos un numero aleatorio de usuarios
    num_users = randint(100, 1000)

    return "Usuarios Conectados: " + str(num_users)
