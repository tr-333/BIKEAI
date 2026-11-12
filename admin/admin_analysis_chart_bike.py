import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

#generuje wykres związany z rowerami użytkowników
def generate_bike_types_chart(bike_types, data_type="bikes"):

    # Ustawienia wygląd
    BAR_COLOR = [
        "turquoise",  # Szosa
        "yellow",  # Gravel
        "brown",  # MTB
        "blue",  # Trekking
        "orange",  # Cross
        "mediumpurple",  # Miejski
        "green",  # Dziecięcy
        "darkred"  # Inny
    ]

    TITLE_COLOR = "limegreen"
    AXIS_COLOR = "white"
    PERCENT_COLOR = "white"

    TITLE_SIZE = 18
    AXIS_SIZE = 12
    PERCENT_SIZE = 11

    # Nazwy typów rowerów
    labels = ["Szosa", "Gravel", "MTB", "Trekking", "Cross", "Miejski", "Dziecięcy", "Inny"]

    values = [bike_types["road"], bike_types["gravel"], bike_types["mtb"], bike_types["trekkingowy"],
              bike_types["cross"], bike_types["city"], bike_types["kids"], bike_types["other"]]

    # Obliczenie procentowe
    total = sum(values)

    if total == 0:

        percentages = [0] * len(values)

    else:

        percentages = [value / total * 100 for value in values]

    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(9, 6))

    # Tło wykresu
    fig.patch.set_alpha(0)
    ax.set_facecolor((0.25, 0.25, 0.25, 0.25))

    # Słupki
    bars = ax.bar(labels, percentages, color=BAR_COLOR, alpha=0.6)

    # Oś y
    ax.set_ylim(0, 100)

    ax.set_yticks(np.arange(0, 101, 10))

    ax.set_ylabel("%", fontsize=AXIS_SIZE, color=AXIS_COLOR)

    # Oś x
    ax.tick_params(axis="x", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

    ax.tick_params(axis="y", labelsize=AXIS_SIZE, colors=AXIS_COLOR)

    # Tytuł
    if data_type == "users":

        title = "Użytkownik posiadający dany rower"

    else:

        title = "Typy rowerów"

    ax.set_title(title, fontsize=TITLE_SIZE, color=TITLE_COLOR)

    # Wyświetlenie procentów nad słupkami
    for bar, percentage in zip(bars, percentages):

        if percentage > 0:

            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f"{percentage:.1f}%", ha="center",
                    va="bottom", fontsize=PERCENT_SIZE, color=PERCENT_COLOR)

    # Estetyka
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    ax.set_axisbelow(True)

    plt.tight_layout()

    # Zapis do pamięci
    image = BytesIO()

    plt.savefig(image, format="png", transparent=True, bbox_inches="tight")

    plt.close(fig)

    image.seek(0)

    return image
