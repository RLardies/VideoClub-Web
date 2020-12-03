import pymongo
import json
import os
import sys, traceback
import collections
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongoDB"]

mycol = mydb["movies"]

db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

try:
    db_conn = None
    db_conn = db_engine.connect()

    db_selected_movies = f"select m.movieid"
    db_selected_movies += f" from imdb_movies as m natural join imdb_moviecountries"
    db_selected_movies += f" where country = 'USA' "
    db_selected_movies += f" order by year desc fetch first 800 rows only"

    result = db_conn.execute(db_selected_movies)
    # ya tenemos los id's, los recorremos obteniendo su info y añadiendolo a la nueva bd
    movies = list(result)

    genres_list = []
    id_movie = 0
    for item in movies:
        Lgenre = []
        db_genres = f"select genre from imdb_moviegenres where movieid = {item[0]}"
        db_result = db_conn.execute(db_genres)
        result = list(db_result)

        for res in result:
            Lgenre.append(res[0])

        genres_list.append(Lgenre)

    for item in movies:
        movie = {}

        db_title = f"select movietitle, year from imdb_movies where movieid = {item[0]}"
        db_result = db_conn.execute(db_title)
        result = list(db_result)
        restitle = result[0][0]
        resyear = result[0][1]

        movie['title'] = restitle
        movie['year'] = resyear

        db_genres = f"select genre from imdb_moviegenres where movieid = {item[0]}"
        db_result = db_conn.execute(db_genres)
        genre_list = list(db_result)
        
        L = []
        for genre in genre_list:
            L.append(genre[0])
            

        movie['genres'] = L
        
        db_directors = f"select directorname from imdb_directors natural join imdb_directormovies "
        db_directors += f"where movieid = '{item[0]}'"
        db_result = db_conn.execute(db_directors)
        director_list = list(db_result)
        L = []
        for director in director_list:
            L.append(director[0])
        
        movie['directors'] = L
        
        db_actors = f"select actorname from imdb_actors natural join imdb_actormovies "
        db_actors += f"where movieid = '{item[0]}'"
        db_result = db_conn.execute(db_actors)
        actor_list = list(db_result)
        L = []
        for actor in actor_list:
            L.append(actor[0])

        Lmost_related = []
        i = 0
        for i in range(0, len(genres_list)):
            genres_list[i].sort()
            movie['genres'].sort()

            if genres_list[i] == movie['genres']:
                if (i != id_movie):
                    relacionada = {}
                    db_title = f"select movietitle, year from imdb_movies where movieid = {movies[i][0]}"
                    db_result = db_conn.execute(db_title)
                    result = list(db_result)

                    relacionada['title'] = result[0][0]
                    relacionada['year'] = result[0][1]

                    Lmost_related.append(relacionada)
            
            if len(Lmost_related) > 10:
                movie['most_related_movies'] = Lmost_related[:10]
            else:
                movie['most_related_movies'] = Lmost_related

        mycol.insert_one(movie)
        id_movie += 1

    db_conn.close()

except:
    if db_conn is not None:
        db_conn.close()
    print("Exception in DB access:")
    print("-"*60)
    traceback.print_exc(file=sys.stderr)
    print("-"*60)


