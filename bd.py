import pymysql


def obtener_conexion():
    return pymysql.connect(host='localhost',
                                user='root',
                                password='Password123*',
                                db='townhall2')