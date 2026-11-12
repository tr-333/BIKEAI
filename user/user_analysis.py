
from flask import render_template, request, session
from analysis.analysis_ride import analysis_rides

# Konfiguracja kategorii modelu AI
MODEL_CATEGORIES = {

    "front_brake": {
        "title": "HAMULEC PRZÓD",
        "components": ["Obsługa", "Hamulec przód", "Klocki przód", "Tarcza przód"]
    },

    "rear_brake": {
        "title": "HAMULEC TYŁ", "components": ["Obsługa", "Hamulec tył", "Klocki tył", "Tarcza tył"]
    },

    "front_wheel": {
        "title": "KOŁO PRZÓD", "components": ["Piasta przód", "Opona przód"]
    },

    "rear_wheel": {
        "title": "KOŁO TYŁ", "components": ["Piasta tył", "Opona tył"]
    },

    "drivetrain": {
        "title": "NAPĘD", "components": ["Korba", "Kaseta", "Łańcuch", "Suport", "Blaty przód"]
    },

    "gears": {
        "title": "BIEGI", "components": ["Przerzutka przód", "Przerzutka tył"]
    }
}

# Obsługa sekcji analizy użytkownika
def user_analysis():

    model_category = False

    if request.args.get("model"):

        pass

    if request.method == "POST":

        action = request.form.get("action")

        #Dla ramki danych modelu
        if action in MODEL_CATEGORIES:

            model_category = MODEL_CATEGORIES[action]

        # Statystyki przejazdów zalogowanego użytkownika
        if action in ["rides_stats", "rides_month_chart", "distance_chart", "speed_chart", "elevation_chart",
                      "weather_chart", "surface_chart"]:

            return analysis_rides(user_id=session["user_id"])

    # Początkowe wyświetlenie sekcji ANALIZA
    return render_template("analysis.html", statistics={}, chart_type=None, show_user_stats=False,
                            show_rides_stats=False, show_model=True if request.args.get("model") or model_category
                            else False, model_category=model_category)
