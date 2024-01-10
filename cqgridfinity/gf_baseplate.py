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
# Gridfinity Baseplates

import cadquery as cq

from cqgridfinity import *
from cqkit.cq_helpers import (
    rounded_rect_sketch,
    composite_from_pts,
    rotate_x,
    recentre,
)
from cqkit import VerticalEdgeSelector, HasZCoordinateSelector


class GridfinityBaseplate(GridfinityObject):
    """Gridfinity Baseplate

    This class represents a basic Gridfinity baseplate object. This baseplate
    more or less conforms to the original simple baseplate released by
    Zach Freedman. As such, it does not include features such as mounting
    holes, magnet holes, weight slots, etc.
      length_u - length in U (42 mm / U)
      width_y - width in U (42 mm / U)
      ext_depth - extrude bottom face by an extra amount in mm
      straight_bottom - remove bottom chamfer and replace with straight side
      corner_screws - add countersink mounting screws to the inside corners
      corner_tab_size - size of mounting screw corner tabs
      csk_hole - mounting screw hole diameter
      csk_diam - mounting screw countersink diameter
      csk_angle - mounting screw countersink angle
    """

    def __init__(self, length_u, width_u, **kwargs):
        super().__init__()
        self.length_u = length_u
        self.width_u = width_u
        self.ext_depth = 0
        self.straight_bottom = False
        self.corner_screws = False
        self.corner_tab_size = 21
        self.csk_hole = 5.0
        self.csk_diam = 10.0
        self.csk_angle = 82
        for k, v in kwargs.items():
            if k in self.__dict__ and v is not None:
                self.__dict__[k] = v
        if self.corner_screws:
            self.ext_depth = max(self.ext_depth, 5.0)

    def _corner_pts(self):
        oxy = self.corner_tab_size / 2
        return [
            (i * (self.length / 2 - oxy), j * (self.width / 2 - oxy), 0)
            for i in (-1, 1)
            for j in (-1, 1)
        ]

    def render(self):
        profile = GR_BASE_PROFILE if not self.straight_bottom else GR_STR_BASE_PROFILE
        if self.ext_depth > 0:
            profile = [*profile, self.ext_depth]
        rc = self.extrude_profile(
            rounded_rect_sketch(GRU_CUT, GRU_CUT, GR_RAD), profile
        )
        rc = rotate_x(rc, 180).translate((GRU2, GRU2, GR_BASE_HEIGHT + self.ext_depth))
        rc = recentre(composite_from_pts(rc, self.grid_centres), "XY")
        r = (
            cq.Workplane("XY")
            .rect(self.length, self.width)
            .extrude(GR_BASE_HEIGHT + self.ext_depth)
            .edges("|Z")
            .fillet(GR_RAD)
            .faces(">Z")
            .cut(rc)
        )
        if self.corner_screws:
            rs = cq.Sketch().rect(self.corner_tab_size, self.corner_tab_size)
            rs = cq.Workplane("XY").placeSketch(rs).extrude(self.ext_depth)
            rs = rs.faces(">Z").cskHole(
                self.csk_hole, cskDiameter=self.csk_diam, cskAngle=self.csk_angle
            )
            r = r.union(recentre(composite_from_pts(rs, self._corner_pts()), "XY"))
            bs = VerticalEdgeSelector(self.ext_depth) & HasZCoordinateSelector(0)
            r = r.edges(bs).fillet(GR_RAD)
        return r
