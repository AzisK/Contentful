CREATE TABLE organization (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE EXTENSION moddatetime;

CREATE TRIGGER organization_modified BEFORE UPDATE ON organization
FOR EACH ROW EXECUTE PROCEDURE moddatetime (modified);

-- Table initialization by Python status

CREATE TYPE table_status AS ENUM ('Not Initialized', 'Running', 'Initialized');

CREATE TABLE init_table_by_python (
    table_name VARCHAR(255) PRIMARY KEY,
    table_status table_status DEFAULT 'Not Initialized'
);
