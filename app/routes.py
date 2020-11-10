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

    if 'num_productos_car' not in session:
        session['num_productos_car'] = []

    for num_movies in range(len(catalogue['peliculas'])):
        session['num_productos_car'].append(0)

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


@app.route('/filmdescription', methods=['GET', 'POST'])
def filmdescription():

    #catalogue_data = open(os.path.join(
    #    app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    #catalogue = json.loads(catalogue_data)

    # obtenemos el id de la pelicula requerida y la buscamos en el catalogo
    movie_id = request.args.get('movie_id')

    #for item in catalogue['peliculas']:
    #    if item['id'] == int(movie_id):
    #        break

    result = database.db_filmdescription(movie_id)
    item = {}
    item['id'] = movie_id
    item['titulo'] = result[0][0]
    item['director'] = result[0][3]
    item['precio'] = result[0][2]
    item['categoria'] = result[0][5]
    item['año'] = result[0][1]
    item['pais'] = result[0][6]
    item['idioma'] = result[0][4]

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

    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    for item in catalogue['peliculas']:
        if int(movie_id) == item['id']:

            # Añadimos la pelicula al carrito
            if 'carrito' not in session:
                session['carrito'] = []
            session['carrito'].append(movie_id)

            # La sumamos al precio total
            if 'precio' not in session:
                session['precio'] = 0
            session['precio'] += item['precio']

            # Añadimos uno al numero de ese producto en el carrito
            if 'num_productos_car' not in session:
                session['num_productos_car'] = []
                for num_movies in range(len(catalogue['peliculas'])):
                    session['num_productos_car'].append(0)
            session['num_productos_car'][int(movie_id)-1] += 1

            # Añadimos 1 al numero de items total del carrito
            if 'num_items' not in session:
                session['num_items'] = 0
            session['num_items'] += 1

            session.modified = True

            break

    return redirect(url_for('filmdescription', movie_id=movie_id))


@app.route('/category', methods=['GET', 'POST'])
def category():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    # Obtenemos el nombre de la categoria que se ha solicitado
    title = request.args.get('nombre')

    movies = []

    # Añadimos las peliculas de esa categoria
    for movie in catalogue['peliculas']:
        if movie['categoria'] == title:
            movies.append(movie)

    return render_template('category.html',
                           title=title,
                           movies=movies,
                           categories=getCategories())


@app.route('/historial', methods=['GET', 'POST'])
def historial():

    # Comrpobamos que el usuario este loggeado
    if session['usuario'] is not None:
        route = "app/users/" + session['usuario'] + "/data.dat"
        with open(route) as data:
            texto = itertools.islice(data, 4, 5)
            for linea in texto:
                saldo = linea[:-1]

        route = "app/users/" + session['usuario'] + "/historial.json"

        # Comprobamos que exista el fichero y lo leemos
        if os.path.isfile(route):

            historial_data = open(route, encoding="utf-8").read()
            historial = json.loads(historial_data)

            msg = None

            # Si el historial esta vacio, no ha habido compras
            if historial == {}:
                msg = "No se ha realizado ninguna compra"

            return render_template('historial.html',
                                   title='Historial de Compra',
                                   historial=historial, msg=msg,
                                   categories=getCategories(), saldo=saldo)

        else:
            return redirect(url_for('home'))

    else:
        return redirect(url_for('home'))


@app.route('/historial/aumentar_saldo', methods=['GET', 'POST'])
def aumentarSaldo():

    username = session['usuario']

    # Abrimos el data.dat del usuario que vamos a modificar
    if os.path.isdir("app/users/" + username):

        route = "app/users/" + username + "/data.dat"

        with open(route) as data:
            texto = itertools.islice(data, 4, 5)
            for linea in texto:
                saldo = linea[:-1]

        # Añadimos 10 euros de saldo
        nuevo_saldo = float(saldo) + 10
        data = []
        with open(route, 'r') as f:
            for linea in f:
                data.append(linea[:-1])

        with open(route, "w") as file:

            file.write(data[0] + os.linesep)
            file.write(data[1] + os.linesep)
            file.write(data[2] + os.linesep)
            file.write(data[3] + os.linesep)
            file.write(str(round(nuevo_saldo, 2)) + os.linesep)

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
                           movies=movies, categories=getCategories())
        
        else:
            msg = "No hay peliculas asociadas a la busqueda '" + search + "'"

            return render_template('search.html', title="Búsqueda",
                           movies=movies, categories=getCategories(), msg=msg)

        #for movie in catalogue['peliculas']:
            # Ponemos los titulos de las peliculas en minuscula
        #    titulo = movie['titulo'].lower()

            # Buscamos la cadena en ellos
        #    if titulo.find(search) >= 0:
        #        movies.append(movie)
    else:
         return render_template('home.html',
                           title="Home",
                           movies=catalogue['peliculas'],
                           categories=getCategories())

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    movies = catalogue['peliculas']
    lista = []

    if 'carrito' not in session:
        session['carrito'] = []

    if 'precio' not in session:
        session['precio'] = 0

    if 'num_productos_car' not in session:
        session['num_productos_car'] = []

    for movie in movies:
        if str(movie['id']) in session['carrito']:
            lista.append(movie)

    return render_template('carrito.html', title="Carrito",
                           lista_carrito=lista,
                           num_elementos=session['num_productos_car'],
                           precio="{0:.2f}".format(session['precio']),
                           categories=getCategories(),  msg="")


@app.route('/carrito/<movie_id>_removed', methods=['GET', 'POST'])
def eliminar(movie_id):

    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']

    # Eliminamos un articulo del carrito
    if movies[int(movie_id)] is not None:
        session['carrito'].remove(movie_id)
        session['precio'] -= movies[int(movie_id)]['precio']
        session['num_productos_car'][int(movie_id) - 1] -= 1
        session['num_items'] -= 1
        session.modified = True

    return redirect(url_for('carrito'))


@app.route('/carrito/<movie_id>_added', methods=['GET', 'POST'])
def añadir(movie_id):
    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']

    # Añadimos un articulo del carrito
    if movies[int(movie_id)] is not None:
        session['carrito'].append(movie_id)
        session['precio'] += movies[int(movie_id)]['precio']
        session['num_productos_car'][int(movie_id) - 1] += 1
        session['num_items'] += 1
        session.modified = True

    return redirect(url_for('carrito'))


@app.route('/finpedido', methods=['GET', 'POST'])
def realizar_pedido():

    catalogue_data = open(os.path.join(
        app.root_path, 'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']

    if 'usuario' in session:

        username = session['usuario']

        # Si el usuario existe, obtenemos su saldo
        if os.path.isdir("app/users/" + username):

            route = "app/users/" + username + "/data.dat"

            with open(route) as data:
                texto = itertools.islice(data, 4, 5)
                for linea in texto:
                    saldo = linea[:-1]

        # Si el precio es mayor que el saldo mostramnos mensaje de error
        if float(saldo) < float(session['precio']):

            lista = []

            if 'carrito' not in session:
                session['carrito'] = []

            if 'precio' not in session:
                session['precio'] = 0

            if 'num_productos_car' not in session:
                session['num_productos_car'] = []

            for movie in movies:
                if str(movie['id']) in session['carrito']:
                    lista.append(movie)

            msg = "Saldo insuficiente"

            return render_template('carrito.html', title="Carrito",
                                   lista_carrito=lista,
                                   num_elementos=session['num_productos_car'],
                                   precio="{0:.2f}".format(session['precio']),
                                   categories=getCategories(), msg=msg)

        # Calculamos nuevo saldo y lo escribimos en data.dat
        nuevo_saldo = float(saldo) - float(session['precio'])
        data = []
        with open(route, 'r') as f:
            for linea in f:
                data.append(linea[:-1])

        with open(route, "w") as file:

            file.write(data[0] + os.linesep)
            file.write(data[1] + os.linesep)
            file.write(data[2] + os.linesep)
            file.write(data[3] + os.linesep)
            file.write(str(round(nuevo_saldo, 2)) + os.linesep)

        # Añadimos al historial las peliculas compradas
        route = "app/users/" + session['usuario'] + "/historial.json"

        if os.path.isfile(route):

            historial_data = open(route, encoding="utf-8").read()
            historial = json.loads(historial_data)
        else:
            historial = {}

        date = time.strftime("%d/%m/%y")
        if str(date) not in historial:
            historial[str(date)] = []

        for movie in session['carrito']:
            in_history = 0
            item = movies[int(movie)-1]

            if historial[str(date)] != []:
                for j in historial[str(date)]:
                    print(j['id'])
                    print(item['id'])
                    if j['id'] == item['id']:
                        in_history = 1
                        break

            if in_history == 0:
                item['cantidad'] = 1
                historial[str(date)].append(item)

            if in_history == 1:
                index = historial[str(date)].index(j)
                historial[str(date)][index]['cantidad'] += 1

        file = open(route, "w")
        file.write(json.dumps(historial, indent=2))

        # Reiniciamos las variables de session
        session['carrito'] = []
        session['num_productos_car'] = []
        for num_movies in range(len(catalogue['peliculas'])):
            session['num_productos_car'].append(0)
        session['precio'] = 0
        session['num_items'] = 0
        session.modified = True

        return redirect(url_for('carrito'))

    else:

        return redirect(url_for('login'))


@app.route('/connected_users')
def connected_user():

    # Tomamos un numero aleatorio de usuarios
    num_users = randint(100, 1000)

    return "Usuarios Conectados: " + str(num_users)
