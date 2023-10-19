
CREATE TABLE IF NOT EXISTS sport (
    name VARCHAR(255) PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN NOT NULL
);
CREATE TYPE  event_type AS ENUM ('preplay', 'inplay');
CREATE TYPE event_status AS ENUM ('Pending', 'Started', 'Ended', 'Cancelled');

CREATE TABLE IF NOT EXISTS event (
    name VARCHAR(255) PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN NOT NULL,
    type event_type NOT NULL,
    sport VARCHAR(255) REFERENCES sport(name),
    status event_status NOT NULL,
    scheduled_start TIMESTAMP WITH TIME ZONE NOT NULL,
    actual_start TIMESTAMP WITH TIME ZONE
);
CREATE TYPE outcome_type AS ENUM ('Unsettled', 'Void', 'Lose', 'Win');
CREATE TABLE IF NOT EXISTS selection (
    name VARCHAR(255),
    event VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN NOT NULL,
    outcome outcome_type NOT NULL,
    PRIMARY KEY (name, event),
    FOREIGN KEY (event) REFERENCES event(name)
);

-- Inserting data into the sport table
INSERT INTO sport (name, slug, active) VALUES ('Football', 'football', true);
INSERT INTO sport (name, slug, active) VALUES ('Basketball', 'basketball', true);

-- Inserting data into the event table
INSERT INTO event (name, slug, active, type, sport, status, scheduled_start)
VALUES ('Football Match 1', 'juventus Bohemians', true, 'preplay', 'Football', 'Pending', '2023-10-20 15:00:00+00');
INSERT INTO event (name, slug, active, type, sport, status, scheduled_start)
VALUES ('Basketball Match 1', 'Miami Brookling', true, 'preplay', 'Basketball', 'Pending', '2023-10-21 18:00:00+00');

-- Inserting data into the selection table
INSERT INTO selection (name, event, price, active, outcome) VALUES ('X', 'Football Match 1', 1.5, true, 'Unsettled');
INSERT INTO selection (name, event, price, active, outcome) VALUES ('1', 'Football Match 1', 2.0, true, 'Unsettled');
INSERT INTO selection (name, event, price, active, outcome) VALUES ('2', 'Football Match 1', 3.0, true, 'Unsettled');
INSERT INTO selection (name, event, price, active, outcome) VALUES ('X', 'Basketball Match 1', 1.8, true, 'Unsettled');
INSERT INTO selection (name, event, price, active, outcome) VALUES ('1', 'Basketball Match 1', 0.23, true, 'Unsettled');
INSERT INTO selection (name, event, price, active, outcome) VALUES ('2', 'Basketball Match 1', 4.5, true, 'Unsettled');
