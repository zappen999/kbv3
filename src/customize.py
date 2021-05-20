#!/usr/bin/env python3
import math
import os
from pprint import pprint
from geometry import Point, \
    LineSegment, \
    segments_distance, \
    deg2rad, \
    point_at_distance \

from settings import FINGERS, \
        KEYCAP_BOX, \
        COLUMN_KEY_DISTANCE


def get_key_back_egde(p, angle):
    p1 = point_at_distance(p, -(KEYCAP_BOX['y']/2), angle)  # back top of the key
    p2 = point_at_distance(p1, -KEYCAP_BOX['z'], angle-90)  # back bottom of the key

    return LineSegment(p1, p2)


def get_key_front_egde(p, angle):
    p1 = point_at_distance(p, KEYCAP_BOX['y']/2, angle)  # top of the key
    p2 = point_at_distance(p1, KEYCAP_BOX['z'], -angle-90)  # bottom of the key

    return LineSegment(p1, p2)


def generate_key_positions(finger):
    angles = range(-finger['max_angle'], -finger['min_angle'], 15)
    # angles = [i / 10.0 for i in range(-finger['max_angle'] * 10, -finger['min_angle'] * 10)]
    p1 = Point(0, 0)  # knuckle (y, z)

    keys = []

    for angle in angles:
        p2 = point_at_distance(p1, finger['proximal_phalanx_length'], angle/3)
        p3 = point_at_distance(p2, finger['middle_phalanx_length'], angle/1.5)
        p4 = point_at_distance(p3, finger['distal_phalanx_length'], angle)

        if not len(keys):  # no keys, add first
            keys.append({
                'p1': p1,
                'p2': p2,
                'p3': p3,
                'p4': p4,
                'angle': angle
            })

            pprint({
                'angle': angle,
                'prev_p4': None,
                'p4': p4,
                'prev_key_egde': None,
                'this_key_egde': None,
                'key_egdes_distance': None,
            })
        else:
            prev_key = keys[-1]
            prev_key_egde = get_key_front_egde(prev_key['p4'], prev_key['angle'])
            this_key_egde = get_key_back_egde(p4, angle)

            key_egdes_distance = segments_distance(prev_key_egde, this_key_egde)

            pprint({
                'angle': angle,
                'prev_p4': prev_key['p4'],
                'p4': p4,
                'prev_key_egde': prev_key_egde,
                'this_key_egde': this_key_egde,
                'key_egdes_distance': key_egdes_distance,
            })

            if key_egdes_distance >= COLUMN_KEY_DISTANCE:
                keys.append({
                    'p1': p1,
                    'p2': p2,
                    'p3': p3,
                    'p4': p4,
                    'angle': angle
                })
                print({
                    'prev_key_egde': prev_key_egde,
                    'this_key_egde': this_key_egde,
                    'distance': key_egdes_distance,
                })

    return keys


def export_openscad_settings(settings):
    f = os.path.join(os.path.dirname(__file__), 'settings.scad')

    with open(f, 'w') as f:
        f.write(settings)


def generate_openscad_settings():
    lines = []

    lines.append('FINGERS = [')

    for name, params in FINGERS.items():
        finger_keys = generate_key_positions(params)

        lines.append("\t[")
        for finger_key in finger_keys:
            lines.append("\t\t[")
            lines.append("\t\t\t%s, %s, %s, %s, %f" % (
                finger_key['p1'].to_openscad(),
                finger_key['p2'].to_openscad(),
                finger_key['p3'].to_openscad(),
                finger_key['p4'].to_openscad(),
                finger_key['angle']))
            lines.append("\t\t],")

        lines.append("\t],")

    lines.append('];')
    lines.append('KEYCAP_BOX = [%f, %f, %f];' % (
        KEYCAP_BOX['x'], KEYCAP_BOX['y'], KEYCAP_BOX['z']))
    lines.append('COLUMN_KEY_DISTANCE  = %f;' % COLUMN_KEY_DISTANCE)

    return '\n'.join(lines)


settings = generate_openscad_settings()
print(settings)
export_openscad_settings(settings)
