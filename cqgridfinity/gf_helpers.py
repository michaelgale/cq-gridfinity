#! /usr/bin/env python3
#
# Copyright (C) 2023  Michael Gale
# This file is part of the cq-gridfinity python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Gridfinity Helper Functions

import cadquery as cq
from cqkit import rotate_z


def quarter_circle(
    outer_rad, inner_rad, height, quad="tr", chamf=0.5, chamf_face=">Z", ext=0
):
    """Renders a quarter circle shaped slot in any of 4 quadrants"""
    r = cq.Workplane("XY").circle(outer_rad).extrude(height)
    rc = cq.Workplane("XY").circle(inner_rad).extrude(height)
    r = r.cut(rc)
    rc = cq.Workplane("XY").rect(outer_rad, outer_rad).extrude(height)
    pos = {
        "tr": (outer_rad / 2, outer_rad / 2, 0),
        "tl": (-outer_rad / 2, outer_rad / 2, 0),
        "br": (outer_rad / 2, -outer_rad / 2, 0),
        "bl": (-outer_rad / 2, -outer_rad / 2, 0),
    }
    pt = pos[quad]
    r = r.intersect(rc.translate(pt))
    r = r.translate((-pt[0], -pt[1], 0))
    if ext > 0:
        faces = {
            "tl": "<Y >X",
            "tr": "<X <Y",
            "br": "<X >Y",
            "bl": ">Y >X",
        }
        for face in faces[quad].split():
            r = r.faces(face).wires().toPending().workplane().extrude(ext, combine=True)
    if chamf > 0:
        r = r.faces(chamf_face).chamfer(chamf)
    return r


def chamf_cyl(rad, height, chamf=0.5):
    """Chamfered cylinder."""
    r = cq.Workplane("XY").circle(rad).extrude(height)
    if chamf > 0:
        return r.faces("<Z or >Z").chamfer(chamf)
    return r


def chamf_rect(length, width, height, angle=0, tol=0.5, z_offset=0):
    """Chamfer rectangular box"""
    if not z_offset > 0:
        length += tol
        width += tol
        height += tol
    r = cq.Workplane("XY").rect(length, width).extrude(height)
    r = r.faces(">Z").chamfer(0.5).translate((0, 0, z_offset))
    return rotate_z(r, angle)
