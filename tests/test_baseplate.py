# Gridfinity tests


# my modules
from cqgridfinity import *
from cqkit import FlatEdgeSelector
from cqkit.cq_helpers import size_3d
from common_test import (
    EXPORT_STEP_FILE_PATH,
    _almost_same,
    _faces_match,
    _export_files,
)


def test_make_baseplate():
    bp = GridfinityBaseplate(4, 3)
    r = bp.render()
    if _export_files("baseplate"):
        bp.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert bp.filename() == "gf_baseplate_4x3"
    assert _almost_same(size_3d(r), (168, 126, 4.75))
    assert _faces_match(r, ">Z", 16)
    assert _faces_match(r, "<Z", 1)
    edge_diff = abs(len(r.edges(FlatEdgeSelector(0)).vals()) - 104)
    assert edge_diff < 3


def test_make_ext_baseplate():
    bp = GridfinityBaseplate(5, 4, ext_depth=5, corner_screws=True)
    r = bp.render()
    assert _almost_same(size_3d(r), (210, 168, 9.75))
    edge_diff = abs(len(r.edges(FlatEdgeSelector(0)).vals()) - 188)
    assert edge_diff < 3
