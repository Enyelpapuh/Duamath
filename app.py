import os
import helpers

from cs50 import SQL
from flask import Flask, flash,redirect, abort,url_for, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///duomath.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def layout():
    return render_template("inicio_p.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect(request.url)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect(request.url)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return redirect(request.url)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/inicio")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")
        if not username:
            flash("Username is required!")
            return redirect(request.url)  # Redirige al formulario de registro actual
        elif not password:
            flash("Password is required!")
            return redirect(request.url)
        elif not confirmation:
            flash("Password confirmation is required!")
            return redirect(request.url)
    
        password_lend = len(password)
        if password_lend < 4:
            flash("La contraseña es muy corta!")
            return redirect(request.url)
        if password != confirmation:
            flash("Las contraseñas no coinciden!")
            return redirect(request.url)
        hash = generate_password_hash(password)
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)", username, hash
            )
            flash("User registered successfully!")
            return redirect("/login")
        except:
            flash("El usuario ya ha sido registrado!")
            return redirect(request.url)
    else:
        return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/inicio")
@login_required
def inicio():
        user_id = session['user_id']
        dbprogress= db.execute("SELECT username FROM users WHERE id = :user_id", user_id=user_id)

        username = dbprogress[0]['username'] if dbprogress else 0
        return render_template('inicio.html', username=username)

@app.route("/clase")
@login_required
def clase_p():
    return render_template("clase.html")

@app.route("/clase_p")
def clase():
    return render_template("clase_p.html")

@app.route("/mapa")
def progreso_L():
    return render_template("mapa_p.html")

@app.route("/progreso")
@login_required
def progreso():
        user_id = session['user_id']
        dbprogress= db.execute("SELECT progreso FROM users WHERE id = :user_id", user_id=user_id)

        progreso = dbprogress[0]['progreso'] if dbprogress else 0
        return render_template('mapa.html', progreso=progreso)


@app.route("/actualizando", methods=["GET"])
@login_required
def actualizar_progreso():
    nivel = request.args.get('nivel')  # Obtener el valor del nivel desde la solicitud

    if nivel is not None:
        try:
            nivel = int(nivel)  # Intenta convertir a entero
        except ValueError:
            # Maneja el error si el valor no es convertible a entero
            abort(400)  # Devuelve un error 400 - Bad Request

        user_id = session['user_id']
        dbprogress = db.execute("SELECT progreso FROM users WHERE id = :user_id", user_id=user_id)
        progreso_actual = dbprogress[0]['progreso'] if dbprogress else 0

        if nivel >= progreso_actual:
            db.execute("UPDATE users SET progreso = :nivel WHERE id = :user_id", nivel=nivel, user_id=user_id)
            return redirect(url_for('progreso'))

    # Redireccionar a la página de progreso por defecto
    return redirect(url_for('progreso'))

@app.route('/mundo_1')
def mostrar_seccion1():
   return render_template('Mundo_1.html')

@app.route('/mundo_2')
def mostrar_seccion2():
   return render_template('Mundo_2.html')

@app.route('/mundo_3')
def mostrar_seccion3():
   return render_template('Mundo_3.html')

@app.route('/mundo4')
def mostrar_seccion4():
   return render_template('Mundo_4.html')

@app.route('/nivel_1')
def nivel1():
    return render_template('nivel_1.html')

@app.route('/nivel_2')
def nivel2():
    return render_template('nivel_2.html')

@app.route('/nivel_3')
def nivel3():
    return render_template('nivel_3.html')

@app.route('/nivel_4')
def nivel4():
    return render_template('nivel_4.html')

@app.route('/nivel_5')
def nivel5():
    return render_template('nivel_5.html')

@app.route('/nivel_6')
def nivel6():
    return render_template('nivel_6.html')

@app.route('/nivel_7')
def nivel7():
    return render_template('nivel_7.html')

@app.route('/nivel_8')
def nivel8():
    return render_template('nivel_8.html')
@app.route('/nivel_9')
def nivel9():
    return render_template('nivel_9.html')
#-----------------------------------------------------#
@app.route('/nivel1_p')
def nivel1_publico():
    return render_template('nivel_1_publico.html')

@app.route('/nivel2_p')
def nivel2_publico():
    return render_template('nivel_2_publico.html')

@app.route('/nivel3_p')
def nivel3_publico():
    return render_template('nivel_3_publico.html')

@app.route('/nivel4_p')
def nivel4_publico():
    return render_template('nivel_4_publico.html')

@app.route('/nivel5_p')
def nivel5_publico():
    return render_template('nivel_5_publico.html')

@app.route('/nivel6_p')
def nivel6_publico():
    return render_template('nivel_6_publico.html')

@app.route('/nivel7_p')
def nivel7_publico():
    return render_template('nivel_7_publico.html')

@app.route('/nivel8_p')
def nivel8_publico():
    return render_template('nivel_8_publico.html')

@app.route('/mundo1_p')
def mostrar_seccion1_publico():
   return render_template('Mundo_1_publico.html')

@app.route('/mundo2_p')
def mostrar_seccion2_publico():
   return render_template('Mundo_2._publico.html')

@app.route('/mundo3_p')
def mostrar_seccion3_publico():
   return render_template('Mundo_3_publico.html')

@app.route('/mundo4_p')
def mostrar_seccion4_publico():
   return render_template('Mundo_4_publico.html')
#------------------------------------------------#

@app.route('/vision')
def vision():
    return render_template('vision.html')
   
@app.route('/mision')
def mision():
    return render_template('mision.html')
   