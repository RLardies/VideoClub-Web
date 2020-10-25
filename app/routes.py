#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, flash
import jinja2
import json
import os
import sys
import hashlib
from random import randint
import itertools
import time


def getMovies():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    return catalogue['peliculas']

def getCategories():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    categories = []

    for movie in catalogue['peliculas']:
        if movie['categoria'] not in categories:
            categories.append(movie['categoria'])
    
    return categories



@app.route('/')
#@app.route('/index')
#def index():
#    print (url_for('static', filename='estilo.css'), file=sys.stderr)
#    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
#    catalogue = json.loads(catalogue_data)
#    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

    

@app.route('/home')
def home():
    print (url_for('static', filename='estilo.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    categories = []

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

    
    return render_template('home.html', title = "Home", movies=catalogue['peliculas'], categories=getCategories())



@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario

        username = request.form['username']

        if os.path.isdir("app/users/" + username):

            route = "app/users/" + username + "/data.dat"

            with open(route) as data:
                texto = itertools.islice(data, 1, 2 )
                for linea in texto:
                    pwd = linea[:-1]

            #password = request.form['password']
            password = hashlib.sha512((request.form['password']).encode('utf-8')).hexdigest()
            #Encriptamos password para compararla:


            if password == pwd:
                session['usuario'] = request.form['username']
                session.modified=True

                # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                return redirect(url_for('home'))

            else:
                #Algo de contraseña invalida
                return render_template('login.html', title = "Sign In", categories=getCategories())
        
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido

            #USUARIO NO EXISTE
            return render_template('login.html', title = "Sign In", categories=getCategories())
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In", categories=getCategories())

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['usuario'] = None
    session.modified=False
    session.pop('usuario', None)
    session.pop('carrito', None)
    session.pop('precio', None)
    session.pop('num_productos_car', 0)
    session.pop('num_items',0)


    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():


    if 'username' in request.form:

        username = request.form['username']

        if os.path.isdir("app/users/" + username):

            #Meter mensaje de error
            #Usuario ya existe
            flash("Ya existe el usuario")
            return render_template('signup.html', title = "Sign Up")

        else:

            os.mkdir("app/users/" + username)

            route = "app/users/" + username + "/data.dat"

            password =  hashlib.sha512((request.form['pwd']).encode('utf-8')).hexdigest()

            file = open(route, "w")

            file.write(request.form['username'] + os.linesep)
            file.write(password + os.linesep)
            file.write(request.form['email'] + os.linesep)
            file.write(request.form['creditcard'] + os.linesep)
            file.write(str(randint(0,100)) + os.linesep)

            hist_route = "app/users/" + username + "/historial.json"
            file = open(hist_route, "w")
            historial = {}

            file.write(json.dumps(historial))

            return render_template('home.html', movies = getMovies(), categories=getCategories())
        
    else:
        return render_template('signup.html', title = "Sign Up", )



@app.route('/filmdescription', methods=['GET', 'POST'])
def filmdescription():

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    movie_id =  request.args.get('movie_id')

    for item in catalogue['peliculas']:
        if item['id'] == int(movie_id):
            break

    return render_template('filmdescription.html', title = item['titulo'], movie = item, categories=getCategories())

@app.route('/filmdescription/<movie_id>_buy', methods=['GET', 'POST'])
def comprar(movie_id):

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    for item in catalogue['peliculas']:
        if int(movie_id) == item['id']:
            if 'carrito' not in session:
                session['carrito'] = []
            session['carrito'].append(movie_id)

            if 'precio' not in session:
                    session['precio'] = 0
            session['precio'] += item['precio']
            if 'num_productos_car' not in session:
                session['num_productos_car'] = []
                for num_movies in range(len(catalogue['peliculas'])):
                    session['num_productos_car'].append(0)
            session['num_productos_car'][int(movie_id)-1] += 1


            if 'num_items' not in session:
                session['num_items'] = 0
            session['num_items'] += 1

            break

    return redirect(url_for('filmdescription', movie_id = movie_id))

@app.route('/category', methods=['GET', 'POST'])
def category():

    title =  request.args.get('nombre')

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    movies = []

    for movie in catalogue['peliculas']:
        if movie['categoria'] == title:
            movies.append(movie)


    
    return render_template('category.html', title = title, movies=movies, categories= getCategories())

@app.route('/historial', methods=['GET', 'POST'])
def historial():

    if session['usuario'] != None:
        route = "app/users/" + session['usuario'] + "/data.dat"
        with open(route) as data:
                texto = itertools.islice(data, 4, 5 )
                for linea in texto:
                    saldo = linea[:-1]

        route = "app/users/" + session['usuario'] + "/historial.json"

        if os.path.isfile(route):

            historial_data = open(route, encoding="utf-8").read()
            historial = json.loads(historial_data)

            return render_template('historial.html', title='Historial de Compra', historial=historial, msg= None, categories=getCategories(), saldo=saldo)

        else:
            return render_template('historial.html', title='Historial de Compra',msg="No se ha realizado ninguna compra", categories=getCategories(), saldo=saldo)
    
    else:
        return redirect(url_for('home'))

@app.route('/historial/aumentar_saldo', methods=['GET', 'POST'])
def aumentarSaldo():

    username = session['usuario']

    if os.path.isdir("app/users/" + username):

        route = "app/users/" + username + "/data.dat"

        with open(route) as data:
            texto = itertools.islice(data, 4, 5 )
            for linea in texto:
                saldo = linea[:-1]

        nuevo_saldo = float(saldo) + 10
        data = []
        with open(route, 'r') as f:
            for linea in f:
                data.append(linea[:-1])

        with open(route, "w") as file:

            file.write(data[0]+ os.linesep)
            file.write(data[1] + os.linesep)
            file.write(data[2] + os.linesep)
            file.write(data[3] + os.linesep)
            file.write(str(round(nuevo_saldo, 2)) + os.linesep) 

    return redirect(url_for('historial'))


@app.route('/search', methods=['GET', 'POST'])
def search():

    search =  request.args.get('search')

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    movies = []
    msg = None

    if 'search' in request.form:

        search = request.form['search']
        search = search.lower()

        for movie in catalogue['peliculas']:
            titulo = movie['titulo'].lower()
            if titulo.find(search) >= 0:
                movies.append(movie)
    else:
        for movie in catalogue['peliculas']:
            movies.append(movie)

    if len(movies) == 0:

        msg = "No hay peliculas asociadas a la busqueda '" + search + "'"
        
    return render_template('search.html', title = "Búsqueda", movies=movies, categories= getCategories(), msg = msg)

@app.route('/carrito', methods=['GET', 'POST'])
def carrito():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies=catalogue['peliculas']
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

    return render_template('carrito.html', title = "Carrito", lista_carrito = lista, num_elementos = session['num_productos_car'], precio="{0:.2f}".format(session['precio']), categories=getCategories())

@app.route('/carrito/<movie_id>_removed', methods=['GET', 'POST'])
def eliminar(movie_id):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies=catalogue['peliculas']

    if movies[int(movie_id)] != None:
        session['carrito'].remove(movie_id)
        session['precio'] -= movies[int(movie_id)]['precio']
        session['num_productos_car'][int(movie_id) - 1] -= 1
        session['num_items'] -= 1

    session.modified = True
    return redirect(url_for('carrito'))

@app.route('/carrito/<movie_id>_added', methods=['GET', 'POST'])
def añadir(movie_id):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies=catalogue['peliculas']

    if movies[int(movie_id)] != None:
        session['carrito'].append(movie_id)
        session['precio'] += movies[int(movie_id)]['precio']
        session['num_productos_car'][int(movie_id) - 1] += 1
        session['num_items'] += 1

    return redirect(url_for('carrito'))

@app.route('/finpedido', methods=['GET', 'POST'])
def realizar_pedido():

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies=catalogue['peliculas']

    if 'usuario' in session:

        username = session['usuario']

        if os.path.isdir("app/users/" + username):

            route = "app/users/" + username + "/data.dat"

            with open(route) as data:
                texto = itertools.islice(data, 4, 5 )
                for linea in texto:
                    saldo = linea[:-1]

        

        if float(saldo) < float(session['precio']):
            flash(u'Saldo insuficiente', 'error')

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

            return render_template('carrito.html', title = "Carrito", lista_carrito = lista, num_elementos = session['num_productos_car'], precio="{0:.2f}".format(session['precio']), categories=getCategories(), msg = msg)

        nuevo_saldo = float(saldo) - float(session['precio'])
        data = []
        with open(route, 'r') as f:
            for linea in f:
                data.append(linea[:-1])

        with open(route, "w") as file:

            file.write(data[0]+ os.linesep)
            file.write(data[1] + os.linesep)
            file.write(data[2] + os.linesep)
            file.write(data[3] + os.linesep)
            file.write(str(round(nuevo_saldo, 2)) + os.linesep)


        route = "app/users/" + session['usuario'] + "/historial.json"

        if os.path.isfile(route):

            historial_data = open(route, encoding="utf-8").read()
            historial = json.loads(historial_data) 
        else:
            historial = {}

        date = time.strftime("%d/%m/%y")
        if str(date) not in historial:
            historial[str(date)]= []


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
                item['cantidad'] = session['num_productos_car'][int(movie)-1]
                session['num_productos_car'][int(movie)-1] = 0
                historial[str(date)].append(item)

            if in_history == 1:
                index = historial[str(date)].index(j)
                historial[str(date)][index]['cantidad'] += session['num_productos_car'][int(movie)-1]
                session['num_productos_car'][int(movie)-1] = 0

        file = open(route, "w")
        file.write(json.dumps(historial, indent=2))

        session['carrito'] = []
        session['num_productos_car'] = []
        for num_movies in range(len(catalogue['peliculas'])):
            session['num_productos_car'].append(0)
        session['precio'] = 0
        session['num_items'] = 0

        return redirect(url_for('carrito'))

    else:

        return redirect(url_for('login'))


@app.route('/connected_users')
def connected_user():
    num_users = randint(100, 1000)

    return "Usuarios Conectados: " + str(num_users)