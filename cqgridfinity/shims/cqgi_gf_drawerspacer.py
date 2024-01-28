import sys
sys.path.append(".") # Relative to `partcad.yaml`

from cqgridfinity.gf_drawer import GridfinityDrawerSpacer

length_u = 2
width_u = 2
length_th = 10.0
width_th = 10.0
thickness = 5.0
chamf_rad = 1.0
show_arrows = True
arrow_h = 0.8
length_fill = 0.0
width_fill = 0.0
align_features = True
align_l = 16.0
align_tol = 0.15
align_min = 8.0
min_margin = 4.0
tolerance = 0.5

result = GridfinityDrawerSpacer(
    length_u=int(length_u),
    width_u=int(width_u),
    length_th=length_th,
    width_th=width_th,
    thickness=thickness,
    chamf_rad=chamf_rad,
    show_arrows=show_arrows,
    arrow_h=arrow_h,
    length_fill=length_fill,
    width_fill=width_fill,
    align_features=align_features,
    align_l=align_l,
    align_tol=align_tol,
    align_min=align_min,
    min_margin=min_margin,
    tolerance=tolerance,
).render().val()

show_object(result)