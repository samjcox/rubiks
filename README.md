# RUBIKS CUBE SOLVER
#### Video Demo: ?????????????
#### Description:
This web app will allow a user to input their rubiks cube's arrangement and then provides the user with steps (either in stages, or in on long list) to solve their Rubiks cube.

This web app has been created as the final project for CS50.

Heroku address: https://rubiks-cube-solver.herokuapp.com/
Github repository: https://github.com/samjcox/rubiks

#### Environment:
Python, HTML, JavaScript, Flask, Jinja, CSS, Bootstrap.

## Main Features of this web app
- The main intent behind this web app is for the user to enter their cube into the system, for the app to tell the user what moves are required to solve the cube.
- The algorithm used to solve the cube is based on a human-memorisable solve method, so this does not result in the smallest number of moves.
- You can chose between being shown moves in stages (with a check at the end of each stage), or being shown all the required moves in one long list.
- To test/experience the website, the user can also ask the web app to generate a random cube.  This is done by taking a solved cube and making random moves on the cube.
- If the user has a solved cube, the web app includes a Randomiser feature to give the user a number of random moves they can follow to randomise their own cube, ready for solving again.
- As the user progresses through each stage, the site shows the user how far through the solve process they currently are (using 8 stages, include nick names and a progress bar).


## Detailed features
- Each user can store their own cubes in the database, with the ability to amend, copy and delete individual cubes from the database.
- You can delete all cubes from the database with one function; this function does include a confirmation message displayed in an overlay.
- There is a Loading overlay that appears when certain actions are started.  It is however updating the database that is taking the most time, not the calculation of cube moves.  Note that when running the app locally (i.e. when using VSCode) the database update is very quick (potentially no need for a loading screen) however when previously working on CS50 IDE the database update took a noticable time (approx 3-4 seconds).  The loading screen has been left in for now, however maybe this could be removed after testing on Heroku (future work) if the database .
- The database is accessed using the sqlite3 module (after originally using the CS50 SQL module).
- The moves calculated would likley originally comprise of a number of opposite moves followed after each other, and also triple rotations (equal to one rotation in the opposite direction), so the web app simplifies the required list of moves to delete opposite moves and replace triple moves with the opposite move.
- Includes a feature to make 100,000 random moves on a cube just to demonstrate that this wouldnt solve the rubiks cube.
- Once the cube is solved, a celebration page appears inviting the user to use the randomiser to shuffle their cube and start again.


## Files & Structure
### Project folder
- app.py - main application include general functions.
- helpers.py - contains detailed cube move algorithms and solve algorithms.
- config.py - contains repeatedly used lists and dictionaries.
- rubiks.db - database contains two tables.  The 'users' table includes username and password. The 'cubes' table includes the current state of all cubes.  More details of database structure included below.
- requirements.txt - lists packages used.

### Static folder
- styles.css
- concert-2527495__340_from_pixabay.jpg - image used for the celebration page once a cube has been solved.
- preloader_cube.gif - rotating rubiks cube used on the loading overlay.

### Templates folder
- layout.html - template file from which all other pages are extended.
- index.html - default page, from which the user can create a new cube, or load an existing cube.
- amend.html - for the user to edit their cube in the database.
- complete.html - to confirm to the user they have succesfully solved their cube.
- enter.html - for the user to manually enter their cube into the database.
- load.html - simply contains larger table of existing cubes should the user have many cubes to scroll through.
- login.html - if the user is not logged in, they will be directed to here where they can either login with existing details or chose to be redirected to register.
- randomiser.html - page to display random moves for the user to shuffle their cube.
- register.html - where the user can enter username and password.
- solve.html - this page displays the current state of the cube, the moves required, and the intended state of the cube after the moves have been made (for the user to check their moves were made correctly).


## Database strucutre
'users' table:
- id - unique id per user.
- username - user chosen username.
- hashed_password - hashed version of users chosen password.

'cubes' table:
- id - unique id per cube.
- user_id - the id of the user who created this cube (users can only get access to their own cubes).
- check - notes if the cube has been correctly entered, or if there are errors that need to be resolved by the user before it can be solved.
- each square of the cube is listed as a seperate column in the table - 54 columns (one for each square on the cube) each of which stores the current colour of that square.  This is updated between each stage of solving, allowing the user to close the application and not lose their progress.


## Difficulties considered
- Possibility of SQL injection attacks - when using dynamic column names in UPDATE queries, this concept potentially opens a vulnerability to SQL injection attacks.  As the column name needs to change (to iterate through each sqaure) the column name cannot be fixed; while you also can't use bind variables to define column names, therefore now using the dynamic naming method. As the names that are being iterated through are hard-coded, this is believed to remove the possibility of SQL injection attacks and is therefore not believed to be an issue.
- Threading issues - during development testing the app was repeatedly showing threading errors, as the database was being connected to once at the beginning of the app and not disconnecting.  To resolve this the app creates and commits/closes the database connection after each use.  Unsure if this is good practice as this seems to be different from other code examples, to be investigated further.
- Using formatted string and eval() to determine function - within the next_action function, the function that needs to be run is dependant on the stage to be solved. Originally, the app would use a series of if/elif functions (i.e. if stage == 1, return solve_stage_1); however the formatted string method is shorter.  As the input into the dynamically created function is generated by the app (not by a user) this is not believed to be a security risk.


## Future improvements / works
- Move the app to Heroku. This would allow real-world access to the app for real-world testing and usage. 
- Improve method of database updates.  The app works with the square/colours as a dictionary.  There is currently one column in the SQL table per square of the cube (54 columns for colour of squares). Consider storing all the squares/colours in one column which will be just one column to update, which is expected to be more efficient. This could be done by storing the squares/colours in the SQL table as a string - however this would introduce the extra step to "encode/decode" the dictionary to a string.  This encode/decode may be more efficient than 54 SQL updates.  However the update time is currently imperceptoble to the user, more testing to be done once uploaded to Heroku.
- Automatic cube entry using image recognition.  Entering a cube into the page is quite time consuming, so it would be much more convenient to hold your cube up to the webcam for automatic entry of cube into the web app.
- Use alternative solve algorithm (instead of being human-memorisable) to reduce number of moves required to solve the cube.  This will however require a lot more processing power.
- Consider adding a 3D visualisation of the cube at each stage in addition to the 2D "unfolded" representation currently used.
- Improve checking of manual cube entry.  At the moment the system checks there are the correct number of colours in the square as a limited method of checking for mistakes.  If however the user randomly enters colours into the cube and totals the correct number of each colour, this will probably not be solvable but wont be flagged as an error by the checking algorithm.