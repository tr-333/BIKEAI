from database import get_connection
from werkzeug.security import generate_password_hash

#pobieramy dane użytkownika z bazy
def get_user_profile(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user

#sprawdzamy czy email sie nie powtarza
def email_exists_for_other_user(email, user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, user_id))

    existing_email = cursor.fetchone()
    cursor.close()
    connection.close()

    return existing_email is not None

#zapis zmienionych danych uzytkownika
def update_user_profile(user_id, email, password):

    updates = []
    values = []

    connection = get_connection()
    cursor = connection.cursor()

    if email:

        updates.append("email = %s")
        values.append(email)

    if password:

        password_hash = generate_password_hash(password)
        updates.append("password_hash = %s")
        values.append(password_hash)

    if updates:

        values.append(user_id)

        query = f"""UPDATE users SET {", ".join(updates)} WHERE id = %s"""

        cursor.execute(query, values)
        connection.commit()

    cursor.close()
    connection.close()

#usuwanie użytkownika z danymi
def delete_user_account(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM rides WHERE user_id = %s", (user_id,))

    cursor.execute("DELETE FROM bikes WHERE user_id = %s", (user_id,))

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))

    connection.commit()
    cursor.close()
    connection.close()