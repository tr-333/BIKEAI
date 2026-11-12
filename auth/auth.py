from flask import render_template, request, session, redirect, url_for
from validation import validate_password
from .auth_database import email_exists, username_exists, create_user, login_user
from werkzeug.security import check_password_hash
from message_system import send_welcome_message

#funkcja rejestracji użytkownika
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]

        # sprawdzenie nazwy użytkownika
        if len(username) < 3:

            return render_template("register.html", error="nazwa musi mieć minimum 3 znaki!")

        # sprawdzenie hasła
        password_error = validate_password(password)

        if password_error:

            return render_template("register.html", error=password_error)

        # sprawdzenie, czy hasła są takie same
        if password != password_confirm:

            return render_template("register.html", error="Hasła nie są takie same!")

        # sprawdzenie, czy email już istnieje
        if email_exists(email):

            return render_template("register.html", error="Podany email już istnieje!")

        # sprawdzenie, czy nazwa użytkownika już istnieje
        if username_exists(username):

            return render_template("register.html", error="Podana nazwa użytkownika już istnieje!")

        # utworzenie użytkownika
        create_user(username, email, password)

        return render_template("register.html",
                               success=f"Rejestracja użytkownika {username} zakończona!")

    return render_template("register.html")

#funkcja logowania użytkownika
def login():

    if request.method == "POST":

        login_input = request.form["login"]
        password = request.form["password"]

        user = login_user(login_input)

        #brak użytkownika
        if user is None:

            return render_template("login.html", error = "Nieprawidłowy email lub hasło!")

        #sprawdzenie hasła
        if not check_password_hash(user["password_hash"], password):

            return render_template("login.html", error = "Nieprawidłowy email lub hasło!")

        #dane zgodne, logujemy
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        # wysłanie powitania tylko przy pierwszym poprawnym logowaniu.
        if user["role"] != "admin":

            send_welcome_message(user["id"])

        return redirect(url_for("menu_bar"))

    return render_template("login.html")

#funkcja wylogowania
def logout():

    session.clear()

    return redirect(url_for("home"))

#funkcja sprawdzająca logowanie
def login_required():

    if "user_id" not in session:

        return redirect(url_for("login_route"))

    return None
