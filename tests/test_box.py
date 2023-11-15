# Gridfinity tests


# my modules
from cqgridfinity import *

# from cqkit.cq_helpers import size_3d
from cqkit.cq_helpers import *
from cqkit import *

from common_test import _almost_same, _edges_match, _faces_match

_EXPORT_STEP_FILES = False


def test_basic_box():
    b1 = GridfinityBox(2, 3, 5, no_lip=True)
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 48)
    assert b1.filename() == "gf_box_2x3x5_basic"
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles")


def test_lite_box():
    b1 = GridfinityBox(2, 3, 5, lite_style=True)
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 48)
    assert b1.filename() == "gf_box_lite_2x3x5"
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles")


def test_empty_box():
    b1 = GridfinityBox(2, 3, 5, holes=True)
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 125.5, 38.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 6)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 72)
    assert b1.filename() == "gf_box_2x3x5_holes"
    assert _almost_same(b1.top_ref_height, 7.2)
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles")


def test_solid_box():
    b1 = GridfinitySolidBox(4, 2, 3)
    r = b1.render()
    assert _almost_same(size_3d(r), (167.5, 83.5, 24.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 8)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 64)
    assert b1.filename() == "gf_box_4x2x3_solid"
    assert _almost_same(b1.top_ref_height, 21)
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles")
    b1.solid_ratio = 0.5
    assert _almost_same(b1.top_ref_height, 14.1)


def test_divided_box():
    b1 = GridfinityBox(3, 3, 3, holes=True, length_div=2, width_div=1)
    r = b1.render()
    assert _almost_same(size_3d(r), (125.5, 125.5, 24.8))
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 9)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 108)
    assert b1.filename() == "gf_box_3x3x3_div2x1_holes"
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles")


def test_all_features_box():
    b1 = GridfinityBox(
        4, 2, 5, holes=True, length_div=2, width_div=1, scoops=True, labels=True
    )
    b1.label_height = 9
    b1.scoop_rad = 20
    r = b1.render()
    assert _almost_same(size_3d(r), (167.5, 83.5, 38.8))
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles/")
        b1.save_stl_file(path="./testfiles/")
    assert _faces_match(r, ">Z", 1)
    assert _faces_match(r, "<Z", 8)
    assert _edges_match(r, ">Z", 16)
    assert _edges_match(r, "<Z", 96)
    assert b1.filename() == "gf_box_4x2x5_div2x1_holes_scoops_labels"
    b1 = GridfinityBox(
        2, 2, 3, holes=True, length_div=1, width_div=1, scoops=True, labels=True
    )
    r = b1.render()
    assert _almost_same(size_3d(r), (83.5, 83.5, 24.8))
    if _EXPORT_STEP_FILES:
        b1.save_step_file(path="./testfiles/")
