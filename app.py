# Standard library modules
import os
import datetime
import random
import sqlite3
from tempfile import mkdtemp
from functools import wraps

# Non-standard modules
from flask import Flask, flash, redirect, render_template, request, session
from flask_caching import Cache
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import pylibmc
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Other files within application
import helpers # Contains functions to support the main routes.
import config # Contains large or repeatedly used data.

# Configure application
app = Flask(__name__)

# Auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached. Sourced from CS50.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure Memcache for session storage, following this Heroku guide:
# https://devcenter.heroku.com/articles/flask-memcache
cache = Cache()
cache_servers = os.environ.get('MEMCACHIER_SERVERS')
if cache_servers == None:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    cache.init_app(app,
        config={'CACHE_TYPE': 'saslmemcached',
                'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                'CACHE_MEMCACHED_USERNAME': cache_user,
                'CACHE_MEMCACHED_PASSWORD': cache_pass,
                'CACHE_OPTIONS': { 'behaviors': {
                    # Faster IO
                    'tcp_nodelay': True,
                    # Keep connection alive
                    'tcp_keepalive': True,
                    # Timeout for set/get requests
                    'connect_timeout': 2000, # ms
                    'send_timeout': 750 * 1000, # us
                    'receive_timeout': 750 * 1000, # us
                    '_poll_timeout': 2000, # ms
                    # Better failover
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30}}})
    app.config.update(
        SESSION_TYPE = 'memcached',
        SESSION_MEMCACHED =
            pylibmc.Client(cache_servers.split(','), binary=True,
                            username=cache_user, password=cache_pass,
                            behaviors={
                                # Faster IO
                                'tcp_nodelay': True,
                                # Keep connection alive
                                'tcp_keepalive': True,
                                # Timeout for set/get requests
                                'connect_timeout': 2000, # ms
                                'send_timeout': 750 * 1000, # us
                                'receive_timeout': 750 * 1000, # us
                                '_poll_timeout': 2000, # ms
                                # Better failover
                                'ketama': True,
                                'remove_failed': 1,
                                'retry_timeout': 2,
                                'dead_timeout': 30,
                            })
    )
Session(app)

# TEMPORARY FOR FLASK LOCAL TESTING ONLY.
# Configure session to use filesystem,
# (instead of signed cookies), sourced from CS50.
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# SQLalchemy has removed support for postgress:// scheme which is used
# by Heroku Postgres, the below maintains compatibility.
# https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Connect to database.
engine = create_engine(uri)
db = scoped_session(sessionmaker(bind=engine))

# Commit and close database.
def db_close():
    db.commit()
    db.close()

# Check user is logged in, sourced from CS50.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            print("LOGIN_REQUIRED - user_id is None.")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Login an already registered user.
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear previous user_id.
    session.clear()

    # If reached by get, present login form.
    if request.method == "GET":
        return render_template("login.html")

    # If reached by post, check input and then log the user in.
    if request.method == "POST":
        # Ensure username was entered.
        if not request.form.get("username"):
            flash("Username was not entered, please enter a username.")
            return render_template("/login.html")
        else:
            username = request.form.get("username")
        # Ensure password was entered.
        if not request.form.get("password"):
            flash("Password was not entered, please enter password.")
            return render_template("/login.html")
        # Check database for username and password.
        SQL = "SELECT * FROM users WHERE username = (:username)"
        data = {"username": username}
        rows = db.execute(SQL, data).fetchall()
        # Commit & close database connection.
        db_close()
        # Check if password matches or if no password found in database.
        if len(rows) != 1 or not check_password_hash(rows[0]["hashed_password"], request.form.get("password")):
            flash("Username and/or password does not match.")
            return render_template("/login.html")
        # Remember user has logged in and set current cube to blank.
        session["user_id"] = rows[0]["id"]
        session["current_cube_id"] = 0
        session["username"] = username
        # Redirect to homepage.
        return redirect("/")


# Logout the current user.
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


# Register a new user.
@app.route("/register", methods=["GET", "POST"])
def register():
    # If user has not submitted form information (arrived via GET).
    if request.method == "GET":
        return render_template("register.html")

    # If user has submitted a form (arrived via POST).
    if request.method == "POST":
        # Check that username has been entered.
        if not request.form.get("username"):
            flash("Username required.")
            return redirect("/register")
        else:
            username = request.form.get("username")
        # Check that username does not already exist.
        SQL = "SELECT username FROM users WHERE username = :username"
        data = {"username": username}
        existing_username = db.execute(SQL, data).fetchall()
        # Close database connection.
        db_close()
        # If username already exists, alert user and return.
        if existing_username:
            flash("Username " + username + " already exists.")
            return redirect("/register")
        # Check that password has been entered.
        password = request.form.get("password")
        if not password:
            flash("Password required.")
            return redirect("/register")
        # Check that second password entry matches the first.
        if not password == request.form.get("confirmation"):
            flash("Passwords do not match.")
            return redirect("/register")
        # Check password has at least 8 characters.
        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect("/register")
        # Check password has at least 1 number.
        if not any(character.isdigit() for character in password):
            flash("Password must contain at least 1 number.")
            return redirect("/register")
        # Hash password
        hashed = generate_password_hash(password, "sha256")
        # Submit username and hashed password to database.
        SQL = "INSERT INTO users (username, hashed_password) VALUES (:username, :hashed)"
        data = {"username": username, "hashed": hashed}
        db.execute(SQL, data)
        # Automatically log user in.
        SQL = "SELECT id FROM users WHERE username = (:username)"
        data = {"username": username}
        user_id = db.execute(SQL, data).fetchall()
        session['user_id'] = user_id[0]["id"]
        session["username"] = username
        # Commit & close database connection.
        db_close()
        # Send user to homepage after registration and login complete.
        flash(f"You have been registered successfully with username: {username}.")
        return redirect("/")


# Create a Guest user.
@app.route("/guest")
def guest():
        # Submit generic guest username in order to get a unique user ID.
        SQL = "INSERT INTO users (username) VALUES (:username)"
        data = {"username": "guest tbc"}
        db.execute(SQL, data)
        # Get user ID to include the ID in the guest username.
        SQL = "SELECT id FROM users WHERE username = (:username)"
        data = {"username": "guest tbc"}
        user_rows = db.execute(SQL, data).fetchone()
        user_id = user_rows[0]
        # Update generic guest username to include their user ID.
        new_guest_username = f"Guest {user_id}"
        SQL = "UPDATE users SET (username) = row(:new_guest_username) WHERE (id) = (:user_id)"
        data = ({"new_guest_username": new_guest_username, "user_id": user_id})
        db.execute(SQL, data)
        # Automatically log user in.
        session['user_id'] = user_id
        session["username"] = new_guest_username
        # Commit & close database connection.
        db_close()
        # Send user to homepage after registration and login complete.
        return redirect("/")


# Load this users cubes, ready for display.
def load_users_cubes():
    # Display previously entered cubes for this user.
    SQL = "SELECT * FROM cubes WHERE user_id = (:user_id) ORDER BY id DESC"
    data = {"user_id": session["user_id"]}
    users_cubes = db.execute(SQL, data).fetchall()
    # Close database connection.
    db_close()
    return users_cubes


# Default route, homepage.
@app.route("/")
@login_required
def index():
    # Load users cubes and render homepage.
    users_cubes = load_users_cubes()
    return render_template("index.html", users_cubes=users_cubes)


# Display only loading table.
@app.route("/load_page", methods=["GET"])
@login_required
def load_page():
    # Load users cubes and render load page.
    users_cubes = load_users_cubes()
    return render_template("load.html", users_cubes=users_cubes)


# Route to delete existing cube.
@app.route("/delete_cube", methods=["POST"])
@login_required
def delete_cube():
    # Delete the selected cube from the database.
    cube_to_delete = request.form.get("delete")
    SQL = "DELETE FROM cubes WHERE id = :cube_to_delete"
    data = {"cube_to_delete": cube_to_delete}
    db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    # If sessions current cube is the cube to be deleted, set current cube to zero.
    if session["current_cube_id"] == cube_to_delete:
        session["current_cube_id"] = 0
    # Alert user to successful deletion and return to homepage.
    flash("Cube ID " + cube_to_delete + " successfully deleted.")
    return redirect("/")


# Delete all cubes of this user.
@app.route("/delete_all_cubes", methods=["GET"])
@login_required
def delete_all_cubes():
    # Delete all cubes that belong to this user.
    SQL = "DELETE FROM cubes WHERE user_id = :user_id"
    data = {"user_id": session["user_id"]}
    db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    # Set current cube to zero.
    session["current_cube_id"] = 0
    # Alert user to successful deletion and return to homepage.
    flash("All your cubes have now been successfully deleted.")
    return redirect("/")


# Create blank cube and store ID
def create_cube():
    # Determine time/date cube created, converted to users local time.
    now = datetime.datetime.now()
    created = now.strftime("%Y/%m/%d %H:%M:%S")
    # Create new cube in database to generate cube ID number.
    SQL = "INSERT INTO cubes (user_id, created) VALUES (:user_id, :created)"
    data = {"user_id": session["user_id"], "created": created}
    db.execute(SQL, data)
    # Find the ID of the cube that has just been created.
    SQL = "SELECT id FROM cubes WHERE user_id = :user_id ORDER BY created DESC LIMIT 1"
    data = {"user_id": session["user_id"]}
    cube_id_list = db.execute(SQL, data).fetchall()
    # Commit & close database connection.
    db_close()
    # Store Id of this new cube and clear the session cube.
    cube_id = cube_id_list[0]['id']
    session["current_cube_id"] = cube_id
    session["cube"] = []


# Check if cube is valid (correct number of colours accounted for):
def check_cube():
    # Create colour_check dictionary and set counts to zero.
    colour_check = dict.fromkeys(config.colours)
    for colour in colour_check:
        colour_check[colour] = 0

    # Sum the total number of each colour.
    print("SESSION CUBE:")
    print(session["cube"])
    for square in session["cube"]:
        for colour in config.colours:
            if session["cube"][square] == colour:
                colour_check[colour] = colour_check[colour] + 1
                break

    # Initiate the list of errors, to be populated next.
    session["errors"] = []

    # Check if colour totals are too many or too few.
    for colour in colour_check:
        # There should be 9 of each colour.
        if colour_check[colour] == 9:
            continue
        elif colour_check[colour] < 9:
            session["errors"].append("Too few " + colour + " squares.")
            continue
        elif colour_check[colour] > 9:
            session["errors"].append("Too many " + colour + " squares.")

    # If no errors, confirm the cube is correct and proceed.
    if not session["errors"]:
        # Add "no errors" & progress status to database.
        progress = helpers.solve_progress(session["cube"])
        SQL = "UPDATE cubes SET (input_check, stage) = ('Input Ok', :stage) WHERE (id) = (:cube_id);"
        data = ({"stage": progress, "cube_id": session["current_cube_id"]}, )
        db.execute(SQL, data)
        # Commit & close database connection.
        db_close()
        print("CHECK_CUBE - Completed with no errors.")
        return redirect("/solve")

    # If errors found, list those errors and ask user to correct.
    else:
        # Load "amend" page to display errors and resolve them.
        SQL = "UPDATE cubes SET (input_check) = row('Error') WHERE (id) = (:cube_id);"
        data = ({"message": 'Error', "cube_id": session["current_cube_id"]})
        db.execute(SQL, data)
        # Commit & close database connection.
        db_close()
        # Flash message to advise that error needs to be resolved.
        flash("Errors found in your cube entry, please resolve before solving.")
        print("CHECK CUBE - Errors found.")
        return redirect("/amend")


# Try to solve with random moves (it won't solve the cube).
@app.route("/solve_randomly")
@login_required
def solve_randomly():
    # Load session cube, define number of moves & initialise counter.
    cube = session["cube"]
    max_number_of_moves = 100000
    move_count = 0
    # Make random moves until cube is solved or move limit reached.
    for move in range(0, max_number_of_moves):
        # If cube is solved, end for loop.
        if helpers.solve_progress(cube) == 8:
            break
        # If cube is not solved, make random move to cube.
        else:
            move_count = move_count + 1
            cube = helpers.random_move(cube)
    # Update session cube with resulting cube.
    for square in config.squares:
        session["cube"][square] = cube[square]
    # Advise user moves were made and return.
    flash(str(move_count) + " randomly picked moves were made.")
    return redirect("/solve")


# Provide random moves to user, for user to randomise real-life cube.
# This will generte a list of moves to make; not amend the cube itself.
# Number of random moves to make will default to 30 unless flask url
# argument received to state otherwise.
@app.route("/randomise_user_cube", defaults={"random_moves":30})
@app.route("/randomise_user_cube/<int:random_moves>")
@login_required
def randomise_user_cube(random_moves):
    # Initialise moves list & move counter.
    random_moves_list = []
    move_count = 0
    # Randomly make moves to cube until max count reached.
    while move_count < random_moves:
        # Randomly select a number between 0 and 11 inclusive.
        y = random.randint(0, 11)
        # Use random number to select a move from list of moves.
        move = config.possible_moves[y]
        # Add move to list of moves to make.
        random_moves_list.append(move)
        # Remove uncesseray/inefficient moves.
        random_moves_list = helpers.improve_efficiency(random_moves_list)
        # Update move_count.
        move_count = len(random_moves_list)
    # Return list of random moves.
    return render_template("randomiser.html", random_moves_list=random_moves_list)


# Randomise a solved cube to ensure it can actually be solved.
@app.route("/random_cube")
@login_required
def random_cube():
    # Load solved cube.
    cube = config.solved_cube
    # Define number of random moves to make.
    random_moves = 50
    # Make random moves.
    for x in range(0, random_moves):
        cube = helpers.random_move(cube)
    # Create new cube in databse:
    create_cube()
    # Enter the randomised data into the dictionary:
    for square in cube:
        # Update database with colour of each square. There may be a
        # better way to update 54 SQL columns, to be investigated.
        # Note that as the input to the below SQL query is hard-coded,
        # there should be no risk of SQL injection attack.
        SQL = f"UPDATE cubes SET {square} = :square WHERE id = :cube_id"
        data = {"square": cube[square], "cube_id": session["current_cube_id"]}
        db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    # Update session cube & return cube check:
    session["cube"] = cube
    print("RANDOM CUBE - Function complete.")
    return check_cube()


# Route to create new cube.
@app.route("/enter", methods=["GET", "POST"])
@login_required
def enter():

    if request.method == "GET":
        # Display blank template to entre new cube.
        return render_template("enter.html", squares=config.squares, colour_initials=config.colour_initials)

    if request.method == "POST":
        # Create empty dictionary of squares, ready for user input.
        cube = dict.fromkeys(config.squares)
        # Create new cube in database:
        create_cube()
        # Enter the submitted data into the dictionary:
        # Note that as the input to the below SQL query is hard-coded,
        # there should be no risk of SQL injection attack.
        for square in cube:
            square_colour = request.form.get(square)
            cube[square] = square_colour
            SQL = f"UPDATE cubes SET {square} = :square_colour WHERE id = :cube_id"
            data = {"square_colour": square_colour, "cube_id": session["current_cube_id"]}
            db.execute(SQL, data)
        # Commit & close database connection.
        db_close()
        # Update session cube & return cube check:
        session["cube"] = cube
        return check_cube()


@app.route("/load", methods=["POST"])
@login_required
def load():
    # Replace current session cube id with the clicked cube_id.
    cube_to_load = request.form.get("load")
    session["current_cube_id"] = cube_to_load
    # Load cube from database into session cube.
    SQL = "SELECT * FROM cubes WHERE id = :cube_to_load"
    data = {"cube_to_load": cube_to_load}
    cube_loading = db.execute(SQL, data)
    # Convert to dictionary from row object to allow lookup by key.
    list = [dict(row) for row in cube_loading]
    session["cube"] = list[0]
    # Commit & close database connection.
    db_close()
    return check_cube()


@app.route("/amend_from_list", methods=["POST"])
@login_required
def amend_from_list():
    # Replace current session cube with clicked cube.
    cube_to_amend = request.form.get("amend")
    session["current_cube_id"] = cube_to_amend
    # Load cube from database into session cube.
    SQL = "SELECT * FROM cubes WHERE id = :cube_to_amend"
    data = {"cube_to_amend": cube_to_amend}
    cube_loading = db.execute(SQL, data).fetchall()
    session["cube"] = cube_loading[0]
    # Commit & close database connection.
    db_close()
    return redirect("/amend")


@app.route("/copy", methods=["POST"])
@login_required
def copy():
    # Load cube to be copied into temporary dictionary.
    cube_id_to_copy = request.form.get("copy")
    # Load cube from database into temp cube.
    SQL = "SELECT * FROM cubes WHERE id = :cube_id_to_copy"
    data = {"cube_id_to_copy": cube_id_to_copy}
    cube_loading = db.execute(SQL, data)
    # Convert to dictionary from row object to allow lookup by key.
    list = [dict(row) for row in cube_loading]
    temp_cube = list[0]
    # Create new blank cube, and make current session cube.
    create_cube()
    # Populate curret session cube with previous cube contents.
    session["cube"] = temp_cube
    session["cube"]["id"] = session["current_cube_id"]
    # Save new cube contents to database.
    # Note that as the input to the below SQL query is hard-coded,
    # there should be no risk of SQL injection attack.
    for item in temp_cube:
        SQL = f"UPDATE cubes SET {item} = (:cube_item) WHERE (id) = (:cube_id)"
        data = {"cube_item": session["cube"][item], "cube_id": session["current_cube_id"]}
        db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    # Flash message to user then proceed to home page.
    flash("Copy of Cube ID " + str(cube_id_to_copy) + ", created as new Cube ID " + str(session["current_cube_id"]))
    return redirect("/")


@app.route("/amend", methods=["GET", "POST"])
@login_required
def amend():
    # If loading page prior to data entry,
    # display squares based on current session cube.
    if request.method == "GET":
        return render_template("amend.html", squares=config.squares, colour_initials=config.colour_initials, cube=session["cube"])

    # If new data submitted:
    if request.method == "POST":
        # Update database with user input from form.
        # Note that as the input to the below SQL query is hard-coded,
        # there should be no risk of SQL injection attack.
        cube = session["cube"]
        for square in config.squares:
            square_colour = request.form.get(square)
            cube[square] = square_colour
            SQL = f"UPDATE cubes SET {square} = (:colour) WHERE (id) = (:cube_id);"
            data = ({"colour": square_colour, "cube_id": session["current_cube_id"]})
            db.execute(SQL, data)
        # Commit & close database connection.
        db_close()
        # Update session cube & return cube check:
        session["cube"] = cube
        return check_cube()


@app.route("/solve", methods=["POST", "GET"])
@login_required
def solve():
    print("SOLVE - Start solve function.")
    # Take current session cube and check progress.
    current_cube_id = session["current_cube_id"]
    progress = helpers.solve_progress(session["cube"])
    # Update solve progress in database.
    SQL = "UPDATE cubes SET (stage) = row(:progress) WHERE (id) = (:cube_id);"
    data = ({"progress": progress, "cube_id": session["current_cube_id"]}, )
    db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    print("SOLVE - Progress stage found to be " + str(progress))
    
    # If cube is completed already, show 'complete' page.
    if progress == 8:
        return render_template("complete.html")

    # Else if cube is not solved, determine next move required.
    else:
        # Start with "next_cube_colours" matching current cube, ready
        # for moves to be mdae.
        session["next_cube_colours"] = session["cube"]
        # Create list of moves required to
        # progress to solve the current stage of the cube.
        next_actions_list = helpers.next_action()
        # Improve efficiency of moves in next_actions_list.
        next_actions_list = helpers.improve_efficiency(next_actions_list)
        # Look up nick name of current stage.
        stage_name = config.stage_names[progress]
        # Render solve page.
        return render_template("solve.html", next_actions_list=next_actions_list, squares=config.squares, cube=session["cube"], next_cube=session["next_cube_colours"], current_cube_id=session["current_cube_id"], progress=progress, stage_name=stage_name)


@app.route("/solve_entirely")
@login_required
def solve_entirely():
    print("SOLVE ENTIRELY - Single stage solve function started.")
    # Initialise list for required moves.
    complete_solve_list = []
    # Prepare temp dictionary.
    session["next_cube_colours"] = session["cube"]
    # Take current session cube and check progress.
    current_cube_id = session["current_cube_id"]
    progress = helpers.solve_progress(session["cube"])
    # Record stage at which cube started, to correctly display
    # the progress bar and stage description on the page.
    starting_progress = progress

    # If cube is completed already, show 'complete' page.
    if progress == 8:
        print("SOLVE ENTIRELY - Solving stage is 8.")
        # Cube already solved, nothing to do.
        return render_template("complete.html")

    # Else if cube is before the final stage, continue to loop round, appending to
    # list of moves required until cube is solved.
    while progress < 7:
        print("SOLVE ENTIRELY - Solving stage less than 7.")
        # Loop through each solve stage.
        # Append moves required for that solve stage to the overall list.
        next_moves_list = helpers.next_action()
        for move in next_moves_list:
            complete_solve_list.append(move)
        # Check if the above moves have solved the cube,
        # in order to break the while loop.
        progress = helpers.solve_progress(session["next_cube_colours"])

    # Else the stage must be 7 (last stage) so determine moves for
    # final stage then render page with list of moves.
    else:
        print("SOLVE ENTIRELY - Solving stage is equal to 7.")
        # Append moves required for that solve stage to the overall list.
        next_moves_list = helpers.next_action()
        for move in next_moves_list:
            complete_solve_list.append(move)
        # Improve efficiency of moves in next_actions_list and render.
        next_actions_list = helpers.improve_efficiency(complete_solve_list)
        # Look up nick name of current stage.
        stage_name = config.stage_names[progress]
        # Render solve page.
        return render_template("solve.html", next_actions_list=complete_solve_list, squares=config.squares, cube=session["cube"], next_cube=session["next_cube_colours"], current_cube_id=session["current_cube_id"], progress=starting_progress, stage_name=stage_name)


# Function to record the user has correctly followed the moves of this stage,
# and loop back into the solve function.
@app.route("/next_stage")
@login_required
def next_stage():
    # User has confirmed that they made the moves correctly, so
    # update session cube with next_cube_colours, then allowing
    # the solve to continue from that point. 
    for square in config.squares:
        session["cube"][square] = session["next_cube_colours"][square]
        # Update the database with new cube state.
        # Note that as the input to the below SQL query is hard-coded,
        # there should be no risk of SQL injection attack.
        SQL = f"UPDATE cubes SET {square} = (:colour) WHERE (id) = (:cube_id)"
        data = ({"square": square, "colour": session['cube'][square], "cube_id": session["current_cube_id"]})
        db.execute(SQL, data)
    # Commit & close database connection.
    db_close()
    print("NEXT_STAGE - Function complete.")
    # Return to solve page to solve this new cube state.
    return redirect("/solve")
