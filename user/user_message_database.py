
from database import get_connection

# pobranie listy wątków użutkownika oraz pomija ukryte wiadomości

def get_user_messages(user_id, search_term=None):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    search_pattern = None

    if search_term:

        search_pattern = f"%{search_term.strip()}%"

    try:

        cursor.execute("""
            SELECT
                messages.*,
                CASE
                    WHEN messages.sender_role = 'admin'
                        THEN 'Administrator'
                    ELSE COALESCE(users.username, 'Użytkownik')
                END AS sender_username

            FROM messages

            LEFT JOIN users
                ON users.id = messages.sender_id

            WHERE messages.id = (
                SELECT MAX(m2.id)
                FROM messages AS m2
                WHERE m2.thread_id = messages.thread_id
            )

            AND EXISTS (
                SELECT 1
                FROM messages AS m3
                WHERE m3.thread_id = messages.thread_id
                  AND (
                      (
                          m3.sender_id = %s
                          AND m3.sender_role = 'user'
                      )
                      OR
                      (
                          m3.recipient_id = %s
                          AND m3.recipient_role = 'user'
                      )
                  )
            )

            AND NOT EXISTS (
                SELECT 1
                FROM hidden_message_threads AS h
                WHERE h.user_id = %s
                  AND h.user_role = 'user'
                  AND h.thread_id = messages.thread_id
            )
            
            AND (
                %s IS NULL

                OR messages.subject COLLATE utf8mb4_0900_ai_ci LIKE %s

                OR messages.content COLLATE utf8mb4_0900_ai_ci LIKE %s

                OR EXISTS (
                    SELECT 1
                    FROM messages AS m4

                    LEFT JOIN users AS u4
                        ON u4.id = m4.sender_id

                    WHERE m4.thread_id = messages.thread_id

                        AND (
                            m4.subject COLLATE utf8mb4_0900_ai_ci LIKE %s

                            OR m4.content COLLATE utf8mb4_0900_ai_ci LIKE %s

                            OR COALESCE(u4.username, '') COLLATE utf8mb4_0900_ai_ci LIKE %s
                        )
                )
            )
            
            ORDER BY messages.created_at DESC, messages.id DESC""", (user_id, user_id, user_id, search_pattern,
                                                                     search_pattern, search_pattern, search_pattern,
                                                                     search_pattern, search_pattern))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# pobiera najnowższą wiadomość w wątku
def get_user_message(user_id, thread_id):


    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                messages.*,
                CASE
                    WHEN messages.sender_role = 'admin'
                        THEN 'Administrator'
                    ELSE COALESCE(users.username, 'Użytkownik')
                END AS sender_username

            FROM messages

            LEFT JOIN users
                ON users.id = messages.sender_id

            WHERE messages.thread_id = %s

              AND EXISTS (
                  SELECT 1
                  FROM messages AS m2
                  WHERE m2.thread_id = messages.thread_id
                    AND (
                        (
                            m2.sender_id = %s
                            AND m2.sender_role = 'user'
                        )
                        OR
                        (
                            m2.recipient_id = %s
                            AND m2.recipient_role = 'user'
                        )
                    )
              )

              AND NOT EXISTS (
                  SELECT 1
                  FROM hidden_message_threads AS h
                  WHERE h.user_id = %s
                    AND h.user_role = 'user'
                    AND h.thread_id = messages.thread_id
              )
              
              ORDER BY messages.created_at DESC, messages.id DESC LIMIT 1""", (thread_id, user_id, user_id, user_id))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()

# pobiera całą histroię wątku
def get_user_thread_messages(user_id, thread_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                messages.*,
                CASE
                    WHEN messages.sender_role = 'admin'
                        THEN 'Administrator'
                    ELSE COALESCE(users.username, 'Użytkownik')
                END AS sender_username

            FROM messages

            LEFT JOIN users
                ON users.id = messages.sender_id

            WHERE messages.thread_id = %s

              AND EXISTS (
                  SELECT 1
                  FROM messages AS m2
                  WHERE m2.thread_id = messages.thread_id
                    AND (
                        (
                            m2.sender_id = %s
                            AND m2.sender_role = 'user'
                        )
                        OR
                        (
                            m2.recipient_id = %s
                            AND m2.recipient_role = 'user'
                        )
                    )
              )

              AND NOT EXISTS (
                  SELECT 1
                  FROM hidden_message_threads AS h
                  WHERE h.user_id = %s
                    AND h.user_role = 'user'
                    AND h.thread_id = messages.thread_id
              )
              
              ORDER BY messages.created_at ASC, messages.id ASC""", (thread_id, user_id, user_id, user_id))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# wysłąnie nowej wiadomości lub odpowiedzi
def send_user_message(user_id, subject, content, thread_id=None):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        if thread_id is not None:

            # sprawdza, czy użytkownik uczestniczy w wątku.
            cursor.execute("""
                SELECT id
                FROM messages
                WHERE thread_id = %s
                  AND (
                      (
                          sender_id = %s
                          AND sender_role = 'user'
                      )
                      OR
                      (
                          recipient_id = %s
                          AND recipient_role = 'user'
                      )
                  )
                LIMIT 1
            """, (thread_id, user_id, user_id))

            if cursor.fetchone() is None:

                raise ValueError("Nie znaleziono wątku lub brak dostępu.")

            # Sprawdza, czy użytkownik ukrył cały wątek.
            cursor.execute("""
                SELECT id
                FROM hidden_message_threads
                WHERE user_id = %s
                  AND user_role = 'user'
                  AND thread_id = %s
                LIMIT 1
            """, (user_id, thread_id))

            if cursor.fetchone() is not None:

                raise ValueError("Nie można odpowiedzieć w ukrytym wątku.")

        # wysłąnie wiadomości do administratora.
        cursor.execute("""
            INSERT INTO messages (
                thread_id,
                sender_id,
                sender_role,
                recipient_id,
                recipient_role,
                subject,
                content,
                is_read
            )
            VALUES (
                %s,
                %s,
                'user',
                NULL,
                'admin',
                %s,
                %s,
                FALSE
            )
        """, (
            thread_id,
            user_id,
            subject,
            content
        ))

        message_id = cursor.lastrowid

        # ID pierwszej wiadomości staje się ID wątku.
        if thread_id is None:

            thread_id = message_id

            cursor.execute("""UPDATE messages SET thread_id = %s WHERE id = %s""", (thread_id, message_id))

        connection.commit()

        return thread_id

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

# wiadomości oznaczone w wątku jako przeczytane
def mark_user_thread_read(user_id, thread_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Sprawdza, czy użytkownik uczestniczy w rozmowie.
        cursor.execute("""
            SELECT id
            FROM messages
            WHERE thread_id = %s
            AND (
                (sender_id = %s AND sender_role = 'user')
                OR
                (recipient_id = %s AND recipient_role = 'user')
            )
            LIMIT 1
        """, (thread_id, user_id, user_id))

        thread_exists = cursor.fetchone()

            #jeśli nie uczetniczy w rozmowie nic nie zmieniamy
        if not thread_exists:

            return

            #oznaczenie jako przeczytana
        cursor.execute("""
            UPDATE messages
            SET is_read = TRUE
            WHERE thread_id = %s
            AND recipient_id = %s
            AND recipient_role = 'user'
        """, (thread_id, user_id))

        connection.commit()

    finally:

        cursor.close()
        connection.close()

# ukrywa cały wątek
def hide_user_thread(user_id, thread_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM messages
            WHERE thread_id = %s
              AND (
                  (sender_id = %s AND sender_role = 'user')
                  OR
                  (recipient_id = %s AND recipient_role = 'user')
              )
            LIMIT 1
        """, (thread_id, user_id, user_id))

        if cursor.fetchone() is None:

            return False

        cursor.execute("""
            INSERT IGNORE INTO hidden_message_threads (
                user_id,
                user_role,
                thread_id
            )
            VALUES (%s, 'user', %s)
        """, (user_id, thread_id))

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

#pobiera liczbę nie przeczytanych wiadomości
def get_user_unread_messages_count(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT COUNT(*) AS unread_count
            FROM messages
            WHERE recipient_id = %s
              AND recipient_role = 'user'
              AND is_read = FALSE
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        return result["unread_count"] if result else 0

    finally:

        cursor.close()
        connection.close()
