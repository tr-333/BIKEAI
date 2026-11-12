
from database import get_connection
from admin.admin_message_database import send_admin_message
from message_templates import (WELCOME_SUBJECT, WELCOME_CONTENT, BLOCKED_SUBJECT, BLOCKED_CONTENT, BIKE_LIMIT_SUBJECT,
                               RIDE_DELETED_SUBJECT, RIDE_DELETED_CONTENT, bike_limit_content)


# Pobranie id administratora
def get_system_admin_id():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""SELECT id FROM users WHERE role = 'admin' ORDER BY id LIMIT 1""")

        result = cursor.fetchone()

        if result is None:

            raise ValueError("Nie znaleziono konta administratora.")

        return result[0]

    finally:

        cursor.close()
        connection.close()

# wysłąnie wiadmości systemowej
def send_system_message(recipient_id, subject, content, admin_id=None):

    if admin_id is None:

        admin_id = get_system_admin_id()

    return send_admin_message(admin_id=admin_id, recipient_id=recipient_id, subject=subject, content=content,
                              is_automatic=True)

# wiadomość powitalna
def send_welcome_message(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""SELECT welcome_message_sent FROM users WHERE id = %s""", (user_id,))

        result = cursor.fetchone()

    finally:

        cursor.close()
        connection.close()

    #nie znaleziono użytkownika.
    if result is None:

        return False

    #powitanie zostało już wysłane.
    if result[0]:

        return False

    #wysyłanie powitania przez istniejący system wiadomości.
    send_system_message(recipient_id=user_id, subject=WELCOME_SUBJECT, content=WELCOME_CONTENT)

    #zapisujemy informację niezależnie od zawartości skrzynki.
    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""UPDATE users SET welcome_message_sent = TRUE WHERE id = %s 
        AND welcome_message_sent = FALSE""", (user_id,))

        connection.commit()

        return cursor.rowcount == 1

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

#wiadmość przy blokowaniu konta
def send_account_blocked_message(user_id, admin_id):

    return send_system_message(recipient_id=user_id, subject=BLOCKED_SUBJECT, content=BLOCKED_CONTENT,
                               admin_id=admin_id)

#wiadmość przy zmianie limitów
def send_bike_limit_changed_message(user_id, new_limit, admin_id):

    return send_system_message(recipient_id=user_id, subject=BIKE_LIMIT_SUBJECT, content=bike_limit_content(new_limit),
                               admin_id=admin_id)

#wiadmość o usunięciu przejazdu
def send_ride_deleted_message(user_id, admin_id):

    return send_system_message(recipient_id=user_id, subject=RIDE_DELETED_SUBJECT, content=RIDE_DELETED_CONTENT,
                               admin_id=admin_id)