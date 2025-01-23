import sys
sys.path.append(".") # Relative to `partcad.yaml`

from cqgridfinity.gf_box import GridfinityBox

length_u = 2
width_u = 2
height_u = 2
length_div = 0.0
width_div = 0.0
scoops = False
labels = False
solid = False
holes = False
no_lip = False
solid_ratio = 1.0
lite_style = False
unsupported_holes = False
label_width = 12.0  # width of the label strip
label_height = 10.0  # thickness of label overhang
label_lip_height = 0.8  # thickness of label vertical lip
scoop_rad = 12.0  # radius of optional interior scoops
fillet_interior = True
wall_th = 1.0

result = GridfinityBox(
    length_u=int(length_u),
    width_u=int(width_u),
    height_u=int(height_u),
    length_div=length_div,
    width_div=width_div,
    scoops=scoops,
    labels=labels,
    solid=solid,
    holes=holes,
    no_lip=no_lip,
    solid_ratio=solid_ratio,
    lite_style=lite_style,
    unsupported_holes=unsupported_holes,
    label_width=label_width,
    label_height=label_height,
    label_lip_height=label_lip_height,
    scoop_rad=scoop_rad,
    fillet_interior=fillet_interior,
    wall_th=wall_th,
).render().val()

show_object(result)