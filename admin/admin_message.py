
from flask import render_template, request, redirect, url_for, session

from admin.admin_message_database import (get_admin_messages, get_admin_message, get_admin_thread_messages,
                                          get_users_for_messages, search_users_for_messages, send_admin_message,
                                          send_admin_message_to_all, mark_admin_thread_read, hide_admin_thread)

# skrzynka wiadomości administratora
def message_admin():

    admin_id = session["user_id"]

    error = None
    success = None

        #wyszukiwanie wiadomości
    search_messages = request.values.get("search_messages", "").strip()

    # identyfikator wątku rozmowy.
    selected_message_id = request.args.get("message_id", type=int)

    show_reply = False

    # wyszukanie i wybór odbiorcy
    search_user = request.args.get("search_user", "").strip()

    selected_recipient_id = request.args.get("recipient_id", type=int)

    # obsługa formularzy
    if request.method == "POST":

        action = request.form.get("action")

        #wiadmości do wszystkich
        if action == "send_all":

            subject = request.form.get("subject", "").strip()

            content = request.form.get("content", "").strip()

            if not subject or not content:

                error = ("Wypełnij temat i treść wiadomości " "przeznaczonej dla wszystkich użytkowników.")

            elif len(subject) > 150:

                error = "Temat może mieć maksymalnie 150 znaków."

            else:

                try:

                    sent_count = send_admin_message_to_all(admin_id, subject, content)

                    if sent_count == 0:

                        error = "Brak użytkowników, do których można wysłać wiadomość."

                    else:

                        success = (f"Wiadomość wysłano do "f"{sent_count} użytkowników.")

                except KeyError:

                    error = ("Nie udało się wysłać wiadomości " "do wszystkich użytkowników.")

        # wiadomość do jednego użytkownika
        elif action == "send":

            recipient_id = request.form.get("recipient_id", type=int)

            subject = request.form.get("subject", "").strip()

            content = request.form.get("content", "").strip()

            users = get_users_for_messages()

            valid_user_ids = {user["id"] for user in users}

            if recipient_id not in valid_user_ids:

                error = "Wybierz prawidłowego użytkownika."

            elif not subject or not content:

                error = "Wypełnij temat i treść wiadomości."

            elif len(subject) > 150:

                error = "Temat może mieć maksymalnie 150 znaków."

            else:

                thread_id = send_admin_message(admin_id, recipient_id, subject, content)

                success = "Wiadomość została wysłana."

                selected_message_id = thread_id

        # otwarcie wątku
        elif action == "open":

            selected_message_id = request.form.get("message_id", type=int)

            if selected_message_id:

                return redirect(url_for("message", message_id=selected_message_id,
                                        search_messages=search_messages or None))

        #ukrycie całego wątku
        elif action == "delete_thread":

            thread_id = request.form.get("thread_id", type=int)

            if thread_id and hide_admin_thread(admin_id, thread_id):

                success = "Rozmowa została usunięta."

                selected_message_id = None

            else:

                error = "Nie udało się usunąć rozmowy."

        # formularz odpowiedzi
        elif action == "reply_form":

            selected_message_id = request.form.get("message_id", type=int)

            show_reply = True

        # odpowiedź w wątku
        elif action == "reply":

            selected_message_id = request.form.get("message_id", type=int)

            content = request.form.get("content", "").strip()

            selected_message = None

            if selected_message_id:

                selected_message = get_admin_message(admin_id, selected_message_id)

            if not selected_message:

                error = "Nie znaleziono wybranej rozmowy."

            elif not content:

                error = "Wpisz treść odpowiedzi."

                show_reply = True

            else:

                # pobranie całej historii rozmowy
                thread_messages = get_admin_thread_messages(admin_id, selected_message_id)

                    #ustalenie identyfikatora zwykłego użytkoniwka dla wątku
                recipient_id = None

                for message in thread_messages:

                    if message["sender_role"] == "user":

                        recipient_id = message["sender_id"]

                        break

                    if message["recipient_role"] == "user":

                        recipient_id = message["recipient_id"]

                        break

                # kontrola przed wysyłką wiadmości
                users = get_users_for_messages()

                valid_user_ids = {user["id"] for user in users}

                if recipient_id not in valid_user_ids:

                    error = ("Nie udało się ustalić użytkownika " "tej rozmowy.")

                else:

                    original_subject = selected_message["subject"]

                    if original_subject.lower().startswith("re:"):

                        reply_subject = original_subject

                    else:

                        reply_subject = f"Re: {original_subject}"

                    #odpowiedź, która trafia do wątku
                    send_admin_message(admin_id, recipient_id, reply_subject, content, thread_id=selected_message_id)

                    return redirect(url_for("message", message_id=selected_message_id))

    # pobiera listę wątków i użytkownika
    messages = get_admin_messages(admin_id, search_messages or None)

    if search_user:

        users = search_users_for_messages(search_user)

    else:

        users = []

        #pobranie rozmowy i jej historii
    selected_message = None

    thread_messages = []

    if selected_message_id:

        selected_message = get_admin_message(admin_id, selected_message_id)

        if selected_message:

            thread_messages = get_admin_thread_messages(admin_id, selected_message_id)

                #oznaczenie jak przeczytana
            mark_admin_thread_read(selected_message_id)

            # aktualizacja stanu w historii
            for message in thread_messages:

                if message["recipient_role"] == "admin":

                    message["is_read"] = True

                #aktualizacja stanu najnowszej wiadomości
            if selected_message["recipient_role"] == "admin":

                selected_message["is_read"] = True

            for message in messages:

                if message["thread_id"] == selected_message_id:

                    if message["recipient_role"] == "admin":

                        message["is_read"] = True

                    break

    return render_template("message.html", messages=messages, search_messages=search_messages,
                           selected_message=selected_message, thread_messages=thread_messages, is_admin=True,
                           users=users, search_user=search_user, selected_recipient_id=selected_recipient_id,
                           show_reply=show_reply, error=error, success=success,
                           compose_open=request.args.get("compose") == "1")
