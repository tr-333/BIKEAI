from flask import render_template, request, redirect, url_for, session
from .admin_ride_database import (get_users_ride_statistics, get_selected_user, get_user_bikes_for_admin,
                                  get_user_rides_for_admin, delete_admin_ride)

from message_system import send_ride_deleted_message

# funkcja akcji przejazdów admin
def rides_admin():

    # Formularz
    if request.method == "POST":

        action = request.form.get("action")

        # Filtr
        if action == "filter_users":

            clear_filter = request.form.get("clear_filter")

            if clear_filter:

                username_filter = ""

            else:

                username_filter = request.form.get("username_filter", "").strip()

            users = get_users_ride_statistics(username_filter)

            return render_template("ride_admin.html", users=users, username_filter=username_filter,
                                   show_details=False)

        # Szczegóły użytkowników
        if action == "show_details":

            user_id = request.form.get("user_id")

            selected_user = get_selected_user(user_id)

            user_bikes = get_user_bikes_for_admin(user_id)

            rides = get_user_rides_for_admin(user_id)

            return render_template("ride_admin.html", show_details=True, selected_user=selected_user,
                                   user_bikes=user_bikes, rides=rides, bike_filter="", date_from="", date_to="",
                                   ride_name_filter="")

        # Filtry przejazdów
        if action == "filter_rides":

            user_id = request.form.get("user_id")

            clear_filter = request.form.get("clear_ride_filter")

            if clear_filter:

                bike_filter = ""
                date_from = ""
                date_to = ""
                ride_name_filter = ""

            else:

                bike_filter = request.form.get("bike_id", "")

                date_from = request.form.get("date_from", "")

                date_to = request.form.get("date_to", "")

                ride_name_filter = request.form.get("ride_name_filter", "").strip()

            selected_user = get_selected_user(user_id)

            user_bikes = get_user_bikes_for_admin(user_id)

            rides = get_user_rides_for_admin(user_id, bike_filter, date_from, date_to, ride_name_filter)

            return render_template("ride_admin.html", show_details=True, selected_user=selected_user,
                                   user_bikes=user_bikes, rides=rides, bike_filter=bike_filter, date_from=date_from,
                                   date_to=date_to, ride_name_filter=ride_name_filter)

        # Potwierdzenie usunięcia
        if action == "delete_admin_ride":

            ride_id = request.form.get("ride_id")

            user_id = request.form.get("user_id")

            selected_user = get_selected_user(user_id)

            user_bikes = get_user_bikes_for_admin(user_id)

            rides = get_user_rides_for_admin(user_id)

            return render_template("ride_admin.html", show_details=True, confirm_delete=True,
                                   selected_user=selected_user, user_bikes=user_bikes, rides=rides,
                                   delete_ride_id=ride_id, delete_user_id=user_id, bike_filter="", date_from="",
                                   date_to="", ride_name_filter="")

        # Usuwanie przejazdu
        if action == "confirm_delete_admin_ride":

            ride_id = request.form.get("ride_id")

            user_id = request.form.get("user_id")

            delete_admin_ride(user_id, ride_id)

            # Wysyłamy automatyczną wiadomość do użytkownika.
            send_ride_deleted_message(user_id=int(user_id), admin_id=session["user_id"])

            return redirect(url_for("ride_route"))

    # Domyślna lista użytkownika
    users = get_users_ride_statistics()

    return render_template("ride_admin.html", users=users, username_filter="", show_details=False)