# Gridfinity tests


# my modules
from cqgridfinity import *
from cqkit.cq_helpers import size_3d
from common_test import _almost_same, _edges_match, _faces_match

_EXPORT_STEP_FILES = False


def test_make_baseplate():
    bp = GridfinityBaseplate(4, 3)
    r = bp.render()
    assert _almost_same(size_3d(r), (168, 126, 5))
    assert _faces_match(r, ">Z", 16)
    assert _faces_match(r, "<Z", 1)
    assert bp.filename() == "gf_baseplate_4x3"
    if _EXPORT_STEP_FILES:
        bp.save_step_file(path="./testfiles")
    bp = GridfinityBaseplate(6, 3)
    if _EXPORT_STEP_FILES:
        bp.save_step_file(path="./testfiles")
        bp.save_stl_file(path="./testfiles")
