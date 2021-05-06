# Standard library modules
# None

# Non-standard modules
from flask import session # Used to manage current user, cube & moves.

# Other files within application
import config # Contains large or repeatedly used data.
import helpers # Contains functions to support the main routes.

# Determine moves required to solve Stage 0, the daisy stage.
# Append moves required to a list as moves are determined.
def solve_stage_0(cube, progress, next_actions_list):
    # Loop through to progressively work towards solving stage 0.
    while progress == 0:
        print("NEXT 0.00, daisy - PROGRESS FOUND TO BE 0.")
        # Start moving white edge pieces from bottom face to top face.
        bottom_face_edge_squares = ('dtm', 'dml', 'dmr', 'dbm')
        print("NEXT - BEGIN ITERATION THROUGH BOTTOM FACE.")
        for square in bottom_face_edge_squares:
            if cube[square] == "white":
                # For each white square on bottom face, check if the
                # opposite square on top face is already white.
                top_square = config.bottom_face_top_square[square]
                while cube[top_square] == "white":
                    # Rotate top face to avoid existing white square
                    # on top face.
                    cube = helpers.move('U', cube)
                    next_actions_list.append("U")
                # If corresponding square on top face is not white,
                # move white square from bottom face to top face.
                if cube[top_square] != "white":
                    moves = config.daisy_bottom_face_moves[square]
                    for action in moves:
                        # Append required moves to the list.
                        next_actions_list.append(action)
                        # Make required moves to cube.
                        cube = helpers.move(action, cube)
        # Now there should be no white squares on the bottom face.
        print("NEXT - NO WHITE SQUARES ON BOTTOM FACE")

        # Next to look for white squares in the middle row, to then
        # bring them up to the top face.
        print("NEXT - BEGIN ITERATION THROUGH MIDDLE ROW.")
        for square in config.middle_row_edge_squares:
            if cube[square] == "white":
                # For each white square in the middle row, check if the
                # appropriate square on the top face is already white.
                top_square = config.daisy_middle_reference_top_square[square]
                while cube[top_square] == 'white':
                    # Rotate top face to find alternative.
                    cube = helpers.move('U', cube)
                    next_actions_list.append("U")
                # If relevant square on top face is not white, then
                # add appropriate move to queue.
                if cube[top_square] != 'white':
                    action = config.daisy_middle_moves[square]
                    next_actions_list.append(action)
                    # Convert Cube Notation into actual move_xx to
                    # action on next_cube_colours.
                    cube = helpers.move(action, cube)
        print("NEXT - NO WHITE SQUARES FOUND IN MIDDLE ROW")
        # Now there should be no white edge pieces in the middle row.

        # Next to look for white edge pieces in bottom row.
        bottom_row_edge_squares = ('fbm', 'lbm', 'bbm', 'rbm')
        print("NEXT - BEGIN ITERATION THROUGH BOTTOM ROW.")
        for square in bottom_row_edge_squares:
            if cube[square] == "white":
                # For each white edge square in bottom row,
                # check if appropriate square on top face is already white.
                top_square = config.daisy_bottom_reference_top_square[square]
                while cube[top_square] == 'white':
                    # If appropriate top face square is white,
                    # rotate top face to find alternative.
                    cube = helpers.move('U', cube)
                    print("NEXT - MAKE MOVE U")
                    next_actions_list.append("U")
                # If appropritate top face square is not white, make
                # moves to bring square from bottom row to top face.
                if cube[top_square] != 'white':
                    moves = config.daisy_bottom_moves[square]
                    print("NEXT - make moves " + str(moves))
                    for action in moves:
                        # Append required moves to the list.
                        next_actions_list.append(action)
                        # Make required moves to cube.
                        cube = helpers.move(action, cube)
        # Now there should be no white squares in the bottom row.
        print("NEXT - NO WHITE SQUARES FOUND IN BOTTOM ROW")

        # Next to look for white edge pieces in top row, to then bring
        # them up to the top face.
        top_row_edge_squares = ('ftm', 'ltm', 'btm', 'rtm')
        print("NEXT - BEGIN ITERATION THROUGH TOP ROW.")
        for square in top_row_edge_squares:
            if cube[square] == "white":
                # For each white square in top row,
                # move it onto the top face.
                moves = config.daisy_top_moves[square]
                print("NEXT - make moves " + str(moves))
                for action in moves:
                    # Append required moves to the list.
                    next_actions_list.append(action)
                    # Make required moves to cube.
                    cube = helpers.move(action, cube)
        # Now there should be no white squares in the top row.
        print("NEXT - NO WHITE SQUARES FOUND IN TOP ROW")
        
        # Check to see if the above has solved this stage to
        # either end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)

    # Stage 0 has now been solved.
    print("NEXT - PROGRESS NO LONGER 0.")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    print("NEXT - SESSION NEXT_CUBE_COLOURS UPDATED FROM STAGE 0.")
    # Return list of actions required to solve the Daisy stage.
    return next_actions_list


# Determine moves required to solve Stage 1, the White Cross stage.
def solve_stage_1(cube, progress, next_actions_list):
    while progress == 1:
        print("NEXT 1.00,  white cross - PROGRESS FOUND TO BE 1.")
        # Move white squares from daisy on top face, to bottom face.
        # Progressively check if the top row middle square of each face
        # is in appropriate position, if not rotate top row until it
        # is correct, then move top face white square to bottom face.

        # Resolve front face.
        while cube['ftm'] != cube['fmm'] or cube['ubm'] != 'white':
            # Rotate top face of cube.
            cube = helpers.move('U', cube)
            # Append required move to the list.
            next_actions_list.append('U')
        # Correctly aligned, so move top face square to bottom face.
        else:
            # Rotate front face twice.
            cube = helpers.move('F', cube)
            cube = helpers.move('F', cube)
            # Append moves to the list.
            next_actions_list.append('F')
            next_actions_list.append('F')
        # Resolve left face.
        while cube['ltm'] != cube['lmm'] or cube['uml'] != 'white':
            # Rotate top face of cube.
            cube = helpers.move('U', cube)
            # Append required move to the list.
            next_actions_list.append('U')
        # Correctly aligned, so move top face square to bottom face.
        else:
            # Rotate left face twice.
            cube = helpers.move('L', cube)
            cube = helpers.move('L', cube)
            # Append moves to the list.
            next_actions_list.append('L')
            next_actions_list.append('L')
        # Resolve back face.
        while cube['btm'] != cube['bmm'] or cube['utm'] != 'white':
            # Rotate front face twice.
            cube = helpers.move('U', cube)
            # Append required move to the list.
            next_actions_list.append('U')
        # Correctly aligned, so move top face square to bottom face.
        else:
            # Rotate back face twice.
            cube = helpers.move('B', cube)
            cube = helpers.move('B', cube)
            # Append moves to the list.
            next_actions_list.append('B')
            next_actions_list.append('B')
        # Resolve right face.
        while cube['rtm'] != cube['rmm'] or cube['umr'] != 'white':
            # Rotate front face twice.
            cube = helpers.move('U', cube)
            # Append required move to the list.
            next_actions_list.append('U')
        # Correctly aligned, so move top face square to bottom face.
        else:
            # Rotate right face twice.
            cube = helpers.move('R', cube)
            cube = helpers.move('R', cube)
            # Append moves to the list.
            next_actions_list.append('R')
            next_actions_list.append('R')
        # Check to see if the above has solved this stage to
        # either end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 1 has now been solved.
    print("NEXT - PROGRESS NO LONGER 1.")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    print("NEXT - SESSION NEXT_CUBE_COLOURS UPDATED FROM STAGE 1.")
    # Return list of actions required to solve the White Cross stage.
    return next_actions_list


# Determine moves required to solve Stage 2, the White Face stage.
def solve_stage_2(cube, progress, next_actions_list):
    while progress == 2:
        print("NEXT 2.00, white face - PROGRESS FOUND TO BE 2")
        # Find any white squares in top row and move them to bottom
        # face by aligning the adjacent square to its correct face and
        # then making the correct sequence of moves.
        # Note that new white squares may be moved to the top row in
        # this step, so this loops round until all squares in top row
        # have been moved to bottom face. 
        while True:
            print("NEXT 2.01 - FINDING WHITE SQUARES ON TOP ROW")
            # Start loop as False, in case no squares are found.
            squares_found = False
            for square in config.top_row_corner_squares:
                # Find white squares in the top row corners.
                if cube[square] == 'white':
                    print("NEXT 2.02 - WHITE SQUARE FOUND ON TOP ROW - " + square)
                    # Mark squares_found as true to loop through again.
                    squares_found = True
                    # Check if adjacent square matches the adjacent
                    # face centre square.
                    adjacent_corner_square = config.top_row_corner_squares[square]
                    centre_square = config.centre_square_for_square[adjacent_corner_square]
                    if cube[adjacent_corner_square] == cube[centre_square]:
                        # Make move to move piece to bottom face.
                        print("NEXT - WHITE SQUARE IN CORRECT POSITION IN TOP ROW, MOVED TO BOTTOM FACE - " + square)
                        for action in config.white_face_top_row_moves[square]:
                            # Append move to list.
                            next_actions_list.append(action)
                            # Make moves to cube.
                            cube = helpers.move(action, cube)
                    # Check if adjacent square does not match the adjacent
                    # face centre square.
                    else:
                        print("NEXT 2.04 - TOP ROW WHITE SQUARE NOT CORRECT, ROTATE TOP ROW")
                        # Rotate top row of cube.
                        cube = helpers.move('U', cube)
                        # Add move to list.
                        next_actions_list.append("U")
            # If no white squares found in top row, break loop.
            if squares_found is False:
                print("NEXT 2.05 - NO WHITE SQUARES REMAIN/FOUND IN TOP ROW")
                break
        # There are now no white squares in the top row.

        # Now look for white squares in the bottom row, and move them
        # into the top row to be resolved accordingly.
        # Start loop as False, in case no squares are found.
        squares_found = False
        print("NEXT - LOOKING FOR WHITE SQUARES IN BOTTOM ROW")
        for square in config.bottom_row_corner_squares:
            if cube[square] == 'white':
                print("NEXT - WHITE SQUARE FOUND IN BOTTOM ROW")
                # Mark squares_found as true to loop through again.
                squares_found = True
                for action in config.bottom_row_corner_squares[square]:
                    # Append move to list.
                    next_actions_list.append(action)
                    # Make moves to cube.
                    cube = helpers.move(action, cube)
                # If a square has been found, stop looking so this
                # square can be correctly resolved.
                break
        # If a square has been found, loop back to start to correctly
        # resolve that square before proceeding further.
        if squares_found is True:
            print("NEXT - LOOPING BACK AS WHITE SQUARES FOUND IN BOTTOM ROW")
            continue
        print("NEXT - NO WHITE SQUARES FOUND IN BOTTOM ROW.")
        # There are now no white squares in the bottom row.

        # Look for incorrectly positioned white corner squares on the
        # bottom face and bring them into the top row to be resolved.
        print("NEXT - NOW LOOKING FOR INCORRECT CORNERS ON WHITE FACE.")
        # Check if square dtl cubelette is correct on all three faces.
        if (cube['dtl'] == 'white' and (cube['fbl'] != 'blue' or cube['lbr'] != 'orange')):
            # If found to be incorrect, make moves to bring incorrect
            # cubelette into top row and append moves to list.
            cube = helpers.move("L'", cube)
            next_actions_list.append("L'")
            cube = helpers.move("U'", cube)
            next_actions_list.append("U'")
            cube = helpers.move("L", cube)
            next_actions_list.append("L")
            print("NEXT - SQUARE dtl MOVED, LOOPING BACK")
            # Loop back to resolve moved squares accordingly.
            continue
        # Check if square dtr cubelette is correct on all three faces.
        if (cube['dtr'] == 'white' and (cube['fbr'] != 'blue' or cube['rbl'] != 'red')):
            # If found to be incorrect, make moves to bring incorrect
            # cubelette into top row and append moves to list.
            cube = helpers.move("R", cube)
            next_actions_list.append("R")
            cube = helpers.move("U", cube)
            next_actions_list.append("U")
            cube = helpers.move("R'", cube)
            next_actions_list.append("R'")
            print("NEXT - SQUARE dtr MOVED, LOOPING BACK")
            # Loop back to resolve moved squares accordingly.
            continue
        # Check if square dbr cubelette is correct on all three faces.
        if (cube['dbr'] == 'white' and (cube['bbl'] != 'green' or cube['rbr'] != 'red')):
            # If found to be incorrect, make moves to bring incorrect
            # cubelette into top row and append moves to list.
            cube = helpers.move("R'", cube)
            next_actions_list.append("R'")
            cube = helpers.move("U'", cube)
            next_actions_list.append("U'")
            cube = helpers.move("R", cube)
            next_actions_list.append("R")
            print("NEXT - SQUARE dbr MOVED, LOOPING BACK")
            # Loop back to resolve moved squares accordingly.
            continue
        # Check if square dbl cubelette is correct on all three faces.
        if (cube['dbl'] == 'white' and (cube['fbl'] != 'blue' or cube['lbr'] != 'orange')):
            # If found to be incorrect, make moves to bring incorrect
            # cubelette into top row and append moves to list.
            cube = helpers.move("L", cube)
            next_actions_list.append("L")
            cube = helpers.move("U", cube)
            next_actions_list.append("U")
            cube = helpers.move("L'", cube)
            next_actions_list.append("L'")
            print("NEXT - SQUARE dbl MOVED, LOOPING BACK")
            # Loop back to resolve moved squares accordingly.
            continue

        print("NEXT - NO INCORRECT CORNERS FOUND ON WHITE FACE.")
        # There are now no incorrectly positioned white corner squares
        # on the bottom face.

        # Now look for white corner squares on the top face and move
        # top face white squares to a side face.
        print("NEXT - NOW LOOKING FOR WHITE SQUARES ON TOP FACE")
        for square in config.top_face_corner_squares:
            if cube[square] == 'white':
                print("NEXT - WHITE SQUARE FOUND ON TOP FACE")
                # If top face square is directly above a white square
                # on bottom face, rotate top face until top face square
                # is not above a white square.
                if cube[config.top_face_corner_squares[square]] == 'white':
                    # Make moves to cube.
                    cube = helpers.move('U', cube)
                    # Append move to list.
                    next_actions_list.append("U")
                    print("NEXT - TOP FACE ROTATED")
                # If top face square is directly above a non-white
                # square, make moves to move it to the bottom face.
                else:
                    print("NEXT - TOP SQUARE MOVED TO FACE")
                    for action in config.top_face_corner_moves[square]:
                        # Append moves to list.
                        next_actions_list.append(action)
                        # Make moves to cube.
                        cube = helpers.move(action, cube)
                # If a square has been found, loop back to start to correctly
                # resolve that square before proceeding further.
                print("NEXT - LOOPING BACK AFTER TOP FACE SQUARE MOVED")
                continue
        print("NEXT - NO WHITE SQUARES FOUND ON TOP FACE")
        # Run progress check to confirm this stage is now solved and
        # to end the loop if solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 2 has now been solved.
    print("NEXT - PROGRESS NO LONGER 2, WHITE FACE NOW SOLVED")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the White Face stage.
    return next_actions_list


# Determine moves required to solve Stage 3, the Middle Row stage.
def solve_stage_3(cube, progress, next_actions_list):
    # This stage has previously sometimes endlessly looped; this
    # should now be fixed, however just in case there may be a cube
    # arrangement that causes a loop this stage includes a loop
    # count to return an error after a large number of loops.
    loop_count = 0
    while progress == 3:
        print("NEXT 3.00, middle row - progress found to be 3")
        # Maximum loop count to return error if endless loop occurs.
        loop_count = loop_count + 1
        print("Loop count = " + str(loop_count))
        if loop_count == 100:
            # Show error in list, which will display on page to user.
            next_actions_list = ["Error - too many loops"]
            print("NEXT - loop terminated after " + str(loop_count) + " loops")
            return next_actions_list
        # This stage can sometimes require a long list of moves, so
        # if more than 20 moves are required an interim list of moves
        # will be returned (that will partially solve this stage).
        if len(next_actions_list) > 20:
            print("NEXT - returning due to actions limit.")
            session["next_cube_colours"] = cube
            return next_actions_list
        print("NEXT 3.01, middle row - progress still 3")
        
        # Find edge cubelettes on top row with no yellow square,
        # then make appropriate moves to cube.
        top_row_edge_cubelettes = {'ftm':'ubm', 'ltm':'uml', 'btm':'utm', 'rtm':'umr'}
        # Continue to loop around until edge cubelettes in top row
        # all have >1 yellow square.  Start as True to begin loop.
        squares_found = True
        while squares_found is True:
            # Start loop as False, to continue to loop until none remaining.
            squares_found = False
            for square in top_row_edge_cubelettes:
                # Check if top row edge cubelette has no yellow square.
                if (cube[square] != 'yellow' and cube[top_row_edge_cubelettes[square]] != 'yellow'):
                    # Top row edge cubelette has no yellow square.
                    squares_found = True
                    print("NEXT 3.02, middle row - top row cubelette doesnt have yellow face, proceed.")
                    # If top row edge square does not match that face,
                    # then rotate the top face until it matches.
                    centre_square = config.centre_square_for_top_middle_square[square]
                    # Check if top row positioning matches the face.
                    if cube[centre_square] != cube[square]:
                        # Top row edge square does not match face,
                        # so rotate top row.
                        print("NEXT 3.03, middle row - middle square " + cube[centre_square] + " does not match top square " + cube[square] + ", so rotate.")
                        # Make required moves to cube.
                        cube = helpers.move("U", cube)
                        # Append moves to list.
                        next_actions_list.append("U")
                        # Loop back around until face/square match.
                        continue
                    # If top row edge square does match that face,
                    # proceed to make required moves.
                    else:
                        # Top row edge square matches face, so rotate
                        # top face away from the face that matches the
                        # colour of the top square. If top square
                        # matches left face, rotate top face
                        # anti-clockwise, and then make left trigger.
                        print("NEXT 3.04, middle row - cubelette is on correct face, proceed.")
                        top_square = top_row_edge_cubelettes[square]
                        left_face_centre = config.left_face_centre[top_square]
                        trigger_moves = {}
                        # Check if top square matches left face.
                        if cube[top_square] == cube[left_face_centre]:
                            # Top square found to match left face.
                            # so rotate top face anti-clockwise, and
                            # then make left trigger moves.
                            print("NEXT 3.05, middle row - " + cube[top_square] + " matching face " + cube[left_face_centre] + " to left, rotate top face anti-clockwise.")
                            # Prepare to make required moves.
                            trigger_moves = config.left_trigger_moves
                        else:
                            # Top square found to match right face.
                            # so rotate top face clockwise, and
                            # then make right trigger moves.
                            print("NEXT 3.06, middle row - " + cube[top_square] + " matching face " + cube[left_face_centre] + " to right, rotate top face clockwise.")
                            # Prepare to make required moves.
                            trigger_moves = config.right_trigger_moves
                        # Action the required trigger option from above:
                        for action in trigger_moves[square]:
                            # Append appropriate trigger moves to list.
                            next_actions_list.append(action)
                            # Make required trigger moves to cube.
                            cube = helpers.move(action, cube)
                        print("NEXT 3.07, middle row - moves made to cube.")
            
            # If squares found above, loop round again to continue
            # to find and resolve top row edge cubelettes.
            if squares_found is True:
                continue
            # If no squares found above, there are no outstanding
            # top row edge cubelettes, so break this loop to move on.
            else:
                break
        # The above may have solved this stage, so check progress and
        # either finalise this stage if solved, or continue to solve.
        progress = helpers.solve_progress(cube)
        if progress != 3:
            break
        
        # If no squares found but stage 3 is still not solved, then
        # there must be incorrect squares in the middle row.  Find
        # those incorrect squares and raise them to the top row, to be
        # moved to correct place.

        # Check if middle edge pieces are wrong colour, if so move out
        # of middle row.
        print("NEXT 3.08, middle row - check if middle row pieces are incorrect.")
        for square in config.middle_row_edge_moves:
            square_found = False
            if cube[square] != config.solved_cube[square]:
                square_found = True
                # Incorrect colour, so move square out of middle row.
                print("NEXT 3.09, middle row - incorrect piece found, move out.")
                for action in config.middle_row_edge_moves[square]:
                    # Append moves to list.
                    next_actions_list.append(action)
                    # Make moves to cube.
                    cube = helpers.move(action, cube)
                # Break loop to solve square that is now in top row.
                break
        # If incorrect square found above, this will now be in the top
        # row and need resolving, so loop back to beginning of stage 3.
        if square_found is True:
            # Break out of 'for' loop, return to stage 3 'while' loop.
            break

    # Stage 3 has now been solved. 
    print("NEXT 3.10, middle row - end of function")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the Middle Row stage.
    return next_actions_list


# Determine moves required to solve Stage 4, the Yellow Cross stage.
def solve_stage_4(cube, progress, next_actions_list):
    # The specific collection of moves specific to this stage is
    # memorised colloquially by a human as "fururf".

    # Moves required to be made depend on the number of yellow edge
    # squares already on the top face and their arrangement compared
    # to each other. 
    while progress == 4:
        print("NEXT 4.00, yellow cross - progress found to be 4")
        # Count yellow edge pieces on top face.
        top_face_edge_squares = ('utm', 'umr', 'ubm', 'uml')
        squares_found = 0
        # Count number of yellow edge squares on top face.
        for square in top_face_edge_squares:
            if cube[square] == 'yellow':
                squares_found = squares_found + 1

        # If there are either zero or one yellow edge piece on the top
        # face, then do the FURURF algorithm anyway.
        if squares_found < 2:
            for action in config.fururf:
                # Append moves to list.
                next_actions_list.append(action)
                # Make moves to cube.
                cube = helpers.move(action, cube)
        
        # If there are two yellow edge squares on opposite ends
        # (forming a line), arrange the top face so they are in
        # utm and ubm positions, then do FURURF algorithm.
        elif squares_found == 2:
            # Check orientation, then do fururf algorithm. 
            if (cube['utm'] == 'yellow' and cube['ubm'] == 'yellow'):
                # Orientation is correct, do fururf algorithm.
                for action in config.fururf:
                    # Append fururf moves to list.
                    next_actions_list.append(action)
                    # Make fururf moves to cube.
                    cube = helpers.move(action, cube)
            elif (cube['uml'] == 'yellow' and cube['umr'] == 'yellow'):
                # Orientation is incorrect, rotate top face.
                cube = helpers.move("U", cube)
                # Append move to list.
                next_actions_list.append("U")
                # Orientation now corrected, do fururf algorithm.
                for action in config.fururf:
                    # Append fururf moves to list.
                    next_actions_list.append(action)
                    # Make fururf moves to cube.
                    cube = helpers.move(action, cube)
            # If there are two yellow edge squares in an L-shape:
            else:
                # Rotate top face until yellow edge squares are in the
                # utm and uml positions, then do FURURF algorithm.
                while ((cube['uml'] != 'yellow') or (cube['utm'] != 'yellow')):
                    # Orientation is incorrect, rotate top face.
                    cube = helpers.move("U", cube)
                    # Append move to list.
                    next_actions_list.append("U")
                # Orientation is correct.
                for action in config.fururf:
                    # Append fururf moves to list.
                    next_actions_list.append(action)
                    # Make fururf moves to cube.
                    cube = helpers.move(action, cube)

        # If there are three yellow edge squares on top, rotate top
        # face so the only non-yellow edge square is in umr position,
        # then make fururf move.
        elif squares_found == 3:
            # Rotate top face until orientation is correct.
            while ((cube['uml'] != 'yellow') or (cube['utm'] != 'yellow') or (cube['ubm'] != 'yellow')):
                # Make move to cube.
                cube = helpers.move("U", cube)
                # Append move to list.
                next_actions_list.append("U")
            # When orientation is correct, then do FURURF algorithm.
            for action in config.fururf:
                # Append fururf moves to list.
                next_actions_list.append(action)
                # Make fururf moves to cube.
                cube = helpers.move(action, cube)
        
        # Check to see if the above has solved this stage to
        # either end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 4 has now been solved.
    print("NEXT 4., yellow cross - end of function")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the Yellow Cross stage.
    return next_actions_list


# Determine moves required to solve Stage 5, the Yellow Face stage.
def solve_stage_5(cube, progress, next_actions_list):
    # The specific collection of moves specific to this stage is
    # memorised colloquially by a human as "rururuur".
    # Depending on the number of yellow corner squares on the top face
    # and their orientation, different preperation is required before
    # making the rururuur algorithm.    
    while progress == 5:
        print("NEXT 5.00, yellow face - progress found to be 5")
        # Count yellow corner squares on top face.
        top_face_corner_squares = ('utl', 'utr', 'ubr', 'ubl')
        squares_found = 0
        for square in top_face_corner_squares:
            print("NEXT 5. - counting yellow corner squares on top face.")
            if cube[square] == 'yellow':
                squares_found = squares_found + 1
        print("NEXT 5. - " + str(squares_found) + " yellow squares found on top face.")

        # If 1 yellow corner square on top face, rotate top face so
        # ubl square is yellow.
        if squares_found == 1:
            # Rotate top face until ubl square is yellow.
            while cube['ubl'] != 'yellow':
                # Rotate top face of cube.
                cube = helpers.move("U", cube)
                # Append moves to list.
                next_actions_list.append("U")
            # Then do rururuur algorithm.
            for action in config.rururuur:
                # Append rururuur moves to list.
                next_actions_list.append(action)
                # Make rururuur moves to cube.
                cube = helpers.move(action, cube)

        # If zero or >1 top face corner squares are yellow then rotate
        # top face until ltr is yellow, then do RURURUUR algorithm.
        else:
            # Rotate top face until ltr square is yellow.
            while cube['ltr'] != 'yellow':
                # Rotate top face of cube.
                cube = helpers.move("U", cube)
                # Append move to list.
                next_actions_list.append("U")
            # Then do RURURUUR algorithm.
            for action in config.rururuur:
                # Append rururuur moves to list.
                next_actions_list.append(action)
                # Make rururuur moves to cube.
                cube = helpers.move(action, cube)
        
        # Check to see if the above has solved this stage to either
        # end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 5 has now been solved.
    print("NEXT 5., yellow face done - end of function")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the Yellow Face stage.
    return next_actions_list


# Determine moves required to solve Stage 6, the Top Corners stage.
def solve_stage_6(cube, progress, next_actions_list):
    # Find the most solved top row (either matching top row corners, or
    # matching top row), then move it to the correct face, and then
    # perform alogorithm (relative to that face) to solve the other
    # corners.

    # Define top row squares, relative to face centre squares.
    top_row_squares = config.top_row_squares
        
    while progress == 6:
        print("NEXT 6.00, top corners - progress found to be 6")
        match_found = False
        # Check if any faces have three matching squares in top row.
        for face in top_row_squares:
            square_0 = cube[top_row_squares[face][0]]
            square_1 = cube[top_row_squares[face][1]]
            square_2 = cube[top_row_squares[face][2]]
            if ((square_0 == square_1) and (square_0 == square_2)):
                # Record the colour of the squares that match, to know
                # which face the squares need to be moved to.
                colour_to_match = square_0
                # Record the squares that are to be moved.
                square_to_match = top_row_squares[face][0]
                match_found = True
                break

        # Check if any face has two corners the same colour.
        if match_found is False:
            for face in top_row_squares:
                square_0 = cube[top_row_squares[face][0]]
                square_2 = cube[top_row_squares[face][2]]
                if square_0 == square_2:
                    # Record the colour of the squares that match, to
                    # know which face the squares need to be moved to.
                    colour_to_match = square_0
                    # Record the squares that are to be moved.
                    square_to_match = top_row_squares[face][0]
                    match_found = True
                    break

        # If either is true, rotate the upper row to the correct face
        # (to match centre square), then depening on which face has
        # the matching corners, perform the appropriate algorithm.
        if match_found is True:
            # Calculate how many times to rotate top to match corners
            # to correct face, and make appropriate moves.
            # Associate a location number with each colour.
            colour_refs = {'blue':0, 'orange':1, 'green':2, 'red':3}
            # Associate a location number with each face.
            face_refs = {'ftl':0, 'ltl':1, 'btl':2, 'rtl':3}
            # Using above location numbers, determine shortest route
            # to move squares to correct face.
            rotations = colour_refs[colour_to_match] - face_refs[square_to_match]
            # Rotate either clockwise or anti-clockwise, whichever
            # is shortest.
            if rotations > 0:
                # Make moves clockwise
                for i in range(rotations):
                    # Make move to cube.
                    cube = helpers.move("U", cube)
                    # Append move to list.
                    next_actions_list.append("U")
            else:
                # Make moves anti-clockwise
                rotations = rotations * -1
                for i in range(rotations):
                    # Make move to cube.
                    cube = helpers.move("U'", cube)
                    # Append move to list.
                    next_actions_list.append("U'")
            # Then perform algorithm to begin to solve all corners.
            for action in config.colour_to_algo[colour_to_match]:
                # Append required corner solve moves to list.
                next_actions_list.append(action)
                # Make corner solve moves to cube.
                cube = helpers.move(action, cube)

        # If there are no matching corners, perform algorithm as if
        # left face was matching.
        if match_found is False:
            for action in config.colour_to_algo['orange']:
                # Append moves to list.
                next_actions_list.append(action)
                # Make moves to cube.
                cube = helpers.move(action, cube)
        
        # Check to see if the above has solved this stage to
        # either end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 6 has now been solved.
    print("NEXT 6., top corners done - end of function")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the Top Corners stage.
    return next_actions_list


# Determine moves required to solve Stage 7, the Top Row stage.
def solve_stage_7(cube, progress, next_actions_list):
    # If one face is already solved, the set of moves required is
    # based on the unsolved faces.  Each unsolved face will have only
    # the top row centre square unsolved - the set of moves required is
    # dependent on if that centre square's correct face is clockwise or
    # anti-clockwise from it's current position.
    # If all faces still have the top row edge square unsolved, make
    # anti-clockwise algorithm moves.    
    
    # Create dictionary of side faces only (not top/bottom), with
    # relevent squares on each face.
    side_faces = {
        key:config.faces[key] for key in ['green', 'orange', 'red', 'blue']
        }
    while progress == 7:
        print("NEXT 7.00, top row - progress found to be 7")
        # Check if one face is already solved.
        for face in side_faces:
            # Start assuming the face is solved.
            face_solved = True
            # Check if each square on this face matches the colour of
            # the face.
            for square in side_faces[face]:
                if cube[square] != face:
                    # If a square is found that does not match, stop
                    # checking this face and move to check other faces.
                    face_solved = False
                    break
            if face_solved is True:
                # If this face is found to be solved, stop checking
                # for any other faces and move on to make moves.
                face_to_align = face
                break
        # If no face is found to be solved, perform anti-clockwise
        # function based on any face. The green face has been chosen
        # randomly.
        if face_solved is False:
            # Do anti-clockwise algorithm moves.
            for action in config.face_anticlockwise_moves['green']:
                # Add anti-clockwise moves to list.
                next_actions_list.append(action)
                # Make anti-clockwise moves to cube.
                cube = helpers.move(action, cube)
        # If a face is solved, check if top row needs moving clockwise
        # or anti-clockwise, then make appropriate moves.
        if face_solved is True:
            # If front (blue) face is unsolved, then check if the
            # unsolved square on the front face matches the
            # left (orange) face. If so make clockwise moves. If not
            # not then make anti-clockwise moves.
            if face_to_align != 'blue':
                if cube['ftm'] == 'orange':
                    # Therefore clockwise algorithm required.
                    moves = config.face_clockwise_moves[face_to_align]
                else:
                    # Therefore anti-clockwise algorithm required.
                    moves = config.face_anticlockwise_moves[face_to_align]
            # If front face is solved, investigate the left (orange)
            # face instead.  If unsolved square of left face matches
            # the back face (green) then make clockwise moves. If not
            # then make anti-clockwise moves.
            else:
                if cube['ltm'] == 'green':
                    # Therefore clockwise algorithm required.
                    moves = config.face_clockwise_moves[face_to_align]
                else:
                    # Therefore anti-clockwise algorithm required.
                    moves = config.face_anticlockwise_moves[face_to_align]
            # Make moves as determined above.
            for action in moves:
                # Append moves to list.
                next_actions_list.append(action)
                # Make moves to cube.
                cube = helpers.move(action, cube)
        
        # Check to see if the above has solved this stage to either
        # end loop or continue to loop until solved.
        progress = helpers.solve_progress(cube)
    
    # Stage 7 has now been solved.
    print("NEXT 7., top edge pieces done, cube solved - end of function")
    # Update the session with the end result of this stage.
    session["next_cube_colours"] = cube
    # Return list of actions required to solve the Top Row stage.
    return next_actions_list
