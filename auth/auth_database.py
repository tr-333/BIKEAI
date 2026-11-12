from database import get_connection
from werkzeug.security import generate_password_hash

#funkcja sprawdzająca email czy już istenieje w bazie
def email_exists(email):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user is not None

#funkcja sprawdzająca nazwę użytkownika czy już istnieje w bazie
def username_exists(username):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user is not None

#funkcja tworząca użykownika do bazy
def create_user(username, email, password):

    password_hash = generate_password_hash(password)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)""", (username, email, password_hash))

    connection.commit()
    cursor.close()
    connection.close()

#funkcja sprawdzające dane logowania
def login_user(login):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s OR username = %s", (login, login))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user