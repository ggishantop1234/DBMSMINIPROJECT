# Alumni Management System (DBMS Mini Project)

A practical mini project using **MySQL + Python Flask** with working CRUD, joins, and normalized schema.

## Problem Statement
Colleges struggle to maintain centralized alumni records and engagement history. This project stores alumni data, department mapping, events, and event registrations in a relational database for fast retrieval and reporting.

## Tech Stack
- MySQL
- Python (Flask)
- HTML + Bootstrap

## ER Diagram (How to draw)
Entities and relationships:
1. **departments** (1) ---- (M) **alumni**
2. **alumni** (M) ---- (M) **events** via **registrations**

Draw these entities with PK/FK labels:
- departments(department_id PK)
- alumni(alumni_id PK, department_id FK)
- events(event_id PK)
- registrations(registration_id PK, alumni_id FK, event_id FK)

## Normalization (quick viva notes)
- **1NF**: Atomic columns (no multi-valued fields).
- **2NF**: Non-key attributes depend on full primary key (handled by separate registrations table for M:N relation).
- **3NF**: No transitive dependency; department name stored in departments table, not repeated in alumni.

## Run Steps (Terminal)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit DB password
mysql -u root -p < sql/schema.sql
python app.py
```
Open: http://127.0.0.1:5000

## Features Implemented
- Add/Delete alumni
- Add events
- Register alumni to events
- Dashboard with JOIN-based reports

## Viva Questions (with short answers)
1. **Why registrations table?**
   - To model many-to-many relation between alumni and events.
2. **Which normal form is this schema in?**
   - Up to 3NF.
3. **What is a foreign key?**
   - A column that references primary key of another table to enforce referential integrity.
4. **Why use JOINs?**
   - To fetch meaningful combined data from normalized tables.
5. **How do you prevent duplicate event registration?**
   - Unique constraint on (alumni_id, event_id).

## Expected Output Screens
1. Dashboard with forms (Add Alumni, Add Event, Registration)
2. Alumni list table
3. Event registration report table
4. Registration history table
