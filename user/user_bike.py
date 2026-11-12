from flask import render_template, request, session, redirect, url_for
from .user_bike_database import (get_user_bikes, get_bike, save_bike, update_bike, delete_bike, get_bike_limit)


#funkcja akcji w formularzu roweru
def bike_user(bike_id=None):

    user_id = session["user_id"]

        #pobranie danych
    bike = None

    if bike_id:

        bike = get_bike(user_id, bike_id)

    bikes = get_user_bikes(user_id)

    bike_limit = get_bike_limit(user_id)

    bike_count = len(bikes)

    # Klucz szkicu formularza dla konkretnego użytkownika i roweru
    draft_key = f"bike_draft_{user_id}_{bike_id or 'new'}"

    # Pobranie wcześniej zapisanych tymczasowo danych
    bike_draft = session.get(draft_key, {})

    # Przy edycji pobranie danych roweru zapisanych w bazie
    form_data = dict(bike) if bike else {}

    # Uzupełnienie danych z bazy o wartości ze szkicu
    # Dane ze szkicu mają pierwszeństwo przed danymi z bazy
    form_data.update(bike_draft)

    # Aktualny zestaw danych formularza
    bike_draft = form_data

    # Konwersja dat z bazy danych do formatu obsługiwanego przez HTML
    for field, value in form_data.items():

        if hasattr(value, "strftime"):

            form_data[field] = value.strftime("%Y-%m-%d")

    if request.method == "POST":

        action = request.form["action"]

        # Przejście do odpowiedniej kategorii formularza
        category_parameters = {
            "category_basic_data": "basic_data",
            "category_wheel": "wheel",
            "category_drive": "drive",
            "category_brake": "brake",
            "category_tires": "tires"
        }

        # Sprawdzenie, czy użytkownik wybrał kategorię
        if action in category_parameters:

            # Zachowanie pól aktualnie wyświetlanej kategorii
            for field, value in request.form.items():

                if field not in ("action", "bike_id"):

                    bike_draft[field] = value

            # Zapis szkicu w sesji
            session[draft_key] = bike_draft

            # Pobranie parametru dla wybranej kategorii
            category = category_parameters[action]

            # Przekierowanie do formularza z wybraną kategorią
            return redirect(url_for("bike_route", **({"bike_id": bike_id} if bike_id else {}), **{category: 1}))

        # limit rowerów
        if action == "limit":

            return render_template("bike.html", bikes=bikes, bike=None, bike_limit=bike_limit,
                                   form_data=form_data, error="Osiągnięto limit rowerów")

        # usuwanie rowerów
        if action == "delete":

            if not bike_id:

                return render_template("bike.html", error="Najpierw wybierz rower!", bikes=bikes,
                                       bike=None, bike_limit=bike_limit, form_data=form_data)

            return render_template("bike.html", bikes=bikes, bike=bike, confirm_delete=True,
                                   delete_bike_id=bike_id, bike_limit=bike_limit, form_data=form_data)

        # potwierdzenie usunięcia
        if action == "confirm_delete":

            bike_id = request.form.get("bike_id")

            delete_bike(user_id, bike_id)

            # Usunięcie szkicu formularza
            session.pop(draft_key, None)

            return redirect(url_for("bike_route"))

        # zapis/edycja
        if action in ["save", "edit"]:

            if not bike_id and bike_count >= bike_limit:

                return render_template("bike.html", bikes=bikes, bike=None, bike_limit=bike_limit,
                                       error="Osiągnięto limit rowerów", form_data=form_data)

            # Uzupełnienie szkicu polami z aktualnej kategorii
            for field, value in request.form.items():

                if field not in ("action", "bike_id"):

                    bike_draft[field] = value

            #zachowanie aktualnego szkicu
            session[draft_key] = bike_draft

            #dane ze wszystkich kategorii
            form_data = bike_draft

            bike_data = {
                #dane podstawowe
                "bike_type": form_data.get("bike_type"),
                "brand": form_data.get("brand"),
                "model": form_data.get("model"),
                "production_year": form_data.get("production_year"),
                "purchase_year": form_data.get("purchase_year"),
                "frame_size": form_data.get("frame_size"),
                "initial_mileage": form_data.get("initial_mileage"),
                "maintenance": form_data.get("maintenance"),
                "handlebar_type": form_data.get("handlebar_type"),

                #biegi
                "shifting_type": form_data.get("shifting_type"),
                "shifting_model": form_data.get("shifting_model"),
                "shifting_mechanism": form_data.get("shifting_mechanism"),
                "shifting_replacement_date": form_data.get("shifting_replacement_date"),
                "shifting_mileage": form_data.get("shifting_mileage"),
                "rear_shifting_model": form_data.get("rear_shifting_model"),
                "rear_shifting_replacement_date": form_data.get("rear_shifting_replacement_date"),
                "rear_shifting_mileage": form_data.get("rear_shifting_mileage"),

                #naped
                "front_gears": form_data.get("front_gears"),
                "rear_gears": form_data.get("rear_gears"),
                "crankset": form_data.get("crankset"),
                "crankset_replacement_date": form_data.get("crankset_replacement_date"),
                "crankset_mileage": form_data.get("crankset_mileage"),
                "cassette": form_data.get("cassette"),
                "cassette_replacement_date": form_data.get("cassette_replacement_date"),
                "cassette_mileage": form_data.get("cassette_mileage"),
                "chain": form_data.get("chain"),
                "chain_replacement_date": form_data.get("chain_replacement_date"),
                "chain_mileage": form_data.get("chain_mileage"),
                "bottom_bracket": form_data.get("bottom_bracket"),
                "bottom_bracket_replacement_date": form_data.get("bottom_bracket_replacement_date"),
                "bottom_bracket_mileage": form_data.get("bottom_bracket_mileage"),

                #hamulce
                "brake_type": form_data.get("brake_type"),
                "kind_pads": form_data.get("kind_pads"),
                "brake_control": form_data.get("brake_control"),
                "brake_model": form_data.get("brake_model"),
                "brake_replacement_date": form_data.get("brake_replacement_date"),
                "brake_mileage": form_data.get("brake_mileage"),
                "rear_brake_model": form_data.get("rear_brake_model"),
                "rear_brake_replacement_date": form_data.get("rear_brake_replacement_date"),
                "rear_brake_mileage": form_data.get("rear_brake_mileage"),
                "brake_rotors": form_data.get("brake_rotors"),
                "brake_rotors_replacement_date": form_data.get("brake_rotors_replacement_date"),
                "brake_rotors_mileage": form_data.get("brake_rotors_mileage"),
                "rear_brake_rotors": form_data.get("rear_brake_rotors"),
                "rear_brake_rotors_replacement_date": form_data.get("rear_brake_rotors_replacement_date"),
                "rear_brake_rotors_mileage": form_data.get("rear_brake_rotors_mileage"),
                "brake_pads": form_data.get("brake_pads"),
                "brake_pads_replacement_date": form_data.get("brake_pads_replacement_date"),
                "brake_pads_mileage": form_data.get("brake_pads_mileage"),
                "rear_brake_pads": form_data.get("rear_brake_pads"),
                "rear_brake_pads_replacement_date": form_data.get("rear_brake_pads_replacement_date"),
                "rear_brake_pads_mileage": form_data.get("rear_brake_pads_mileage"),

                #koła i opony
                "wheel_size": form_data.get("wheel_size"),
                "front_hub": form_data.get("front_hub"),
                "front_hub_replacement_date": form_data.get("front_hub_replacement_date"),
                "front_hub_mileage": form_data.get("front_hub_mileage"),
                "rear_hub": form_data.get("rear_hub"),
                "rear_hub_replacement_date": form_data.get("rear_hub_replacement_date"),
                "rear_hub_mileage": form_data.get("rear_hub_mileage"),
                "tire_brand": form_data.get("tire_brand"),
                "tire_model": form_data.get("tire_model"),
                "tire_width": form_data.get("tire_width"),
                "tire_replacement_date": form_data.get("tire_replacement_date"),
                "tire_mileage": form_data.get("tire_mileage"),
                "rear_tire_brand": form_data.get("rear_tire_brand"),
                "rear_tire_model": form_data.get("rear_tire_model"),
                "rear_tire_width": form_data.get("rear_tire_width"),
                "rear_tire_replacement_date": form_data.get("rear_tire_replacement_date"),
                "rear_tire_mileage": form_data.get("rear_tire_mileage")
            }

            # pola wymagane
            required_fields = ["bike_type", "brand", "model", "initial_mileage", "maintenance",
                               "shifting_type", "shifting_model", "rear_shifting_model", "front_gears", "rear_gears",
                               "chain", "cassette", "crankset", "bottom_bracket", "brake_control", "brake_type",
                               "brake_model", "rear_brake_model", "brake_rotors", "rear_brake_rotors", "brake_pads",
                               "rear_brake_pads", "kind_pads", "wheel_size", "front_hub",
                               "rear_hub", "tire_brand", "tire_model"]

            missing_fields = [field for field in required_fields if not bike_data.get(field)]

            if missing_fields:

                return render_template("bike.html", error="Uzupełnij wszystkie wymagane pola.",
                                       bikes=bikes, bike=bike, bike_limit=bike_limit, form_data=form_data)

            # edycja zapisanego roweru
            if bike_id:

                update_bike(user_id, bike_id, bike_data)

                #usunięcie szkicu po udanej edycji
                session.pop(draft_key, None)

                bikes = get_user_bikes(user_id)

                return render_template("bike.html", success="Edycja zapisana!",
                                       bike_limit=bike_limit, bikes=bikes, bike=None, form_data={})

            # zapis nowego
            else:

                save_bike(user_id, bike_data)

                # Usunięcie szkicu po udanym zapisie
                session.pop(draft_key, None)

                bikes = get_user_bikes(user_id)

                return render_template("bike.html", success="Dane roweru zapisane!",
                                       bike_limit=bike_limit, bikes=bikes, bike=None, form_data={})

    bikes = get_user_bikes(user_id)

    return render_template("bike.html", bikes=bikes, bike=bike, bike_limit=bike_limit,
                           form_data=form_data)
