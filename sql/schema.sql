-- 1) Create database
CREATE DATABASE IF NOT EXISTS alumni_management;
USE alumni_management;

-- 2) Master table: departments
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

-- 3) Main table: alumni
CREATE TABLE alumni (
    alumni_id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    graduation_year YEAR NOT NULL,
    current_company VARCHAR(120) NOT NULL,
    current_role VARCHAR(120) NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 4) Event table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(150) NOT NULL,
    event_date DATE NOT NULL,
    venue VARCHAR(150) NOT NULL,
    description TEXT NOT NULL
);

-- 5) Junction table for many-to-many (alumni <-> events)
CREATE TABLE registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    alumni_id INT NOT NULL,
    event_id INT NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attended TINYINT(1) DEFAULT 0,
    UNIQUE KEY unique_registration (alumni_id, event_id),
    FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO departments (department_name) VALUES
('Computer Science'), ('Electronics'), ('Mechanical'), ('Civil');

INSERT INTO alumni (department_id, full_name, email, phone, graduation_year, current_company, current_role) VALUES
(1, 'Aman Gupta', 'aman.gupta@example.com', '9876543210', 2021, 'Infosys', 'Software Engineer'),
(2, 'Neha Sharma', 'neha.sharma@example.com', '9876501234', 2020, 'TCS', 'Systems Analyst'),
(1, 'Rohit Verma', 'rohit.verma@example.com', '9811122233', 2019, 'Google', 'Backend Developer');

INSERT INTO events (event_name, event_date, venue, description) VALUES
('Annual Alumni Meet', '2026-07-20', 'Main Auditorium', 'Networking session with alumni and students'),
('Career Guidance Talk', '2026-08-15', 'Seminar Hall', 'Career roadmap and interview preparation');

INSERT INTO registrations (alumni_id, event_id, attended) VALUES
(1, 1, 1),
(2, 1, 0),
(3, 2, 0);

-- Example CRUD + JOIN queries for viva/demo
-- UPDATE example
UPDATE alumni SET current_company = 'Microsoft', current_role = 'SDE II' WHERE alumni_id = 1;

-- DELETE example
DELETE FROM registrations WHERE registration_id = 2;

-- SELECT with joins
SELECT a.full_name, d.department_name, e.event_name, r.attended
FROM registrations r
JOIN alumni a ON r.alumni_id = a.alumni_id
JOIN departments d ON a.department_id = d.department_id
JOIN events e ON r.event_id = e.event_id;
