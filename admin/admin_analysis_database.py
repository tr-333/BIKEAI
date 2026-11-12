from database import get_connection

#Pobiera użytkowników do analizy
def get_user_statistics():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""SELECT COUNT(DISTINCT u.id) AS user_count, COUNT(b.id) AS bike_count,
    COALESCE(SUM(u.bike_limit), 0) AS limit_count FROM users u LEFT JOIN bikes b ON b.user_id = u.id
    WHERE u.role != 'admin' """)

    statistics = cursor.fetchone()
    cursor.close()
    conn.close()

    return statistics

# pobiera typy rowerów do statystki
def get_bike_types_statistics(stat_type="bikes"):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if stat_type == "users":

        count_sql = "COUNT(DISTINCT bikes.user_id)"

    else:

        count_sql = "COUNT(*)"

    cursor.execute(f"""SELECT bike_type, {count_sql} AS count FROM bikes
    JOIN users ON bikes.user_id = users.id WHERE users.role != 'admin' GROUP BY bike_type """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    statistics = {
        "road": 0,
        "gravel": 0,
        "mtb": 0,
        "trekkingowy": 0,
        "cross": 0,
        "city": 0,
        "kids": 0,
        "other": 0
    }

    for row in rows:

        if row["bike_type"] in statistics:

            statistics[row["bike_type"]] = row["count"]

    return statistics
