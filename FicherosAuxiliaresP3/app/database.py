# -*- coding: utf-8 -*-

import os
import sys, traceback, time
import sqlalchemy
from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1_borra", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getListaCliMes(db_conn, mes, anio, iumbral, iintervalo, use_prepare, break0, niter):

    # TODO: implementar la consulta; asignar nombre 'cc' al contador resultante
    consulta = " ... "
    
    # TODO: ejecutar la consulta 
    # - mediante PREPARE, EXECUTE, DEALLOCATE si use_prepare es True
    # - mediante db_conn.execute() si es False

    # Array con resultados de la consulta para cada umbral
    dbr=[]

    for ii in range(niter):

        # TODO: ...

        # Guardar resultado de la query
        dbr.append({"umbral":iumbral,"contador":res['cc']})

        # TODO: si break0 es True, salir si contador resultante es cero
        
        # Actualizacion de umbral
        iumbral = iumbral + iintervalo
                
    return dbr

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):
    
    # Array de trazas a mostrar en la página
    dbr=[]

    db_conn = dbConnect()

    # TODO: Ejecutar consultas de borrado
    # - ordenar consultas según se desee provocar un error (bFallo True) o no
    # - ejecutar commit intermedio si bCommit es True
    # - usar sentencias SQL ('BEGIN', 'COMMIT', ...) si bSQL es True
    # - suspender la ejecución 'duerme' segundos en el punto adecuado para forzar deadlock
    # - ir guardando trazas mediante dbr.append()

    try:

        query1 = "delete from orderdetail where orderdetail.orderid in (select orders.orderid from orders where customerid = {});".format(customerid)
        query2 = "delete from orders where customerid = {};".format(customerid)
        query3 = "delete from customers where customerid = {};".format(customerid)

        # Transaccion via sentencias SQL
        if bSQL:
            command = "BEGIN;"
            sql = sqlalchemy.text(command)
            db_conn.execute(sql)

        # Transaccion via funciones SQLAlchemy
        else:
            #Opcional
            tr = db_conn.begin()

        dbr.append("Hacemos BEGIN")

        if bFallo:

            sql = sqlalchemy.text(query1)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Orderdetail")

            # hacemos commit intermedio
            if bCommit:
                if bSQL:
                    command = "COMMIT;"
                    sql = sqlalchemy.text(command)
                    db_conn.execute(sql)

                    command = "BEGIN;"
                    sql = sqlalchemy.text(command)
                    db_conn.execute(sql)

                    dbr.append("Realizamos COMMIT intermedio")
                else:
                    tr.commit()
                    tr = db_conn.begin()
                    dbr.append("Realizamos COMMIT intermedio")

            #Provocamos fallo, borramos antes de la tabla costumers
            sql = sqlalchemy.text(query3)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Costumers")

            sql = sqlalchemy.text(query2)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Orders")

        else:
            sql = sqlalchemy.text(query1)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Orderdetail")
            
            time.sleep(duerme)
            
            sql = sqlalchemy.text(query2)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Orders")

            sql = sqlalchemy.text(query3)
            db_conn.execute(sql)
            dbr.append("Borramos datos del cliente de Costumers")


    except Exception as e:
        
        dbr.append("Se ha producido algun error al borrar el cliente")

        if bSQL:
            command = "ROLLBACK;"
            sql = sqlalchemy.text(command)
            db_conn.execute(sql)

            dbr.append("Realizamos ROLLBACK")
        
        else:
            tr.rollback()
            dbr.append("Realizamos ROLLBACK")

    else:
        # TODO: confirmar cambios si todo va bien
        dbr.append("Borrado completado con exito")

        if bSQL:
            command = "COMMIT;"
            sql = sqlalchemy.text(command)
            db_conn.execute(sql)

            dbr.append("COMMIT realizado")

        else:
            tr.commit()
            dbr.append("COMMIT realizado")

    return dbr

