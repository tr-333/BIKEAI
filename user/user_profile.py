from flask import render_template, request, session, redirect, url_for
from validation import validate_password
from .user_database import (get_user_profile, email_exists_for_other_user, update_user_profile, delete_user_account)

#funkcja akcji na profilu użytkownika
def profile_user():

    user_id = session["user_id"]

    user = get_user_profile(user_id)

    if request.method == "POST":

        action = request.form.get("action")


        if action == "delete_account":

            return render_template("profil.html", user=user, delete_account=True)


        if action == "cancel_delete_account":

            return render_template("profil.html", user=user)


        if action == "confirm_delete_account":

            delete_user_account(user_id)

            session.clear()

            return redirect(url_for("home"))

        email = request.form["email"].strip()
        password = request.form["password"].strip()


        if email != user["email"]:

            if email_exists_for_other_user(email, user_id):

                return render_template("profil.html", user=user, error="Podany email już istnieje!")

        if password:

            password_error = validate_password(password)

            if password_error:

                return render_template("profil.html", user=user, password_error=password_error)

        update_user_profile(user_id, email if email != user["email"] else None, password if password else None)

        user = get_user_profile(user_id)

        return render_template("profil.html", user=user, success="Dane zostały zmienione!")

    return render_template("profil.html", user=user)