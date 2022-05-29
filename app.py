from unicodedata import name
from flask import Flask, redirect, render_template, request, session, url_for
import mysql.connector
import base64
import controlador
from datetime import timedelta
from functools import wraps


conn = mysql.connector.connect(host="localhost", port="3306", user="root", password=":)", database="")
cursor= conn.cursor()

app = Flask(__name__)
app.secret_key="secret key"


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username_admin' in session:
            return f(*args, **kwargs)
        else:
            return render_template('access-denied.html')
    return wrap


def capturist_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username_capturist' in session:
            return f(*args, **kwargs)
        else:
            return render_template('access-denied.html')
    return wrap


def guest_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username_guest' in session:
            return f(*args, **kwargs)
        else:
            return render_template('access-denied.html')
    return wrap

@app.route('/')
@app.route('/inicio')
def index():
    return render_template("inicio.html")


@app.route('/adminhome')
@admin_required
def home():
    return render_template('admin_home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT user, password, idprivilegios from usuario where user=%s and password=%s and idprivilegios=1', (username,password))
        record = cursor.fetchone()
        if record:
            session['username_admin'] = username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect(url_for('home'))
        else:
            msg="Incorrect"

    return render_template('login.html', msg=msg)


@app.route('/loginCapturista')
def loginCapturista():
    return render_template('login_capturista.html')


@app.route('/capturista')
@capturist_required
def capturista():
    return render_template('capturista_home.html')

@app.route('/loginC', methods=['GET','POST'])
def loginC():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT user, password, idprivilegios from usuario where user=%s and password=%s and idprivilegios=2', (username,password))        
        record = cursor.fetchone()
        if record:
            session['username_capturist'] = username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect(url_for('capturista'))
        else:
            msg="Incorrect"

    return render_template('login_capturista.html', msg=msg)

@app.route('/loginvisitante')
def loginvisitante():
    return render_template('login_visitante.html')


@app.route('/visitante')
@guest_required
def visitante():
    return render_template('visitante.html')

@app.route('/loginV', methods=['GET','POST'])
def loginV():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor.execute('SELECT user, password, idprivilegios from usuario where user=%s and password=%s and idprivilegios=3', (username,password))        
        record = cursor.fetchone()
        if record:
            session['username_guest'] = username
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=120)
            return redirect(url_for('visitante'))
        else:
            msg="Incorrect"

    return render_template('login_visitante.html', msg=msg)


@app.route('/reportesV')
@guest_required
def reportesV():
    reportes = controlador.obtener_reporte()
    return render_template('reportes_visitante.html', reportes=reportes)


@app.route('/formularioCapturista')
@capturist_required
def formularioCapturista():
    return render_template('formularioCapturista.html')


@app.route('/formularioAdministrador')
@admin_required
def formularioAdministrador():
    return render_template('formularioAdministrador.html')


@app.route('/reportesA')
@admin_required
def reportesA():
    reportes = controlador.obtener_reporte()
    return render_template('reportes_administrador.html', reportes=reportes)

@app.route('/captura', methods=['POST'])
def captura():
    if request.method == 'POST':
        if not request.files.get('cartadepoder'):
            file = request.files['solicitud']
            file1 =request.files['acreditacion']
            file2 =request.files['actaconstitutiva']
            file3 =request.files['identificacion']
            file4 =request.files['ubicacion']
            file5 =request.files['plano']
            blob = base64.b64encode(file.read())
            blob1 = base64.b64encode(file1.read())
            blob2 = base64.b64encode(file2.read())
            blob3 = base64.b64encode(file3.read())
            blob4 = base64.b64encode(file4.read())
            blob5 = base64.b64encode(file5.read())
            id = request.form['id']
            descripcion = request.form['descripcion']
            query='INSERT INTO `1.solicitud` (`idsolicitud`,`solicitud`) VALUES (%s,%s)'
            query1='INSERT INTO `2.acreditacion` (`document`,`idtipo_titulo`) VALUES (%s,%s)'
            query2='INSERT INTO `3.acta_constitutiva` (`acta`,`idaplicable`) VALUES (%s,%s)'
            query3='INSERT INTO `4.identificacion` (`identificacion_pdf`,`idtipo_de_identificacion`) VALUES (%s,%s)'
            query4='INSERT INTO `5.ubicacion` (`ubicacion_pdf`,`link_ubi`) VALUES (%s,%s)'
            query5='INSERT INTO `6.plano` (`plano_pdf`,`descripcion`) VALUES (%s,%s)'
            query6='INSERT INTO `7.carta_poder` (`cartapoder_pdf`,`id_aplicable`) VALUES (%s,%s)'
            if blob:
                value = None
                cursor.execute(query,(id,blob,))
                cursor.execute(query1,(blob1,3,))
                cursor.execute(query2,(blob2,1,))
                cursor.execute(query3,(blob3,1,))
                cursor.execute(query4,(blob4,"Base de datos",))
                cursor.execute(query5,(blob5,descripcion,))
                cursor.execute(query6,(value,1,))
                conn.commit()
            return redirect(url_for('home'))
        else:
            file = request.files['solicitud']
            file1 =request.files['acreditacion']
            file2 =request.files['actaconstitutiva']
            file3 =request.files['identificacion']
            file4 =request.files['ubicacion']
            file5 =request.files['plano']
            file6 =request.files['cartadepoder']
            blob = base64.b64encode(file.read())
            blob1 = base64.b64encode(file1.read())
            blob2 = base64.b64encode(file2.read())
            blob3 = base64.b64encode(file3.read())
            blob4 = base64.b64encode(file4.read())
            blob5 = base64.b64encode(file5.read())
            blob6 = base64.b64encode(file6.read())
            id = request.form['id']
            descripcion = request.form['descripcion']
            query='INSERT INTO `1.solicitud` (`idsolicitud`,`solicitud`) VALUES (%s,%s)'
            query1='INSERT INTO `2.acreditacion` (`document`,`idtipo_titulo`) VALUES (%s,%s)'
            query2='INSERT INTO `3.acta_constitutiva` (`acta`,`idaplicable`) VALUES (%s,%s)'
            query3='INSERT INTO `4.identificacion` (`identificacion_pdf`,`idtipo_de_identificacion`) VALUES (%s,%s)'
            query4='INSERT INTO `5.ubicacion` (`ubicacion_pdf`,`link_ubi`) VALUES (%s,%s)'
            query5='INSERT INTO `6.plano` (`plano_pdf`,`descripcion`) VALUES (%s,%s)'
            query6='INSERT INTO `7.carta_poder` (`cartapoder_pdf`,`id_aplicable`) VALUES (%s,%s)'
            if blob:
                cursor.execute(query,(id,blob,))
                cursor.execute(query1,(blob1,3,))
                cursor.execute(query2,(blob2,1,))
                cursor.execute(query3,(blob3,1,))
                cursor.execute(query4,(blob4,"Base de datos",))
                cursor.execute(query5,(blob5,descripcion,))
                cursor.execute(query6,(blob6,1,))
                conn.commit()
                return redirect(url_for('home'))
            else:
                return '<h1> Fallo </h1>'


@app.route('/capturaA', methods=['POST'])
def capturaA():
    if request.method == 'POST':
        if not request.files.get('cartadepoder'):
            file = request.files['solicitud']
            file1 =request.files['acreditacion']
            file2 =request.files['actaconstitutiva']
            file3 =request.files['identificacion']
            file4 =request.files['ubicacion']
            file5 =request.files['plano']
            blob = base64.b64encode(file.read())
            blob1 = base64.b64encode(file1.read())
            blob2 = base64.b64encode(file2.read())
            blob3 = base64.b64encode(file3.read())
            blob4 = base64.b64encode(file4.read())
            blob5 = base64.b64encode(file5.read())
            id = request.form['id']
            descripcion = request.form['descripcion']
            query='INSERT INTO `1.solicitud` (`idsolicitud`,`solicitud`) VALUES (%s,%s)'
            query1='INSERT INTO `2.acreditacion` (`document`,`idtipo_titulo`) VALUES (%s,%s)'
            query2='INSERT INTO `3.acta_constitutiva` (`acta`,`idaplicable`) VALUES (%s,%s)'
            query3='INSERT INTO `4.identificacion` (`identificacion_pdf`,`idtipo_de_identificacion`) VALUES (%s,%s)'
            query4='INSERT INTO `5.ubicacion` (`ubicacion_pdf`,`link_ubi`) VALUES (%s,%s)'
            query5='INSERT INTO `6.plano` (`plano_pdf`,`descripcion`) VALUES (%s,%s)'
            query6='INSERT INTO `7.carta_poder` (`cartapoder_pdf`,`id_aplicable`) VALUES (%s,%s)'
            if blob:
                value = None
                cursor.execute(query,(id,blob,))
                cursor.execute(query1,(blob1,3,))
                cursor.execute(query2,(blob2,1,))
                cursor.execute(query3,(blob3,1,))
                cursor.execute(query4,(blob4,"Base de datos",))
                cursor.execute(query5,(blob5,descripcion,))
                cursor.execute(query6,(value,1,))
                conn.commit()
            return redirect(url_for('capturista'))
        else:
            file = request.files['solicitud']
            file1 =request.files['acreditacion']
            file2 =request.files['actaconstitutiva']
            file3 =request.files['identificacion']
            file4 =request.files['ubicacion']
            file5 =request.files['plano']
            file6 =request.files['cartadepoder']
            blob = base64.b64encode(file.read())
            blob1 = base64.b64encode(file1.read())
            blob2 = base64.b64encode(file2.read())
            blob3 = base64.b64encode(file3.read())
            blob4 = base64.b64encode(file4.read())
            blob5 = base64.b64encode(file5.read())
            blob6 = base64.b64encode(file6.read())
            id = request.form['id']
            descripcion = request.form['descripcion']
            query='INSERT INTO `1.solicitud` (`idsolicitud`,`solicitud`) VALUES (%s,%s)'
            query1='INSERT INTO `2.acreditacion` (`document`,`idtipo_titulo`) VALUES (%s,%s)'
            query2='INSERT INTO `3.acta_constitutiva` (`acta`,`idaplicable`) VALUES (%s,%s)'
            query3='INSERT INTO `4.identificacion` (`identificacion_pdf`,`idtipo_de_identificacion`) VALUES (%s,%s)'
            query4='INSERT INTO `5.ubicacion` (`ubicacion_pdf`,`link_ubi`) VALUES (%s,%s)'
            query5='INSERT INTO `6.plano` (`plano_pdf`,`descripcion`) VALUES (%s,%s)'
            query6='INSERT INTO `7.carta_poder` (`cartapoder_pdf`,`id_aplicable`) VALUES (%s,%s)'
            if blob:
                cursor.execute(query,(id,blob,))
                cursor.execute(query1,(blob1,3,))
                cursor.execute(query2,(blob2,1,))
                cursor.execute(query3,(blob3,1,))
                cursor.execute(query4,(blob4,"Base de datos",))
                cursor.execute(query5,(blob5,descripcion,))
                cursor.execute(query6,(blob6,1,))
                conn.commit()
                return redirect(url_for('capturista'))
            else:
                return '<h1> Fallo </h1>'

@app.route('/reportes')
def reportes():
    reportes = controlador.obtener_reporte()
    return render_template('reportes.html', reportes=reportes)

@app.route('/editar')
def editar_reporte():
    reportes = controlador.obtener_reporte()
    return render_template('editar_reporte.html', reportes=reportes)

@app.route('/edit_reporte/<int:id>')
def edit_reporte(id):
    reportes = controlador.getting_report(id)
    return render_template('editing_report.html', reportes=reportes)

@app.route('/eliminar')
def eliminar():
    reportes = controlador.obtener_reporte()
    return render_template('eliminarreporte.html', reportes=reportes)

@app.route("/eliminar_reporte", methods=["POST"])
def eliminar_reporte():
    controlador.eliminar_reporte(request.form["id"])
    return redirect("/eliminar")


@app.route("/cerrar-sesion-capturista")
def logout_capturist():
    session.pop('username_capturist',None)
    session.permanent = False
    return redirect('/inicio')

@app.route("/cerrar-sesion-admin")
def logout_admin():
    session.pop('username_admin',None)
    session.permanent = False
    return redirect('/inicio')

@app.route("/cerrar-sesion-visitante")
def logout_guest():
    session.pop('username_guest',None)
    session.permanent = False
    return redirect('/inicio')
    

#Handling Errors

@app.errorhandler(400)
def handle_bad_request(e):
    return render_template('eerror-400.html'), 400

@app.errorhandler(403)
def handle_bad_request(e):
    return render_template('error-403.html'), 403

@app.errorhandler(404)
def not_found(self):
    return render_template('error-404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error-500.html'), 500

@app.errorhandler(405)
def method_not_found(error):
    return render_template('error-405.html'), 405



if __name__ == "__main__":
    app.run(debug=True) 
