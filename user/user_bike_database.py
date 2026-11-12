from database import get_connection


# Funkcja zapisu nowego roweru
def save_bike(user_id, bike_data):

    connection = get_connection()
    cursor = connection.cursor()

    # Nazwy kolumn odpowiadają polom ze słownika bike_data
    columns = (
        "bike_type",
        "brand",
        "model",
        "production_year",
        "purchase_year",
        "frame_size",
        "initial_mileage",
        "maintenance",
        "handlebar_type",

        # Biegi
        "shifting_type",
        "shifting_model",
        "shifting_mechanism",
        "shifting_replacement_date",
        "shifting_mileage",
        "rear_shifting_model",
        "rear_shifting_replacement_date",
        "rear_shifting_mileage",

        # Napęd
        "front_gears",
        "rear_gears",
        "crankset",
        "crankset_replacement_date",
        "crankset_mileage",
        "cassette",
        "cassette_replacement_date",
        "cassette_mileage",
        "chain",
        "chain_replacement_date",
        "chain_mileage",
        "bottom_bracket",
        "bottom_bracket_replacement_date",
        "bottom_bracket_mileage",

        # Hamulce
        "brake_type",
        "kind_pads",
        "brake_control",
        "brake_model",
        "brake_replacement_date",
        "brake_mileage",
        "rear_brake_model",
        "rear_brake_replacement_date",
        "rear_brake_mileage",
        "brake_rotors",
        "brake_rotors_replacement_date",
        "brake_rotors_mileage",
        "rear_brake_rotors",
        "rear_brake_rotors_replacement_date",
        "rear_brake_rotors_mileage",
        "brake_pads",
        "brake_pads_replacement_date",
        "brake_pads_mileage",
        "rear_brake_pads",
        "rear_brake_pads_replacement_date",
        "rear_brake_pads_mileage",

        # Koła i opony
        "wheel_size",
        "front_hub",
        "front_hub_replacement_date",
        "front_hub_mileage",
        "rear_hub",
        "rear_hub_replacement_date",
        "rear_hub_mileage",
        "tire_brand",
        "tire_model",
        "tire_width",
        "tire_replacement_date",
        "tire_mileage",
        "rear_tire_brand",
        "rear_tire_model",
        "rear_tire_width",
        "rear_tire_replacement_date",
        "rear_tire_mileage"
    )

    # Przygotowanie zapytania SQL
    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * (len(columns) + 1))

    cursor.execute(
        f"""
        INSERT INTO bikes (
            user_id, {column_names}
        )
        VALUES ({placeholders})
        """,
        (user_id, *(bike_data[field] for field in columns))
    )

    connection.commit()
    cursor.close()
    connection.close()


    #metoda do odczytu roweru użytkownika
def get_user_bikes(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT * FROM bikes WHERE user_id = %s ORDER BY id DESC""", (user_id,))

    bikes = cursor.fetchall()
    cursor.close()
    connection.close()

    return bikes


    #funkcja do pobrania roweru by uzupelnic formularz
def get_bike(user_id, bike_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT * FROM bikes WHERE id = %s AND user_id = %s""", (bike_id, user_id))

    bike = cursor.fetchone()
    cursor.close()
    connection.close()

    return bike


    #funkcja do usuwania roweru
def delete_bike(user_id, bike_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""DELETE FROM bikes WHERE id = %s AND user_id = %s""", (bike_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()


    #funkcja edycji roweru
def update_bike(user_id, bike_id, bike_data):

    connection = get_connection()
    cursor = connection.cursor()

    # Nazwy kolumn odpowiadają polom ze słownika bike_data
    columns = (
        "bike_type",
        "brand",
        "model",
        "production_year",
        "purchase_year",
        "frame_size",
        "initial_mileage",
        "maintenance",
        "handlebar_type",

        # Biegi
        "shifting_type",
        "shifting_model",
        "shifting_mechanism",
        "shifting_replacement_date",
        "shifting_mileage",
        "rear_shifting_model",
        "rear_shifting_replacement_date",
        "rear_shifting_mileage",

        # Napęd
        "front_gears",
        "rear_gears",
        "crankset",
        "crankset_replacement_date",
        "crankset_mileage",
        "cassette",
        "cassette_replacement_date",
        "cassette_mileage",
        "chain",
        "chain_replacement_date",
        "chain_mileage",
        "bottom_bracket",
        "bottom_bracket_replacement_date",
        "bottom_bracket_mileage",

        # Hamulce
        "brake_type",
        "kind_pads",
        "brake_control",
        "brake_model",
        "brake_replacement_date",
        "brake_mileage",
        "rear_brake_model",
        "rear_brake_replacement_date",
        "rear_brake_mileage",
        "brake_rotors",
        "brake_rotors_replacement_date",
        "brake_rotors_mileage",
        "rear_brake_rotors",
        "rear_brake_rotors_replacement_date",
        "rear_brake_rotors_mileage",
        "brake_pads",
        "brake_pads_replacement_date",
        "brake_pads_mileage",
        "rear_brake_pads",
        "rear_brake_pads_replacement_date",
        "rear_brake_pads_mileage",

        # Koła i opony
        "wheel_size",
        "front_hub",
        "front_hub_replacement_date",
        "front_hub_mileage",
        "rear_hub",
        "rear_hub_replacement_date",
        "rear_hub_mileage",
        "tire_brand",
        "tire_model",
        "tire_width",
        "tire_replacement_date",
        "tire_mileage",
        "rear_tire_brand",
        "rear_tire_model",
        "rear_tire_width",
        "rear_tire_replacement_date",
        "rear_tire_mileage"
    )

    # Przygotowanie części SET zapytania SQL
    set_clause = ", ".join(f"{column} = %s" for column in columns)

    cursor.execute(f""" UPDATE bikes SET {set_clause} WHERE id = %s AND user_id = %s""",
                   (*(bike_data[field] for field in columns), bike_id, user_id))

    connection.commit()
    cursor.close()
    connection.close()


    #funkcja pobiera limity użytkownika
def get_bike_limit(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""SELECT bike_limit FROM users WHERE id = %s""", (user_id,))

    user = cursor.fetchone()
    cursor.close()
    connection.close()

    return user["bike_limit"]