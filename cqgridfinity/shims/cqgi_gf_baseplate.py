import sys
sys.path.append(".") # Relative to `partcad.yaml`

from cqgridfinity.gf_baseplate import GridfinityBaseplate

length_u = 2
width_u = 2
ext_depth = 0.0
straight_bottom = False
corner_screws = False
corner_tab_size = 21
csk_hole = 5.0
csk_diam = 10.0
csk_angle = 82

result = GridfinityBaseplate(
    length_u=int(length_u),
    width_u=int(width_u),
    ext_depth=ext_depth,
    straight_bottom=straight_bottom,
    corner_screws=corner_screws,
    corner_tab_size=corner_tab_size,
    csk_hole=csk_hole,
    csk_diam=csk_diam,
    csk_angle=csk_angle,
).render().val()

show_object(result)