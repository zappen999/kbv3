include <settings.scad>;

SWITCH_PLATE_THICKNESS=3;
SWITCH_MIN_SPACE_CC=18.5;

function deg2rad(deg) = deg*PI/180;
function inch2mm(inches) = inches*25.4;

// Returns a new point in the yz plane based on distance and angle
function yz_point_at_distance(prev_joint_p, distance, angle) = [
	prev_joint_p[0] + (distance * cos(angle)),
	prev_joint_p[1] + (distance * sin(angle))
];

module finger_plane(p, angle) {
	translate([0, p[0], p[1]])
		rotate([angle+90, 0, 0])
			children();
}

module finger_joint() {
	cube(3, center=true);
}

module keycap() {
	translate([0, 0, -KEYCAP_BOX.z/2])
		cube(KEYCAP_BOX, center=true);
}

module mx_switch_plate() {
	difference() {
		cube([
			SWITCH_MIN_SPACE_CC,
			SWITCH_MIN_SPACE_CC,
			SWITCH_PLATE_THICKNESS,
		], center=true);
		cube([
			inch2mm(0.551),
			inch2mm(0.551),
			SWITCH_PLATE_THICKNESS*2,
		], center=true);
	}
}

module line(p1, p2, thickness=1, hex="#fafafa") {
	color(hex)
		hull() {
			translate([0, p1[0], p1[1]])
				cube(thickness, center=true);
			translate([0, p2[0], p2[1]])
				cube(thickness, center=true);
		}
}

for (finger = FINGERS) {
	for (key = finger) {
		p1 = key[0];
		p2 = key[1];
		p3 = key[2];
		p4 = key[3];
		angle = key[4];
		prev_key_egde = key[5];
		this_key_egde = key[6];
		
		echo(p1=p1, p2=p2, p3=p3, p4=p4, angle=angle, prev_key_egde, this_key_egde);

		finger_plane(p4, angle)
			#keycap();

		line(p1, p2);
		line(p2, p3);
		line(p3, p4);

		if (prev_key_egde)
			line(prev_key_egde[0], prev_key_egde[1], 0.5, "red");

		if (this_key_egde)
			line(this_key_egde[0], this_key_egde[1], 0.5, "green");

		finger_plane(p1, angle) finger_joint();
		finger_plane(p2, angle/3) finger_joint();
		finger_plane(p3, angle/1.5) finger_joint();
		finger_plane(p4, angle) finger_joint();
	}
}
