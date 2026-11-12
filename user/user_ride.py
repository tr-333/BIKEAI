from flask import render_template, request, session, redirect, url_for
import json
import os
import uuid
from werkzeug.utils import secure_filename
from .user_ride_database import (save_rides, get_user_rides, delete_ride)
from .user_bike_database import get_user_bikes


# funkcja akcji przejazdow użytkownika
def ride_user():

    user_id = session["user_id"]

    # Ustawienia widoku
    show_form = False

    show_history = False

    if request.args.get("add"):

        show_form = True

    if request.args.get("history"):

        show_history = True

    # Pobranie rowerów
    bikes = get_user_bikes(user_id)

    # Filtry
    ride_name_filter = request.args.get("ride_name_filter", "").strip()

    distance_from = request.args.get("distance_from", "").strip()

    distance_to = request.args.get("distance_to", "").strip()

    # Pobieranie przejazdów
    rides = get_user_rides(user_id, ride_name_filter, distance_from, distance_to)

    # Formularz
    if request.method == "POST":

        action = request.form["action"]

        # Zapis nowego przejazdu
        if action == "save":

            day = request.form.get("day", "")

            month = request.form.get("month", "")

            year = request.form.get("year", "")

            ride_date = f"{year}-{month}-{day}"

            # Plik z gpx
            gpx_file = request.files.get("gpx_file")

            gpx_filename = None

            if gpx_file and gpx_file.filename:

                original_filename = secure_filename(gpx_file.filename)

                extension = os.path.splitext(original_filename)[1]

                gpx_filename = (f"ride_{uuid.uuid4().hex}", f"{extension}")

            # Dane przejazdu
            ride_data = {

                "bike_id": request.form.get("bike_id"),

                "ride_name": request.form.get("ride_name"),

                "ride_date": ride_date,

                "start_time": request.form.get("start_time"),

                "full_time": request.form.get("full_time"),

                "distance": request.form.get("distance"),

                "elevation": request.form.get("elevation"),

                "avg_speed": request.form.get("avg_speed"),

                "max_speed": request.form.get("max_speed"),

                "temperature": request.form.get("temperature"),

                "humidity": request.form.get("humidity"),

                "wind": request.form.get("wind"),

                "weather": json.dumps(request.form.getlist("weather")),

                "surface": json.dumps(request.form.getlist("surface")),

                "notes": request.form.get("notes"),

                "gpx_file": gpx_filename}

            # Pola wymagane
            required_fields = ["bike_id", "ride_name", "ride_date", "start_time", "full_time", "distance", "elevation",
                               "avg_speed", "max_speed"]

            # Sprawdzenie brakujących pól
            missing_fields = [field for field in required_fields if not ride_data.get(field)]

            if missing_fields:

                return render_template("ride.html", error="Uzupełnij wszystkie wymagane pola.",
                                       show_form=True, show_history=False, bikes=bikes, rides=rides)

            # Zapis gpx
            if gpx_file and gpx_file.filename:

                gpx_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gpx", gpx_filename)

                gpx_file.save(gpx_path)

            # Zapis do bazy
            save_rides(user_id, ride_data)

            return render_template("ride.html", success="Dane zapisano!", show_form=True,
                                   show_history=False, bikes=bikes, rides=rides)

        # Rozpoczęcie usuwania przejazdu
        if action == "delete":

            ride_id = request.form.get("ride_id")

            return render_template("ride.html", show_form=False, show_history=True, bikes=bikes,
                                   rides=rides, confirm_delete=True, delete_ride_id=ride_id)


        # Potwierdzenie usunięcia
        if action == "confirm_delete":

            ride_id = request.form.get("ride_id")

            delete_ride(user_id, ride_id)

            return redirect(url_for("ride_route", history=1))

    # Wyświetlenie strony
    return render_template("ride.html", show_form=show_form, show_history=show_history,
                           bikes=bikes, rides=rides, ride_name_filter=ride_name_filter, distance_from=distance_from,
                           distance_to=distance_to)