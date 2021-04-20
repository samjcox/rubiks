



# Create list of individual faces of each cubelet, referred to as squares and state correct colour of that square.
squares = ('bbr', 'bbm', 'bbl', 'bmr', 'bmm', 'bml', 'btr', 'btm', 'btl', 'lbl', 'lml', 'ltl', 'lbm', 'lmm', 'ltm', 'lbr', 'lmr', 'ltr', 'utl', 'utm', 'utr', 'uml', 'umm', 'umr', 'ubl', 'ubm', 'ubr', 'rtr', 'rmr', 'rbr', 'rtm', 'rmm', 'rbm', 'rtl', 'rml', 'rbl', 'ftl', 'ftm', 'ftr', 'fml', 'fmm', 'fmr', 'fbl', 'fbm', 'fbr', 'dtl', 'dtm', 'dtr', 'dml', 'dmm', 'dmr', 'dbl', 'dbm', 'dbr')

colours = ('red', 'blue', 'green', 'yellow', 'orange', 'white')

# Define squares on each face.
faces = {
    'green':('bbl', 'bbm', 'bbr', 'bml', 'bmm', 'bmr', 'btl', 'btm', 'btr'),
    'orange':('lbl', 'lml', 'ltl', 'lbm', 'lmm', 'ltm', 'lbr', 'lmr', 'ltr'),
    'yellow':('utl', 'utm', 'utr', 'uml', 'umm', 'umr', 'ubl', 'ubm', 'ubr'),
    'red':('rtr', 'rmr', 'rbr', 'rtm', 'rmm', 'rbm', 'rtl', 'rml', 'rbl'),
    'blue':('ftl', 'ftm', 'ftr', 'fml', 'fmm', 'fmr', 'fbl', 'fbm', 'fbr'),
    'white':('dtl', 'dtm', 'dtr', 'dml', 'dmm', 'dmr', 'dbl', 'dbm', 'dbr')
}

# Define a solved cube.
solved_cube = {
    'bbr':'green',
    'bbm':'green',
    'bbl':'green',
    'bmr':'green',
    'bmm':'green',
    'bml':'green',
    'btr':'green',
    'btm':'green',
    'btl':'green',
    'lbl':'orange',
    'lml':'orange',
    'ltl':'orange',
    'lbm':'orange',
    'lmm':'orange',
    'ltm':'orange',
    'lbr':'orange',
    'lmr':'orange',
    'ltr':'orange',
    'utl':'yellow',
    'utm':'yellow',
    'utr':'yellow',
    'uml':'yellow',
    'umm':'yellow',
    'umr':'yellow',
    'ubl':'yellow',
    'ubm':'yellow',
    'ubr':'yellow',
    'rtr':'red',
    'rmr':'red',
    'rbr':'red',
    'rtm':'red',
    'rmm':'red',
    'rbm':'red',
    'rtl':'red',
    'rml':'red',
    'rbl':'red',
    'ftl':'blue',
    'ftm':'blue',
    'ftr':'blue',
    'fml':'blue',
    'fmm':'blue',
    'fmr':'blue',
    'fbl':'blue',
    'fbm':'blue',
    'fbr':'blue',
    'dtl':'white',
    'dtm':'white',
    'dtr':'white',
    'dml':'white',
    'dmm':'white',
    'dmr':'white',
    'dbl':'white',
    'dbm':'white',
    'dbr':'white'
}

# Solve Stage 7 - Reference Information:
face_anticlockwise_moves = {
    'green':("F", "F", "U'", "R'", "L", "F", "F", "L'", "R", "U'", "F", "F"),
    'red':("L", "L", "U'", "F'", "B", "L", "L", "B'", "F", "U'", "L", "L"),
    'blue':("B", "B", "U'", "L'", "R", "B", "B", "R'", "L", "U'", "B", "B"),
    'orange':("R", "R", "U'", "B'", "F", "R", "R", "F'", "B", "U'", "R", "R")
}

face_clockwise_moves = {
    'green':("F", "F", "U", "R'", "L", "F", "F", "L'", "R", "U", "F", "F"),
    'red':("L", "L", "U", "F'", "B", "L", "L", "B'", "F", "U", "L", "L"),
    'blue':("B", "B", "U", "L'", "R", "B", "B", "R'", "L", "U", "B", "B"),
    'orange':("R", "R", "U", "B'", "F", "R", "R", "F'", "B", "U", "R", "R")
}

# List of possible moves.
possible_moves = ["F", "F'", "U", "U'", "R", "R'", "L", "L'", "B", "B'", "D", "D'"]