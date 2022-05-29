from bd import obtener_conexion

def obtener_reporte():
    conexion = obtener_conexion()
    solicitud = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM `expediente`")
        solicitud = cursor.fetchall()
    conexion.close()
    return solicitud

def getting_report(id):
    connection = obtener_conexion()
    request = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `expediente` WHERE idExpediente = %s;", (id,))
        request = cursor.fetchall()
    connection.close()
    return request

def eliminar_reporte(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM `expediente` WHERE idExpediente = %s", (id,))
    conexion.commit()
    conexion.close()



