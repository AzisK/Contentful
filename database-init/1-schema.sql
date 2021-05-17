-- Organization

CREATE TABLE organization (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE EXTENSION moddatetime;

CREATE TRIGGER organization_modified BEFORE UPDATE ON organization
FOR EACH ROW EXECUTE PROCEDURE moddatetime (modified);

-- App user

CREATE TABLE app_user (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE NOT NULL,
    plan_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    current BOOLEAN NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TRIGGER app_user_modified BEFORE UPDATE ON app_user
FOR EACH ROW EXECUTE PROCEDURE moddatetime (modified);

-- Active user count

CREATE TABLE user_active_count (
    date DATE PRIMARY KEY,
    count VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE NOT NULL,
    plan_name VARCHAR(255) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- User events

CREATE TABLE user_event (
    id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    username VARCHAR(255),
    user_email VARCHAR(255),
    user_type VARCHAR(255),
    organization_name VARCHAR(255) REFERENCES organization(name) ON DELETE CASCADE,
    plan_name VARCHAR(255),
    received_at TIMESTAMP NOT NULL,
    date DATE NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TRIGGER user_event_modified BEFORE UPDATE ON user_event
FOR EACH ROW EXECUTE PROCEDURE moddatetime (modified);

-- Table initialization by Python status

CREATE TYPE table_status AS ENUM ('Not Initialized', 'Running', 'Initialized');

CREATE TABLE init_table_by_python (
    table_name VARCHAR(255) PRIMARY KEY,
    table_status table_status DEFAULT 'Not Initialized'
);
