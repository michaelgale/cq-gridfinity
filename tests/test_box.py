# Gridfinity tests
import pytest

# my modules
from cqgridfinity import *

from cqkit.cq_helpers import *
from cqkit import *

from common_test import (
    EXPORT_STEP_FILE_PATH,
    _almost_same,
    _edges_match,
    _faces_match,
    _export_files,
)


def test_basic_box():
    b1 = GridfinityBox(2, 3, 5, no_lip=True)
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 48)
    assert b1.filename() == "gf_box_2x3x5_basic"
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    b1 = GridfinityBox(2, 3, 5, no_lip=True)
    if _export_files("box"):
        b1.wall_th = 1.5
        r = b1.render()
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)


def test_invalid_box():
    with pytest.raises(ValueError):
        b1 = GridfinityBox(2, 3, 5, lite_style=True, solid=True)
        b1.render()
    with pytest.raises(ValueError):
        b1 = GridfinityBox(2, 3, 5, lite_style=True, holes=True)
        b1.render()
    with pytest.raises(ValueError):
        b1 = GridfinityBox(2, 3, 5, lite_style=True, wall_th=2.0)
        b1.render()
    with pytest.raises(ValueError):
        b1 = GridfinityBox(2, 3, 5, wall_th=0.4)
        b1.render()
    with pytest.raises(ValueError):
        b1 = GridfinityBox(2, 3, 5, wall_th=3.0)
        b1.render()


def test_lite_box():
    b1 = GridfinityBox(2, 3, 5, lite_style=True)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 48)
    assert b1.filename() == "gf_box_lite_2x3x5"
    if _export_files("box"):
        b1 = GridfinityBox(2, 3, 5, lite_style=True)
        b1.wall_th = 1.2
        r = b1.render()
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    b1 = GridfinityBox(1, 1, 1, lite_style=True)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (41.5, 41.5, 10.8))

    b1 = GridfinityBox(1, 1, 2, lite_style=True)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (41.5, 41.5, 17.8))


def test_empty_box():
    b1 = GridfinityBox(2, 3, 5, holes=True)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 72)
    assert b1.filename() == "gf_box_2x3x5_holes"
    assert _almost_same(b1.top_ref_height, 7)
    if _export_files("box"):
        b1 = GridfinityBox(2, 3, 5, holes=True)
        b1.wall_th = 1.5
        r = b1.render()
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    b1 = GridfinityBox(1, 1, 1)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (41.5, 41.5, 10.8))

    b1 = GridfinityBox(1, 1, 2)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (41.5, 41.5, 17.8))


def test_solid_box():
    b1 = GridfinitySolidBox(4, 2, 3)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (167.5, 83.5, 24.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 8)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 64)
    assert len(r.faces(FlatFaceSelector(21)).vals()) == 1
    assert len(r.edges(FlatEdgeSelector(21)).vals()) == 8
    assert b1.filename() == "gf_box_4x2x3_solid"
    assert _almost_same(b1.top_ref_height, 21)
    b1.solid_ratio = 0.5
    assert _almost_same(b1.top_ref_height, 14)


def test_divided_box():
    b1 = GridfinityBox(3, 3, 3, holes=True, length_div=2, width_div=1)
    r = b1.render()
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
    assert _almost_same(size_3d(r), (125.5, 125.5, 24.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 9)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 108)
    assert len(r.faces(FlatFaceSelector(21)).vals()) == 1
    bs = FlatEdgeSelector(21) - EdgeLengthSelector("<0.1")
    assert len(r.edges(bs).vals()) == 54
    assert b1.filename() == "gf_box_3x3x3_div2x1_holes"


def test_all_features_box():
    b1 = GridfinityBox(
        4, 2, 5, holes=True, length_div=2, width_div=1, scoops=True, labels=True
    )
    b1.label_height = 9
    b1.scoop_rad = 20
    r = b1.render()
    assert _almost_same(size_3d(r), (167.5, 83.5, 38.8))
    s1 = str(b1)
    assert len(s1.splitlines()) == 9
    assert "167.50 x 83.50 x 38.80 mm" in s1
    assert "thickness: 1.00 mm" in s1
    assert "20.00 mm radius" in s1
    assert "label shelf 12.00 mm wide" in s1
    assert "25.20" in s1
    assert "54.37" in s1
    assert "40.15" in s1
    assert "gf_box_4x2x5_div2x1_holes_scoops_labels" in s1
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
        b1.save_stl_file(path=EXPORT_STEP_FILE_PATH)
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 8)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 96)
    assert len(r.faces(FlatFaceSelector(35)).vals()) == 1
    assert len(r.edges(FlatEdgeSelector(35)).vals()) == 51
    assert b1.filename() == "gf_box_4x2x5_div2x1_holes_scoops_labels"
    b1 = GridfinityBox(
        2, 2, 3, holes=True, length_div=1, width_div=1, scoops=True, labels=True
    )
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 83.5, 24.8))
    if _export_files("box"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
        b1 = GridfinityBox(
            2,
            2,
            3,
            holes=True,
            length_div=1,
            width_div=1,
            scoops=True,
            labels=True,
            wall_th=1.25,
        )
        r = b1.render()
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
