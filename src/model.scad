// TODO: These should be per finger later on
PROXIMAL_PHALANX_LENGTH=55;
MIDDLE_PHALANX_LENGTH=25;
DISTAL_PHALANX_LENGTH=23;

SWITCH_PLATE_THICKNESS=3;
SWITCH_MIN_SPACE_CC=18.5;


function deg2rad(deg) = deg*PI/180;
function inch2mm(inches) = inches*25.4;

function finger_joint_yz(prev_joint_p, phalanx_len, angle) = [
	prev_joint_p[0] + (phalanx_len * cos(angle)),
	prev_joint_p[1] + (phalanx_len * sin(angle))
];

module finger_plane(p, angle) {
	translate([0, p[0], -p[1]])
		rotate([-angle+90, 0, 0])
			children();
}

module finger_joint() {
	rotate([0, 90, 0])
		sphere(d=3, $fn=20);
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

module finger_sweep(
	proximal_phalanx_len,
	middle_phalanx_len,
	distal_phalanx_len
) {
	// Knuckle
	p1 = [0, 0];

	finger_plane(p1, 0)
		finger_joint();

	for (angle = [0:19:140]) {
		// Proximal bone end
		p2 = finger_joint_yz(p1, proximal_phalanx_len, angle/3);

		// Middle bone end
		p3 = finger_joint_yz(p2, middle_phalanx_len, angle/1.5);

		// Distal bone end (tip)
		p4 = finger_joint_yz(p3, distal_phalanx_len, angle);

		finger_plane(p2, angle)
			finger_joint();

		finger_plane(p3, angle)
			finger_joint();

		finger_plane(p4, angle)
			finger_joint();

		finger_plane(p4, angle)
			mx_switch_plate();
	}
}

// Index finger
finger_sweep(PROXIMAL_PHALANX_LENGTH, MIDDLE_PHALANX_LENGTH, DISTAL_PHALANX_LENGTH);
