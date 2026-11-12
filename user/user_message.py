
from flask import render_template, request, session, redirect, url_for
from user.user_message_database import (get_user_messages, get_user_message, get_user_thread_messages,
                                        send_user_message, mark_user_thread_read, hide_user_thread)

# skrzynka wiadomości dla użytkownika
def message_user():

    user_id = session["user_id"]

    error = None
    success = None

        #wyszukiwanie wiadomości
    search_messages = request.values.get("search_messages", "").strip()

    # Identyfikator wątku rozmowy.
    selected_message_id = request.args.get("message_id", type=int)

    show_reply = False

    # obsługa formularzy
    if request.method == "POST":

        action = request.form.get("action")


        # nowa wiadomość od admina
        if action == "send":

            subject = request.form.get("subject", "").strip()

            content = request.form.get("content", "").strip()

            if not subject or not content:

                error = "Wypełnij temat i treść wiadomości."

            elif len(subject) > 150:

                error = "Temat może mieć maksymalnie 150 znaków."

            else:

                thread_id = send_user_message(user_id, subject, content)

                if thread_id:

                    success = "Wiadomość została wysłana."

                    selected_message_id = thread_id

                else:

                    error = "Nie udało się wysłać wiadmości"


        # otwarcie wątku wiadomości
        elif action == "open":

            selected_message_id = request.form.get("message_id", type=int)

            if selected_message_id:

                return redirect(url_for("message", message_id=selected_message_id,
                                        search_messages=search_messages or None))


        #ukrycie całego wątku
        elif action == "delete_thread":

            thread_id = request.form.get("thread_id", type=int)

            if thread_id and hide_user_thread(user_id, thread_id):

                success = "Rozmowa została usunięta."

                selected_message_id = None

            else:

                error = "Nie udało się usunąć rozmowy."

        # formularz dla odpowiedzi
        elif action == "reply_form":

            selected_message_id = request.form.get("message_id", type=int)

            show_reply = True


        # odpowiedź w wątku
        elif action == "reply":

            selected_message_id = request.form.get("message_id", type=int)

            content = request.form.get("content", "").strip()

            selected_message = None

            if selected_message_id:

                selected_message = get_user_message(user_id, selected_message_id)

            if selected_message is None:

                error = "Nie znaleziono wybranej rozmowy."

            elif not content:

                error = "Wpisz treść odpowiedzi."

                show_reply = True

            else:

                original_subject = selected_message["subject"]

                if original_subject.lower().startswith("re:"):

                    reply_subject = original_subject

                else:

                    reply_subject = f"Re: {original_subject}"

                send_user_message(user_id, reply_subject, content, thread_id=selected_message_id)

                return redirect(url_for("message", message_id=selected_message_id))


    # filtrowanie listy wątków wiadomości.
    messages = get_user_messages(user_id, search_messages or None)


    # pobranie wybranej rozmowy oraz historii
    selected_message = None

    thread_messages = []

    if selected_message_id:

        selected_message = get_user_message(user_id, selected_message_id)

        if selected_message:

            thread_messages = get_user_thread_messages(user_id, selected_message_id)

            # oznaczenie jako przeczytane wiadomości
            mark_user_thread_read(user_id, selected_message_id)

            # aktalizacja stanu w wyświetlanych danych.
            for message in thread_messages:

                if (message["recipient_id"] == user_id and message["recipient_role"] == "user"):

                    message["is_read"] = True


            # aktualizacja statusu najnowszej wiadomości.
            if (selected_message["recipient_id"] == user_id and selected_message["recipient_role"] == "user"):

                selected_message["is_read"] = True

            for message in messages:

                if message["thread_id"] == selected_message_id:

                    if (message["recipient_id"] == user_id and message["recipient_role"] == "user"):

                        message["is_read"] = True

                    break


    return render_template("message.html", messages=messages, search_messages=search_messages,
                           selected_message=selected_message, thread_messages=thread_messages, is_admin=None, users=[],
                           show_reply=show_reply, error=error, success=success)