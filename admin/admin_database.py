
from database import get_connection

# Funkcja pobiera wszystkich użytkowników
def get_all_users():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, username, email, email_verified, created_at, role, blocked FROM users ORDER BY id""")

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

# Filtruje użytkowników
def get_filtered_users(username_filter="", email_filter="", role_filter="", created_from="",
                       created_to=""):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT id, username, email, email_verified, created_at, role, blocked FROM users WHERE 1=1"""

    values = []


    if username_filter:

        query += " AND username LIKE %s"\

        values.append(f"%{username_filter}%")


    if email_filter:

        query += " AND email LIKE %s"

        values.append(f"%{email_filter}%")


    if role_filter in ["user", "admin"]:

        query += " AND role = %s"

        values.append(role_filter)


    if created_from:

        query += " AND DATE(created_at) >= %s"

        values.append(created_from)


    if created_to:

        query += " AND DATE(created_at) <= %s"

        values.append(created_to)


    query += " ORDER BY id"

    cursor.execute(query, values)

    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users

# Aktualizuje rolę użytkownika
def update_user_role(user_id, role):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""UPDATE users SET role = %s WHERE id = %s""", (role, user_id))

    connection.commit()
    cursor.close()
    connection.close()

# Blokuje lub odblokowuje konto użytkownika
def toggle_user_block(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Pobieramy aktualny status i blokujemy rekord
        cursor.execute("""SELECT blocked FROM users WHERE id = %s AND role != 'admin' FOR UPDATE""", (user_id,))

        user = cursor.fetchone()

        if user is None:

            connection.rollback()

            return None

        # Ustalamy nowy status konta.
        if user[0] == "zablokowany":

            new_status = "aktywny"

        else:

            new_status = "zablokowany"

        cursor.execute("""UPDATE users SET blocked = %s WHERE id = %s AND role != 'admin' """, (new_status, user_id))

        if cursor.rowcount != 1:

            connection.rollback()

            return None

        connection.commit()

        # Zwracamy nowy status dopiero po zatwierdzeniu zmiany.
        return new_status

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

# Usuwa użytkownika
def delete_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM rides WHERE user_id = %s", (user_id,))

    cursor.execute("DELETE FROM bikes WHERE user_id = %s", (user_id,))

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

    connection.commit()
    cursor.close()
    connection.close()
