
from database import get_connection


# pobranie listy wątdków
def get_admin_messages(admin_id, search_term=None):

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
                          AND m3.sender_role = 'admin'
                      )
                      OR
                      (
                          m3.recipient_role = 'admin'
                      )
                  )
            )

            AND NOT EXISTS (
                SELECT 1
                FROM hidden_message_threads AS h
                WHERE h.user_id = %s
                  AND h.user_role = 'admin'
                  AND h.thread_id = messages.thread_id
            )
            
            AND (
                NOT EXISTS (
                    SELECT 1
                    FROM messages AS automatic_message
                    WHERE automatic_message.thread_id = messages.thread_id
                      AND automatic_message.is_automatic = TRUE
                )      
                OR EXISTS (
                    SELECT 1
                    FROM messages AS user_reply
                    WHERE user_reply.thread_id = messages.thread_id  
                      AND user_reply.sender_role = 'user'
                )
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
            
            ORDER BY messages.created_at DESC, messages.id DESC""", (admin_id, admin_id, search_pattern, search_pattern,
                                                                     search_pattern, search_pattern, search_pattern,
                                                                     search_pattern))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# pobiera najnowszą wiadomość w wątku
def get_admin_message(admin_id, thread_id):

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
                            AND m2.sender_role = 'admin'
                        )
                        OR
                        (
                            m2.recipient_role = 'admin'
                        )
                    )
              )

              AND NOT EXISTS (
                  SELECT 1
                  FROM hidden_message_threads AS h
                  WHERE h.user_id = %s
                    AND h.user_role = 'admin'
                    AND h.thread_id = messages.thread_id
              )
              
              ORDER BY messages.created_at DESC, messages.id DESC LIMIT 1""", (thread_id, admin_id, admin_id))

        return cursor.fetchone()

    finally:

        cursor.close()
        connection.close()

# pobranie całej historii wątku
def get_admin_thread_messages(admin_id, thread_id):

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
                            AND m2.sender_role = 'admin'
                        )
                        OR
                        (
                            m2.recipient_role = 'admin'
                        )
                    )
              )

              AND NOT EXISTS (
                  SELECT 1
                  FROM hidden_message_threads AS h
                  WHERE h.user_id = %s
                    AND h.user_role = 'admin'
                    AND h.thread_id = messages.thread_id
              )
              
              ORDER BY messages.created_at ASC, messages.id ASC""", (thread_id, admin_id, admin_id))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# pobranie użytkowników
def get_users_for_messages():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""SELECT id, username FROM users WHERE role != 'admin' ORDER BY username""")

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# wyszukiwanie użytkowników
def search_users_for_messages(search_user):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        search_pattern = f"%{search_user.strip()}%"

        cursor.execute("""SELECT id, username, email FROM users WHERE role != 'admin' AND (username LIKE %s 
        OR email LIKE %s) ORDER BY username""", (search_pattern, search_pattern))

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()

# wysłanie nowej wiadomości lub odpowiedzi
def send_admin_message(admin_id, recipient_id, subject, content, thread_id=None, is_automatic=False):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        if thread_id is not None:

            # sprawdza kogo dotyczy wątek
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
            """, (thread_id, recipient_id, recipient_id))

            if cursor.fetchone() is None:

                raise ValueError("Nie znaleziono wątku dla wybranego użytkownika.")

            # sprawdza ukrycie wątku
            cursor.execute("""SELECT id FROM hidden_message_threads WHERE user_id = %s AND user_role = 'admin'
             AND thread_id = %s LIMIT 1""", (admin_id, thread_id))

            if cursor.fetchone() is not None:

                raise ValueError("Nie można odpowiedzieć w ukrytym wątku.")

        # wysłanie wiadmości do danego użytkownika
        cursor.execute("""
            INSERT INTO messages (
                thread_id,
                sender_id,
                sender_role,
                recipient_id,
                recipient_role,
                subject,
                content,
                is_read,
                is_automatic
            )
            VALUES (
                %s,
                %s,
                'admin',
                %s,
                'user',
                %s,
                %s,
                FALSE,
                %s
            )
        """, (
            thread_id,
            admin_id,
            recipient_id,
            subject,
            content,
            is_automatic
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

# wysyłanie wiadomości do wszystkich
def send_admin_message_to_all(admin_id, subject, content):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""SELECT id FROM users WHERE role != 'admin' """)

        users = cursor.fetchall()

        if not users:

            return 0

        for user in users:

            recipient_id = user[0]

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
                    NULL,
                    %s,
                    'admin',
                    %s,
                    'user',
                    %s,
                    %s,
                    FALSE
                )
            """, (
                admin_id,
                recipient_id,
                subject,
                content
            ))

            message_id = cursor.lastrowid

            cursor.execute("""UPDATE messages SET thread_id = %s WHERE id = %s""", (message_id, message_id))

        connection.commit()

        return len(users)

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

# oznaczenie wątku wiadmości
def mark_admin_thread_read(thread_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE messages
            SET is_read = TRUE
            WHERE thread_id = %s
              AND recipient_role = 'admin'
              AND EXISTS (
                  SELECT 1
                  FROM (
                      SELECT thread_id
                      FROM messages
                      WHERE thread_id = %s
                        AND (
                            sender_role = 'admin'
                            OR recipient_role = 'admin'
                        )
                  ) AS authorized_thread
                  WHERE authorized_thread.thread_id = messages.thread_id
              )
        """, (thread_id, thread_id))

        connection.commit()

    finally:

        cursor.close()
        connection.close()

#ukrycie pełnego wątku
def hide_admin_thread(admin_id, thread_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM messages
            WHERE thread_id = %s
              AND (
                  (sender_id = %s AND sender_role = 'admin')
                  OR
                  recipient_role = 'admin'
              )
            LIMIT 1
        """, (thread_id, admin_id))

        if cursor.fetchone() is None:

            return False

        cursor.execute("""
            INSERT IGNORE INTO hidden_message_threads (
                user_id,
                user_role,
                thread_id
            )
            VALUES (%s, 'admin', %s)
        """, (admin_id, thread_id))

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        raise

    finally:

        cursor.close()
        connection.close()

#licznik nieprzeczytanych wiadomości
def get_admin_unread_messages_count():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute("""SELECT COUNT(*) AS unread_count FROM messages WHERE recipient_role = 'admin'
              AND is_read = FALSE""")

        result = cursor.fetchone()

        return result["unread_count"] if result else 0

    finally:

        cursor.close()
        connection.close()
