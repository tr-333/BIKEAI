import re

#funkcja do sprawdzania założeń hasła w czasie rejesteracji i aktualizacji danych
def validate_password(password):

    if len(password) < 8:

        return "Hasło musi mieć minimum 8 znaków!"

    if not re.search(r"\d", password):

        return "Hasło musi mieć min jedną liczbę!"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]]', password):

        return "Hasło musi mieć min jeden znak specjalny!"

    return None