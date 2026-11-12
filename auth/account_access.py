from flask import session, request, redirect, url_for
from database import get_connection


# sprawdza, czy konto użytkownika jest zablokowane
def is_user_blocked():

    if "user_id" not in session:

        return False

    if session.get("role") == "admin":

        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("SELECT blocked FROM users WHERE id = %s", (session["user_id"],))

        result = cursor.fetchone()

        if result is None:

            return True

        return result[0] == "zablokowany"

    finally:

        cursor.close()
        connection.close()


# blokuje dostępu do stron
def register_account_access(app):

    @app.before_request
    def restrict_blocked_users():

        if "user_id" not in session:

            return None

        if session.get("role") == "admin":

            return None

        allowed_endpoints = {"menu_bar", "profil", "message", "logout_route", "static"}

        if request.endpoint in allowed_endpoints:

            return None

        if is_user_blocked():

            return redirect(url_for("menu_bar"))

        return None

    # status konta dla szablonów html
    @app.context_processor
    def inject_account_status():

        return {"is_account_blocked": is_user_blocked()}