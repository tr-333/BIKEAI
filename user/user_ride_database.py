from database import get_connection

# Zapis przejazdu
def save_rides(user_id, ride_data):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO rides (
            user_id,
            bike_id,
            ride_name,
            ride_date,
            start_time,
            full_time,
            distance,
            elevation,
            avg_speed,
            max_speed,
            temperature,
            humidity,
            wind,
            weather,
            surface,
            notes,
            gpx_file
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """,
        (
            user_id,
            ride_data["bike_id"],
            ride_data["ride_name"],
            ride_data["ride_date"],
            ride_data["start_time"],
            ride_data["full_time"],
            ride_data["distance"],
            ride_data["elevation"],
            ride_data["avg_speed"],
            ride_data["max_speed"],
            ride_data["temperature"],
            ride_data["humidity"],
            ride_data["wind"],
            ride_data["weather"],
            ride_data["surface"],
            ride_data["notes"],
            ride_data["gpx_file"]
        )
    )

    connection.commit()
    cursor.close()
    connection.close()


# Pobranie przejazdów użytkownika
def get_user_rides(user_id, ride_name_filter="", distance_from="", distance_to=""):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT rides.*, bikes.brand, bikes.model FROM rides JOIN bikes ON rides.bike_id = bikes.id 
    WHERE rides.user_id = %s"""

    values = [user_id]

    if ride_name_filter:

        query += " AND rides.ride_name LIKE %s"

        values.append(f"%{ride_name_filter}%")

    if distance_from:

        query += " AND rides.distance >= %s"

        values.append(distance_from)

    if distance_to:

        query += " AND rides.distance <= %s"

        values.append(distance_to)

    query += """ ORDER BY rides.ride_date DESC, rides.id DESC"""

    cursor.execute(query, values)

    rides = cursor.fetchall()
    cursor.close()
    connection.close()

    return rides

# Usunięcie przejazdu
def delete_ride(user_id, ride_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM rides WHERE id = %s AND user_id = %s""", (ride_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()