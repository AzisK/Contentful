-- Organization

CREATE TABLE organization (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE EXTENSION moddatetime;

CREATE TRIGGER organization_modified BEFORE UPDATE ON organization
FOR EACH ROW EXECUTE PROCEDURE moddatetime (modified);

-- User

CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE NOT NULL,
    plan_name VARCAHR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    current BOOLEAN NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- User

CREATE TABLE user_active_count (
    date DATE PRIMARY KEY,
    count VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE NOT NULL,
    plan_name VARCAHR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- User events

CREATE TABLE user_event (
    id VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_type VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE NOT NULL,
    plan_name VARCAHR(255) NOT NULL,
    received_at TIMESTAMP NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table initialization by Python status

CREATE TYPE table_status AS ENUM ('Not Initialized', 'Running', 'Initialized');

CREATE TABLE init_table_by_python (
    table_name VARCHAR(255) PRIMARY KEY,
    table_status table_status DEFAULT 'Not Initialized'
);
