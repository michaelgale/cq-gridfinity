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
    multi_extrude,
    rounded_rect_sketch,
    composite_from_pts,
    rotate_x,
)


class GridfinityBaseplate(GridfinityObject):
    """Gridfinity Baseplate
    
    This class represents a basic Gridfinity baseplate object. This baseplate
    more or less conforms to the original simple baseplate released by 
    Zach Freedman. As such, it does not include features such as mounting
    holes, magnet holes, weight slots, etc."""

    def __init__(self, length_u, width_u, **kwargs):
        self.length_u = length_u
        self.width_u = width_u
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

    def render(self):
        rcu = rounded_rect_sketch(GRU_CUT, GRU_CUT, GR_RAD)
        rc = (
            cq.Workplane("XY")
            .placeSketch(rcu)
            .extrude(GR_BASE_TOP_CHAMF * SQRT2, taper=45)
        )
        rc = multi_extrude(rc, [GR_STR_H, (GR_BASE_CHAMF_H * SQRT2, 45)])
        rc = rotate_x(rc, 180).translate((GRU2, GRU2, GR_BASE_HEIGHT))
        pts = [
            (x * GRU, y * GRU)
            for x in range(self.length_u)
            for y in range(self.width_u)
        ]
        cutter = composite_from_pts(rc, pts)
        r = (
            cq.Workplane("XY")
            .box(self.length, self.width, GR_BASE_HEIGHT)
            .edges("|Z")
            .fillet(GR_RAD)
            .translate((self.length / 2, self.width / 2, GR_BASE_HEIGHT / 2,))
            .faces(">Z")
            .cut(cutter)
        )
        return r.translate((-self.length / 2, -self.width / 2, 0))
