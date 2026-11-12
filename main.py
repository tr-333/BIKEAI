
from flask import Flask, render_template, session, send_file
from auth.auth import register, login, logout, login_required
from user.user_profile import profile_user
from admin.admin_profile import profile_admin
from user.user_database import get_user_profile
from user.user_bike import bike_user
from admin.admin_bike import bike_admin
from user.user_ride import ride_user
from admin.admin_ride import rides_admin
from admin.admin_analysis import admin_analysis, bike_types_chart
from user.user_analysis import user_analysis
from analysis.analysis_ride import (rides_by_month_chart, rides_distribution_chart, ride_conditions_chart)
from ride_gpx import generate_gpx_map
from user.user_message import message_user
from admin.admin_message import message_admin
from user.user_message_database import get_user_unread_messages_count
from admin.admin_message_database import get_admin_unread_messages_count
from auth.account_access import register_account_access
import os


app = Flask(__name__)

app.secret_key = os.environ.get("BIKE_KEY")

if not app.secret_key:

    raise RuntimeError("BIKE_KEY not set")

register_account_access(app)

#licznik wiadmości
@app.context_processor
def inject_unread_messages_count():

    if "user_id" not in session:

        return {"unread_messages_count": 0}

    if session["role"] == "admin":

        count = get_admin_unread_messages_count()
    else:
        count = get_user_unread_messages_count(session["user_id"])

    return {"unread_messages_count": count}

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register_route():

    return register()

@app.route("/login", methods=["GET", "POST"])
def login_route():

    return login()

@app.route("/Menu")
def menu_bar():

    check = login_required()

    if check:

        return check

    return render_template("menu_bar.html")

@app.route("/wiadomości", methods=["GET", "POST"])
def message():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return message_admin()

    return message_user()

@app.route("/profil", methods=["GET", "POST"])
def profil():

    check = login_required()

    if check:

        return check

    user = get_user_profile(session["user_id"])

    if session["role"] == "admin":

        return profile_admin(user)

    return profile_user()

@app.route("/rower", methods=["GET", "POST"])
@app.route("/rower/<int:bike_id>", methods=["GET", "POST"])
def bike_route(bike_id=None):

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return bike_admin()

    return bike_user(bike_id)

@app.route("/gpx_map/<filename>")
def gpx_map(filename):

    gpx_filename = os.path.splitext(filename)[0] + ".gpx"

    image = generate_gpx_map(gpx_filename)

    return send_file(image, mimetype="image/png")

@app.route("/przejazdy", methods=["GET", "POST"])
def ride_route():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return rides_admin()

    return ride_user()

@app.route("/analiza", methods=["GET", "POST"])
def analysis_route():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return admin_analysis()

    return user_analysis()

# Wykres typów rowerów
@app.route("/wykres-typy-rowerow")
def bike_types_chart_route():

    check = login_required()

    if check:

        return check

    if session["role"] != "admin":

        return "Brak dostępu", 403

    return bike_types_chart()

# Liczba przejazdów w poszczególnych miesiącach
@app.route("/wykres-przejazdow-miesiecznie")
def rides_by_month_chart_route():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return rides_by_month_chart()

    return rides_by_month_chart(user_id=session["user_id"])

# Rozkład parametrów przejazdów
@app.route("/wykresy-przejazdow-rozklad")
def rides_distribution_chart_route():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return rides_distribution_chart()

    return rides_distribution_chart(user_id=session["user_id"])

# Warunki pogodowe i rodzaj nawierzchni
@app.route("/wykres-warunki-przejazdow")
def ride_conditions_chart_route():

    check = login_required()

    if check:

        return check

    if session["role"] == "admin":

        return ride_conditions_chart()

    return ride_conditions_chart(user_id=session["user_id"])

@app.route("/logout")
def logout_route():

    return logout()

if __name__ == "__main__":
    app.run(debug=True)