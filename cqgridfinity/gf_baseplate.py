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
    """

    def __init__(self, length_u, width_u, **kwargs):
        super().__init__()
        self.length_u = length_u
        self.width_u = width_u
        self.ext_depth = 0  # extra extrusion depth below bottom face
        self.straight_bottom = False  # remove chamfered bottom lip
        self.corner_screws = False
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

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
            rs = cq.Sketch().rect(21, 21)
            rs = cq.Workplane("XY").placeSketch(rs).extrude(self.ext_depth)
            rs = rs.faces(">Z").cskHole(5, cskDiameter=10, cskAngle=82)
            pts = [
                (i * (self.length / 2 - 10.5), j * (self.width / 2 - 10.5), 0)
                for i in (-1, 1)
                for j in (-1, 1)
            ]
            rp = composite_from_pts(rs, pts)
            rp = recentre(rp, "XY")
            r = r.union(rp)
            r = r.edges(
                VerticalEdgeSelector(self.ext_depth) & HasZCoordinateSelector(0)
            ).fillet(GR_RAD)
            pts = [
                (i * (self.length / 2 - 10), j * (self.width / 2 - 10), 0)
                for i in (-1, 1)
                for j in (-1, 1)
            ]

        return r
