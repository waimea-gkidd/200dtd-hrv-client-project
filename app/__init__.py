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
        {#counting all the clients#}
        res = client.execute("SELECT COUNT(*) AS c FROM clients", [])
        client_count = res.rows[0]["c"] if res.rows else 0  {#defaulted if no rows as otherwise = crash#}

        {#last 5 clients#)
        sql = "SELECT id, name, phone, email, status, notes FROM clients ORDER BY id DESC LIMIT 5"
        result = client.execute(sql, [])
        clients = result.rows

    {#client list#}
    return render_template(
        "pages/home.jinja",
        clients=clients,
        client_count=client_count
    )
        
#-----------------------------------------------------------
# Clients page: list + inline add form
#   - list query pattern from: template "Things.jinja"
#-----------------------------------------------------------
@app.get("/clients")
def clients_page():
    with connect_db() as client:
        sql = "SELECT id, name, phone, email, status, notes FROM clients ORDER BY id DESC"
        result = client.execute(sql, [])
        clients = result.rows

    return render_template("pages/clients.jinja", clients=clients)


#-----------------------------------------------------------
# Add a new client
#   (copied from flask-turso-intro)
#-----------------------------------------------------------
@app.post("/clients/add")
def add_client():
    {#form values#}
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

    {#go back to clients page#}
    return redirect("/clients")
