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
# Gridfinity Boxes

import math

import cadquery as cq
from cqkit import HasZCoordinateSelector, VerticalEdgeSelector
from cqkit.cq_helpers import multi_extrude, rounded_rect_sketch, composite_from_pts
from cqgridfinity import *


class GridfinityBox(GridfinityObject):
    """Gridfinity Box
    
    This class represents a Gridfinity compatible box module. As a minimum, 
    this class is initialized with basic 3D unit dimensions for length,
    width, and height.  length and width are multiples of 42 mm Gridfinity
    intervals and height represents multiples of 7 mm.
    
    Many box features can be enabled with attributes provided either as 
    keywords or direct dotted access.  These attributes include:
    - solid :   renders the box without an interior, i.e. a solid block. This
                is useful for making custom Gridfinity modules by subtracting
                out shapes from the solid interior. Normally, the box is 
                rendered solid up to its maximum size; however, the
                solid_ratio attribute can specify a solid fill of between
                0.0 to 1.0, i.e. 0 to 100% fill.
    - holes : adds bottom mounting holes for magnets or screws
    - scoops : adds a radiused bottom edge to the interior to help fetch 
               parts from the box
    - labels : adds a flat flange along each compartment for adding a label
    - no_lip : removes the contoured lip on the top module used for stacking
    - length_div, width_div : subdivides the box into sub-compartments in 
                 length and/or width.

    """

    def __init__(self, length_u, width_u, height_u, **kwargs):
        self.length_u = length_u
        self.width_u = width_u
        self.height_u = height_u
        self.length_div = 0
        self.width_div = 0
        self.scoops = False
        self.labels = False
        self.solid = False
        self.holes = False
        self.no_lip = False
        self.solid_ratio = 1.0
        self.label_width = 12  # width of the label strip
        self.label_height = 10  # thickness of label overhang
        self.label_lip_height = 0.8  # thickness of label vertical lip
        self.scoop_rad = 11  # radius of optional interior scoops
        self.fillet_interior = True
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        self._int_shell = None

    def render(self):
        """Returns a CadQuery Workplane object representing this Gridfinity box."""
        self._int_shell = None
        r = self.render_shell()
        rd = self.render_dividers()
        rs = self.render_scoops()
        rl = self.render_labels()
        for e in (rd, rs, rl):
            if e is not None:
                r = r.union(e)
        if not self.solid and self.fillet_interior:
            heights = [GR_FLOOR]
            if self.labels:
                heights.append(self.safe_label_height(backwall=True, from_bottom=True))
                heights.append(self.safe_label_height(backwall=False, from_bottom=True))
            bs = (
                HasZCoordinateSelector(heights, min_points=1, tolerance=0.5)
                + VerticalEdgeSelector(">5")
                - HasZCoordinateSelector("<%.2f" % (GR_FLOOR))
            )
            r = r.edges(bs).fillet(GR_FILLET)
        if self.holes:
            r = self.render_holes(r)
        return r.translate((-self.half_l, -self.half_w, GR_BASE_HEIGHT))

    @property
    def top_ref_height(self):
        """The height of the top surface of a solid box or the floor
        height of an empty box."""
        if self.solid:
            return self.max_height * self.solid_ratio + GR_BOT_H
        return GR_BOT_H

    def safe_label_height(self, backwall=False, from_bottom=False):
        lw = self.label_width
        if backwall:
            lw += self.lip_width
        lh = self.label_height * (lw / self.label_width)
        yl = self.max_height - self.label_height + GR_WALL
        if backwall:
            yl -= self.lip_width
        if yl < 0:
            lh = self.max_height - 1.5 * GR_FILLET - 0.1
        elif yl < 1.5 * GR_FILLET:
            lh -= 1.5 * GR_FILLET - yl + 0.1
        if from_bottom:
            ws = math.sin(math.atan2(self.label_height, self.label_width))
            if backwall:
                lh = self.max_height + GR_FLOOR - lh + ws * GR_WALL
            else:
                lh = self.max_height + GR_FLOOR - lh + ws * GR_DIV_WALL
        return lh

    @property
    def interior_solid(self):
        if self._int_shell is not None:
            return self._int_shell
        ri = rounded_rect_sketch(*self.inner_dim, self.inner_rad)
        rci = (
            cq.Workplane("XY")
            .placeSketch(ri)
            .extrude(self.int_height)
            .translate((*self.half_dim, GR_FLOOR))
        )
        if self.no_lip:
            rci = multi_extrude(rci, GR_NO_PROFILE)
        else:
            rci = multi_extrude(rci, GR_LIP_PROFILE)
        if self.solid:
            hs = self.max_height * self.solid_ratio
            rf = cq.Workplane("XY").placeSketch(ri).extrude(hs)
            rf = rf.translate((*self.half_dim, GR_FLOOR))
            rci = rci.cut(rf)
        if self.scoops and not self.no_lip:
            rf = (
                cq.Workplane("XY")
                .rect(self.inner_l, 2 * GR_UNDER_H)
                .extrude(self.max_height)
            )
            rf = rf.translate((self.half_l, -self.half_in, GR_FLOOR))
            rci = rci.cut(rf)
        self._int_shell = rci
        return self._int_shell

    def render_shell(self):
        rb = rounded_rect_sketch(GRU, GRU, GR_RAD)
        r = (
            cq.Workplane("XY")
            .placeSketch(rb)
            .extrude(GR_BOX_TOP_CHAMF * SQRT2, taper=45)
        )
        r = multi_extrude(r, [GR_STR_H, (GR_BOX_CHAMF_H * SQRT2, 45)])
        r = r.mirror(mirrorPlane="XY")
        pts = [
            (x * GRU, y * GRU)
            for x in range(self.length_u)
            for y in range(self.width_u)
        ]
        r = composite_from_pts(r, pts)
        rs = rounded_rect_sketch(*self.outer_dim, GR_RAD)
        rw = (
            cq.Workplane("XY")
            .placeSketch(rs)
            .extrude(self.box_height)
            .translate((*self.half_dim, 0))
        )
        rc = (
            cq.Workplane("XY")
            .placeSketch(rs)
            .extrude(-GR_BASE_HEIGHT - 1)
            .translate((*self.half_dim, 0.5))
        )
        return rc.intersect(r).union(rw).cut(self.interior_solid)

    def render_dividers(self):
        r = None
        if self.length_div > 0 and not self.solid:
            wall_w = (
                cq.Workplane("XY")
                .rect(GR_DIV_WALL, self.outer_w)
                .extrude(self.max_height)
                .translate((0, 0, GR_FLOOR))
            )
            xl = self.inner_l / (self.length_div + 1)
            pts = [
                ((x + 1) * xl - self.half_in, self.half_w)
                for x in range(self.length_div)
            ]
            r = composite_from_pts(wall_w, pts)

        if self.width_div > 0 and not self.solid:
            wall_l = (
                cq.Workplane("XY")
                .rect(self.outer_l, GR_DIV_WALL)
                .extrude(self.max_height)
                .translate((0, 0, GR_FLOOR))
            )
            yl = self.inner_w / (self.width_div + 1)
            pts = [
                (self.half_l, (y + 1) * yl - self.half_in)
                for y in range(self.width_div)
            ]
            rw = composite_from_pts(wall_l, pts)
            if r is not None:
                r = r.union(rw)
            else:
                r = rw
        return r

    def render_scoops(self):
        if not self.scoops or self.solid:
            return None
        # front wall scoop
        # prevent the scoop radius exceeding the internal height
        srad = min(self.scoop_rad, self.int_height - 0.1)
        rs = cq.Sketch().rect(srad, srad).vertices(">X and >Y").circle(srad, mode="s")
        rsc = cq.Workplane("YZ").placeSketch(rs).extrude(self.inner_l)
        rsc = rsc.translate((0, 0, srad / 2 + GR_FLOOR))
        yo = -self.half_in + srad / 2
        # offset front wall scoop by top lip overhang if applicable
        if not self.no_lip:
            yo += GR_UNDER_H
        rs = rsc.translate((-self.half_in, yo, 0))
        # intersect to prevent solids sticking out of rounded corners
        r = rs.intersect(self.interior_solid)
        if self.width_div > 0:
            # add scoops along each internal dividing wall
            yl = self.inner_w / (self.width_div + 1)
            pts = [
                (-self.half_in, (y + 1) * yl - self.half_in)
                for y in range(self.width_div)
            ]
            rs = composite_from_pts(rsc, pts)
            r = r.union(rs.translate((0, GR_DIV_WALL / 2 + srad / 2, 0)))
        return r

    def render_labels(self):
        if not self.labels or self.solid:
            return None
        # back wall label flange with compensated width and height
        lw = self.label_width + self.lip_width
        rs = (
            cq.Sketch()
            .segment((0, 0), (lw, 0))
            .segment((lw, -self.safe_label_height(backwall=True)))
            .segment((0, -self.label_lip_height))
            .close()
            .assemble()
            .vertices("<X")
            .vertices("<Y")
            .fillet(self.label_lip_height / 2)
        )
        rsc = cq.Workplane("YZ").placeSketch(rs).extrude(self.inner_l)
        yo = -lw + self.outer_w / 2 + self.half_w + GR_WALL / 4
        rs = rsc.translate((-self.half_in, yo, GR_FLOOR + self.max_height))
        # intersect to prevent solids sticking out of rounded corners
        r = rs.intersect(self.interior_solid)
        if self.width_div > 0:
            # add label flanges along each dividing wall
            rs = (
                cq.Sketch()
                .segment((0, 0), (self.label_width, 0))
                .segment((self.label_width, -self.safe_label_height(backwall=False)))
                .segment((0, -self.label_lip_height))
                .close()
                .assemble()
                .vertices("<X")
                .vertices("<Y")
                .fillet(self.label_lip_height / 2)
            )
            rsc = cq.Workplane("YZ").placeSketch(rs).extrude(self.inner_l)
            rsc = rsc.translate((0, -self.label_width, GR_FLOOR + self.max_height))
            yl = self.inner_w / (self.width_div + 1)
            pts = [
                (-self.half_in, (y + 1) * yl - self.half_in + GR_DIV_WALL / 2)
                for y in range(self.width_div)
            ]
            r = r.union(composite_from_pts(rsc, pts))
        return r

    def render_holes(self, obj):
        if not self.holes:
            return obj
        hole_pts = [
            (x * GRU - GR_HOLE_DIST * i, -(y * GRU - GR_HOLE_DIST * j),)
            for x in range(self.length_u)
            for y in range(self.width_u)
            for i in (-1, 1)
            for j in (-1, 1)
        ]
        obj = (
            obj.faces("<Z")
            .workplane()
            .pushPoints(hole_pts)
            .cboreHole(GR_BOLT_D, GR_HOLE_D, GR_HOLE_H, depth=GR_BOLT_H)
        )
        return obj


class GridfinitySolidBox(GridfinityBox):
    """Convenience class to represent a solid Gridfinity box."""

    def __init__(self, length_u, width_u, height_u, **kwargs):
        super().__init__(length_u, width_u, height_u, **kwargs, solid=True)
