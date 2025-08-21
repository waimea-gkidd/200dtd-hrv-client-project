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
        # Get all the meetings from the DB
        sql = "SELECT id, name FROM clients ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        clients = result.rows

        return render_template("pages/home.jinja", clients=clients)


#-----------------------------------------------------------
# clients page route
#-----------------------------------------------------------
@app.get("/clients/")
def clients():
    return render_template("pages/clients.jinja")


#-----------------------------------------------------------
# meetings page route - Show all the meetings, and new follow-ups form
#-----------------------------------------------------------
@app.get("/meetings/")
def show_all_meetings():
    with connect_db() as client:
        # Get all the meetings from the DB
        sql = "SELECT id, name FROM meetings ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        meetings = result.rows

        # And show them on the page
        return render_template("pages/meetings.jinja", meetings=meetings)


#-----------------------------------------------------------
# follow-ups page route - Show details of a single follow-ups
#-----------------------------------------------------------
@app.get("/follow-ups/<int:id>")
def show_one_follow_ups(id):
    with connect_db() as client:
        # Get the follow-ups details from the DB
        sql = "SELECT id, name, price FROM meetings WHERE id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            follow_ups = result.rows[0]
            return render_template("pages/follow-ups.jinja", follow_ups=follow_ups)

        else:
            # No, so show error
            return not_found_error()


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


