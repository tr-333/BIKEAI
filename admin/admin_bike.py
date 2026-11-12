from flask import render_template, request, session

from .admin_bike_database import (get_users_bike_limits, update_bike_limit)

from message_system import send_bike_limit_changed_message


#funkcja akcji z formularzu rower
def bike_admin():

    if request.method == "POST":

        action = request.form.get("action")

        # filtr użytkowników
        if action == "filter_users":

            clear_filter = request.form.get("clear_filter")


            if clear_filter:

                username_filter = ""

            else:

                username_filter = request.form.get("username_filter", "").strip()

            users = get_users_bike_limits(username_filter)

            return render_template("bike-admin.html", users=users, username_filter=username_filter)


        if action == "edit_limit":

            edit_limit_user_id = request.form.get("user_id")

            users = get_users_bike_limits()

            return render_template("bike-admin.html", users=users,
                                   edit_limit_user_id=int(edit_limit_user_id))


        if action == "cancel_edit_limit":

            users = get_users_bike_limits()

            return render_template("bike-admin.html", users=users)


        if action == "save_limit":

            user_id = request.form.get("user_id")

            bike_limit = request.form.get("bike_limit")

            update_bike_limit(user_id, bike_limit)

            # Wysyłamy automatyczną wiadomość do użytkownika.
            send_bike_limit_changed_message(user_id=int(user_id), new_limit=int(bike_limit),
                                            admin_id=session['user_id'])

            users = get_users_bike_limits()

            return render_template("bike-admin.html", users=users)

    users = get_users_bike_limits()

    return render_template("bike-admin.html", users=users)