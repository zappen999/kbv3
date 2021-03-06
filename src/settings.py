FINGERS = {
    'index': {
        'min_angle': 0,
        'max_angle': -140,
        'proximal_phalanx_length': 55,
        'middle_phalanx_length': 25,
        'distal_phalanx_length': 23,
    },
    'middle': {
        'min_angle': 0,
        'max_angle': -130,
        'proximal_phalanx_length': 57,
        'middle_phalanx_length': 31,
        'distal_phalanx_length': 27,
    },
    'ring': {
        'min_angle': 0,
        'max_angle': -140,
        'proximal_phalanx_length': 51,
        'middle_phalanx_length': 28,
        'distal_phalanx_length': 25,
    },
    'pinky': {
        'min_angle': 0,
        'max_angle': -140,
        'proximal_phalanx_length': 35,
        'middle_phalanx_length': 19,
        'distal_phalanx_length': 22,
    },
}

KNUCKLE_WIDTH = 72;
FINGER_SPREAD = 120;

KEYCAP_BOX = {'x': 18, 'y': 18, 'z': 7}

# The script will cram in as many keys as possible without keycap collisions.
# This defines the minimum clearance at the front top of the keycap.
KEY_INTERSECTION_CLEARANCE = 3

SHOW_DEBUG_GEOMETRY = True
