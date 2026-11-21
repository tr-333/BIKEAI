
from flask import render_template, request, session
from analysis.analysis_ride import analysis_rides
from user.user_bike_database import get_user_bikes

# Konfiguracja kategorii modelu AI
MODEL_CATEGORIES = {

    "front_brake": {
        "title": "HAMULEC PRZÓD",
        "components": [
            ("Obsługa", "brake_control", "brake_mileage"),
            ("Hamulec przód", "brake_model", "brake_mileage"),
            ("Klocki przód", "brake_pads", "brake_pads_mileage"),
            ("Tarcza przód", "brake_rotors", "brake_rotors_mileage")
        ]
    },

    "rear_brake": {
        "title": "HAMULEC TYŁ",
        "components": [
            ("Obsługa", "brake_control", "brake_mileage"),
            ("Hamulec tył", "rear_brake_model", "rear_brake_mileage"),
            ("Klocki tył", "rear_brake_pads", "rear_brake_pads_mileage"),
            ("Tarcza tył", "rear_brake_rotors", "rear_brake_rotors_mileage")
        ]
    },

    "front_wheel": {
        "title": "KOŁO PRZÓD",
        "components": [
            ("Piasta przód", "front_hub", "front_hub_mileage"),
            ("Opona przód", "front_tire", "tire_mileage")
        ]
    },

    "rear_wheel": {
        "title": "KOŁO TYŁ",
        "components": [
            ("Piasta tył", "rear_hub", "rear_hub_mileage"),
            ("Opona tył", "rear_tire", "rear_tire_mileage")
        ]
    },

    "drivetrain": {
        "title": "NAPĘD",
        "components": [
            ("Korba", "crankset", "crankset_mileage"),
            ("Kaseta", "cassette", "cassette_mileage"),
            ("Łańcuch", "chain", "chain_mileage"),
            ("Suport", "bottom_bracket", "bottom_bracket_mileage"),
            ("Blaty przód", "crankset", "crankset_mileage")
        ]
    },

    "gears": {
        "title": "BIEGI",
        "components": [
            ("Obsługa", "shifting_type", "shifting_mileage"),
            ("Przerzutka przód", "shifting_model", "shifting_mileage"),
            ("Przerzutka tył", "rear_shifting_model", "rear_shifting_mileage")
        ]
    }
}

# Tłumaczenie nazw komponentów
COMPONENT_TRANSLATIONS = {
    "integrated_levers": "Klamkomanetki",
    "brake_levers": "Klamki hamulcowe",
    "trigger_shifters": "Manetki",
    "grip_shift": "Manetka obrotowa",
    "other": "Inna"
}

# Pobieranie szczegółowej nazwy komponentu
def get_component_name(bike, field):

    # Opony – połączenie producenta, modelu i szerokości
    if field == "front_tire":
        values = [
            bike.get("tire_brand"),
            bike.get("tire_model"),
            bike.get("tire_width")
        ]

    elif field == "rear_tire":
        values = [
            bike.get("rear_tire_brand"),
            bike.get("rear_tire_model"),
            bike.get("rear_tire_width")
        ]

    else:
        values = [bike.get(field)]

    name_parts = []

    for value in values:

        if value:

            value = str(value).strip()

            translated_value = COMPONENT_TRANSLATIONS.get(value, value)

            name_parts.append(translated_value)

    name = " ".join(name_parts)

    return name if name else "Brak danych"

# Przygotowanie danych komponentów
def prepare_model_components(bike, category):

    components = []

    for title, name_field, mileage_field in category["components"]:

        mileage = bike.get(mileage_field)

        if mileage is None or mileage == "":

            mileage = bike.get("initial_mileage") or 0

        components.append({
            "name": title,
            "full_name": get_component_name(bike, name_field),
            "mileage": mileage,
            "condition": 100
        })

    return components

# Obsługa sekcji analizy użytkownika
def user_analysis():

    model_category = None

    #pobieranie rowerów user
    bikes = get_user_bikes(session["user_id"])

    selected_bike = None

    selected_bike_id = request.form.get("bike_choice") if request.method == "POST" else request.args.get("bike_choice")

    #wybór roweru
    for bike in bikes:

        if selected_bike_id and bike["id"] == int(selected_bike_id):

            selected_bike = bike

            break

    if request.method == "POST":

        action = request.form.get("action")

        #Dla ramki danych modelu
        if action in MODEL_CATEGORIES and selected_bike:

            model_category = MODEL_CATEGORIES[action].copy()

            model_category["components"] = prepare_model_components(selected_bike, MODEL_CATEGORIES[action])

        # Statystyki przejazdów zalogowanego użytkownika
        if action in ["rides_stats", "rides_month_chart", "distance_chart", "speed_chart", "elevation_chart",
                      "weather_chart", "surface_chart"]:

            return analysis_rides(user_id=session["user_id"])

        #przebieg całkowity
    total_mileage = (selected_bike.get("initial_mileage") or 0 if selected_bike else 0)

    # Początkowe wyświetlenie sekcji ANALIZA
    return render_template("analysis.html", statistics={}, chart_type=None, show_user_stats=False,
                            show_rides_stats=False, show_model=True if request.args.get("model") or model_category
                            else False, model_category=model_category, bikes=bikes, selected_bike_id=selected_bike_id,
                           total_mileage=total_mileage)
