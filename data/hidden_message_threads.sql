USE users;

CREATE TABLE hidden_message_threads (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    user_role VARCHAR(20) NOT NULL,
    thread_id INT NOT NULL,
    hidden_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY unique_hidden_thread (
        user_id,
        user_role,
        thread_id
    )
);

SELECT *FROM hidden_message_threads;
