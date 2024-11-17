CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE listings (
    name TEXT,
    age_months INTEGER,
    sex TEXT,
    location INTEGER REFERENCES locations,
    category INTEGER REFERENCES categories,
    species_breed TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visible BOOLEAN DEFAULT TRUE
);
