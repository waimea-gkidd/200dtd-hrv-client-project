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

        # Asks the db how many clients exist
        client_count = 0   # default set to 0 as there are no clients
        res = client.execute("SELECT COUNT(*) AS c FROM clients", [])
        if res.rows:
            client_count = res.rows[0]["c"]

        followup_count = 0   # To-do: when followups table is actually made
        task_count     = 0   # To-do: if tasks are added later

        # Recent clients (last 5). Using id DESC (descending) until updated
        sql = """
            SELECT id, name, phone, email, status, notes
            FROM clients
            ORDER BY id DESC
            LIMIT 5
        """
        result = client.execute(sql, [])
        clients = result.rows

    # Keep your template path the same
    return render_template("pages/home.jinja",
                           clients=clients,
                           client_count=client_count,
                           followup_count=followup_count,
                           task_count=task_count)


#-----------------------------------------------------------
# Clients page route (now actually lists clients)
#-----------------------------------------------------------
@app.get("/clients/")
def clients():
    with connect_db() as client:
        sql = """
          SELECT id, name, phone, email, status, notes
          FROM clients
          ORDER BY id DESC
        """
        result = client.execute(sql, [])
        clients = result.rows
    return render_template("pages/clients.jinja", clients=clients)


#-----------------------------------------------------------
# Meetings page route — safe even if table not ready
#-----------------------------------------------------------
@app.get("/meetings/")
def show_all_meetings():
    meetings = []
    with connect_db() as client:
        try:
            result = client.execute("SELECT id FROM meetings ORDER BY id DESC", [])
            meetings = result.rows
        except Exception:
            meetings = []  # if table is missing; list shows "None"
    return render_template("pages/meetings.jinja", meetings=meetings)


#-----------------------------------------------------------
# Follow-ups list route — placeholder so nav doesn't 404
#-----------------------------------------------------------
@app.get("/follow-ups")
def followups_list():
    return render_template("pages/follow-ups-list.jinja")


#-----------------------------------------------------------
# Route for adding a follow-ups, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_follow_ups():
    # Get the data from the form
    name  = request.form.get("name")
    price = request.form.get("price")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the follow-ups to the DB
        sql = "INSERT INTO meetings (name, price) VALUES (?, ?)"
        params = [name, price]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"follow-ups '{name}' added", "success")
        return redirect("/meetings")


#-----------------------------------------------------------
# Route for deleting a follow-ups, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_follow_ups(id):
    with connect_db() as client:
        # Delete the follow-ups from the DB
        sql = "DELETE FROM meetings WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("follow-ups deleted", "success")
        return redirect("/meetings")
#-----------------------------------------------------------
# Route for adding client form
#-----------------------------------------------------------
@app.get("/clients/new")
def new_client_form():
    return render_template("pages/clients_new.jinja")
#-----------------------------------------------------------
# route for posting new client from 'new client form
# into '/clients'
#-----------------------------------------------------------
@app.get("/clients")
def create_client(): 
#-----------------------------------------------------------
# Handle the form POST (actually add client to DB)
#-----------------------------------------------------------
@app.post("/clients")
def create_client():
    # grab the fields from the form (all text)
    name   = (request.form.get("name") or "").strip()
    phone  = (request.form.get("phone") or "").strip()
    email  = (request.form.get("email") or "").strip()
    status = (request.form.get("status") or "").strip()
    notes  = (request.form.get("notes") or "").strip()

    # quick check: must have a name or we complain
    if not name:
        flash("Name is required.", "error")  # show red message
        return redirect("/clients/new")

    # clean the text a little (stops weird symbols breaking HTML)
    name   = html.escape(name)
    phone  = html.escape(phone)
    email  = html.escape(email)
    status = html.escape(status)
    notes  = html.escape(notes)

    # now actually save into the DB
    with connect_db() as client:
        sql = """
            INSERT INTO clients (name, phone, email, status, notes)
            VALUES (?, ?, ?, ?, ?)
        """
        params = [name, phone, email, status, notes]
        client.execute(sql, params)

    # tell myself it worked
    flash("Client added.", "success")

    # then send me back to the client list
    return redirect("/clients/")







