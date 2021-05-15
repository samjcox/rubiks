# This config file contains most of the collections of repetitive 
# or large data.  This file includes no functions, only data.

# Create list of individual faces of each cubelet,
# referred to as squares and state correct colour of that square.
# Legend to square references is face-row-column,
# for example 'bmr' is back face, middle row, right column.
# Directions are given from the perspective of looking at that face.
squares = (
    'bbr', # back face, bottom row, right column.
    'bbm', # back face, bottom row, middle column.
    'bbl', # back face, bottom row, left column.
    'bmr', # back face, middle row, right column.
    'bmm', # back face, middle row, middle colum.
    'bml', # back face, middle row, left column.
    'btr', # back face, top row, right column.
    'btm', # back face, top row, middle colum.
    'btl', # back face, top row, left column.
    'lbl', # left face, bottom row, left column.
    'lml', # left face, middle row, left colum.
    'ltl', # left face, top row, left column.
    'lbm', # left face, bottom row, middle column.
    'lmm', # left face, middle row, middle column.
    'ltm', # left face, top row, middle column.
    'lbr', # left face, bottom row, right column.
    'lmr', # left face, middle row, right column.
    'ltr', # left face, top row, right column.
    'utl', # upper face, top row, left column.
    'utm', # upper face, top row, middle column.
    'utr', # upper face, top row, right column.
    'uml', # upper face, middle row, left column.
    'umm', # upper face, middle row, middle column.
    'umr', # upper face, middle row, right column.
    'ubl', # upper face, bottom row, left column.
    'ubm', # upper face, bottom row, middle column.
    'ubr', # upper face, bottom row, right column.
    'rtr', # right face, top row, right column
    'rmr', # right face, middle row, right column
    'rbr', # right face, bottom row, right column.
    'rtm', # right face, top row, middle column
    'rmm', # right face, middle row, middle column
    'rbm', # right face, bottom row, middle column.
    'rtl', # right face, top row, left column
    'rml', # right face, middle row, left column
    'rbl', # right face, bottom row, left column.
    'ftl', # front face, top row, left column.
    'ftm', # front face, top row, middle column.
    'ftr', # front face, top row, right column.
    'fml', # front face, middle row, left column.
    'fmm', # front face, middle row, middle column.
    'fmr', # front face, middle row, right column.
    'fbl', # front face, bottom row, left column.
    'fbm', # front face, bottom row, middle column.
    'fbr', # front face, bottom row, right column.
    'dtl', # down (bottom) face, top row, left column.
    'dtm', # down (bottom) face, top row, middle column.
    'dtr', # down (bottom) face, top row, right column.
    'dml', # down (bottom) face, middle row, left column.
    'dmm', # down (bottom) face, middle row, middle column.
    'dmr', # down (bottom) face, middle row, right column.
    'dbl', # down (bottom) face, bottom row, left column.
    'dbm', # down (bottom) face, bottom row, middle column.
    'dbr', # down (bottom) face, bottom row, right column.
    )

# Define list of colours.
colours = ('red', 'blue', 'green', 'yellow', 'orange', 'white')

# Define a solved cube.
solved_cube = {
    'bbr':'green', 'bbm':'green', 'bbl':'green',
    'bmr':'green', 'bmm':'green', 'bml':'green',
    'btr':'green', 'btm':'green', 'btl':'green',
    'lbl':'orange', 'lml':'orange', 'ltl':'orange',
    'lbm':'orange', 'lmm':'orange', 'ltm':'orange',
    'lbr':'orange', 'lmr':'orange', 'ltr':'orange',
    'utl':'yellow', 'utm':'yellow', 'utr':'yellow',
    'uml':'yellow', 'umm':'yellow', 'umr':'yellow',
    'ubl':'yellow', 'ubm':'yellow', 'ubr':'yellow',
    'rtr':'red', 'rmr':'red', 'rbr':'red',
    'rtm':'red', 'rmm':'red', 'rbm':'red',
    'rtl':'red', 'rml':'red', 'rbl':'red',
    'ftl':'blue', 'ftm':'blue', 'ftr':'blue',
    'fml':'blue', 'fmm':'blue', 'fmr':'blue',
    'fbl':'blue', 'fbm':'blue', 'fbr':'blue',
    'dtl':'white', 'dtm':'white', 'dtr':'white',
    'dml':'white', 'dmm':'white', 'dmr':'white',
    'dbl':'white', 'dbm':'white', 'dbr':'white'
}

# Define squares on each face.
faces = {
    'green':(
        'bbl', 'bbm', 'bbr',
        'bml', 'bmm', 'bmr',
        'btl', 'btm', 'btr'
        ),
    'orange':(
        'lbl', 'lml', 'ltl',
        'lbm', 'lmm', 'ltm',
        'lbr', 'lmr', 'ltr'
        ),
    'yellow':(
        'utl', 'utm', 'utr',
        'uml', 'umm', 'umr',
        'ubl', 'ubm', 'ubr'
        ),
    'red':(
        'rtr', 'rmr', 'rbr',
        'rtm', 'rmm', 'rbm',
        'rtl', 'rml', 'rbl'
        ),
    'blue':(
        'ftl', 'ftm', 'ftr',
        'fml', 'fmm', 'fmr',
        'fbl', 'fbm', 'fbr'
        ),
    'white':(
        'dtl', 'dtm', 'dtr',
        'dml', 'dmm', 'dmr',
        'dbl', 'dbm', 'dbr'
        )
}

# Check stages - listed by Stage, then,squares, then colour criteria.
check_stages = [
    [2, [
        [('dtl', 'dtm', 'dtr',
            'dml', 'dmm', 'dmr',
            'dbl', 'dbm', 'dbr'),
            'white']
        ]
    ],
    [3, [
        [('bmr', 'bmm', 'bml'), 'green'],
        [('lml', 'lmm', 'lmr'), 'orange'],
        [('rmr', 'rmm', 'rml'), 'red'],
        [('fml', 'fmm', 'fmr'), 'blue']
        ]
    ],
    [4, [
        [('utm', 'uml', 'umm',
            'umr', 'ubm'), 'yellow']
        ]
    ],
    [5, [
        [('utl', 'utm', 'utr',
            'uml', 'umm', 'umr',
            'ubl', 'ubm', 'ubr'),
            'yellow']
        ]
    ],
    [6, [
        [('btr', 'btl'), 'green'],
        [('ltl', 'ltr'), 'orange'],
        [('rtr', 'rtl'), 'red'],
        [('ftl', 'ftr'), 'blue']
        ]
    ],
    [7, [
        [('btr', 'btm', 'btl'), 'green'],
        [('ltl', 'ltm', 'ltr'), 'orange'],
        [('rtr', 'rtm', 'rtl'), 'red'],
        [('ftl', 'ftm', 'ftr'), 'blue']
        ]
    ]
]

# List of possible moves.
possible_moves = [
    "F", "F'", "U",
    "U'", "R", "R'",
    "L", "L'", "B",
    "B'", "D", "D'"
]

# MOVE DEFINITIONS:
# Definition of changes to cube when a move is made.
# The first item in the list is the new square position, the second
# item in the list is the old square position.

move_definitions = {
    "R":(('rtr', 'rtl'), ('rmr', 'rtm'), ('rbr', 'rtr'),
        ('rtm', 'rml'), ('rbm', 'rmr'), ('rtl', 'rbl'),
        ('rml', 'rbm'), ('rbl', 'rbr'), ('utr', 'ftr'),
        ('umr', 'fmr'), ('ubr', 'fbr'), ('bbl', 'utr'),
        ('bml', 'umr'), ('btl', 'ubr'), ('ftr', 'dtr'),
        ('fmr', 'dmr'), ('fbr', 'dbr'), ('dbr', 'btl'),
        ('dmr', 'bml'), ('dtr', 'bbl')),
    "R'":(('rtl', 'rtr'), ('rtm', 'rmr'), ('rtr', 'rbr'),
        ('rml', 'rtm'), ('rmr', 'rbm'), ('rbl', 'rtl'),
        ('rbm', 'rml'), ('rbr', 'rbl'), ('ftr', 'utr'),
        ('fmr', 'umr'), ('fbr', 'ubr'), ('utr', 'bbl'),
        ('umr', 'bml'), ('ubr', 'btl'), ('dtr', 'ftr'),
        ('dmr', 'fmr'), ('dbr', 'fbr'), ('btl', 'dbr'),
        ('bml', 'dmr'), ('bbl', 'dtr')),
    "L":(('ltr', 'ltl'), ('lmr', 'ltm'), ('lbr', 'ltr'),
        ('ltm', 'lml'), ('lbm', 'lmr'), ('ltl', 'lbl'),
        ('lml', 'lbm'), ('lbl', 'lbr'), ('dtl', 'ftl'),
        ('dml', 'fml'), ('dbl', 'fbl'), ('ftl', 'utl'),
        ('fml', 'uml'), ('fbl', 'ubl'), ('bbr', 'dtl'),
        ('bmr', 'dml'), ('btr', 'dbl'), ('ubl', 'btr'),
        ('uml', 'bmr'), ('utl', 'bbr')),
    "L'":(('ltl', 'ltr'), ('ltm', 'lmr'), ('ltr', 'lbr'),
        ('lml', 'ltm'), ('lmr', 'lbm'), ('lbl', 'ltl'),
        ('lbm', 'lml'), ('lbr', 'lbl'), ('ftl', 'dtl'),
        ('fml', 'dml'), ('fbl', 'dbl'), ('utl', 'ftl'),
        ('uml', 'fml'), ('ubl', 'fbl'), ('dtl', 'bbr'),
        ('dml', 'bmr'), ('dbl', 'btr'), ('btr', 'ubl'),
        ('bmr', 'uml'), ('bbr', 'utl')),
    "U":(('utr', 'utl'), ('umr', 'utm'), ('ubr', 'utr'),
        ('utm', 'uml'), ('ubm', 'umr'), ('utl', 'ubl'),
        ('uml', 'ubm'), ('ubl', 'ubr'), ('btl', 'ltl'),
        ('btm', 'ltm'), ('btr', 'ltr'), ('rtr', 'btr'),
        ('rtm', 'btm'), ('rtl', 'btl'), ('ftr', 'rtr'),
        ('ftm', 'rtm'), ('ftl', 'rtl'), ('ltl', 'ftl'),
        ('ltm', 'ftm'), ('ltr', 'ftr')),
    "U'":(('utl', 'utr'), ('utm', 'umr'), ('utr', 'ubr'),
        ('uml', 'utm'), ('umr', 'ubm'), ('ubl', 'utl'),
        ('ubm', 'uml'), ('ubr', 'ubl'), ('ltl', 'btl'),
        ('ltm', 'btm'), ('ltr', 'btr'), ('btr', 'rtr'),
        ('btm', 'rtm'), ('btl', 'rtl'), ('rtr', 'ftr'),
        ('rtm', 'ftm'), ('rtl', 'ftl'), ('ftl', 'ltl'),
        ('ftm', 'ltm'), ('ftr', 'ltr')),
    "F":(('ftr', 'ftl'), ('fmr', 'ftm'), ('fbr', 'ftr'),
        ('ftm', 'fml'), ('fbm', 'fmr'), ('ftl', 'fbl'),
        ('fml', 'fbm'), ('fbl', 'fbr'), ('ubr', 'ltr'),
        ('ubm', 'lmr'), ('ubl', 'lbr'), ('rtl', 'ubl'),
        ('rml', 'ubm'), ('rbl', 'ubr'), ('dtr', 'rtl'),
        ('dtm', 'rml'), ('dtl', 'rbl'), ('ltr', 'dtl'),
        ('lmr', 'dtm'), ('lbr', 'dtr')),
    "F'":(('ftl', 'ftr'), ('ftm', 'fmr'), ('ftr', 'fbr'),
        ('fml', 'ftm'), ('fmr', 'fbm'), ('fbl', 'ftl'),
        ('fbm', 'fml'), ('fbr', 'fbl'), ('ltr', 'ubr'),
        ('lmr', 'ubm'), ('lbr', 'ubl'), ('ubl', 'rtl'),
        ('ubm', 'rml'), ('ubr', 'rbl'), ('rtl', 'dtr'),
        ('rml', 'dtm'), ('rbl', 'dtl'), ('dtl', 'ltr'),
        ('dtm', 'lmr'), ('dtr', 'lbr')),
    "B":(('bbr', 'btr'), ('bmr', 'btm'), ('btr', 'btl'),
        ('bbm', 'bmr'), ('btm', 'bml'), ('bbl', 'bbr'),
        ('bml', 'bbm'), ('btl', 'bbl'), ('lbl', 'utl'),
        ('lml', 'utm'), ('ltl', 'utr'), ('dbl', 'ltl'),
        ('dbm', 'lml'), ('dbr', 'lbl'), ('rbr', 'dbl'),
        ('rmr', 'dbm'), ('rtr', 'dbr'), ('utl', 'rtr'),
        ('utm', 'rmr'), ('utr', 'rbr')),
    "B'":(('btr', 'bbr'), ('btm', 'bmr'), ('btl', 'btr'),
        ('bmr', 'bbm'), ('bml', 'btm'), ('bbr', 'bbl'),
        ('bbm', 'bml'), ('bbl', 'btl'), ('utl', 'lbl'),
        ('utm', 'lml'), ('utr', 'ltl'), ('ltl', 'dbl'),
        ('lml', 'dbm'), ('lbl', 'dbr'), ('dbl', 'rbr'),
        ('dbm', 'rmr'), ('dbr', 'rtr'), ('rtr', 'utl'),
        ('rmr', 'utm'), ('rbr', 'utr')),
    "D":(('dtr', 'dtl'), ('dmr', 'dtm'), ('dbr', 'dtr'),
        ('dtm', 'dml'), ('dbm', 'dmr'), ('dtl', 'dbl'),
        ('dml', 'dbm'), ('dbl', 'dbr'), ('rbl', 'fbl'),
        ('rbm', 'fbm'), ('rbr', 'fbr'), ('bbl', 'rbl'),
        ('bbm', 'rbm'), ('bbr', 'rbr'), ('lbr', 'bbr'),
        ('lbm', 'bbm'), ('lbl', 'bbl'), ('fbl', 'lbl'),
        ('fbm', 'lbm'), ('fbr', 'lbr')),
    "D'":(('dtl', 'dtr'), ('dtm', 'dmr'), ('dtr', 'dbr'),
        ('dml', 'dtm'), ('dmr', 'dbm'), ('dbl', 'dtl'),
        ('dbm', 'dml'), ('dbr', 'dbl'), ('fbl', 'rbl'),
        ('fbm', 'rbm'), ('fbr', 'rbr'), ('rbl', 'bbl'),
        ('rbm', 'bbm'), ('rbr', 'bbr'), ('bbr', 'lbr'),
        ('bbm', 'lbm'), ('bbl', 'lbl'), ('lbl', 'fbl'),
        ('lbm', 'fbm'), ('lbr', 'fbr'))
}

# Names of each stage.
stage_names = [
    "Daisy", "White Cross", "White Face",
    "Middle Row", "Yellow Cross", "Yellow Face",
    "Top Corners", "Final Stage"
]

# Solve Stage 0:
bottom_face_top_square = {
    'dtm':'ubm', 'dml':'uml', 'dbm':'utm', 'dmr':'umr'
}
daisy_bottom_face_moves = {
    "dtm":("F", "F"), "dml":("L", "L"), "dmr":("R", "R"), "dbm":("B", "B")
}
middle_row_edge_squares = (
    'fml', 'fmr', 'rml', 'rmr', 'bml', 'bmr', 'lml', 'lmr'
)
daisy_middle_reference_top_square = {
    'fmr':'umr', 'fml':'uml', 'lmr':'ubm',
    'lml':'utm', 'bmr':'uml', 'bml':'umr',
    'rmr':'utm', 'rml':'ubm'
}
daisy_middle_moves = {
    "fmr":"R", "fml":"L'", "lmr":"F",
    "lml":"B'", "bmr":"L", "bml":"R'",
    "rmr":"B'", "rml":"F'"
}
daisy_bottom_reference_top_square = {
    'fbm':'ubm', 'lbm':'uml', 'bbm':'utm', 'rbm':'umr'
}
daisy_bottom_moves = {
    'fbm':("F", "U", "L'"), 'lbm':("L", "U", "B'"), 'bbm':("B", "U", "R'"),
    'rbm':("R", "U", "F'")
}
daisy_top_moves = {
    'ftm':("F", "U'", "R"), 'ltm':("L", "U'", "F"), 'btm':("B", "U'", "L"),
    'rtm':("R", "U'", "B")
}

# Solve Stage 2:
top_row_corner_squares = {
    'ftl':'ltr', 'ftr':'rtl', 'ltl':'btr',
    'ltr':'ftl', 'btl':'rtr', 'btr':'ltl',
    'rtl':'ftr', 'rtr':'btl'
}
centre_square_for_square = {
    'ftl':'fmm', 'ftr':'fmm', 'rtl':'rmm',
    'rtr':'rmm', 'btl':'bmm', 'btr':'bmm',
    'ltl':'lmm', 'ltr':'lmm'
}
white_face_top_row_moves = {
    "ftl":("F", "U", "F'"), "ftr":("F'", "U'", "F"), "rtl":("R", "U", "R'"),
    "rtr":("R'", "U'", "R"), "btl":("B", "U", "B'"), "btr":("B'", "U'", "B"),
    "ltl":("L", "U", "L'"), "ltr":("L'", "U'", "L")
}
bottom_row_corner_squares = {
    "fbl":("F", "U", "F'"), "fbr":("F'", "U'", "F"), "rbl":("R", "U", "R'"),
    "rbr":("R'", "U'", "R"), "bbl":("B", "U", "B'"), "bbr":("B'", "U'", "B"),
    "lbl":("L", "U", "L'"), "lbr":("L'", "U'", "L")
}
top_face_corner_squares = {
    'ubl':'dtl', 'utl':'dbl', 'utr':'dbr', 'ubr':'dtr'
}
top_face_corner_moves = {
    "ubl":("L'", "U'", "U'", "L"), "ubr":("R", "U", "U", "R'"),
    "utr":("R'", "U'", "U'", "R"), "utl":("L", "U", "U", "L'")
}

# Solve Stage 3:
left_trigger_moves = {
    "ftm":("U'", "L'", "U'", "L", "U", "F", "U", "F'"),
    "ltm":("U'", "B'", "U'", "B", "U", "L", "U", "L'"),
    "btm":("U'", "R'", "U'", "R", "U", "B", "U", "B'"),
    "rtm":("U'", "F'", "U'", "F", "U", "R", "U", "R'")
}
right_trigger_moves = {
    "ftm":("U", "R", "U", "R'", "U'", "F'", "U'", "F"),
    "ltm":("U", "F", "U", "F'", "U'", "L'", "U'", "L"),
    "btm":("U", "L", "U", "L'", "U'", "B'", "U'", "B"),
    "rtm":("U", "B", "U", "B'", "U'", "R'", "U'", "R")
}
middle_row_edge_moves = {
    'fml':("L'", "U'", "L", "U", "F", "U", "F'"),
    'fmr':("R", "U", "R'", "U'", "F'", "U'", "F"),
    'rml':("R", "U", "R'", "U'", "F'", "U'", "F"),
    'rmr':("R'", "U'", "R", "U", "B", "U", "B'"),
    'bml':("R'", "U'", "R", "U", "B", "U", "B'"),
    'bmr':("L", "U", "L'", "U'", "B'", "U'", "B"),
    'lml':("L", "U", "L'", "U'", "B'", "U'", "B"),
    'lmr':("L'", "U'", "L", "U", "F", "U", "F'"),
}
centre_square_for_top_middle_square = {
    'ftm':'fmm', 'ltm':'lmm', 'btm':'bmm', 'rtm':'rmm'
}
left_face_centre = {
    'ubm':'lmm', 'uml':'bmm', 'utm':'rmm', 'umr':'fmm'
}

# Solve Stage 4:
fururf = ("F", "U", "R", "U'", "R'", "F'")

# Solve Stage 5:
rururuur = ("R", "U", "R'", "U", "R", "U", "U", "R'")

# Solve Stage 6:
top_row_squares = {
    'lmm':('ltl', 'ltm', 'ltr'),
    'bmm':('btl', 'btm', 'btr'),
    'rmm':('rtl', 'rtm', 'rtr'),
    'fmm':('ftl', 'ftm', 'ftr')
}
colour_to_algo = {
    'orange':("L'", "U", "R", "U'", "L", "U", "U", "R'", "U", "R", "U", "U", "R'"),
    'green':("B'", "U", "F", "U'", "B", "U", "U", "F'", "U", "F", "U", "U", "F'"),
    'red':("R'", "U", "L", "U'", "R", "U", "U", "L'", "U", "L", "U", "U", "L'"),
    'blue':("F'", "U", "B", "U'", "F", "U", "U", "B'", "U", "B", "U", "U", "B'")
}

# Solve Stage 7:
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

# Improve efficiency:
move_to_replace_triples = {
    "F":"F'", "F'":"F", "U":"U'",
    "U'":"U", "L":"L'", "L'":"L",
    "R":"R'", "R'":"R", "D":"D'",
    "D'":"D", "B":"B'", "B'":"B"
}
opposite_moves = {
    "F":"F'", "F'":"F", "U":"U'",
    "U'":"U", "L":"L'", "L'":"L",
    "R":"R'", "R'":"R", "D":"D'",
    "D'":"D", "B":"B'", "B'":"B"
}



