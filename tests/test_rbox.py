# Gridfinity tests

# my modules
from cqgridfinity import *

# from cqkit.cq_helpers import size_3d
from cqkit.cq_helpers import *
from cqkit import *

from common_test import (
    EXPORT_STEP_FILE_PATH,
    _almost_same,
    _edges_match,
    _faces_match,
    _export_files,
)


def test_rugged_box():
    b1 = GridfinityRuggedBox(5, 4, 6)
    b1.inside_baseplate = True
    b1.lid_baseplate = True
    b1.front_handle = True
    b1.front_label = True
    b1.side_clasps = True
    b1.stackable = True
    b1.wall_vgrooves = True
    b1.side_handles = True
    b1.back_feet = True
    b1.hinge_bolted = False
    assert b1.filename() == "gf_ruggedbox_5x4x6_fr-hl_sd-hc_stack_lidbp"
    r = b1.render()
    assert r is not None
    assert _almost_same(size_3d(r), (230.0, 194.15, 47.5))
    if _export_files("rbox"):
        export_step_file(r, EXPORT_STEP_FILE_PATH + os.sep + "rbox6.step")

    r = b1.render_accessories()
    assert len(r.solids().vals()) == 16
