import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import json

# wykres procentowy w podziale na miesiące
def generate_rides_by_month_chart(rows):

        #kolory i czcionki
    TITLE_COLOR = "limegreen"
    AXIS_COLOR = "white"

    TITLE_SIZE = 18
    AXIS_SIZE = 12

        # Kolory przypisane do poszczególnych lat
    colors_line = {
        2026: "yellow",
        2027: "blue",
        2028: "orange",
        2029: "green"
    }

        #skróty miesięcy na osi x
    months = ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"]

    years = sorted(set(row["year"] for row in rows))

        # Ustawienie przezroczystego tła całego obrazu
    fig, ax = plt.subplots(figsize=(9, 6))

    fig.patch.set_alpha(0)

    ax.set_facecolor((0.25, 0.25, 0.25, 0.25))

        # Utworzenie osobnej linii dla każdego roku
    for year in years:

        year_rows = [row for row in rows if row["year"] == year]

        values = [0] * 12

        # Przypisanie procentowego udziału przejazdów do odpowiednich miesięcy
        for row in year_rows:

            month_index = row["month"] - 1

            values[month_index] = row["percentage"]

            # Narysowanie linii z punktami i dodanie roku do legendy
        ax.plot(months, values, marker="o", linewidth=2, label=str(year), alpha=0.7, color=colors_line[year])

        #zakres osi Y i opisy osi i kolory
    ax.set_ylim(0, 100)

    ax.set_yticks(np.arange(0, 101, 10))

    ax.set_ylabel("%", fontsize=AXIS_SIZE, color=AXIS_COLOR)

    ax.tick_params(axis="x", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

    ax.tick_params(axis="y", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

        #tytuł wykresu
    ax.set_title("Udział przejazdów w poszczególnych miesiącach", fontsize=TITLE_SIZE, color=TITLE_COLOR)

    ax.legend()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

        # Dodanie poziomej siatki pomocniczej
    ax.grid(axis="y", linestyle="--", alpha=0.4)

        # Umieszczenie siatki za liniami wykresu
    ax.set_axisbelow(True)

        # Dopasowanie marginesów wykresu do zawartości
    plt.tight_layout()

        #utworzenie bufora do pamięci
    image = BytesIO()

    plt.savefig(image, format="png", transparent=True, bbox_inches="tight")

    plt.close(fig)

    image.seek(0)

    return image

# Generowanie wykresu procentowego rozkładu dystansu, prędkości lub przewyższenia
def generate_rides_distribution_chart(rows, chart_type):

    # Kolory słupków, tytułu, osi i wartości procentowych, czcionki
    BAR_COLOR = [
        "turquoise",
        "blue",
        "mediumpurple",
        "yellow",
        "orange",
        "darkred"
    ]
    TITLE_COLOR = "limegreen"
    AXIS_COLOR = "white"
    PERCENT_COLOR = "white"

    TITLE_SIZE = 18
    AXIS_SIZE = 12
    PERCENT_SIZE = 11

    # Przygotowanie danych dla wykresu dystansu
    if chart_type == "distance":

        title = "Rozkład dystansu przejazdów"

        labels = ["0–25 km", "25–50 km", "50–75 km", "75–100 km", "100–150 km", "150+ km"]

        values = [0] * len(labels)

        # Przypisanie każdego przejazdu do odpowiedniego przedziału dystansu
        for row in rows:

            distance = row["distance"]

            if distance < 25:

                values[0] += 1

            elif distance < 50:

                values[1] += 1

            elif distance < 75:

                values[2] += 1

            elif distance < 100:

                values[3] += 1

            elif distance < 150:

                values[4] += 1

            else:

                values[5] += 1

        # Przygotowanie danych dla wykresu średniej prędkości
    elif chart_type == "speed":

        title = "Rozkład średniej prędkości"

        labels = ["0–15 km/h", "15–20 km/h", "20–25 km/h", "25–30 km/h", "30–35 km/h", "35+ km/h"]

        values = [0] * len(labels)

        for row in rows:

            speed = row["avg_speed"]

            if speed < 15:

                values[0] += 1

            elif speed < 20:

                values[1] += 1

            elif speed < 25:

                values[2] += 1

            elif speed < 30:

                values[3] += 1

            elif speed < 35:

                values[4] += 1

            else:

                values[5] += 1

        # Przygotowanie danych dla wykresu przewyższenia
    elif chart_type == "elevation":

        title = "Rozkład przewyższenia"

        labels = ["0–250 m", "250–500 m", "500–750 m", "750–1000 m", "1000–1500 m", "1500+ m"]

        values = [0] * len(labels)

        for row in rows:

            elevation = row["elevation"]

            if elevation < 250:

                values[0] += 1

            elif elevation < 500:

                values[1] += 1

            elif elevation < 750:

                values[2] += 1

            elif elevation < 1000:

                values[3] += 1

            elif elevation < 1500:

                values[4] += 1

            else:

                values[5] += 1

    else:

        return None

    total = sum(values)

    if total == 0:

        percentages = [0] * len(values)
    else:

        percentages = [value / total * 100 for value in values]

    fig, ax = plt.subplots(figsize=(9, 6))

    fig.patch.set_alpha(0)

    ax.set_facecolor((0.25, 0.25, 0.25, 0.25))

    bars = ax.bar(labels, percentages, color=BAR_COLOR, alpha=0.6)

    ax.set_ylim(0, 100)

    ax.set_yticks(np.arange(0, 101, 10))

    ax.set_ylabel("%", fontsize=AXIS_SIZE, color=AXIS_COLOR)

    ax.tick_params(axis="x", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

    ax.tick_params(axis="y", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

    ax.set_title(title, fontsize=TITLE_SIZE, color=TITLE_COLOR)

    # Wyświetlenie wartości procentowych nad słupkami
    for bar, percentage in zip(bars, percentages):

        if percentage > 0:

            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{percentage:.1f}%", ha="center",
                    va="bottom", fontsize=PERCENT_SIZE, color=PERCENT_COLOR)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax.set_axisbelow(True)

    plt.tight_layout()

    image = BytesIO()

    plt.savefig(image, format="png", transparent=True, bbox_inches="tight")

    plt.close(fig)

    image.seek(0)

    return image

# Generowanie wykresu kołowego warunków pogodowych lub rodzaju nawierzchni
def generate_ride_pie_chart(rows, chart_type):

        #przypisanie kolorów oraz czcionki
    TITLE_COLOR = "limegreen"
    TITLE_SIZE = 18

    WEATHER_COLORS = {"suche": "yellowgreen", "deszcz": "blue", "przelotny_deszcz": "lightblue", "mokra": "violet",
                      "mgla": "gray", "snieg": "white"}

    SURFACE_COLORS = {"asfalt": "darkgrey", "szuter": "gold", "droga_gruntowa": "orange", "lesna": "brown",
                      "kostka": "gray"}

        # Przygotowanie danych dla wykresu warunków pogodowych
    if chart_type == "weather":

        title = "Warunki podczas przejazdów"

        colors_map = WEATHER_COLORS

        # Przypisanie czytelnych nazw do wartości zapisanych w bazie danych
        labels_map = {"suche": "Sucho", "deszcz": "Deszcz", "przelotny_deszcz": "Przelotny deszcz", "mokra": "Mokro",
                      "mgla": "Mgła", "snieg": "Śnieg"}

        # Utworzenie liczników dla wszystkich obsługiwanych warunków
        counts = {
            "suche": 0,
            "deszcz": 0,
            "przelotny_deszcz": 0,
            "mokra": 0,
            "mgla": 0,
            "snieg": 0
        }

        # Zliczanie wystąpień warunków pogodowych w przejazdach
        for row in rows:

            weather = row["weather"]

            if weather:

                if isinstance(weather, str):

                    weather = json.loads(weather)

                for condition in weather:

                    if condition in counts:

                        counts[condition] += 1

        # Przygotowanie danych dla wykresu rodzaju nawierzchni
    elif chart_type == "surface":

        title = "Rodzaj nawierzchni"

        colors_map = SURFACE_COLORS

        labels_map = {"asfalt": "Asfalt", "szuter": "Szuter", "droga_gruntowa": "Droga gruntowa",
                      "lesna": "Droga leśna", "kostka": "Kostka"}

        counts = {
            "asfalt": 0,
            "szuter": 0,
            "droga_gruntowa": 0,
            "lesna": 0,
            "kostka": 0
        }

        for row in rows:

            surface = row["surface"]

            if surface:

                if isinstance(surface, str):

                    surface = json.loads(surface)

                for item in surface:

                    if item in counts:

                        counts[item] += 1
    else:

        return None

        # Przygotowanie list nazw, liczebności i kolorów dla wykresu
    labels = []
    values = []
    colors = []

        # Dodanie do wykresu tylko kategorii, które wystąpiły przynajmniej raz
    for key, label in labels_map.items():

        if counts[key] > 0:

            labels.append(label)
            values.append(counts[key])
            colors.append(colors_map[key])

    if not values:

        return None

    fig, ax = plt.subplots(figsize=(9, 6))

    fig.patch.set_alpha(0)

    ax.set_facecolor((0.25, 0.25, 0.25, 0.25))

        # Narysowanie wykresu kołowego z nazwami i procentami
    ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90, wedgeprops={"alpha": 0.6},
           textprops={"color": "white", "fontweight": "bold"})

    ax.set_title(title, fontsize=TITLE_SIZE, color=TITLE_COLOR)

    ax.axis("equal")

    plt.tight_layout()

    image = BytesIO()

    plt.savefig(image, format="png", transparent=True, bbox_inches="tight")

    plt.close(fig)

    image.seek(0)

    return image