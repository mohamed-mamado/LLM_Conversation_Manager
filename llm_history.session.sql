DROP TABLE masseges;
DROP TABLE converstion;
DROP TABLE user_history;
CREATE TABLE user_history (
    id_user SERIAL PRIMARY KEY,
    name TEXT,
    converstion_ids INTEGER [],
    date TIMESTAMP
);
CREATE TABLE converstion (
    converstion_id SERIAL PRIMARY KEY,
    history_arry TEXT [],
    last_summary TEXT,
    id_user INTEGER REFERENCES user_history(id_user)
);
CREATE TABLE masseges (
    chat_id SERIAL PRIMARY KEY,
    human_chat TEXT,
    human_chat_token INTEGER,
    date_human TIMESTAMP,
    ai_chat TEXT,
    ai_chat_token INTEGER,
    date_ai TIMESTAMP,
    summary TEXT,
    summary_token INTEGER,
    data JSONB,
    id_user INTEGER REFERENCES user_history(id_user),
    id_converstion INTEGER REFERENCES converstion(converstion_id)
);
SELECT *
FROM user_history;
SELECT *
FROM masseges;
SELECT *
FROM converstion;
SELECT id_user,
    converstion_ids AS converstion_id
FROM user_history
WHERE id_user = 0
    AND 1111 = ANY(converstion_ids);