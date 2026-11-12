from database import get_connection

    #funkcja pobierająca limity użytkowników
def get_users_bike_limits(username_filter=""):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT users.id, users.username, users.bike_limit, COUNT(bikes.id) AS bike_count FROM users
    LEFT JOIN bikes ON users.id = bikes.user_id WHERE users.role != 'admin'"""

    values = []

    if username_filter:

        query += " AND users.username LIKE %s"
        values.append(f"%{username_filter}%")

    query += """GROUP BY users.id, users.username, users.bike_limit ORDER BY users.id"""

    cursor.execute(query, values)

    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users

    #funkcja edytująca limity użytkowników
def update_bike_limit(user_id, bike_limit):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""UPDATE users SET bike_limit = %s WHERE id = %s""", (bike_limit, user_id))

    connection.commit()
    cursor.close()
    connection.close()