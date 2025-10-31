#===========================================================
# HRV Client Tracker — super simple, Billy-style
# Gideon Kidd
#-----------------------------------------------------------
# How pages are layedout and what they need done here:
#   -Home page: counts (how many clients, follow-ups, and tasks are displayed up top) as well as 
# recent clients which is literally previous clients
#   -Clients (list) and New clients (form)
#   -meetings (list) and New/schedule meeting (form) 
#   -follow-ups (list) displays the meetings. No actual meetings page is needed (unlike originally thought)
#   Keep in mind while coding: there is no 'add follow-up' button because of the above
#
# Notes:
# - DB patterns copied from class demos / some inspo from Billy’s project but I did not directly copy (call it a grey area?):
#   e.g. connect_db().execute(SQL, params).rows
# - CSS from pico
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
# HOME
#-----------------------------------------------------------
# Shows a count of total clients, total follow-ups (meetings), and total tasks (what needs done).
# Tasks are follow-ups because they’re the same thing (is it strange? yes. Most definitely).
# lists the 5 most recent clients.
# copied from the flask-intro 'home page' just changed the SQL.
#-----------------------------------------------------------
@app.get("/")

def home():

    with connect_db() as db:
        #total clients
        result = db.execute("SELECT COUNT(*) AS c FROM clients", [])
        client_count = result.rows[0]["c"] if result.rows else 0

        #follow-ups are just meetings here
        result = db.execute("SELECT COUNT(*) AS c FROM meetings", [])
        followups_count = result.rows[0]["c"] if result.rows else 0

        #tasks = follow-ups (probably an oversimplification but oh well)
        tasks_count = followups_count

        # 5 most recent clients
        result = db.execute(
            "SELECT id, name, phone, email, status, notes "
            "FROM clients ORDER BY id DESC LIMIT 5",
            []
        )
        clients = result.rows

    return render_template(
        "pages/home.jinja",
        client_count=client_count,
        followups_count=followups_count,
        tasks_count=tasks_count,
        clients=clients
    )

#-----------------------------------------------------------
# CLIENTS (list)
#-----------------------------------------------------------
# All clients in a list.
# copied from 'list things' page in flask-intro, renamed columns.
#-----------------------------------------------------------
@app.get("/clients")
def clients_list():
    with connect_db() as db:
        result = db.execute(
            "SELECT id, name, phone, email, status, notes "
            "FROM clients ORDER BY id DESC",
            []
        )
        clients = result.rows
    return render_template("pages/clients.jinja", clients=clients)

#-----------------------------------------------------------
# NEW CLIENT (FORM and POST)
#-----------------------------------------------------------
# copied 'add new thing' from flask-turso-intro.
# Separate form page (rather than both client pages being together) 
# and then a post route to add it.
#-----------------------------------------------------------
@app.get("/clients/new")
def client_form():
    return render_template("pages/client-form.jinja")

@app.post("/clients/new")
def client_create():
    name   = request.form.get("name")   or ""
    phone  = request.form.get("phone")  or ""
    email  = request.form.get("email")  or ""
    status = request.form.get("status") or ""
    notes  = request.form.get("notes")  or ""

    with connect_db() as db:
        db.execute(
            "INSERT INTO clients (name, phone, email, status, notes) VALUES (?, ?, ?, ?, ?)",
            [name, phone, email, status, notes]
        )

    return redirect("/clients")

#-----------------------------------------------------------
# MEETINGS / FOLLOW-UPS
#-----------------------------------------------------------
# I didn’t make a 'meetings' page (list). Scheduling/adding a meeting
# adds it to follow-ups too. So you just use the form and it shows up there :).
#-----------------------------------------------------------

#@app.get("/meetings")
#def meetings_redirect():
    # sends straight to follow-ups instead of a separate meetings page
#    return redirect("/follow-ups")      *this redirect is commented out because I dont think its needed 

@app.get("/meetings/new")
def meeting_form():
    #all clients in a dropdown (while not a searchbar but better than typing in SQL NO. for each client)
    with connect_db() as db:
        result = db.execute("SELECT id, name FROM clients ORDER BY name ASC", [])
        clients = result.rows
    return render_template("pages/meeting-form.jinja", clients=clients)

@app.post("/meetings/new")
def meeting_create():
    client_id = request.form.get("client_id") or ""
    date      = request.form.get("date")      or ""
    time      = request.form.get("time")      or ""
    type_     = request.form.get("type")      or ""
    location  = request.form.get("location")  or ""
    notes     = request.form.get("notes")     or ""

    with connect_db() as db:
        #type is quoted because it was apparently breaking my code once upon a time (chatgpt helped with that one I admit)
        #also was in one of the previous codes
        db.execute(
            'INSERT INTO meetings (client_id, date, time, "type", location, notes) VALUES (?, ?, ?, ?, ?, ?)',
            [client_id, date, time, type_, location, notes]
        )

    return redirect("/follow-ups")

#-----------------------------------------------------------
# FOLLOW-UPS PAGE
#-----------------------------------------------------------
# This page lists everything from the meetings form (like how meetings would have).
# copied from 'list things' in flask-intro.
#-----------------------------------------------------------
@app.get("/follow-ups")
def followups_list():
    with connect_db() as db:
        result = db.execute(
            "SELECT id, client_id, date, time, type, location, notes FROM meetings ORDER BY id DESC",
            []
        )
        items = result.rows
    return render_template("pages/follow-ups.jinja", items=items)
#-----------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True) 
##