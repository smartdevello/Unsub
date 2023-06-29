DROP TABLE IF EXISTS unsub_emails;

CREATE TABLE unsub_emails (
    email    TEXT PRIMARY KEY,
    processed BOOLEAN DEFAULT 0
);