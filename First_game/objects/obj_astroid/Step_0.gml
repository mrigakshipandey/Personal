// Moves towards player
if (instance_exists(obj_ufo)) move_towards_point(obj_ufo.x,obj_ufo.y,sp);
image_angle=direction;

// Destroy object
if (hp<=0) instance_destroy();