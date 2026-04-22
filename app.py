"""Flask application for Alumni Management System mini project."""
from datetime import datetime
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mysqldb import MySQL


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

# MySQL configuration (read from environment variables)
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "alumni_management")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def home():
    """Dashboard: list alumni, events, and registrations."""
    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT a.alumni_id, a.full_name, a.email, a.phone, d.department_name, a.graduation_year,
               a.current_company, a.current_role
        FROM alumni a
        JOIN departments d ON a.department_id = d.department_id
        ORDER BY a.alumni_id DESC
        """
    )
    alumni = cur.fetchall()

    cur.execute("SELECT department_id, department_name FROM departments ORDER BY department_name")
    departments = cur.fetchall()

    cur.execute(
        """
        SELECT e.event_id, e.event_name, e.event_date, e.venue, e.description,
               COUNT(r.registration_id) AS registrations_count
        FROM events e
        LEFT JOIN registrations r ON e.event_id = r.event_id
        GROUP BY e.event_id
        ORDER BY e.event_date DESC
        """
    )
    events = cur.fetchall()

    cur.execute(
        """
        SELECT r.registration_id, a.full_name, e.event_name, r.registered_at, r.attended
        FROM registrations r
        JOIN alumni a ON r.alumni_id = a.alumni_id
        JOIN events e ON r.event_id = e.event_id
        ORDER BY r.registration_id DESC
        """
    )
    registrations = cur.fetchall()

    cur.close()
    return render_template(
        "index.html",
        alumni=alumni,
        departments=departments,
        events=events,
        registrations=registrations,
    )


@app.route("/alumni/add", methods=["POST"])
def add_alumni():
    """Create a new alumni record."""
    form = request.form
    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO alumni (department_id, full_name, email, phone, graduation_year, current_company, current_role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            form["department_id"],
            form["full_name"],
            form["email"],
            form["phone"],
            form["graduation_year"],
            form["current_company"],
            form["current_role"],
        ),
    )
    mysql.connection.commit()
    cur.close()
    flash("Alumni added successfully.", "success")
    return redirect(url_for("home"))


@app.route("/alumni/<int:alumni_id>/delete", methods=["POST"])
def delete_alumni(alumni_id):
    """Delete alumni record by ID."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM alumni WHERE alumni_id = %s", (alumni_id,))
    mysql.connection.commit()
    cur.close()
    flash("Alumni deleted.", "success")
    return redirect(url_for("home"))


@app.route("/events/add", methods=["POST"])
def add_event():
    """Create a new event record."""
    form = request.form
    event_date = datetime.strptime(form["event_date"], "%Y-%m-%d").date()

    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO events (event_name, event_date, venue, description)
        VALUES (%s, %s, %s, %s)
        """,
        (form["event_name"], event_date, form["venue"], form["description"]),
    )
    mysql.connection.commit()
    cur.close()
    flash("Event created successfully.", "success")
    return redirect(url_for("home"))


@app.route("/registrations/add", methods=["POST"])
def add_registration():
    """Register an alumni for an event."""
    form = request.form
    cur = mysql.connection.cursor()
    cur.execute(
        """
        INSERT INTO registrations (alumni_id, event_id, attended)
        VALUES (%s, %s, %s)
        """,
        (form["alumni_id"], form["event_id"], form.get("attended", 0)),
    )
    mysql.connection.commit()
    cur.close()
    flash("Registration completed.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
