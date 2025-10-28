#===========================================================
# HRV Client Tracker — super simple, Billy-style
# Gideon Kidd
#-----------------------------------------------------------
# Pages:
#   - Home counts (how many clients, follow-ups and tasks) & recent clients literally previous clients
#   - Clients list % New Client form
#   - Meetings list & New Meeting form
#   - Follow-ups list gets input from meetings; no separate table is needed as follow-ups displays 
#   (there is no 'add follow-ups' button for this reason **important to keep in mind*)
#
# Notes:
# - DB patterns copied from class demos / some inspo from Billy’s project (only copied simplicity):
#   connect_db().execute(SQL, params).rows
# - CSS from PicoCSS CDN
#===========================================================
from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now
app = Flask(__name__)

#-----------------------------------------------------------
# Home page
#   - clients, follow-ups, and tasks count
#   - 5 most recent clients
#   (copied from your Flask-intro)
#-----------------------------------------------------------
@app.get("/")
def home():
    with connect_db() as db:
        # total clients
        res = db.execute("SELECT COUNT(*) AS c FROM clients", [])
        client_count = res.rows[0]["c"] if res.rows else 0

        # 5 most recent clients (simple DESC by id)
        res = db.execute(
            "SELECT id, name, phone, email, status, notes "
            "FROM clients ORDER BY id DESC LIMIT 5",
            []
        )
        recent_clients = res.rows

    return render_template(
        "pages/home.jinja",
        client_count=client_count,
        clients=recent_clients
    )

#-----------------------------------------------------------
# Clients — LIST
#   (Layout + simplicity copied from Billy’s list page)
#-----------------------------------------------------------
@app.get("/clients")
def clients_list():
    with connect_db() as db:
        res = db.execute(
            "SELECT id, name, phone, email, status, notes "
            "FROM clients ORDER BY id DESC",
            []
        )
        clients = res.rows
    return render_template("pages/clients.jinja", clients=clients)

#-----------------------------------------------------------
# New Client — FORM (GET)
#   (Separate form page like Billy: /addPiece, /addGlaze)
#-----------------------------------------------------------
@app.get("/clients/new")
def client_form():
    return render_template("pages/client-form.jinja")

#-----------------------------------------------------------
# New Client — POST
#-----------------------------------------------------------
@app.post("/clients/new")
def client_create():
    name   = request.form.get("name")   or ""
    phone  = request.form.get("phone")  or ""
    email  = request.form.get("email")  or ""
    status = request.form.get("status") or ""
    notes  = request.form.get("notes")  or ""

    with connect_db() as db:
        db.execute(
            "INSERT INTO clients (name, phone, email, status, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            [name, phone, email, status, notes]
        )

    return redirect("/clients")

#-----------------------------------------------------------
# Meetings — LIST
#   (shows client_id; join name)
#-----------------------------------------------------------
@app.get("/meetings")
def meetings_list():
    with connect_db() as db:
        # Join to show client name
        sql = '''
            SELECT
                m.id,
                m.client_id,
                c.name AS client_name,
                m.date,
                m.time,
                m."type",
                m.location,
                m.notes
            FROM meetings AS m
            LEFT JOIN clients AS c ON c.id = m.client_id
            ORDER BY m.id DESC
        '''
        res = db.execute(sql, [])
        meetings = res.rows

    return render_template("pages/meetings.jinja", meetings=meetings)

#-----------------------------------------------------------
# New Meeting — FORM (GET)
#   (<select> with id & name)
#-----------------------------------------------------------
@app.get("/meetings/new")
def meeting_form():
    with connect_db() as db:
        res = db.execute("SELECT id, name FROM clients ORDER BY name ASC", [])
        clients = res.rows
    return render_template("pages/meeting-form.jinja", clients=clients)

#-----------------------------------------------------------
# New Meeting — POST
#   Note: "type" has to be quoted in SQL, as a safeguard.
#-----------------------------------------------------------
@app.post("/meetings/new")
def meeting_create():
    client_id = request.form.get("client_id") or ""
    date      = request.form.get("date")      or ""
    time      = request.form.get("time")      or ""
    type_     = request.form.get("type")      or ""
    location  = request.form.get("location")  or ""
    notes     = request.form.get("notes")     or ""

    with connect_db() as db:
        db.execute(
            'INSERT INTO meetings (client_id, date, time, "type", location, notes) '
            "VALUES (?, ?, ?, ?, ?, ?)",
            [client_id, date, time, type_, location, notes]
        )

    return redirect("/meetings")

#-----------------------------------------------------------
# Follow-ups — LIST (from meetings)
#   This page JUST lists
#   meetings as “follow-ups.”
#   No use of the separate follow-ups table here 
#   (as a follow-up is = to a meeting). 
#-----------------------------------------------------------
@app.get("/follow-ups")
def followups_list():
    with connect_db() as db:
        sql = '''
            SELECT
                m.id,
                m.client_id,
                c.name AS client_name,
                m.date,
                m.time,
                m."type",
                m.location,
                m.notes
            FROM meetings AS m
            LEFT JOIN clients AS c ON c.id = m.client_id
            ORDER BY m.id DESC
        '''
        res = db.execute(sql, [])
        items = res.rows

    return render_template("pages/follow-ups.jinja", items=items)


#-----------------------------------------------------------
# Debug entrypoint (optional)
#-----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
