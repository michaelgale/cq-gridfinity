import sys
sys.path.append(".") # Relative to `partcad.yaml`

from cqgridfinity.gf_ruggedbox import GridfinityRuggedBox

length_u = 2
width_u = 2
height_u = 2
lid_height = 10.0
wall_vgrooves = True
front_handle = True
stackable = True
side_clasps = True
lid_baseplate = True
inside_baseplate = True
side_handles = True
front_label = True
label_length = 0.0
label_height = 0.0
label_th = 0.5
back_feet = True
hinge_width = 32.0
hinge_bolted = False

result = GridfinityRuggedBox(
    length_u=int(length_u),
    width_u=int(width_u),
    height_u=int(height_u),
    lid_height=lid_height,
    wall_vgrooves=wall_vgrooves,
    front_handle=front_handle,
    stackable=stackable,
    side_clasps=side_clasps,
    lid_baseplate=lid_baseplate,
    inside_baseplate=inside_baseplate,
    side_handles=side_handles,
    front_label=front_label,
    label_length=label_length,
    label_height=label_height,
    label_th=label_th,
    back_feet=back_feet,
    hinge_width=hinge_width,
    hinge_bolted=hinge_bolted,
).render().val()

show_object(result)