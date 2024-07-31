CREATE TABLE "Group" (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(10) CHECK (role IN ('admin', 'user')) NOT NULL,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES "Group" (group_id)
);

CREATE TABLE "Prompt" (
    prompt_id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    price NUMERIC(10, 2) DEFAULT 1000,
    state VARCHAR(10) CHECK (state IN ('pending', 'active', 'review', 'reminder', 'to_delete')) NOT NULL,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "User" (user_id)
);

CREATE TABLE "Vote" (
    vote_id SERIAL PRIMARY KEY,
    prompt_id INTEGER,
    user_id INTEGER,
    vote_value INTEGER CHECK (vote_value IN (1, 2)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES "Prompt" (prompt_id),
    FOREIGN KEY (user_id) REFERENCES "User" (user_id)
);

CREATE TABLE "Rating" (
    rating_id SERIAL PRIMARY KEY,
    prompt_id INTEGER,
    user_id INTEGER,
    rating_value INTEGER CHECK (rating_value BETWEEN -10 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES "Prompt" (prompt_id),
    FOREIGN KEY (user_id) REFERENCES "User" (user_id)
);
