import math


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point [%.2f, %.2f]" % (self.x, self.y)

    def to_openscad(self):
        return "[%f, %f]" % (self.x, self.y)


class DDDPoint:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return "Point [%.2f, %.2f, %.2f]" % (self.x, self.y, self.z)

    def to_openscad(self):
        return "[%f, %f, %f]" % (self.x, self.y, self.z)


class LineSegment:
    def __init__(self, p1, p2):
        assert isinstance(p1, Point), \
            "p1 is not of type Point, but of %r" % type(p1)
        assert isinstance(p2, Point), \
            "p2 is not of type Point, but of %r" % type(p2)
        self.p1 = p1
        self.p2 = p2

    def to_openscad(self):
        return "[%s, %s]" % (self.p1.to_openscad(), self.p2.to_openscad())

    def __repr__(self):
        return "LineSegment {p1: %s, p2: %s}" % (repr(self.p1), repr(self.p2))


def segments_distance(segment1, segment2):
    if segments_intersect(segment1, segment2):
        return 0
    # try each of the 4 vertices w/the other segment
    distances = []
    distances.append(point_segment_distance(segment1.p1, segment2))
    distances.append(point_segment_distance(segment1.p2, segment2))
    distances.append(point_segment_distance(segment2.p1, segment1))
    distances.append(point_segment_distance(segment2.p2, segment1))
    return min(distances)

def segments_intersect(s0,s1):
    dx0 = s0.p2.x-s0.p1.x
    dx1 = s1.p2.x-s1.p1.x
    dy0 = s0.p2.y-s0.p1.y
    dy1 = s1.p2.y-s1.p1.y
    p0 = dy1*(s1.p2.x-s0.p1.x) - dx1*(s1.p2.y-s0.p1.y)
    p1 = dy1*(s1.p2.x-s0.p2.x) - dx1*(s1.p2.y-s0.p2.y)
    p2 = dy0*(s0.p2.x-s1.p1.x) - dx0*(s0.p2.y-s1.p1.y)
    p3 = dy0*(s0.p2.x-s1.p2.x) - dx0*(s0.p2.y-s1.p2.y)
    return (p0*p1<=0) & (p2*p3<=0)


def point_segment_distance(point, segment):
    assert isinstance(point, Point), \
        "point is not of type Point, but of %r" % type(point)
    dx = segment.p2.x - segment.p1.x
    dy = segment.p2.y - segment.p1.y
    if dx == dy == 0:  # the segment's just a point
        return math.hypot(point.x - segment.p1.x, point.y - segment.p1.y)

    if dx == 0:
        if (point.y <= segment.p1.y or point.y <= segment.p2.y) and \
           (point.y >= segment.p2.y or point.y >= segment.p2.y):
            return abs(point.x - segment.p1.x)

    if dy == 0:
        if (point.x <= segment.p1.x or point.x <= segment.p2.x) and \
           (point.x >= segment.p2.x or point.x >= segment.p2.x):
            return abs(point.y - segment.p1.y)

    # Calculate the t that minimizes the distance.
    t = ((point.x - segment.p1.x) * dx + (point.y - segment.p1.y) * dy) / \
        (dx * dx + dy * dy)

    # See if this represents one of the segment's
    # end points or a point in the middle.
    if t < 0:
        dx = point.x - segment.p1.x
        dy = point.y - segment.p1.y
    elif t > 1:
        dx = point.x - segment.p2.x
        dy = point.y - segment.p2.y
    else:
        near_x = segment.p1.x + t * dx
        near_y = segment.p1.y + t * dy
        dx = point.x - near_x
        dy = point.y - near_y

    return math.hypot(dx, dy)


def deg2rad(deg):
    return deg * math.pi / 180


def point_at_distance(p, distance, angle):
    angle_rad = deg2rad(angle)

    return Point(
        p.x + (distance * math.cos(angle_rad)),
        p.y + (distance * math.sin(angle_rad))
    )


def distance_between_points(p1, p2):
    return math.sqrt((math.pow(p2.x-p1.x, 2))+(math.pow(p2.y-p1.y, 2)))

