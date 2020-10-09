#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
import hashlib
from random import randint
import itertools

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
    return render_template('home.html', title = "Home", movies=catalogue['peliculas'])



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
                return render_template('login.html', title = "Sign In")
        
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido

            #USUARIO NO EXISTE
            return render_template('login.html', title = "Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['usuario'] = None
    session.modified=False
    session.pop('usuario', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():


    if 'username' in request.form:

        username = request.form['username']

        if os.path.isdir("app/users/" + username):

            #Meter mensaje de error
            #Usuario ya existe
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


            session['usuario'] = request.form['username']
            session.modified=True

            return render_template('home.html')
        
    else:
        return render_template('signup.html', title = "Sign Up")



@app.route('/filmdescription', methods=['GET', 'POST'])
def filmdescription():

    description = "Armado con tan solo una palabra –Tenet– el protagonista de esta historia deberá pelear por la supervivencia del mundo entero en una misión que le lleva a viajar a través del oscuro mundo del espionaje internacional, y cuya experiencia se desdoblará más allá del tiempo lineal. (FILMAFFINITY)"

    title = "La guerra de las galaxias"
    
    return render_template('filmdescription.html', title = title, description= description)
