
# wiadomość powitalna

WELCOME_SUBJECT = "Witamy w BIKE AI!"

WELCOME_CONTENT = (
    "Witamy w aplikacji BIKE AI! "
    "Życzymy przyjemnego korzystania z aplikacji "
    "i wielu udanych przejazdów."
)


# wiadmość o blokadzie konta

BLOCKED_SUBJECT = "Informacja o blokadzie konta"

BLOCKED_CONTENT = (
    "Twoje konto w aplikacji BIKE AI zostało zablokowane. "
    "Jeśli chcesz poznać powód blokady lub uzyskać dodatkowe "
    "informacje, możesz odpowiedzieć na tę wiadomość, "
    "kontaktując się z administratorem."
)


# wiadmość przy zmianie limitu

BIKE_LIMIT_SUBJECT = "Zmiana limitu rowerów"

def bike_limit_content(new_limit):

    return (
        "Administrator zmienił limit rowerów przypisany "
        "do Twojego konta. "
        f"Twój aktualny limit wynosi: {new_limit}."
    )


# wiadmość o usunięciu przejazdu

RIDE_DELETED_SUBJECT = "Informacja o usunięciu przejazdu"

RIDE_DELETED_CONTENT = (
    "Jeden z Twoich przejazdów został usunięty przez "
    "administratora. Jeśli chcesz poznać powód tej decyzji "
    "lub uzyskać dodatkowe informacje, możesz odpowiedzieć "
    "na tę wiadomość, kontaktując się z administratorem."
)