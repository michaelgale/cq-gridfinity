# Gridfinity tests

# my modules
from cqgridfinity import *

from cqkit.cq_helpers import *
from cqkit import *

from common_test import (
    EXPORT_STEP_FILE_PATH,
    _almost_same,
    _export_files,
)


def _rugged_box():
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
    return b1


def test_rugged_box():
    b1 = _rugged_box()
    assert b1.filename() == "gf_ruggedbox_5x4x6_fr-hl_sd-hc_stack_lidbp"
    r = b1.render()
    assert r is not None
    assert _almost_same(size_3d(r), (230.0, 194.15, 47.5))
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)


def test_rugged_box_lid():
    b1 = _rugged_box()
    r = b1.render_lid()
    assert r is not None
    assert _almost_same(size_3d(r), (230.0, 188, 12.5))
    assert b1.filename() == "gf_ruggedbox_5x4x6_lid_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)


def test_rugged_box_acc():
    b1 = _rugged_box()
    r = b1.render_accessories()
    assert len(r.solids().vals()) == 16
    assert b1.filename() == "gf_ruggedbox_5x4x6_acc_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)


def test_rugged_box_parts():
    b1 = _rugged_box()
    r = b1.render_handle()
    assert r is not None
    assert b1.filename() == "gf_ruggedbox_5x4x6_handle_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = b1.render_hinge()
    assert r is not None
    assert b1.filename() == "gf_ruggedbox_5x4x6_hinge_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = b1.render_label()
    assert r is not None
    assert b1.filename() == "gf_ruggedbox_5x4x6_label_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)

    r = b1.render_latch()
    assert r is not None
    assert b1.filename() == "gf_ruggedbox_5x4x6_latch_fr-hl_sd-hc_stack_lidbp"
    if _export_files("rbox"):
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)


def test_rugged_box_assembly():
    if _export_files("rbox"):
        b1 = _rugged_box()
        r = b1.render_assembly()
        assert b1.filename() == "gf_ruggedbox_5x4x6_assembly_fr-hl_sd-hc_stack_lidbp"
        b1.save_step_file(path=EXPORT_STEP_FILE_PATH)
