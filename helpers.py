from flask import session # Used to manage current user, cube & moves.
import config # Contains large or repeatedly used data.
import random # Used to generate random numbers.
import solvers


# Select random cube move and make that move to the input cube.
def random_move(cube):
    # Randomly select and make a move function.
    random_move = random.choice(config.possible_moves)
    cube = move(random_move, cube)
    # Return cube state after move is made.
    return cube


# Determine stage of solving:
def solve_progress(cube):
    # Initialise counter for solved stages.
    solve_progress = 0
    # Check Stage 0&1 - Daisy & White Cross stage.
    # Check if white cross & daisy are solved.
    # In this one instance, two stages are check together due to the
    # nature of how this stage of solving works. Specifically that
    # if white cross is solved, the daisy must not be solved but to
    # solve the white cross you must first solve the daisy.
    white_cross_squares = ('dtm', 'dml', 'dmm', 'dmr', 'dbm')
    white_cross_solved = True
    daisy_solved = True
    for square in white_cross_squares:
        if cube[square] != 'white':
            white_cross_solved = False
            # If white cross is unsolved, check if daisy is solved
            daisy_squares = ('utm', 'uml', 'umr', 'ubm')
            for square in daisy_squares:
                if cube[square] != 'white':
                    daisy_solved = False
                    break
            break
    # If daisy is first unsolved stage, return progress as 0.
    if daisy_solved is False:
        solve_progress = 0
        return solve_progress
    # If white cross is first unsolved stage, return progress as 1.
    elif white_cross_solved is False:
        solve_progress = 1
        return solve_progress
    # Solve process is linear from stage 2 onwards.
    # Check each stage against criteria. 
    for stage in config.check_stages:
        # Move through faces as required (sometimes only one face).
        for face in stage[1]:
            # Move through squares on face (not always the full face).
            for square in face[0]:
                # Check if colour of square matches criteria.
                if cube[square] != face[1]:
                    solve_progress = stage[0]
                    return solve_progress
    # If none of the above criteria have been met, then cube is solved.        
    solve_progress = 8
    return solve_progress


# Determine what moves are required to progress solving the cube.
def next_action():
    print("NEXT - START NEXT_ACTION FUNCTION")
    # Prepare temporary dictionary and check current progress. 
    cube = session["next_cube_colours"]
    progress = solve_progress(cube)
    # Create blank list, ready to receive the list of moves required to
    # progress to solve the current stage of the cube.
    next_actions_list = []
    print("NEXT - FORMALITIES COMPLETED.")
    # Run appropriate solve function depending on current progress.
    # Instead of using a formatted string, this could instead use a
    # dictionary to link solve stage with the required solve function;
    # leaving as it is until pros/cons considered.
    function_as_string = f'solvers.solve_stage_{progress}(cube, progress, next_actions_list)'
    next_actions_list = eval(function_as_string)
    return next_actions_list


# Define changes to the squares of the cube when a move is made.
def move(move, cube):
    # Create blank dictionary
    new_cube_colours = {}
    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]
    # Change squares that need to be changed.
    for square in config.move_definitions[move]:
        new_cube_colours[square[0]] = cube[square[1]]
    print(f"MOVE - make move {move}")
    # Return amended dictionary of cube colours.
    return new_cube_colours


# Improve efficiency of the list of moves to be made. 
# Once moves required are determined, remove any opposite moves that
# occur directly after each other (i.e. if "U" was followed by "U'",
# both would be removed from the list) and replace triple moves with
# the equivalent single move in the opposite direction (i.e. if the
# list contained "U", "U", "U" this would be replaced with "U'") to
# reduce the number of moves to be made by the user.
def improve_efficiency(moves_list):
    # Improve efficiency of moves in moves_list. Repeat until
    # no inefficiencies are found.
    inefficiencies = True
    while inefficiencies is True:
        print("SOLVE - start loop to remove inefficiencies.")
        print(f'Starting List:{str(moves_list)}')
        # Set to False to end the loop if no inefficiencies are found.
        inefficiencies = False
        
        # Find triple moves and replace them with one opposite move.
        list_length = len(moves_list)
        index = 0
        while index < (list_length - 3):
            # Check each move in the list to see if it matches the
            # following two moves.
            move_0 = moves_list[index]
            move_1 = moves_list[index + 1]
            move_2 = moves_list[index + 2]
            if ((move_0 == move_1) and (move_0 == move_2)):
                print("SOLVE - TRIPLE MOVES FOUND & REPLACED: " + move_0)
                # If triple is found, replace the first move with the
                # move from the replacement list.
                print("TO BE REPLACED WITH: " + config.move_to_replace_triples[move_0])
                moves_list[index] = config.move_to_replace_triples[move_0]
                # Then remove the following move.
                moves_list.pop(index + 1)
                # Then remove the third move (which is not the second).
                moves_list.pop(index + 1)
                # Reduce list length to account for removeal of moves.
                list_length = list_length - 2
                # Record that triples were found to continue to loop
                # around again to look for more triples.
                inefficiencies = True
            # Move onto the next move in the list.
            index = index + 1

        # Remove opposite moves directly one after the other.
        list_length = len(moves_list)
        index = 0
        while index < (list_length - 2):
            # Check each move in the list to see if they are opposites
            # of each other and delete them both if so.
            move_0 = moves_list[index]
            move_1 = moves_list[index + 1]
            if move_0 == config.opposite_moves[move_1]:
                print("SOLVE - OPPOSITE MOVES FOUND & REMOVED")
                # If opposite moves are found, remove both.
                moves_list.pop(index)
                moves_list.pop(index)
                # Reduce list length to account for removeal of moves.
                list_length = list_length - 2
                # Record that triples were found to continue to loop
                # around again to look for more triples.
                inefficiencies = True
            # Move onto the next move in the list.
            index = index + 1
        # Continue to loop around until no ineffiencies are been found.
    # Inefficiencies have now been removed.
    print(f'Resulting List:{str(moves_list)}')
    print("SOLVE - NEXT ACTIONS LIST UPDATED.")
    # Return improved list of actions.
    return moves_list
