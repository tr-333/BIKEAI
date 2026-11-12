
from flask import render_template, request, send_file
from .analysis_ride_database import (riders_statistics, get_rides_by_month, get_rides_distribution, get_ride_conditions)
from .analysis_ride_chart import (generate_rides_by_month_chart, generate_rides_distribution_chart,
                                  generate_ride_pie_chart)

# Obsługa statystyk przejazdów
def analysis_rides(user_id=None):

    action = request.form.get("action")

    statistics = riders_statistics(user_id)


    if action == "rides_stats":

        chart_type = None


    elif action == "rides_month_chart":

        chart_type = "rides_month"


    elif action in ["distance_chart", "speed_chart", "elevation_chart"]:

        chart_type = action.replace("_chart", "")


    elif action in ["weather_chart", "surface_chart"]:

        chart_type = action.replace("_chart", "")

    else:

        chart_type = None

    return render_template("analysis.html", statistics=statistics, chart_type=chart_type,
                           show_user_stats=False, show_rides_stats=True, show_exploitation=False)

# Liczba przejazdów w poszczególnych miesiącach
def rides_by_month_chart(user_id=None):

    rows = get_rides_by_month(user_id)

    image = generate_rides_by_month_chart(rows)

    return send_file(image, mimetype="image/png")


# Wykresy rozkładu parametrów przejazdów
def rides_distribution_chart(user_id=None):

    chart_type = request.args.get("chart_type", "distance")

    rows = get_rides_distribution(user_id)

    image = generate_rides_distribution_chart(rows, chart_type)

    if image is None:

        return "", 404

    return send_file(image, mimetype="image/png")


# Wykresy pogody i rodzaju nawierzchni
def ride_conditions_chart(user_id=None):

    chart_type = request.args.get("chart_type", "weather")

    rows = get_ride_conditions(user_id)

    image = generate_ride_pie_chart(rows, chart_type)

    if image is None:

        return "", 404

    return send_file(image, mimetype="image/png")
