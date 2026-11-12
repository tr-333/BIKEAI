from flask import render_template, request, send_file
from .admin_analysis_database import (get_user_statistics, get_bike_types_statistics)
from analysis.analysis_ride import analysis_rides
from .admin_analysis_chart_bike import generate_bike_types_chart

#funkcja akcji formularza analizy admina
def admin_analysis():

    if request.method == "POST":

        action = request.form.get("action")


        if action == "users_stats":

            statistics = get_user_statistics()

            bike_types = get_bike_types_statistics("bikes")

            users_bike_types = get_bike_types_statistics("users")

            return render_template("analysis.html", statistics=statistics, bike_types=bike_types,
                                   users_bike_types=users_bike_types, chart_type=None, show_user_stats=True,
                                   show_rides_stats=False)


        if action == "bike_chart":

            statistics = get_user_statistics()

            bike_types = get_bike_types_statistics("bikes")

            users_bike_types = get_bike_types_statistics("users")

            return render_template("analysis.html", statistics=statistics, bike_types=bike_types,
                                   users_bike_types=users_bike_types, chart_type="bikes", show_user_stats=True,
                                   show_rides_stats=False)


        if action == "user_chart":

            statistics = get_user_statistics()

            bike_types = get_bike_types_statistics("bikes")

            users_bike_types = get_bike_types_statistics("users")

            return render_template("analysis.html", statistics=statistics, bike_types=bike_types,
                                   users_bike_types=users_bike_types, chart_type="users", show_user_stats=True,
                                   show_rides_stats=False)


        if action in ["rides_stats", "rides_month_chart", "distance_chart", "speed_chart", "elevation_chart",
                      "weather_chart", "surface_chart"]:

            return analysis_rides()

    return render_template("analysis.html")


#procentowy udział typów rowerów, procentowy udział użytkowników posiadających dany typ roweru
def bike_types_chart():

    data_type = request.args.get("data_type", "bikes")

    bike_types = get_bike_types_statistics(data_type)

    image = generate_bike_types_chart(bike_types, data_type)

    return send_file(image, mimetype="image/png")
