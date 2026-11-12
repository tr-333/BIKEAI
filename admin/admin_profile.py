
from flask import render_template, request, session
from .admin_database import (get_all_users, get_filtered_users, update_user_role, delete_user, toggle_user_block)
from user.user_profile import profile_user
from message_system import send_account_blocked_message

#funkcja akcji profilu admina
def profile_admin(user):

    action = request.form.get("action")

    allowed_actions = ["users", "edit", "cancel_edit", "delete_user", "confirm_delete", "cancel_delete", "save_role",
                      "toggle_block"]

    if request.method == "GET":

        return profile_user()


    if action is None:

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)


    if action not in allowed_actions:

        return profile_user()


    if action == "users":

        clear_filters = request.form.get("clear_filters")

        if clear_filters:

            username_filter = ""
            email_filter = ""
            role_filter = ""
            created_from = ""
            created_to = ""

        else:

            username_filter = request.form.get("username_filter", "").strip()

            email_filter = request.form.get("email_filter", "").strip()

            role_filter = request.form.get("role_filter", "").strip()

            created_from = request.form.get("created_from", "").strip()

            created_to = request.form.get("created_to", "").strip()

        users = get_filtered_users(username_filter, email_filter, role_filter, created_from, created_to)

        return render_template("profil.html", user=user, users=users, show_users=True,
                               username_filter=username_filter, email_filter=email_filter, role_filter=role_filter,
                               created_from=created_from, created_to=created_to)


    if action == "edit":

        edit_user_id = request.form.get("user_id")

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True,
                               edit_user_id=int(edit_user_id))


    if action == "cancel_edit":

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)


    if action == "delete_user":

        delete_user_id = request.form.get("user_id")

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True,
                               delete_user_id=int(delete_user_id))


    if action == "confirm_delete":

        delete_user_id = request.form.get("user_id")

        delete_user(delete_user_id)

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)


    if action == "cancel_delete":

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)


    if action == "save_role":

        user_id_to_edit = request.form.get("user_id")

        new_role = request.form.get("role")

        if new_role not in ["user", "admin"]:

            users = get_all_users()

            return render_template("profil.html", user=user, users=users, show_users=True,
                                   error="Nieprawidłowa rola.")

        update_user_role(user_id_to_edit, new_role)

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)


    if action == "toggle_block":

        target_user_id = request.form.get("user_id")

        try:

            target_user_id = int(target_user_id)

        except (TypeError, ValueError):

            users = get_all_users()

            return render_template("profil.html", user=user, users=users, show_users=True,
                                   error="Nieprawidłowe konto użytkownika.")

        users = get_all_users()

        target_user = next((listed_user for listed_user in users if int(listed_user["id"]) == target_user_id), None)

        if target_user is None:

            return render_template("profil.html", user=user, users=users, show_users=True,
                                   error="Nie znaleziono użytkownika.")

        current_user_id = session.get("user_id")

        is_admin = target_user["role"] == "admin"

        is_self = (current_user_id is not None and target_user_id == int(current_user_id))


        if is_admin or is_self:

            return render_template("profil.html", user=user, users=users, show_users=True,
                                   error="Nie można zablokować konta administratora.")

        new_status = toggle_user_block(target_user_id)


        # Wiadomość wysyłamy wyłącznie po skutecznym zablokowaniu.
        if new_status == "zablokowany":

            send_account_blocked_message(user_id=target_user_id, admin_id=session["user_id"])

        users = get_all_users()

        return render_template("profil.html", user=user, users=users, show_users=True)

    return render_template("profil.html", user=user)