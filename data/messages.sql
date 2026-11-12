USE users;


CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    sender_role VARCHAR(20) NOT NULL,
    recipient_id INT NULL,
    recipient_role VARCHAR(20) NOT NULL,
    subject VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

SHOW TABLES;
SELECT *FROM messages;

UPDATE messages
SET thread_id = id
WHERE thread_id IS NULL;
SHOW CREATE TABLE messages;

ALTER TABLE messages
ADD COLUMN thread_id INT NULL;

SELECT
    id,
    thread_id,
    sender_role,
    recipient_role,
    subject,
    created_at
FROM messages
ORDER BY id;

ALTER TABLE messages
ADD COLUMN is_automatic BOOLEAN NOT NULL DEFAULT FALSE;