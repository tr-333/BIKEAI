
from database import get_connection


# Pobiera statystyki przejazdów
def riders_statistics(user_id=None):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            COUNT(*) AS ride_count,
            COALESCE(SUM(distance), 0) AS total_distance,
            COALESCE(MAX(distance), 0) AS longest_distance,
            COALESCE(AVG(avg_speed), 0) AS average_speed,
            COALESCE(MAX(max_speed), 0) AS max_speed,
            COALESCE(AVG(elevation), 0) AS average_elevation,
            COALESCE(MAX(elevation), 0) AS highest_elevation
        FROM rides
    """

    values = []

    if user_id is not None:

        query += " WHERE user_id = %s"
        values.append(user_id)

    cursor.execute(query, values)
    statistics = cursor.fetchone()

    if statistics["ride_count"] > 0:

        statistics["average_distance"] = (statistics["total_distance"] / statistics["ride_count"])

    else:

        statistics["average_distance"] = 0

    cursor.close()
    conn.close()

    return statistics


# Pobiera informacje o miesiącach
def get_rides_by_month(user_id=None):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """SELECT YEAR(ride_date) AS year, MONTH(ride_date) AS month, COUNT(*) AS ride_count FROM rides"""

    values = []

    if user_id is not None:

        query += " WHERE user_id = %s"
        values.append(user_id)

    query += """ GROUP BY YEAR(ride_date), MONTH(ride_date) ORDER BY YEAR(ride_date), MONTH(ride_date)"""

    cursor.execute(query, values)
    rows = cursor.fetchall()

    year_totals = {}

    for row in rows:

        year = row["year"]

        if year not in year_totals:

            year_totals[year] = 0

        year_totals[year] += row["ride_count"]

    months = ["", "Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"]

    for row in rows:

        year = row["year"]

        row["percentage"] = (row["ride_count"] / year_totals[year] * 100)

        row["month_name"] = months[row["month"]]

    cursor.close()
    conn.close()

    return rows


# Pobiera informacje o rozkładzie parametrów przejazdów
def get_rides_distribution(user_id=None):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """SELECT distance, avg_speed, elevation FROM rides"""

    values = []

    if user_id is not None:

        query += " WHERE user_id = %s"
        values.append(user_id)

    cursor.execute(query, values)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# Pobiera informacje o pogodzie i nawierzchni
def get_ride_conditions(user_id=None):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """SELECT weather, surface FROM rides"""

    values = []

    if user_id is not None:

        query += " WHERE user_id = %s"
        values.append(user_id)

    cursor.execute(query, values)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
