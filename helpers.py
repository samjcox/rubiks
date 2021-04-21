from flask import session
import config

# Determine stage of solving (manual stage checking):
def solve_progress(cube):

    # Check if white cross is solved.
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

    # Check if white face is solved.
    white_face_solved = True
    white_face_squares = ('dtl', 'dtm', 'dtr', 'dml', 'dmm', 'dmr', 'dbl', 'dbm', 'dbr')
    for square in white_face_squares:
        if cube[square] != 'white':
                white_face_solved = False
                break

    # Check if middle row is solved.
    middle_row_solved = True
    middle_row_squares_green = ('bmr', 'bmm', 'bml')
    for square in middle_row_squares_green:
        if cube[square] != 'green':
            middle_row_solved = False
            break

    middle_row_squares_orange = ('lml', 'lmm', 'lmr')
    for square in middle_row_squares_orange:
        if cube[square] != 'orange':
            middle_row_solved = False
            break

    middle_row_squares_red = ('rmr', 'rmm', 'rml')
    for square in middle_row_squares_red:
        if cube[square] != 'red':
            middle_row_solved = False
            break

    middle_row_squares_blue = ('fml', 'fmm', 'fmr')
    for square in middle_row_squares_blue:
        if cube[square] != 'blue':
            middle_row_solved = False
            break

    # Check if yellow cross is solved.
    yellow_cross_squares = ('utm', 'uml', 'umm', 'umr', 'ubm')
    yellow_cross_solved = True
    for square in yellow_cross_squares:
        if cube[square] != 'yellow':
            yellow_cross_solved = False
            break

    # Check if yellow face is solved.
    yellow_face_solved = True
    yellow_face_squares = ('utl', 'utm', 'utr', 'uml', 'umm', 'umr', 'ubl', 'ubm', 'ubr')
    for square in yellow_face_squares:
        if cube[square] != 'yellow':
            yellow_face_solved = False
            break

    # Check if top corners are solved.
    top_corners_solved = True
    top_corners_squares_green = ('btr', 'btl')
    for square in top_corners_squares_green:
        if cube[square] != 'green':
            top_corners_solved = False
            break

    top_corners_squares_orange = ('ltl', 'ltr')
    for square in top_corners_squares_orange:
        if cube[square] != 'orange':
            top_corners_solved = False
            break

    top_corners_squares_red = ('rtr', 'rtl')
    for square in top_corners_squares_red:
        if cube[square] != 'red':
            top_corners_solved = False
            break

    top_corners_squares_blue = ('ftl', 'ftr')
    for square in top_corners_squares_blue:
        if cube[square] != 'blue':
            top_corners_solved = False
            break

    # Check if top row is solved.
    top_row_solved = True
    top_row_squares_green = ('btr', 'btm', 'btl')
    for square in top_row_squares_green:
        if cube[square] != 'green':
            top_row_solved = False
            break

    top_row_squares_orange = ('ltl', 'ltm', 'ltr')
    for square in top_row_squares_orange:
        if cube[square] != 'orange':
            top_row_solved = False
            break

    top_row_squares_red = ('rtr', 'rtm', 'rtl')
    for square in top_row_squares_red:
        if cube[square] != 'red':
            top_row_solved = False
            break

    top_row_squares_blue = ('ftl', 'ftm', 'ftr')
    for square in top_row_squares_blue:
        if cube[square] != 'blue':
            top_row_solved = False
            break

    # Check if whole cube is solved.
    stages_solved = {'daisy':daisy_solved, 'white_cross':white_cross_solved, 'white_face':white_face_solved, 'middle_row':middle_row_solved, 'yellow_cross':yellow_cross_solved, 'yellow_face':yellow_face_solved, 'top_corners':top_corners_solved, 'top_row':top_row_solved}

    # Summarise stage of solving.
    solve_progress = 0
    cube_solved = True
    for stage in stages_solved:
        if stages_solved[stage] == False:
            cube_solved = False
            break
        solve_progress = solve_progress + 1

    return (solve_progress)


# Function to convert cube notation into moves on a cube.
def notation_conversion(cube, notation):

    new_cube_colours = {}

    if notation == "R":
        new_cube_colours = move_rc(cube)
    elif notation == "R'":
        new_cube_colours = move_ra(cube)
    elif notation == "L":
        new_cube_colours = move_lc(cube)
    elif notation == "L'":
        new_cube_colours = move_la(cube)
    elif notation == "U":
        new_cube_colours = move_uc(cube)
    elif notation == "U'":
        new_cube_colours = move_ua(cube)
    elif notation == "D":
        new_cube_colours = move_dc(cube)
    elif notation == "D'":
        new_cube_colours = move_da(cube)
    elif notation == "B":
        new_cube_colours = move_bc(cube)
    elif notation == "B'":
        new_cube_colours = move_ba(cube)
    elif notation == "F":
        new_cube_colours = move_fc(cube)
    elif notation == "F'":
        new_cube_colours = move_fa(cube)

    return new_cube_colours

# Determine what moves are required.
def next_action():

    print("NEXT - START NEXT_ACTION FUNCTION")

    cube = session["next_cube_colours"]
    progress = solve_progress(cube)

    # Create blank list, ready to receive the list of moves required to
    # progress to solve the current stage of the cube.
    next_actions_list = []

    print("NEXT - FORMALITIES COMPLETED.")


    # If daisy not solved, solve daisy stage.
    if progress == 0:
        print("NEXT - PROGRESS FOUND TO BE 0.")
        while progress == 0:
            print("NEXT - PROGRESS STILL 0.")
            # Determine moves required to solve the daisy stage.
            # Start with moving white edge pieces from bottom face to top face.
            bottom_face_edge_squares = ('dtm', 'dml', 'dmr', 'dbm')
            print("NEXT - BEGIN ITERATION THROUGH BOTTOM FACE.")
            for square in bottom_face_edge_squares:
                if cube[square] == "white":
                    # for each white square on bottom face,
                    # check if the opposite square on top face is already white.
                    bottom_face_top_square = {'dtm':'ubm', 'dml':'uml', 'dbm':'utm', 'dmr':'umr'}
                    while cube[bottom_face_top_square[square]] == "white":
                        # Rotate top face to avoid existing white square on top face.
                        cube = move_uc(cube)
                        print("NEXT - MAKE MOVE U")
                        next_actions_list.append("U")
                    # If corresponding square on top face is not white,
                    # make move to get white square from bottom face to top face.
                    if cube[bottom_face_top_square[square]] != "white":
                        daisy_bottom_face_moves = {"dtm":("F", "F"), "dml":("L", "L"), "dmr":("R", "R"), "dbm":("B", "B")}
                        for action in daisy_bottom_face_moves[square]:
                            next_actions_list.append(action)
                            print("NEXT - MAKE MOVE " + str(daisy_bottom_face_moves[square]))
                            cube = notation_conversion(cube, action)
                    progress = solve_progress(cube)
            print("NEXT - NO WHITE SQUARES ON BOTTOM FACE")
            # Now there should be no white squares on the bottom face.

            # Next to look for white squares in the middle row.
            print("NEXT - BEGIN ITERATION THROUGH MIDDLE ROW.")
            middle_row_edge_squares = ('fml', 'fmr', 'rml', 'rmr', 'bml', 'bmr', 'lml', 'lmr')
            for square in middle_row_edge_squares:
                if cube[square] == "white":
                    # For each white square in the middle row,
                    # check if the appropriate square on the top face is already white.
                    daisy_middle_reference_top_square = {'fmr':'umr', 'fml':'uml', 'lmr':'ubm', 'lml':'utm', 'bmr':'uml', 'bml':'umr', 'rmr':'utm', 'rml':'ubm'}
                    while cube[daisy_middle_reference_top_square[square]] == 'white':
                        # Rotate top face to find alternative.
                        cube = move_uc(cube)
                        print("NEXT - MAKE MOVE U")
                        next_actions_list.append("U")
                    # If relevant square on top face is not white, then add appropriate move to queue.
                    if cube[daisy_middle_reference_top_square[square]] != 'white':
                        daisy_middle_moves = {"fmr":"R", "fml":"L'", "lmr":"F", "lml":"B'", "bmr":"L", "bml":"R'","rmr":"B'", "rml":"F'"}
                        next_actions_list.append(daisy_middle_moves[square])
                        print("NEXT - MAKE MOVE " + daisy_middle_moves[square])
                        # Convert Cube Notation into actual move_xx to action on next_cube_colours.
                        cube = notation_conversion(cube, daisy_middle_moves[square])
                    progress = solve_progress(cube)
            print("NEXT - NO WHITE SQUARES FOUND IN MIDDLE ROW")
            # Now there should be no white edge pieces in the middle row.

            # Next to look for white edge pieces in bottom row.
            bottom_row_edge_squares = ('fbm', 'lbm', 'bbm', 'rbm')
            print("NEXT - BEGIN ITERATION THROUGH BOTTOM ROW.")
            for square in bottom_row_edge_squares:
                if cube[square] == "white":
                    # For each white edge square in bottom row,
                    # check if appropriate square on top face is already white.
                    daisy_bottom_reference_top_square = {'fbm':'ubm', 'lbm':'uml', 'bbm':'utm', 'rbm':'umr'}
                    while cube[daisy_bottom_reference_top_square[square]] == 'white':
                        # Rotate top face to find alternative.
                        cube = move_uc(cube)
                        print("NEXT - MAKE MOVE U")
                        next_actions_list.append("U")
                    if cube[daisy_bottom_reference_top_square[square]] != 'white':
                        daisy_bottom_moves = {'fbm':("F", "U", "L'"), 'lbm':("L", "U", "B'"), 'bbm':("B", "U", "R'"), 'rbm':("R", "U", "F'")}
                        for action in daisy_bottom_moves[square]:
                            next_actions_list.append(action)
                            print("NEXT - MAKE MOVE " + str(daisy_bottom_moves[square]))
                            cube = notation_conversion(cube, action)

                    progress = solve_progress(cube)

            print("NEXT - NO WHITE SQUARES FOUND IN BOTTOM ROW")

            # Now there should be no white squares in the bottom row.

            # Next to look for white edge pieces in top row.
            top_row_edge_squares = ('ftm', 'ltm', 'btm', 'rtm')
            print("NEXT - BEGIN ITERATION THROUGH TOP ROW.")
            for square in top_row_edge_squares:
                if cube[square] == "white":
                    # For each white square in top row,
                    # move it onto the top face.
                    daisy_top_moves = {'ftm':("F", "U'", "R"), 'ltm':("L", "U'", "F"), 'btm':("B", "U'", "L"), 'rtm':("R", "U'", "B")}
                    for action in daisy_top_moves[square]:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)
                    progress = solve_progress(cube)
            print("NEXT - NO WHITE SQUARES FOUND IN TOP ROW")

        print("NEXT - PROGRESS NO LONGER 0.")

        # Update the session with the end result of this stage.
        session["next_cube_colours"] = cube
        print("NEXT - SESSION NEXT_CUBE_COLOURS UPDATED FROM STAGE 0.")
        # Return the list of actions required to solve the Daisy stage.
        return next_actions_list

    # If white cross not solved, solve white cross.
    elif progress == 1:
        print("NEXT - PROGRESS FOUND TO BE 1.")
        while progress == 1:
            print("NEXT - PROGRESS STILL 1.")
            # Move white squares from daisy on top face, to bottom face.
            while cube['ftm'] != cube['fmm'] or cube['ubm'] != 'white':
                cube = move_uc(cube)
                next_actions_list.append('U')
            else:
                cube = move_fc(move_fc(cube))
                next_actions_list.append('F')
                next_actions_list.append('F')

            while cube['ltm'] != cube['lmm'] or cube['uml'] != 'white':
                cube = move_uc(cube)
                next_actions_list.append('U')
            else:
                cube = move_lc(move_lc(cube))
                next_actions_list.append('L')
                next_actions_list.append('L')

            while cube['btm'] != cube['bmm'] or cube['utm'] != 'white':
                cube = move_uc(cube)
                next_actions_list.append('U')
            else:
                cube = move_bc(move_bc(cube))
                next_actions_list.append('B')
                next_actions_list.append('B')

            while cube['rtm'] != cube['rmm'] or cube['umr'] != 'white':
                cube = move_uc(cube)
                next_actions_list.append('U')
            else:
                cube = move_rc(move_rc(cube))
                next_actions_list.append('R')
                next_actions_list.append('R')
            progress = solve_progress(cube)

        print("NEXT - PROGRESS NO LONGER 1.")
        # Update the session with the end result of this stage.
        session["next_cube_colours"] = cube
        print("NEXT - SESSION NEXT_CUBE_COLOURS UPDATED FROM STAGE 1.")
        # Return the list of actions required to solve the Daisy stage.
        return next_actions_list


    # If white face not solved, solve white face.
    elif progress == 2:
        print("NEXT - PROGRESS FOUND TO BE 2")
        while progress == 2:
            print("NEXT - PROGRESS STILL 2")

            # Find any white squares in top row and move them to bottom face.
            top_row_corner_squares = {'ftl':'ltr', 'ftr':'rtl', 'ltl':'btr', 'ltr':'ftl', 'btl':'rtr', 'btr':'ltl', 'rtl':'ftr', 'rtr':'btl'}
            centre_square_for_square = {'ftl':'fmm', 'ftr':'fmm', 'rtl':'rmm', 'rtr':'rmm', 'btl':'bmm', 'btr':'bmm', 'ltl':'lmm', 'ltr':'lmm'}
            white_face_top_row_moves = {"ftl":("F", "U", "F'"), "ftr":("F'", "U'", "F"), "rtl":("R", "U", "R'"), "rtr":("R'", "U'", "R"), "btl":("B", "U", "B'"), "btr":("B'", "U'", "B"), "ltl":("L", "U", "L'"), "ltr":("L'", "U'", "L")}
            while True:
                print("NEXT - FINDING WHITE SQUARES ON TOP ROW")
                squares_found = 0
                for square in top_row_corner_squares:
                    if cube[square] == 'white':
                        print("NEXT - WHITE SQUARE FOUND ON TOP ROW - " + square)
                        squares_found = squares_found + 1
                        adjacent_corner_square = top_row_corner_squares[square]
                        centre_square = centre_square_for_square[adjacent_corner_square]
                        if cube[adjacent_corner_square] == cube[centre_square]:
                            # Make move to move piece to bottom face.
                            print("NEXT - WHITE SQUARE IN CORRECT POSITION IN TOP ROW, MOVED TO BOTTOM FACE - " + square)
                            for action in white_face_top_row_moves[square]:
                                next_actions_list.append(action)
                                cube = notation_conversion(cube, action)
                            progress = solve_progress(cube)

                        else:
                            print("NEXT - TOP ROW WHITE SQUARE NOT CORRECT, ROTATE TOP ROW")
                            cube = move_uc(cube)
                            next_actions_list.append("U")

                if squares_found == 0:
                    print("NEXT - NO WHITE SQUARES REMAIN/FOUND IN TOP ROW")
                    break
            # There are now no white squares in the top row.

            # Now look for white squares in the bottom row.
            bottom_row_corner_squares = {"fbl":("F", "U", "F'"), "fbr":("F'", "U'", "F"), "rbl":("R", "U", "R'"), "rbr":("R'", "U'", "R"), "bbl":("B", "U", "B'"), "bbr":("B'", "U'", "B"), "lbl":("L", "U", "L'"), "lbr":("L'", "U'", "L")}
            squares_found = 0
            print("NEXT - LOOKING FOR WHITE SQUARES IN BOTTOM ROW")
            for square in bottom_row_corner_squares:
                if cube[square] == 'white':
                    print("NEXT - WHITE SQUARE FOUND IN BOTTOM ROW")
                    squares_found = squares_found + 1
                    for action in bottom_row_corner_squares[square]:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)
                    break
            if squares_found > 0:
                print("NEXT - LOOPING BACK AS WHITE SQUARES FOUND IN BOTTOM ROW")
                continue
            print("NEXT - NO WHITE SQUARES FOUND IN BOTTOM ROW.")
            # There are now no white squares in the bottom row.

            # Now look for incorrect white corner squares on the bottom face,
            # and bring them into the top row for correct repositioning.
            print("NEXT - NOW LOOKING FOR INCORRECT CORNERS ON WHITE FACE.")
            if (cube['dtl'] == 'white' and (cube['fbl'] != 'blue' or cube['lbr'] != 'orange')):
                squares_found = squares_found + 1
                cube = move_la(cube)
                next_actions_list.append("L'")
                cube = move_ua(cube)
                next_actions_list.append("U'")
                cube = move_lc(cube)
                next_actions_list.append("L")
                print("NEXT - SQUARE dtl MOVED, LOOPING BACK")
                continue

            if (cube['dtr'] == 'white' and (cube['fbr'] != 'blue' or cube['rbl'] != 'red')):
                squares_found = squares_found + 1
                cube = move_rc(cube)
                next_actions_list.append("R")
                cube = move_uc(cube)
                next_actions_list.append("U")
                cube = move_ra(cube)
                next_actions_list.append("R'")
                print("NEXT - SQUARE dtr MOVED, LOOPING BACK")
                continue

            if (cube['dbr'] == 'white' and (cube['bbl'] != 'green' or cube['rbr'] != 'red')):
                squares_found = squares_found + 1
                cube = move_ra(cube)
                next_actions_list.append("R'")
                cube = move_ua(cube)
                next_actions_list.append("U'")
                cube = move_rc(cube)
                next_actions_list.append("R")
                print("NEXT - SQUARE dbr MOVED, LOOPING BACK")
                continue

            if (cube['dbl'] == 'white' and (cube['fbl'] != 'blue' or cube['lbr'] != 'orange')):
                squares_found = squares_found + 1
                cube = move_lc(cube)
                next_actions_list.append("L")
                cube = move_uc(cube)
                next_actions_list.append("U")
                cube = move_la(cube)
                next_actions_list.append("L'")
                print("NEXT - SQUARE dbl MOVED, LOOPING BACK")
                continue

            print("NEXT - NO INCORRECT CORNERS FOUND ON WHITE FACE.")
            # There are now no incorrectly positioned white corner squares
            # on the bottom face.

            # Now look for white corner squares on the top face.
            # move top face squares to a side face.
            top_face_corner_squares = {'ubl':'dtl', 'utl':'dbl', 'utr':'dbr', 'ubr':'dtr'}
            top_face_corner_moves = {"ubl":("L'", "U'", "U'", "L"), "ubr":("R", "U", "U", "R'"), "utr":("R'", "U'", "U'", "R"), "utl":("L", "U", "U", "L'")}
            squares_found = 0
            print("NEXT - NOW LOOKING FOR WHITE SQUARES ON TOP FACE")
            for square in top_face_corner_squares:
                if cube[square] == 'white':
                    print("NEXT - WHITE SQUARE FOUND ON TOP FACE")
                    squares_found = squares_found + 1
                    if cube[top_face_corner_squares[square]] == 'white':
                        cube = move_uc(cube)
                        next_actions_list.append("U")
                        print("NEXT - TOP FACE ROTATED")
                    else:
                        print("NEXT - TOP SQUARE MOVED TO FACE")
                        for action in top_face_corner_moves[square]:
                            next_actions_list.append(action)
                            cube = notation_conversion(cube, action)
            if squares_found > 0:
                print("NEXT - LOOPING BACK AFTER TOP FACE SQUARE MOVED")
                continue

        session["next_cube_colours"] = cube
        print("NEXT - PROGRESS NO LONGER 2, WHITE FACE NOW SOLVED")
        return next_actions_list

    # If middle row not solved, solve middle row.

    elif progress == 3:
        print("NEXT 3.00, middle row - progress found to be 3")
        loop_count = 0
        while progress == 3:
            # Limit number of moves returned to a maximum.
            if len(next_actions_list) > 20:
                print("NEXT - returning due to actions limit.")
                session["next_cube_colours"] = cube
                return next_actions_list
            loop_count = loop_count + 1
            print("Loop count = " + str(loop_count))
            if loop_count == 100:
                next_actions_list = ["Error - too many loops"]
                print("NEXT - loop terminated after " + str(loop_count) + " loops")
                return next_actions_list
            print("NEXT 3.01, middle row - progress still 3")
            print(cube)
            # Find cubelettes on top row that do not have a yellow face on either square.
            top_row_edge_cubelettes = {'ftm':'ubm', 'ltm':'uml', 'btm':'utm', 'rtm':'umr'}

            # Loop around while there is a non-yellow edge cubelette in the top row.
            non_yellow_remaining = True
            while non_yellow_remaining == True:
                for square in top_row_edge_cubelettes:
                    if (cube[square] != 'yellow' and cube[top_row_edge_cubelettes[square]] != 'yellow'):
                        non_yellow_remaining = True
                        # Check if top row positioning matches the face.
                        print("NEXT 3.02, middle row - top row cubelette doesnt have yellow face, proceed.")
                        centre_square_for_top_middle_square = {'ftm':'fmm', 'ltm':'lmm', 'btm':'bmm', 'rtm':'rmm'}
                        if cube[centre_square_for_top_middle_square[square]] != cube[square]:
                            # Rotate top row so side square is on correct face.
                            print("NEXT 3.03, middle row - middle square " + cube[centre_square_for_top_middle_square[square]] + " does not match top square " + cube[square] + ", so rotate.")
                            cube = move_uc(cube)
                            next_actions_list.append("U")
                            continue
                        else:
                            # Then rotate top row away from the face that matches the colour of the top square.
                            # if top square matches left face middle, rotate top face anti-clockwise, and then perform left trigger move.
                            print("NEXT 3.04, middle row - cubelette is on correct face, proceed.")
                            corresponding_left_face_centre = {'ubm':'lmm', 'uml':'bmm', 'utm':'rmm', 'umr':'fmm'}
                            top_square = top_row_edge_cubelettes[square]
                            trigger_moves = {}
                            if cube[top_square] == cube[corresponding_left_face_centre[top_square]]:
                                print("NEXT 3.05, middle row - " + cube[top_square] + " matching face " + cube[corresponding_left_face_centre[top_square]] + " to left, rotate top face anti-clockwise.")
                                cube = move_ua(cube)
                                next_actions_list.append("U'")
                                trigger_moves = {
                                    "ftm":("L'", "U'", "L", "U", "F", "U", "F'"),
                                    "ltm":("B'", "U'", "B", "U", "L", "U", "L'"),
                                    "btm":("R'", "U'", "R", "U", "B", "U", "B'"),
                                    "rtm":("F'", "U'", "F", "U", "R", "U", "R'")
                                }
                            # else (i.e. top square matches right face middle), rotate top face clockwise, and then perform right trigger move.
                            else:
                                print("NEXT 3.06, middle row - " + cube[top_square] + " matching face " + cube[corresponding_left_face_centre[top_square]] + " to right, rotate top face clockwise.")
                                cube = move_uc(cube)
                                next_actions_list.append("U")
                                trigger_moves = {
                                    "ftm":("R", "U", "R'", "U'", "F'", "U'", "F"),
                                    "ltm":("F", "U", "F'", "U'", "L'", "U'", "L"),
                                    "btm":("L", "U", "L'", "U'", "B'", "U'", "B"),
                                    "rtm":("B", "U", "B'", "U'", "R'", "U'", "R")
                                }

                            # Action either trigger option:

                            for action in trigger_moves[square]:
                                next_actions_list.append(action)
                                cube = notation_conversion(cube, action)
                            # Check if above has solve this stage.
                            print("NEXT 3.07, middle row - moves made to cube.")
                            progress = solve_progress(cube)

                for square in top_row_edge_cubelettes:
                    if (cube[square] != 'yellow' and cube[top_row_edge_cubelettes[square]] != 'yellow'):
                        non_yellow_remaining = True
                        break
                    else:
                        non_yellow_remaining = False

            # Then if no yellow edge pieces in top row left, but middle row still not solved:
            # raise that middle piece to the top row, to be moved to correct place.
            middle_row_edge_squares = {
                'fml':("L'", "U'", "L", "U", "F", "U", "F'"),
                'fmr':("R", "U", "R'", "U'", "F'", "U'", "F"),
                'rml':("R", "U", "R'", "U'", "F'", "U'", "F"),
                'rmr':("R'", "U'", "R", "U", "B", "U", "B'"),
                'bml':("R'", "U'", "R", "U", "B", "U", "B'"),
                'bmr':("L", "U", "L'", "U'", "B'", "U'", "B"),
                'lml':("L", "U", "L'", "U'", "B'", "U'", "B"),
                'lmr':("L'", "U'", "L", "U", "F", "U", "F'"),
            }

            # check if middle edge pieces are wrong colour, if so move out of middle row.
            print("NEXT 3.08, middle row - check if middle row pieces are incorrect.")
            for square in middle_row_edge_squares:
                if cube[square] != config.solved_cube[square]:
                    # Incorrect colour, so move square out of middle row.
                    print("NEXT 3.09, middle row - incorrect piece found, move out.")
                    for action in middle_row_edge_squares[square]:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)
                    # Look back to solve square that is now in top row.
                    break
            progress = solve_progress(cube)
            if progress == 3:
                continue

        session["next_cube_colours"] = cube
        print("NEXT 3.10, middle row - end of function")
        return next_actions_list

    # If yellow cross not solved, solve yellow cross.
    elif progress == 4:
        print("NEXT 4.00, yellow cross - progress found to be 4")
        fururf = ("F", "U", "R", "U'", "R'", "F'")

        while progress == 4:
            # count yellow edge pieces on top face.
            top_face_edge_squares = ('utm', 'umr', 'ubm', 'uml')
            squares_found = 0
            for square in top_face_edge_squares:
                if cube[square] == 'yellow':
                    squares_found = squares_found + 1

            # if there are no yellow edge pieces on the top face or one yellow edge piece,
            # then do the FURURF algorithm.
            if squares_found < 2:
                for action in fururf:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            elif squares_found == 2:
                # if there are two yellow edge pieces on opposite ends,
                # arrange the top face so they are in utm and ubm positions,
                # then do FURURF algorithm
                if (cube['utm'] == 'yellow' and cube['ubm'] == 'yellow'):
                    for action in fururf:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)
                elif (cube['uml'] == 'yellow' and cube['umr'] == 'yellow'):
                    cube = move_uc(cube)
                    next_actions_list.append("U")
                    for action in fururf:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)
                # if there are two yellow edge pieces not in line:
                else:
                    # rotate the top face until they are in the utm and uml positions,
                    # then do FURURF algorithm.
                    while ((cube['uml'] != 'yellow') or (cube['utm'] != 'yellow')):
                        cube = move_uc(cube)
                        next_actions_list.append("U")
                    for action in fururf:
                        next_actions_list.append(action)
                        cube = notation_conversion(cube, action)

            # if three yellow pieces on top, rotate top face so the only non-yellow edge piece is in umr.
            elif squares_found == 3:
                while ((cube['uml'] != 'yellow') or (cube['utm'] != 'yellow') or (cube['ubm'] != 'yellow')):
                    cube = move_uc(cube)
                    next_actions_list.append("U")
                # then do FURURF algorithm.
                for action in fururf:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            progress = solve_progress(cube)

        session["next_cube_colours"] = cube
        print("NEXT 4., yellow cross - end of function")
        return next_actions_list


    # If yellow face not solved, solve yellow face.
    elif progress == 5:
        print("NEXT 5.00, yellow face - progress found to be 5")
        rururuur = ("R", "U", "R'", "U", "R", "U", "U", "R'")

        while progress == 5:
            # count yellow corner pieces on top face.
            top_face_corner_squares = ('utl', 'utr', 'ubr', 'ubl')
            squares_found = 0
            for square in top_face_corner_squares:
                print("NEXT 5. - counting yellow corner squares on top face.")
                if cube[square] == 'yellow':
                    squares_found = squares_found + 1
            print("NEXT 5. - " + str(squares_found) + " yellow squares found on top face.")

            # if 1 yellow corner square on top face,
            # rotate top face so ubl square is yellow.
            if squares_found == 1:
                while cube['ubl'] != 'yellow':
                    cube = move_uc(cube)
                    next_actions_list.append("U")
                # then do RURURUUR algorithm.
                for action in rururuur:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            # else, rotate top face until ltr is yellow,
            # then do RURURUUR algorithm.
            else:
                while cube['ltr'] != 'yellow':
                    cube = move_uc(cube)
                    next_actions_list.append("U")
                # then do RURURUUR algorithm.
                for action in rururuur:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            progress = solve_progress(cube)

        session["next_cube_colours"] = cube
        print("NEXT 5., yellow face done - end of function")
        return next_actions_list

    # If top corners not solved, solve top corners.
    elif progress == 6:
        print("NEXT 6.00, top corners - progress found to be 6")

        while progress == 6:

            top_row_squares = {'lmm':('ltl', 'ltm', 'ltr'), 'bmm':('btl', 'btm', 'btr'), 'rmm':('rtl', 'rtm', 'rtr'), 'fmm':('ftl', 'ftm', 'ftr')}
            centre_squares_for_corners = {'ltl':'lmm', 'btl':'bmm', 'rtl':'rmm', 'ftl':'fmm'}


            colour_refs = {'blue':0, 'orange':1, 'green':2, 'red':3}
            face_refs = {'ftl':0, 'ltl':1, 'btl':2, 'rtl':3}
            colour_to_algo = {
                'orange':("L'", "U", "R", "U'", "L", "U", "U", "R'", "U", "R", "U", "U", "R'"),
                'green':("B'", "U", "F", "U'", "B", "U", "U", "F'", "U", "F", "U", "U", "F'"),
                'red':("R'", "U", "L", "U'", "R", "U", "U", "L'", "U", "L", "U", "U", "L'"),
                'blue':("F'", "U", "B", "U'", "F", "U", "U", "B'", "U", "B", "U", "U", "B'")
            }

            match_found = False

            # Check if any faces have three matching squares in top row.
            for face in top_row_squares:
                if ((cube[top_row_squares[face][0]] == cube[top_row_squares[face][1]]) and (cube[top_row_squares[face][0]] == cube[top_row_squares[face][2]])):
                    colour_to_match = cube[top_row_squares[face][0]]
                    square_to_match = top_row_squares[face][0]
                    match_found = True
                    break

            # If not three matching squares, check if any faces have two corners the same colour,
            if match_found == False:
                for face in top_row_squares:
                    if (cube[top_row_squares[face][0]] == cube[top_row_squares[face][2]]):
                        colour_to_match = cube[top_row_squares[face][0]]
                        square_to_match = top_row_squares[face][0]
                        match_found = True
                        break

            # If either is true, rotate the upper row to the correct face (to match centre square),
            # then depening on which face has the matching corners, perform the appropriate algorithm.
            if match_found == True:

                # Calculate how many times to rotate top to match corners to correct face,
                # and make moves to align corners with correct face.
                rotations = colour_refs[colour_to_match] - face_refs[square_to_match]
                if rotations > 0:
                    # Make moves clockwise
                    for i in range(rotations):
                        cube = move_uc(cube)
                        next_actions_list.append("U")
                else:
                    # Make moves anti-clockwise
                    rotations = rotations * -1
                    for i in range(rotations):
                        cube = move_ua(cube)
                        next_actions_list.append("U'")

                # Then perform algorithm to begin to solve all corners.
                for action in colour_to_algo[colour_to_match]:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            # If there are no matching corners, perform algorithm as if left face was matching.
            if match_found == False:
                for action in colour_to_algo['orange']:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            progress = solve_progress(cube)

        session["next_cube_colours"] = cube
        print("NEXT 6., top corners done - end of function")
        return next_actions_list

    # If top row not solved, solve top row.
    elif progress == 7:

        # Reference information in config file.
        side_faces = {key:config.faces[key] for key in ['green', 'orange', 'red', 'blue']}
        face_anticlockwise_moves = config.face_anticlockwise_moves
        face_clockwise_moves = config.face_clockwise_moves

        while progress == 7:
            # Check if one face is already solved.
            for face in side_faces:
                face_solved = True
                #face = face
                for square in side_faces[face]:
                    if cube[square] != face:
                        face_solved = False
                        break
                if face_solved == True:
                    face_to_align = face
                    break
            # If no face solved, perform anti-clockwise function based on any face.
            if face_solved == False:
                for action in face_anticlockwise_moves['green']:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)
            # If a face is solved, check if top row needs moving clockwise or anti-clockwise,
            if face_solved == True:
                if face_to_align != 'blue':
                    if cube['ftm'] == 'orange':
                        # Therefore clockwise algorithm required.
                        moves = face_clockwise_moves[face_to_align]
                    else:
                        # Therefore anti-clockwise algorithm required.
                        moves = face_anticlockwise_moves[face_to_align]
                else:
                    if cube['ltm'] == 'green':
                        # Therefore clockwise algorithm required.
                        moves = face_clockwise_moves[face_to_align]
                    else:
                        # Therefore anti-clockwise algorithm required.
                        moves = face_anticlockwise_moves[face_to_align]
                for action in moves:
                    next_actions_list.append(action)
                    cube = notation_conversion(cube, action)

            progress = solve_progress(cube)

        session["next_cube_colours"] = cube
        print("NEXT 7., top edge pieces done, cube solved - end of function")
        return next_actions_list


def improve_efficiency(next_actions_list):
    # Improve efficiency of moves in next_actions_list.
    # Repeat until no inefficiencies found.
    inefficiencies = True
    while inefficiencies == True:
        print("SOLVE - start loop to remove inefficiencies.")
        inefficiencies = False
        # Exchange triple moves with one of the opposite move.
        move_to_replace_triples = {"F":"F'", "F'":"F", "U":"U'", "U'":"U", "L":"L'", "L'":"L", "R":"R'", "R'":"R", "D":"D'", "D'":"D", "B":"B'", "B'":"B"}
        list_length = len(next_actions_list)
        index = 0
        while index < (list_length - 3):
            if ((next_actions_list[index] == next_actions_list[index + 1]) and (next_actions_list[index] == next_actions_list[index + 2])):
                print("SOLVE - TRIPLE MOVES FOUND & REPLACED: " + next_actions_list[index])
                next_actions_list[index] = move_to_replace_triples[next_actions_list[index]]
                next_actions_list.pop(index + 1)
                next_actions_list.pop(index + 1)
                list_length = list_length - 2
                inefficiencies = True
            index = index + 1

        # Remove opposite moves directly one after the other.
        opposite_moves = {"F":"F'", "F'":"F", "U":"U'", "U'":"U", "L":"L'", "L'":"L", "R":"R'", "R'":"R", "D":"D'", "D'":"D", "B":"B'", "B'":"B"}
        list_length = len(next_actions_list)
        index = 0
        while index < (list_length - 2):
            if next_actions_list[index + 1] == opposite_moves[next_actions_list[index]]:
                print("SOLVE - OPPOSITE MOVES FOUND & REMOVED")
                next_actions_list.pop(index)
                next_actions_list.pop(index)
                list_length = list_length - 2
                inefficiencies = True
            index = index + 1

    print("SOLVE - NEXT ACTIONS LIST UPDATED.")

    return next_actions_list


# INDIVIDUAL CUBE MOVES BELOW

# R (clockwise)
def move_rc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['rtr'] = cube['rtl']
    new_cube_colours['rmr'] = cube['rtm']
    new_cube_colours['rbr'] = cube['rtr']
    new_cube_colours['rtm'] = cube['rml']
    new_cube_colours['rbm'] = cube['rmr']
    new_cube_colours['rtl'] = cube['rbl']
    new_cube_colours['rml'] = cube['rbm']
    new_cube_colours['rbl'] = cube['rbr']
    new_cube_colours['utr'] = cube['ftr']
    new_cube_colours['umr'] = cube['fmr']
    new_cube_colours['ubr'] = cube['fbr']
    new_cube_colours['bbl'] = cube['utr']
    new_cube_colours['bml'] = cube['umr']
    new_cube_colours['btl'] = cube['ubr']
    new_cube_colours['ftr'] = cube['dtr']
    new_cube_colours['fmr'] = cube['dmr']
    new_cube_colours['fbr'] = cube['dbr']
    new_cube_colours['dbr'] = cube['btl']
    new_cube_colours['dmr'] = cube['bml']
    new_cube_colours['dtr'] = cube['bbl']

    return new_cube_colours

# R' (anti-clockwise)
def move_ra(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['rtl'] = cube['rtr']
    new_cube_colours['rtm'] = cube['rmr']
    new_cube_colours['rtr'] = cube['rbr']
    new_cube_colours['rml'] = cube['rtm']
    new_cube_colours['rmr'] = cube['rbm']
    new_cube_colours['rbl'] = cube['rtl']
    new_cube_colours['rbm'] = cube['rml']
    new_cube_colours['rbr'] = cube['rbl']
    new_cube_colours['ftr'] = cube['utr']
    new_cube_colours['fmr'] = cube['umr']
    new_cube_colours['fbr'] = cube['ubr']
    new_cube_colours['utr'] = cube['bbl']
    new_cube_colours['umr'] = cube['bml']
    new_cube_colours['ubr'] = cube['btl']
    new_cube_colours['dtr'] = cube['ftr']
    new_cube_colours['dmr'] = cube['fmr']
    new_cube_colours['dbr'] = cube['fbr']
    new_cube_colours['btl'] = cube['dbr']
    new_cube_colours['bml'] = cube['dmr']
    new_cube_colours['bbl'] = cube['dtr']

    return new_cube_colours

# L (clockwise)
def move_lc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['ltr'] = cube['ltl']
    new_cube_colours['lmr'] = cube['ltm']
    new_cube_colours['lbr'] = cube['ltr']
    new_cube_colours['ltm'] = cube['lml']
    new_cube_colours['lbm'] = cube['lmr']
    new_cube_colours['ltl'] = cube['lbl']
    new_cube_colours['lml'] = cube['lbm']
    new_cube_colours['lbl'] = cube['lbr']
    new_cube_colours['dtl'] = cube['ftl']
    new_cube_colours['dml'] = cube['fml']
    new_cube_colours['dbl'] = cube['fbl']
    new_cube_colours['ftl'] = cube['utl']
    new_cube_colours['fml'] = cube['uml']
    new_cube_colours['fbl'] = cube['ubl']
    new_cube_colours['bbr'] = cube['dtl']
    new_cube_colours['bmr'] = cube['dml']
    new_cube_colours['btr'] = cube['dbl']
    new_cube_colours['ubl'] = cube['btr']
    new_cube_colours['uml'] = cube['bmr']
    new_cube_colours['utl'] = cube['bbr']

    return new_cube_colours

# L' (anti-clockwise)
def move_la(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['ltl'] = cube['ltr']
    new_cube_colours['ltm'] = cube['lmr']
    new_cube_colours['ltr'] = cube['lbr']
    new_cube_colours['lml'] = cube['ltm']
    new_cube_colours['lmr'] = cube['lbm']
    new_cube_colours['lbl'] = cube['ltl']
    new_cube_colours['lbm'] = cube['lml']
    new_cube_colours['lbr'] = cube['lbl']
    new_cube_colours['ftl'] = cube['dtl']
    new_cube_colours['fml'] = cube['dml']
    new_cube_colours['fbl'] = cube['dbl']
    new_cube_colours['utl'] = cube['ftl']
    new_cube_colours['uml'] = cube['fml']
    new_cube_colours['ubl'] = cube['fbl']
    new_cube_colours['dtl'] = cube['bbr']
    new_cube_colours['dml'] = cube['bmr']
    new_cube_colours['dbl'] = cube['btr']
    new_cube_colours['btr'] = cube['ubl']
    new_cube_colours['bmr'] = cube['uml']
    new_cube_colours['bbr'] = cube['utl']

    return new_cube_colours

# U (clockwise)
def move_uc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['utr'] = cube['utl']
    new_cube_colours['umr'] = cube['utm']
    new_cube_colours['ubr'] = cube['utr']
    new_cube_colours['utm'] = cube['uml']
    new_cube_colours['ubm'] = cube['umr']
    new_cube_colours['utl'] = cube['ubl']
    new_cube_colours['uml'] = cube['ubm']
    new_cube_colours['ubl'] = cube['ubr']
    new_cube_colours['btl'] = cube['ltl']
    new_cube_colours['btm'] = cube['ltm']
    new_cube_colours['btr'] = cube['ltr']
    new_cube_colours['rtr'] = cube['btr']
    new_cube_colours['rtm'] = cube['btm']
    new_cube_colours['rtl'] = cube['btl']
    new_cube_colours['ftr'] = cube['rtr']
    new_cube_colours['ftm'] = cube['rtm']
    new_cube_colours['ftl'] = cube['rtl']
    new_cube_colours['ltl'] = cube['ftl']
    new_cube_colours['ltm'] = cube['ftm']
    new_cube_colours['ltr'] = cube['ftr']

    return new_cube_colours

# U' (anti-clockwise)
def move_ua(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['utl'] = cube['utr']
    new_cube_colours['utm'] = cube['umr']
    new_cube_colours['utr'] = cube['ubr']
    new_cube_colours['uml'] = cube['utm']
    new_cube_colours['umr'] = cube['ubm']
    new_cube_colours['ubl'] = cube['utl']
    new_cube_colours['ubm'] = cube['uml']
    new_cube_colours['ubr'] = cube['ubl']
    new_cube_colours['ltl'] = cube['btl']
    new_cube_colours['ltm'] = cube['btm']
    new_cube_colours['ltr'] = cube['btr']
    new_cube_colours['btr'] = cube['rtr']
    new_cube_colours['btm'] = cube['rtm']
    new_cube_colours['btl'] = cube['rtl']
    new_cube_colours['rtr'] = cube['ftr']
    new_cube_colours['rtm'] = cube['ftm']
    new_cube_colours['rtl'] = cube['ftl']
    new_cube_colours['ftl'] = cube['ltl']
    new_cube_colours['ftm'] = cube['ltm']
    new_cube_colours['ftr'] = cube['ltr']

    return new_cube_colours

# F' (anti-clockwise)
def move_fa(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['ftl'] = cube['ftr']
    new_cube_colours['ftm'] = cube['fmr']
    new_cube_colours['ftr'] = cube['fbr']
    new_cube_colours['fml'] = cube['ftm']
    new_cube_colours['fmr'] = cube['fbm']
    new_cube_colours['fbl'] = cube['ftl']
    new_cube_colours['fbm'] = cube['fml']
    new_cube_colours['fbr'] = cube['fbl']

    new_cube_colours['ltr'] = cube['ubr']
    new_cube_colours['lmr'] = cube['ubm']
    new_cube_colours['lbr'] = cube['ubl']
    new_cube_colours['ubl'] = cube['rtl']
    new_cube_colours['ubm'] = cube['rml']
    new_cube_colours['ubr'] = cube['rbl']
    new_cube_colours['rtl'] = cube['dtr']
    new_cube_colours['rml'] = cube['dtm']
    new_cube_colours['rbl'] = cube['dtl']
    new_cube_colours['dtl'] = cube['ltr']
    new_cube_colours['dtm'] = cube['lmr']
    new_cube_colours['dtr'] = cube['lbr']

    return new_cube_colours

# F (clockwise)
def move_fc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['ftr'] = cube['ftl']
    new_cube_colours['fmr'] = cube['ftm']
    new_cube_colours['fbr'] = cube['ftr']
    new_cube_colours['ftm'] = cube['fml']
    new_cube_colours['fbm'] = cube['fmr']
    new_cube_colours['ftl'] = cube['fbl']
    new_cube_colours['fml'] = cube['fbm']
    new_cube_colours['fbl'] = cube['fbr']

    new_cube_colours['ubr'] = cube['ltr']
    new_cube_colours['ubm'] = cube['lmr']
    new_cube_colours['ubl'] = cube['lbr']
    new_cube_colours['rtl'] = cube['ubl']
    new_cube_colours['rml'] = cube['ubm']
    new_cube_colours['rbl'] = cube['ubr']
    new_cube_colours['dtr'] = cube['rtl']
    new_cube_colours['dtm'] = cube['rml']
    new_cube_colours['dtl'] = cube['rbl']
    new_cube_colours['ltr'] = cube['dtl']
    new_cube_colours['lmr'] = cube['dtm']
    new_cube_colours['lbr'] = cube['dtr']

    return new_cube_colours

# B (clockwise)
def move_bc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['bbr'] = cube['btr']
    new_cube_colours['bmr'] = cube['btm']
    new_cube_colours['btr'] = cube['btl']
    new_cube_colours['bbm'] = cube['bmr']
    new_cube_colours['btm'] = cube['bml']
    new_cube_colours['bbl'] = cube['bbr']
    new_cube_colours['bml'] = cube['bbm']
    new_cube_colours['btl'] = cube['bbl']
    new_cube_colours['lbl'] = cube['utl']
    new_cube_colours['lml'] = cube['utm']
    new_cube_colours['ltl'] = cube['utr']
    new_cube_colours['dbl'] = cube['ltl']
    new_cube_colours['dbm'] = cube['lml']
    new_cube_colours['dbr'] = cube['lbl']
    new_cube_colours['rbr'] = cube['dbl']
    new_cube_colours['rmr'] = cube['dbm']
    new_cube_colours['rtr'] = cube['dbr']
    new_cube_colours['utl'] = cube['rtr']
    new_cube_colours['utm'] = cube['rmr']
    new_cube_colours['utr'] = cube['rbr']

    return new_cube_colours

# B' (anti-clockwise)
def move_ba(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['btr'] = cube['bbr']
    new_cube_colours['btm'] = cube['bmr']
    new_cube_colours['btl'] = cube['btr']
    new_cube_colours['bmr'] = cube['bbm']
    new_cube_colours['bml'] = cube['btm']
    new_cube_colours['bbr'] = cube['bbl']
    new_cube_colours['bbm'] = cube['bml']
    new_cube_colours['bbl'] = cube['btl']
    new_cube_colours['utl'] = cube['lbl']
    new_cube_colours['utm'] = cube['lml']
    new_cube_colours['utr'] = cube['ltl']
    new_cube_colours['ltl'] = cube['dbl']
    new_cube_colours['lml'] = cube['dbm']
    new_cube_colours['lbl'] = cube['dbr']
    new_cube_colours['dbl'] = cube['rbr']
    new_cube_colours['dbm'] = cube['rmr']
    new_cube_colours['dbr'] = cube['rtr']
    new_cube_colours['rtr'] = cube['utl']
    new_cube_colours['rmr'] = cube['utm']
    new_cube_colours['rbr'] = cube['utr']

    return new_cube_colours

# D (clockwise)
def move_dc(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['dtr'] = cube['dtl']
    new_cube_colours['dmr'] = cube['dtm']
    new_cube_colours['dbr'] = cube['dtr']
    new_cube_colours['dtm'] = cube['dml']
    new_cube_colours['dbm'] = cube['dmr']
    new_cube_colours['dtl'] = cube['dbl']
    new_cube_colours['dml'] = cube['dbm']
    new_cube_colours['dbl'] = cube['dbr']
    new_cube_colours['rbl'] = cube['fbl']
    new_cube_colours['rbm'] = cube['fbm']
    new_cube_colours['rbr'] = cube['fbr']
    new_cube_colours['bbl'] = cube['rbl']
    new_cube_colours['bbm'] = cube['rbm']
    new_cube_colours['bbr'] = cube['rbr']
    new_cube_colours['lbr'] = cube['bbr']
    new_cube_colours['lbm'] = cube['bbm']
    new_cube_colours['lbl'] = cube['bbl']
    new_cube_colours['fbl'] = cube['lbl']
    new_cube_colours['fbm'] = cube['lbm']
    new_cube_colours['fbr'] = cube['lbr']

    return new_cube_colours

# D' (anti-clockwise)
def move_da(cube):

    # Create blank dictionary
    new_cube_colours = {}

    # Iterate through to ONLY copy over squares, not ID etc.
    for square in config.squares:
        new_cube_colours[square] = cube[square]

    # Change squares that need to be changed.
    new_cube_colours['dtl'] = cube['dtr']
    new_cube_colours['dtm'] = cube['dmr']
    new_cube_colours['dtr'] = cube['dbr']
    new_cube_colours['dml'] = cube['dtm']
    new_cube_colours['dmr'] = cube['dbm']
    new_cube_colours['dbl'] = cube['dtl']
    new_cube_colours['dbm'] = cube['dml']
    new_cube_colours['dbr'] = cube['dbl']
    new_cube_colours['fbl'] = cube['rbl']
    new_cube_colours['fbm'] = cube['rbm']
    new_cube_colours['fbr'] = cube['rbr']
    new_cube_colours['rbl'] = cube['bbl']
    new_cube_colours['rbm'] = cube['bbm']
    new_cube_colours['rbr'] = cube['bbr']
    new_cube_colours['bbr'] = cube['lbr']
    new_cube_colours['bbm'] = cube['lbm']
    new_cube_colours['bbl'] = cube['lbl']
    new_cube_colours['lbl'] = cube['fbl']
    new_cube_colours['lbm'] = cube['fbm']
    new_cube_colours['lbr'] = cube['fbr']

    return new_cube_colours


# CUBE MOVE FUNCTIONS BELOW

# Right trigger
def right_trigger(cube):
    new_cube_colours = move_rc(cube)
    new_cube_colours = move_uc(new_cube_colours)
    new_cube_colours = move_ra(new_cube_colours)
    return new_cube_colours

# Left trigger
def left_trigger(cube):
    new_cube_colours = move_la(cube)
    new_cube_colours = move_ua(new_cube_colours)
    new_cube_colours = move_lc(new_cube_colours)
    return new_cube_colours

# FURU'R'F' algorithm
def fururf(cube):
    new_cube_colours = move_fc(cube)
    new_cube_colours = move_uc(new_cube_colours)
    new_cube_colours = move_rc(new_cube_colours)
    new_cube_colours = move_ua(new_cube_colours)
    new_cube_colours = move_ra(new_cube_colours)
    new_cube_colours = move_fa(new_cube_colours)
    return new_cube_colours
