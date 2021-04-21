import os
import datetime
import random
import helpers
import config

from config import squares
from config import colours
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# ?!?!?!? check if any of the above are redundant.

# Configure application
app = Flask(__name__)

# Auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True


# ?!?! Ensure responses aren't cached ?!?!?! do I want this ?!?! Sourced from CS50.
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies), sourced from CS50.
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 library to use SQLite database
db = SQL("sqlite:///rubiks.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Login page.
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

        # Ensure password was entered.
        if not request.form.get("password"):
            flash("Password was not entered, please enter password.")
            return render_template("/login.html")

        # Check database for username and password.
        rows = db.execute("SELECT * FROM users  WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hashed_password"], request.form.get("password")):
            flash("Username and/or password does not match.")
            return render_template("/login.html")

        # Remember user has logged in and set current cube to blank.
        session["user_id"] = rows[0]["id"]
        session["current_cube_id"] = 0
        session["username"] = request.form.get("username")

        # Redirect to homepage.
        flash("Login successful")
        return redirect("/")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


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

        # Check that username does not already exist.
        if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            flash("Username " + request.form.get("username") + " already exists.")
            return redirect("/register")

        # Check that password has been entered.
        if not request.form.get("password"):
            flash("Password required.")
            return redirect("/register")

        # Check that second password entry matches the first.
        if not request.form.get("password") == request.form.get("confirmation"):
            flash("Passwords do not match.")
            return redirect("/register")

        # Check password has at least 8 characters.
        if len(request.form.get("password")) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect("/register")

        password = request.form.get("password")

        # Check password has at least 1 number.
        if not any(character.isdigit() for character in password):
            flash("Password must contain at least 1 number.")
            return redirect("/register")

        # Hash password
        password = request.form.get("password")
        hashed = generate_password_hash(password, "sha256")

        # Submit username and hashed password to database.
        db.execute("INSERT INTO users(username, hashed_password) VALUES (?,?)", request.form.get("username"), hashed)

        # Automatically log user in.
        user_id = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))
        session['user_id'] = user_id[0]["id"]
        session["username"] = request.form.get("username")

        # Send user to homepage.
        flash("You have been registered successfully.")
        return redirect("/")


# Default route
@app.route("/")
@login_required
def index():
    # Display previously entered cubes.
    users_cubes = db.execute("SELECT * FROM cubes WHERE user_id = ? ORDER BY id DESC", session["user_id"])

    return render_template("index.html", users_cubes=users_cubes)


# Route to display only loading table.
@app.route("/load_page", methods=["GET"])
@login_required
def load_page():
    # Display previously entered cubes.
    users_cubes = db.execute("SELECT * FROM cubes WHERE user_id = ? ORDER BY id DESC", session["user_id"])

    return render_template("load.html", users_cubes=users_cubes)


# Route to delete existing cube.
@app.route("/delete_cube", methods=["POST"])
@login_required
def delete_cube():

    cube_to_delete = request.form.get("delete")
    db.execute("DELETE FROM cubes WHERE id = ?", cube_to_delete)

    # If sessions current cube is the cube to be deleted, set current cube to zero.
    if session["current_cube_id"] == cube_to_delete:
        session["current_cube_id"] = 0

    flash("Cube ID " + cube_to_delete + " successfully deleted.")
    return redirect("/")


# Route to delete all users existing cubes
@app.route("/delete_all_cubes", methods=["GET"])
@login_required
def delete_all_cubes():

    db.execute("DELETE FROM cubes WHERE user_id = ?", session["user_id"])

    # Set current cube to zero.
    session["current_cube_id"] = 0

    flash("All your cubes have now been successfully deleted.")
    return redirect("/")


# Create blank cube and store ID
def create_cube():

    # Create new cube in database to generate cube ID number.
    created = datetime.datetime.now()
    db.execute("INSERT INTO cubes (user_id, created) VALUES (?, ?)", session["user_id"], created)

    # Cannot currently get lastrowid to work, so using latest entered cube based on time instead.
    cube_id_list = db.execute("SELECT id FROM cubes WHERE user_id = ? ORDER BY created DESC LIMIT 1", session["user_id"])
    cube_id = cube_id_list[0]['id']

    # Store Id of this new cube and empty session cube.
    session["current_cube_id"] = cube_id
    session["cube"] = []


# Check if cube is valid (one of each cubelette accounted for):
def check_cube():

    # Create colour_check dictionary and set counts to zero.
    colour_check = dict.fromkeys(colours)
    for colour in colour_check:
        colour_check[colour] = 0

    # Iterate through the squares to sum the colours.
    for square in session["cube"]:
        for colour in colours:
            if session["cube"][square] == colour:
                colour_check[colour] = colour_check[colour] + 1
                break

    # Initiate the list of errors, to be populated next.
    session["errors"] = []

    # Iterate through the colour totals to check if too many or too few.
    for colour in colour_check:
        if colour_check[colour] == 9:
            continue
        elif colour_check[colour] < 9:
            session["errors"].append("Too few " + colour + " squares.")
            continue
        elif colour_check[colour] > 9:
            session["errors"].append("Too many " + colour + " squares.")

    if not session["errors"]:
        # Add "no errors" & progress status to database.
        progress = helpers.solve_progress(session["cube"])
        db.execute("UPDATE cubes SET 'check' = 'Input Ok', 'stage' = ? WHERE id = ?", progress, session["current_cube_id"])
        # Flash message to confirm successful save.
        flash("Cube " + str(session["current_cube_id"]) + " has been checked and is correct.")
        print("CHECK CUBE NO ERRORS COMPLETE.")
        return redirect("/solve")

    else:
        # Load "amend" page to display errors and resolve them.
        db.execute("UPDATE cubes SET 'check' = 'Error' WHERE id = ?", session["current_cube_id"])
        flash("Errors found in your cube entry, please resolve before solving.")
        print("CHECK CUBE WITH ERRORS COMPLETE.")
        return redirect("/amend")


# Route to solve a cube with random moves.
@app.route("/solve_randomly")
@login_required
def solve_randomly():

    cube = session["cube"]
    max_number_of_moves = 100000
    move_count = 0
    for move in range(0,max_number_of_moves):
        if helpers.solve_progress(cube) == 8:
            for square in squares:
                session["cube"][square] = cube[square]
            return redirect("/solve")
        else:
            move_count = move_count + 1
            cube = random_move(cube)
    for square in squares:
        session["cube"][square] = cube[square]

    flash(str(move_count) + " randomly picked moves were made.")
    return redirect("/solve")


# Select random cube move.
def random_move(cube):
    y = random.randint(0, 11)
    if y == 0:
        cube = helpers.move_rc(cube)
    elif y == 1:
        cube = helpers.move_ra(cube)
    elif y == 2:
        cube = helpers.move_lc(cube)
    elif y == 3:
        cube = helpers.move_la(cube)
    elif y == 4:
        cube = helpers.move_uc(cube)
    elif y == 5:
        cube = helpers.move_ua(cube)
    elif y == 6:
        cube = helpers.move_fc(cube)
    elif y == 7:
        cube = helpers.move_fa(cube)
    elif y == 8:
        cube = helpers.move_bc(cube)
    elif y == 9:
        cube = helpers.move_ba(cube)
    elif y == 10:
        cube = helpers.move_dc(cube)
    elif y == 11:
        cube = helpers.move_da(cube)
    return cube

# Route to provide random moves to user, for user to randomise their own real-life cube.
@app.route("/randomise_user_cube")
@login_required
def randomise_user_cube():

    # Define number of random moves to make.
    random_moves = 20

    random_moves_list = []
    move_count = len(random_moves_list)

    while move_count < random_moves:
        y = random.randint(0, 11)
        move = config.possible_moves[y]
        random_moves_list.append(move)
        random_moves_list = helpers.improve_efficiency(random_moves_list)
        move_count = len(random_moves_list)

    # Return list of random moves.
    return render_template("randomiser.html", random_moves_list=random_moves_list)


# Route to randomise a solved cube to ensure it can actually be solved.
@app.route("/random_cube")
@login_required
def random_cube():

    # Load solved cube.
    cube = config.solved_cube

    # Define number of random moves to make.
    random_moves = 50

    for x in range(0, random_moves):
        cube = random_move(cube)

    # Create new cube in databse:
    create_cube()

    # Enter the randomised data into the dictionary:
    for square in cube:
        db.execute("UPDATE cubes SET ? = ? WHERE id = ?", square, cube[square], session["current_cube_id"])

    # Run cube check and store result in database:
    session["cube"] = cube
    print("RANDOM CUBE FUNCTION COMPLETE.")
    return check_cube()


# Route to create new cube.
@app.route("/enter", methods=["GET", "POST"])
@login_required
def enter():

    if request.method == "GET":

        # Display blank template to entre new cube.
        return render_template("enter.html", squares=squares)

    if request.method == "POST":

        # Create empty dictionary of squares, ready for user input.
        cube = dict.fromkeys(squares)

        # Create new cube in database:
        create_cube()

        # Enter the submitted data into the dictionary:
        for square in cube:
            square_colour = request.form.get(square)
            cube[square] = square_colour
            db.execute("UPDATE cubes SET ? = ? WHERE id = ?", square, square_colour, session["current_cube_id"])

        session["cube"] = cube

        # Run check function.
        return check_cube()


@app.route("/load", methods=["POST"])
@login_required
def load():

    # Replace current session["current_cube_id"] with the clicked cube_id.
    # Then proceed to solve page.
    cube_to_load = request.form.get("load")
    session["current_cube_id"] = cube_to_load
    cube_loading = db.execute("SELECT * FROM cubes WHERE id = ?", cube_to_load)
    session["cube"] = cube_loading[0]

    flash("Cube ID " + cube_to_load + " has been loaded.")

    return check_cube()


@app.route("/amend_from_list", methods=["POST"])
@login_required
def amend_from_list():

    # Replace current session cube with clicked cube.
    cube_to_amend = request.form.get("amend")
    session["current_cube_id"] = cube_to_amend
    cube_loading = db.execute("SELECT * FROM cubes WHERE id = ?", cube_to_amend)
    session["cube"] = cube_loading[0]

    flash("Cube ID " + cube_to_amend + " has been loaded for amendment.")
    return redirect("/amend")


@app.route("/copy", methods=["POST"])
@login_required
def copy():

    # Load cube to be copied into temporary dictionary.
    cube_id_to_copy = request.form.get("copy")
    cube_loading = db.execute("SELECT * FROM cubes WHERE id = ?", cube_id_to_copy)
    temp_cube = cube_loading[0]

    # Create new blank cube, and make current session cube.
    create_cube()

    # Populate curret session cube with previous cube contents.
    session["cube"] = temp_cube
    session["cube"]["id"] = session["current_cube_id"]

    # Save new cube contents to database.
    for item in temp_cube:
        db.execute("UPDATE cubes SET ? = ? WHERE id = ?", item, session["cube"][item], session["current_cube_id"])

    flash("Copy of Cube ID " + str(cube_id_to_copy) + ", created as new Cube ID " + str(session["current_cube_id"]))

    return redirect("/")


@app.route("/amend", methods=["GET", "POST"])
@login_required
def amend():

    # If loading page originally:
    if request.method == "GET":
        return render_template("amend.html", squares=squares, cube=session["cube"])

    # If new data submitted:
    if request.method == "POST":
        # Take input from form to update cube in database.
        for square in squares:
            square_colour = request.form.get(square)
            session["cube"][square] = square_colour
            db.execute("UPDATE cubes SET ? = ? WHERE id = ?", square, square_colour, session["current_cube_id"])

        return check_cube()


@app.route("/solve", methods=["POST", "GET"])
@login_required
def solve():

    print("SOLVE - START SOLVE FUNCTION.")

    # Take current session cube and check progress.
    current_cube_id = session["current_cube_id"]
    progress = helpers.solve_progress(session["cube"])
    db.execute("UPDATE cubes SET 'stage' = ? WHERE id = ?", progress, session["current_cube_id"])

    print("SOLVE - PROGRESS CHECK COMPLETED")
    print("SOLVE - Progress stage found to be " + str(progress))

    if progress == 8:
        # Cube is completed already, show complete page.
        return render_template("complete.html")

    else:
        # Moves are required, determine moves.
        session["next_cube_colours"] = session["cube"]
        print("SOLVE - NEXT_CUBE_COLOURS CREATED.")

        # Create list of moves required to
        # progress to solve the current stage of the cube.
        next_actions_list = helpers.next_action()

        # Improve efficiency of moves in next_actions_list.
        next_actions_list = helpers.improve_efficiency(next_actions_list)

        stage_name = config.stage_names[progress]

        return render_template("solve.html", next_actions_list=next_actions_list, squares=squares, cube=session["cube"], next_cube=session["next_cube_colours"], current_cube_id=session["current_cube_id"], progress=progress, stage_name=stage_name)


@app.route("/solve_entirely")
@login_required
def solve_entirely():

    print("Complete solve function started.")

    complete_solve_list = []
    session["next_cube_colours"] = session["cube"]

    # Take current session cube.
    current_cube_id = session["current_cube_id"]
    progress = helpers.solve_progress(session["cube"])

    if progress == 8:
        print("SOLVE ENTIRELY - Solving stage is 8.")
        # Cube already solved, nothing to do.
        return render_template("complete.html")

    while progress < 7:
        print("SOLVE ENTIRELY - Solving stage less than 7.")

        # Loop through each solve stage.
        # Append moves required for that solve stage to the overall list.
        next_moves_list = helpers.next_action()
        for move in next_moves_list:
            complete_solve_list.append(move)

        progress = helpers.solve_progress(session["next_cube_colours"])

    else:
        if progress == 7:
            print("SOLVE ENTIRELY - Solving stage is 7.")

            # Final run of next_actions, then return results.
            # Append moves required for that solve stage to the overall list.
            next_moves_list = helpers.next_action()
            for move in next_moves_list:
                complete_solve_list.append(move)

        # Improve efficiency of moves in next_actions_list.
        next_actions_list = helpers.improve_efficiency(complete_solve_list)
        return render_template("solve.html", next_actions_list=complete_solve_list, squares=squares, cube=session["cube"], next_cube=session["next_cube_colours"], current_cube_id=session["current_cube_id"], progress=progress)

    # ?!?!?! correct progress bar on solve page for this sove_entirely option.


# Function to record the user has correctly followed the moves of this stage,
# and loop back into the solve function.
@app.route("/next_stage")
@login_required
def next_stage():
    for square in squares:
        session["cube"][square] = session["next_cube_colours"][square]
        # Update the database with new cube state.
        db.execute("UPDATE cubes SET ? = ? WHERE id = ?", square, session['cube'][square], session["current_cube_id"])

    return redirect("/solve")