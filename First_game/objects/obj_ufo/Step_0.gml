// Moving Around
if (keyboard_check(vk_right)) x=x+5;
if (keyboard_check(vk_left)) x=x-5;
if (keyboard_check(vk_up)) y=y-5;
if (keyboard_check(vk_down)) y=y+5;
if (keyboard_check(vk_control)) image_angle=image_angle+1;

//Shooting Bullets
if (keyboard_check(vk_space) && cooldown < 0)
{
	instance_create_layer(x,y,"lay_bullets",obj_bullet)
	cooldown = 5;
}

cooldown -=1;