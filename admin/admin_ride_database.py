from database import get_connection

# Pobranie listy użytkowników
def get_users_ride_statistics(username_filter=""):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT users.id, users.username, COUNT(rides.id) AS ride_count,
    COALESCE(SUM(rides.distance), 0) AS total_distance FROM users LEFT JOIN rides ON users.id = rides.user_id
    WHERE users.role != 'admin'"""

    values = []

    if username_filter:

        query += """AND users.username LIKE %s"""

        values.append(f"%{username_filter}%")

    query += """GROUP BY users.id, users.username ORDER BY users.id"""

    cursor.execute(query, values)

    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return users

# Pobranie wybranego użytkownika
def get_selected_user(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT id, username FROM users WHERE id = %s AND role != 'admin'""", (user_id,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user

# Pobranie rowerów użytkownika
def get_user_bikes_for_admin(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT id, brand, model FROM bikes WHERE user_id = %s ORDER BY id DESC""", (user_id,))

    bikes = cursor.fetchall()
    cursor.close()
    connection.close()

    return bikes

# Pobranie przejazdów użytkownika
def get_user_rides_for_admin(user_id, bike_filter="", date_from="", date_to="", ride_name_filter=""):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT rides.id, rides.ride_name, rides.ride_date, rides.distance, bikes.brand, bikes.model 
    FROM rides LEFT JOIN bikes ON rides.bike_id = bikes.id WHERE rides.user_id = %s"""

    values = [user_id]

    if bike_filter:

        query += """AND rides.bike_id = %s"""

        values.append(bike_filter)

    if date_from:

        query += """AND rides.ride_date >= %s"""

        values.append(date_from)

    if date_to:

        query += """AND rides.ride_date <= %s"""

        values.append(date_to)

    if ride_name_filter:

        query += """AND rides.ride_name LIKE %s"""

        values.append(f"%{ride_name_filter}%")

    query += """ORDER BY rides.ride_date DESC, rides.id DESC"""

    cursor.execute(query, values)

    rides = cursor.fetchall()
    cursor.close()
    connection.close()

    return rides

# Usunięcie przejazdu przez admina
def delete_admin_ride(user_id, ride_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM rides WHERE id = %s AND user_id = %s""", (ride_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()