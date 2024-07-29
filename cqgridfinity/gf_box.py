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
from cqkit import HasZCoordinateSelector, VerticalEdgeSelector, FlatEdgeSelector
from cqkit.cq_helpers import rounded_rect_sketch, composite_from_pts
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
    - lite_style : render box as an economical shell without elevated floor
    - unsupported_holes : render bottom holes as 3D printer friendly versions
                          which can be printed without supports
    - label_width : width of top label ledge face overhang
    - label_height : height of label ledge overhang
    - scoop_rad : radius of the bottom scoop feature
    - wall_th : wall thickness
    - hole_diam : magnet/counterbore bolt hole diameter

    """

    def __init__(self, length_u, width_u, height_u, **kwargs):
        super().__init__()
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
        self.lite_style = False
        self.unsupported_holes = False
        self.label_width = 12  # width of the label strip
        self.label_height = 10  # thickness of label overhang
        self.label_lip_height = 0.8  # thickness of label vertical lip
        self.scoop_rad = 14  # radius of optional interior scoops
        self.fillet_interior = True
        self.wall_th = GR_WALL
        self.hole_diam = GR_HOLE_D  # magnet/bolt hole diameter
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        self._int_shell = None
        self._ext_shell = None

    def __str__(self):
        s = []
        s.append(
            "Gridfinity Box %dU x %dU x %dU (%.2f x %.2f x %.2f mm)"
            % (
                self.length_u,
                self.width_u,
                self.height_u,
                self.length - GR_TOL,
                self.width - GR_TOL,
                self.height,
            )
        )
        sl = "no mating top lip" if self.no_lip else "with mating top lip"
        ss = "Lite style box  " if self.lite_style else ""
        s.append("  %sWall thickness: %.2f mm  %s" % (ss, self.wall_th, sl))
        s.append(
            "  Floor height  : %.2f mm  Inside height: %.2f mm  Top reference height: %.2f mm"
            % (self.floor_h + GR_BASE_HEIGHT, self.int_height, self.top_ref_height)
        )
        if self.solid:
            s.append("  Solid filled box with fill ratio %.2f" % (self.solid_ratio))
        if self.holes:
            s.append("  Bottom mounting holes with %.2f mm diameter" % (self.hole_diam))
            if self.unsupported_holes:
                s.append("  Holes are 3D printer friendly and can be unsupported")
        if self.scoops:
            s.append("  Lengthwise scoops with %.2f mm radius" % (self.scoop_rad))
        if self.labels:
            s.append(
                "  Lengthwise label shelf %.2f mm wide with %.2f mm overhang"
                % (self.label_width, self.label_height)
            )
        if self.length_div:
            xl = (self.inner_l - GR_DIV_WALL * (self.length_div)) / (
                self.length_div + 1
            )
            s.append(
                "  %dx lengthwise divisions for %.2f mm compartment lengths"
                % (self.length_div, xl)
            )
        if self.width_div:
            yl = (self.inner_w - GR_DIV_WALL * (self.width_div)) / (self.width_div + 1)
            s.append(
                "  %dx widthwise divisions for %.2f mm compartment widths"
                % (self.width_div, yl)
            )
        s.append("  Auto filename: %s" % (self.filename()))
        return "\n".join(s)

    def render(self):
        """Returns a CadQuery Workplane object representing this Gridfinity box."""
        self._int_shell = None
        if self.lite_style:
            # just force the dividers to the desired quantity in both dimensions
            # rather than raise a exception
            if self.length_div:
                self.length_div = self.length_u - 1
            if self.width_div:
                self.width_div = self.width_u - 1
            if self.solid:
                raise ValueError(
                    "Cannot select both solid and lite box styles together"
                )
            if self.holes:
                raise ValueError(
                    "Cannot select both holes and lite box styles together"
                )
            if self.wall_th > 1.5:
                raise ValueError(
                    "Wall thickness cannot exceed 1.5 mm for lite box style"
                )
        if self.wall_th > 2.5:
            raise ValueError("Wall thickness cannot exceed 2.5 mm")
        if self.wall_th < 0.5:
            raise ValueError("Wall thickness must be at least 0.5 mm")
        r = self.render_shell()
        rd = self.render_dividers()
        rs = self.render_scoops()
        rl = self.render_labels()
        for e in (rd, rl, rs):
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
                - HasZCoordinateSelector("<%.2f" % (self.floor_h))
            )
            if self.lite_style and self.scoops:
                bs = bs - HasZCoordinateSelector("<=%.2f" % (self.floor_h))
                bs = bs - VerticalEdgeSelector()
            r = self.safe_fillet(r, bs, self.safe_fillet_rad)

            if self.lite_style and not self.has_dividers:
                bs = FlatEdgeSelector(self.floor_h)
                if self.wall_th < 1.2:
                    r = self.safe_fillet(r, bs, 0.5)
                elif self.wall_th < 1.5:
                    r = self.safe_fillet(r, bs, 0.25)

            if not self.labels and self.has_dividers:
                bs = VerticalEdgeSelector(
                    GR_TOPSIDE_H, tolerance=0.05
                ) & HasZCoordinateSelector(GRHU * self.height_u - GR_BASE_HEIGHT)
                r = self.safe_fillet(r, bs, GR_TOPSIDE_H - EPS)

        if self.holes:
            r = self.render_holes(r)
        r = r.translate((-self.half_l, -self.half_w, GR_BASE_HEIGHT))
        if self.unsupported_holes:
            r = self.render_hole_fillers(r)
        return r

    @property
    def top_ref_height(self):
        """The height of the top surface of a solid box or the floor
        height of an empty box."""
        if self.solid:
            return self.max_height * self.solid_ratio + GR_BOT_H
        if self.lite_style:
            return self.floor_h
        return GR_BOT_H

    @property
    def bin_height(self):
        return self.height - GR_BASE_HEIGHT

    def safe_label_height(self, backwall=False, from_bottom=False):
        lw = self.label_width
        if backwall:
            lw += self.lip_width
        lh = self.label_height * (lw / self.label_width)
        yl = self.max_height - self.label_height + self.wall_th
        if backwall:
            yl -= self.lip_width
        if yl < 0:
            lh = self.max_height - 1.5 * GR_FILLET - 0.1
        elif yl < 1.5 * GR_FILLET:
            lh -= 1.5 * GR_FILLET - yl + 0.1
        if from_bottom:
            ws = math.sin(math.atan2(self.label_height, self.label_width))
            if backwall:
                lh = self.max_height + GR_FLOOR - lh + ws * self.wall_th
            else:
                lh = self.max_height + GR_FLOOR - lh + ws * GR_DIV_WALL
        return lh

    @property
    def has_dividers(self):
        return self.length_div > 0 or self.width_div > 0

    @property
    def interior_solid(self):
        if self._int_shell is not None:
            return self._int_shell
        self._int_shell = self.render_interior()
        return self._int_shell

    def render_interior(self, force_solid=False):
        """Renders the interior cutting solid of the box."""
        wall_u = self.wall_th - GR_WALL
        wall_h = self.int_height + wall_u
        under_h = ((GR_UNDER_H - wall_u) * SQRT2, 45)
        profile = GR_NO_PROFILE if self.no_lip else [under_h, *GR_LIP_PROFILE[1:]]
        profile = [wall_h, *profile]
        if self.int_height < 0:
            profile = [self.height - GR_BOT_H]
        rci = self.extrude_profile(
            rounded_rect_sketch(*self.inner_dim, self.inner_rad), profile
        )
        rci = rci.translate((*self.half_dim, self.floor_h))
        if self.solid or force_solid:
            hs = self.max_height * self.solid_ratio
            ri = rounded_rect_sketch(*self.inner_dim, self.inner_rad)
            rf = cq.Workplane("XY").placeSketch(ri).extrude(hs)
            rf = rf.translate((*self.half_dim, self.floor_h))
            rci = rci.cut(rf)
        if self.scoops and not self.no_lip and not self.lite_style:
            rf = (
                cq.Workplane("XY")
                .rect(self.inner_l, 2 * self.under_h)
                .extrude(self.max_height)
                .translate((self.half_l, -self.half_in, self.floor_h))
            )
            rci = rci.cut(rf)
        if self.lite_style:
            r = composite_from_pts(self.base_interior(), self.grid_centres)
            rci = rci.union(r)
        return rci

    def solid_shell(self):
        """Returns a completely solid box object useful for intersecting with other solids."""
        if self._ext_shell is not None:
            return self._ext_shell
        r = self.render_shell(as_solid=True)
        self._ext_shell = r.cut(self.render_interior(force_solid=True))
        return self._ext_shell

    def mask_with_obj(self, obj):
        """Intersects a solid object with this box."""
        return obj.intersect(self.solid_shell())

    def base_interior(self):
        profile = [GR_BASE_HEIGHT, *GR_BOX_PROFILE]
        zo = GR_BASE_HEIGHT + GR_BASE_CLR
        if self.int_height < 0:
            h = self.bin_height - GR_BASE_HEIGHT
            profile = [h, *profile]
            zo += h
        r = self.extrude_profile(
            rounded_rect_sketch(GRU - GR_TOL, GRU - GR_TOL, self.outer_rad),
            profile,
        )
        rx = r.faces("<Z").shell(-self.wall_th)
        r = r.cut(rx).mirror(mirrorPlane="XY").translate((0, 0, zo))
        return r

    def render_shell(self, as_solid=False):
        """Renders the box shell without any added features."""
        r = self.extrude_profile(
            rounded_rect_sketch(GRU, GRU, self.outer_rad + GR_BASE_CLR), GR_BOX_PROFILE
        )
        r = r.translate((0, 0, -GR_BASE_CLR))
        r = r.mirror(mirrorPlane="XY")
        r = composite_from_pts(r, self.grid_centres)
        rs = rounded_rect_sketch(*self.outer_dim, self.outer_rad)
        rw = (
            cq.Workplane("XY")
            .placeSketch(rs)
            .extrude(self.bin_height - GR_BASE_CLR)
            .translate((*self.half_dim, GR_BASE_CLR))
        )
        rc = (
            cq.Workplane("XY")
            .placeSketch(rs)
            .extrude(-GR_BASE_HEIGHT - 1)
            .translate((*self.half_dim, 0.5))
        )
        rc = rc.intersect(r).union(rw)
        if not as_solid:
            return rc.cut(self.interior_solid)
        return rc

    def render_dividers(self):
        r = None
        if self.length_div > 0 and not self.solid:
            wall_w = (
                cq.Workplane("XY")
                .rect(GR_DIV_WALL, self.outer_w)
                .extrude(self.max_height)
                .translate((0, 0, self.floor_h))
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
                .translate((0, 0, self.floor_h))
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
        if not self.no_lip and not self.lite_style:
            yo += self.under_h
        zo = -GR_BOT_H + self.wall_th if self.lite_style else 0
        rs = rsc.translate((-self.half_in, yo, zo))
        # intersect to prevent solids sticking out of rounded corners
        r = rs.intersect(self.interior_solid)
        if self.width_div > 0:
            # add scoops along each internal dividing wall in the width dimension
            yl = self.inner_w / (self.width_div + 1)
            pts = [
                (-self.half_in, (y + 1) * yl - self.half_in)
                for y in range(self.width_div)
            ]
            rs = composite_from_pts(rsc, pts)
            r = r.union(rs.translate((0, GR_DIV_WALL / 2 + srad / 2, zo)))
            r = r.intersect(self.render_shell(as_solid=True))
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
        yo = -lw + self.outer_w / 2 + self.half_w + self.wall_th / 4
        rs = rsc.translate((-self.half_in, yo, self.floor_h + self.max_height))
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
            rsc = rsc.translate((0, -self.label_width, self.floor_h + self.max_height))
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
        h = GR_HOLE_H
        if self.unsupported_holes:
            h += GR_HOLE_SLICE
        return (
            obj.faces("<Z")
            .workplane()
            .pushPoints(self.hole_centres)
            .cboreHole(GR_BOLT_D, self.hole_diam, h, depth=GR_BOLT_H)
        )

    def render_hole_fillers(self, obj):
        rc = (
            cq.Workplane("XY")
            .rect(self.hole_diam / 2, self.hole_diam)
            .extrude(GR_HOLE_SLICE)
        )
        xo = self.hole_diam / 2
        rs = composite_from_pts(rc, [(-xo, 0, GR_HOLE_H), (xo, 0, GR_HOLE_H)])
        rs = composite_from_pts(rs, self.hole_centres)
        return obj.union(rs.translate((-self.half_l, self.half_w, 0)))


class GridfinitySolidBox(GridfinityBox):
    """Convenience class to represent a solid Gridfinity box."""

    def __init__(self, length_u, width_u, height_u, **kwargs):
        super().__init__(length_u, width_u, height_u, **kwargs, solid=True)
