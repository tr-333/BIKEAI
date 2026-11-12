import os
from io import BytesIO
import gpxpy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Odczyt pliku gpx
def read_gpx(gpx_filename):

    gpx_path = os.path.join(os.path.dirname(__file__), "gpx", gpx_filename)

    with open(gpx_path, "r", encoding="utf-8") as gpx_file:

        gpx = gpxpy.parse(gpx_file)

    points = []

    for track in gpx.tracks:

        for segment in track.segments:

            for point in segment.points:

                points.append({"latitude": point.latitude, "longitude": point.longitude})

    return points

# Generowanie mapy gpx
def generate_gpx_map(gpx_filename):

    points = read_gpx(gpx_filename)

    if not points:

        return None

    latitudes = [point["latitude"] for point in points]

    longitudes = [point["longitude"] for point in points]

    # Utworzenie obrazu
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=(0.0, 0.0, 0.5, 0.4)) #kolor navy

    ax.set_facecolor("navy")

    # Rysowanie śladu
    ax.plot(longitudes, latitudes, color="turquoise", linewidth=3, solid_capstyle="round", solid_joinstyle="round")

    # Początek trasy
    ax.scatter(longitudes[0], latitudes[0], facecolors=(0.0, 0.0, 0.5, 0.4), edgecolors="white", s=140, linewidths=4,
               zorder=5)

    # Koniec trasy
    ax.scatter(longitudes[-1], latitudes[-1], facecolors="turquoise", edgecolors="white", s=140, linewidths=4, zorder=5)

    # Zakres całej trasy
    min_x = min(longitudes)
    max_x = max(longitudes)

    min_y = min(latitudes)
    max_y = max(latitudes)

    # Margines wokół trasy
    padding_x = (max_x - min_x) * 0.25
    padding_y = (max_y - min_y) * 0.25

    # Zabezpieczenie dla bardzo krótkiej trasy
    if padding_x == 0:

        padding_x = 0.001

    if padding_y == 0:

        padding_y = 0.001

    ax.set_xlim(min_x - padding_x, max_x + padding_x)

    ax.set_ylim(min_y - padding_y, max_y + padding_y)

    # Usunięcie osi
    ax.set_axis_off()

    plt.tight_layout(pad=0)

    #utworzenie buforu w pamięci
    image = BytesIO()

    #zapis do pamięci
    plt.savefig(image, format="png", dpi=150, facecolor=(0.0, 0.0, 0.5, 0.4))

    #ustawienie początku bufora
    image.seek(0)

    plt.close(fig)

    return image
