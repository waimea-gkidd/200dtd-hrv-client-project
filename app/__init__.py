#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps

#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        #counting all the clients#
        res = client.execute("SELECT COUNT(*) AS c FROM clients", [])
        client_count = res.rows[0]["c"] if res.rows else 0  #defaulted if no rows as otherwise = crash#



        #last 5 clients#
        sql = "SELECT id, name, phone, email, status, notes FROM clients ORDER BY id DESC LIMIT 5"
        result = client.execute(sql, [])
        clients = result.rows

       



    #client list#
    return render_template(
        "pages/home.jinja",
        clients=clients,
        client_count=client_count
    )
        
#-----------------------------------------------------------
# Clients page
#-----------------------------------------------------------
@app.get("/clients")
def clients_page():
    return render_template("pages/clients.jinja")


#-----------------------------------------------------------
# Add a new client
#   (copied from flask-turso-intro)
#-----------------------------------------------------------
@app.post("/clients/add")
def add_client():
    #form values#
    name   = request.form.get("name")   or ""
    phone  = request.form.get("phone")  or ""
    email  = request.form.get("email")  or ""
    status = request.form.get("status") or ""
    notes  = request.form.get("notes")  or ""


    with connect_db() as client:
        client.execute(
            "INSERT INTO clients (name, phone, email, status, notes) VALUES (?, ?, ?, ?, ?)",
            [name, phone, email, status, notes]
        )

    #go back to clients page#
    return redirect("/clients")
#-----------------------------------------------------------
# Meetings page
#-----------------------------------------------------------
@app.get("/meetings")
def meetings_page():
    with connect_db() as client:
        #from thing.jinja (flask-turso-intro)#

        result = client.execute( """
            SELECT id, client_id, date, time, "type", location, notes
            FROM meetings
            ORDER BY id DESC
        """, [])
        meetings = result.rows

        sql = "SELECT id FROM clients ORDER BY name DESC"
        params = []
        result = client.execute(sql, params)
        clients = result.rows 



    return render_template("pages/meetings.jinja", meetings=meetings, clients=clients)


#-----------------------------------------------------------
# Add a new meeting
#  -copied from clients (copied from flask-turso-intro)
#-----------------------------------------------------------
@app.post("/meetings/add")
def add_meeting():
    client_id = request.form.get("client_id") or ""
    date      = request.form.get("date")      or ""
    time      = request.form.get("time")      or ""
    type      = request.form.get("type")      or ""
    location  = request.form.get("location")  or ""
    notes     = request.form.get("notes")     or ""



    with connect_db() as client:

        #from add-thing (flask-turso-intro)#
        sql = " INSERT INTO meetings (client_id, date, time, type, location, notes) VALUES (?, ?, ?, ?, ?, ?)"
        params = [client_id, date, time, type, location, notes]
        result = client.execute(sql, params)
        meetings = result.rows 
        

    return redirect("/meetings", meetings=meetings)

#-----------------------------------------------------------
# Follow-ups page: list + inline add form
#   - list query pattern from: template "Things.jinja"
#-----------------------------------------------------------
@app.get("/follow-ups")
def followups_page():
    with connect_db() as client:
        result = client.execute(
            """
            SELECT id, client_id, "type", priority, due_date, status, notes
            FROM "follow-ups"
            ORDER BY id DESC
            """,
            []
        )
        followups = result.rows

    return render_template("pages/follow-ups.jinja", followups=followups)


#-----------------------------------------------------------
# Add a new follow-up (inline form POST)
#   - INSERT & redirect copied from turso-intro add_thing
#-----------------------------------------------------------
@app.post("/follow-ups/add")
def add_followup():
    due_date  = request.form.get("due_date")  or ""
    priority  = request.form.get("priority")  or ""
    status    = request.form.get("status")    or ""
    type_     = request.form.get("type")      or ""
    notes     = request.form.get("notes")     or ""
    client_id = request.form.get("client_id") or ""

    with connect_db() as client:
        client.execute(
            """
            INSERT INTO "follow-ups" (client_id, "type", priority, due_date, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [client_id, type_, priority, due_date, status, notes]
        )

    return redirect("/follow-ups")
