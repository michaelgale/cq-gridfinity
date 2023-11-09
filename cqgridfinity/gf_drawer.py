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
# Gridfinity Drawer Spacers

import math

import cadquery as cq

from cqgridfinity import *
from cqkit.cq_helpers import rotate_x, rotate_y, rotate_z


class GridfinityDrawerSpacer(GridfinityObject):
    """Gridfinity Drawer Spacers
    This class is used for making spacer elements which help fit Gridfinity baseplates
    snugly into a drawer.  The spacers consist of 4x corner elements plus a left/right
    pair and front/back pair. If the spacers are wide enough, they will include
    interlocking alignment pegs/holes.    
    """

    def __init__(self, dr_width=None, dr_depth=None, **kwargs):
        self.length_u = 1
        self.width_u = 1
        self.length_th = 10
        self.width_th = 10
        self.thickness = GR_BASE_HEIGHT
        self.chamf_rad = 1.0
        self.show_arrows = True
        self.arrow_h = 0.8
        self.length_fill = 0
        self.width_fill = 0
        self.align_features = True
        self.align_l = 16
        self.align_tol = 0.15
        self.align_min = 8
        self.min_margin = 4
        self.tolerance = GR_TOL
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        if dr_width is not None and dr_depth is not None:
            verbose = kwargs["verbose"] if "verbose" in kwargs else False
            self.best_fit_to_dim(dr_width, dr_depth, verbose=verbose)

    def best_fit_to_dim(self, length, width, verbose=False):
        """Computes the best fit of Gridfinity units to fill a drawer dimensions.
        The geometry of all the spacer elements is then computed to securely 
        centre the Gridfinity baseplate(s) inside the drawer footprint."""
        self.size = length, width
        lu, wu = (math.floor(x / GRU) for x in (length, width))
        lg, wg = (x * GRU for x in (lu, wu))
        lm, wm = (length - lg) / 2, (width - wg) / 2
        self.size_u = lu, wu
        self.width_th, self.length_th = lm - self.tolerance, wm - self.tolerance
        self.length_u, self.width_u = math.floor(lu / 3), math.floor(wu / 3)
        self.length_fill, self.width_fill = lg - 2 * self.length, wg - 2 * self.width
        if self.wide_enough:
            self.align_l = 1.5 * self.width_th
        if self.deep_enough:
            self.align_l = min(self.align_l, 1.5 * self.length_th)
        self.align_l = min(self.align_l, 16)
        if verbose:
            print("Best fit for %.2f x %.2f mm is %dU x %dU" % (length, width, lu, wu))
            print(
                "with %.2f mm margin each side and %.2f mm margin front and back"
                % (lm, wm)
            )
            if self.wide_enough and self.deep_enough:
                print(
                    "Corner spacers     : %dU wide x %dU deep"
                    % (self.length_u, self.width_u)
                )
            elif self.wide_enough:
                print(
                    "Corner spacers     : %dU deep x %.2f mm"
                    % (self.width_u, self.width_th)
                )
            elif self.deep_enough:
                print(
                    "Corner spacers     : %dU wide x %.2f mm"
                    % (self.length_u, self.length_th)
                )

            if self.deep_enough:
                print(
                    "Front/back spacers : %dU wide x %.2f mm +%.2f mm tolerance"
                    % (self.length_fill / GRU, self.length_th, self.tolerance)
                )
            else:
                print("Front/back spacers : not required")
            if self.wide_enough:
                print(
                    "Left/right spacers : %dU deep x %.2f mm +%.2f mm tolerance"
                    % (self.width_fill / GRU, self.width_th, self.tolerance)
                )
            else:
                print("Left/right spacers : not required")

    @property
    def fillet_rad(self):
        rads = [GR_RAD]
        if self.wide_enough:
            rads.append(self.width_th / 6)
        if self.deep_enough:
            rads.append(self.length_th / 6)
        return min(rads)

    @property
    def safe_chamfer_rad(self):
        rads = [self.chamf_rad]
        if self.wide_enough:
            rads.append(self.width_th / 6)
        if self.deep_enough:
            rads.append(self.length_th / 6)
        return min(rads)

    @property
    def wide_enough(self):
        return self.width_th > self.min_margin

    @property
    def deep_enough(self):
        return self.length_th > self.min_margin

    def render(self, arrows_top=True, arrows_bottom=True):
        """Renders a corner spacer component. This component can be used for any of
        the four corners due to symmetry.  Optional arrows can be cut into the 
        component on the top or bottom to show the drawer sliding/depth-wise direction"""
        sp_length = self.length + self.width_th + self.tolerance
        sp_width = self.width + self.length_th + self.tolerance
        r, rd = None, None
        if self.deep_enough:
            r = (
                cq.Workplane("XY")
                .rect(sp_length, self.length_th)
                .extrude(self.thickness)
            )
            r = r.translate((sp_length / 2, self.length_th / 2, 0))
            r = r.edges("|Z").edges("<X").edges("<Y").fillet(GR_RAD)
            r = r.edges("|Z").fillet(self.fillet_rad)
        if self.wide_enough:
            rd = (
                cq.Workplane("XY").rect(self.width_th, sp_width).extrude(self.thickness)
            )
            rd = rd.translate((self.width_th / 2, sp_width / 2, 0))
            rd = rd.edges("|Z").edges("<X").edges("<Y").fillet(GR_RAD)
            rd = rd.edges("|Z").fillet(self.fillet_rad)

        if r is not None and rd is not None:
            r = r.union(rd)
        elif r is None and rd is not None:
            r = rd
        r = r.faces(">Z or <Z").chamfer(self.safe_chamfer_rad)
        r = self.orientation_arrows(
            r, self.width_th / 2, sp_width / 2, top=arrows_top, bottom=arrows_bottom
        )
        if self.align_features and self.length_th > self.align_min:
            rc = self.alignment_feature(as_cutter=True)
            r = r.cut(rc.translate((sp_length, self.length_th / 2, 0)))
        if self.align_features and self.width_th > self.align_min:
            rc = self.alignment_feature(as_cutter=False, horz=False)
            r = r.union(rc.translate((self.width_th / 2, sp_width, 0)))
        return r

    def alignment_feature(self, as_cutter=False, horz=True):
        """Renders optional mating alignment pegs/holes for connecting the spacer components."""
        x, y = self.align_l, self.length_th / 2
        if not horz:
            y = self.width_th / 2
        fr = min(GR_RAD / 2, y / 3)
        if as_cutter:
            x += 2 * self.align_tol
            y += 2 * self.align_tol
            fr += self.align_tol
        rs = (
            cq.Sketch()
            .segment((0, y / 3), (x / 2, y / 2))
            .segment((x / 2, -y / 2))
            .segment((0, -y / 3))
            .segment((-x / 2, -y / 2))
            .segment((-x / 2, y / 2))
            .close()
            .assemble()
            .vertices()
            .fillet(fr)
        )
        r = cq.Workplane("XY").placeSketch(rs).extrude(self.thickness)
        if not horz:
            r = rotate_z(r, 90)
        if not as_cutter:
            r = r.faces(">Z or <Z").chamfer(self.safe_chamfer_rad)
        return r

    def orientation_arrows(self, obj, x, y, up=True, down=True, top=True, bottom=True):
        """Renders optional orientation arrows which show the sliding (depth-wise)
        direction of the drawer."""
        if self.show_arrows and self.wide_enough:
            la = self.width_th / 2
            ra = (
                cq.Sketch()
                .segment((0, 0), (la / 2, la))
                .segment((la, 0))
                .close()
                .assemble()
            )
            ru = (
                cq.Workplane("XY")
                .placeSketch(ra)
                .extrude(self.arrow_h)
                .translate((-la / 2, -la / 2, 0))
            )
            rd = ru.rotate((0, 0, 0), (0, 0, 1), 180)
            th = self.thickness - self.arrow_h
            yo = 10 * self.width_th / 15 if up and down else 0
            if up and top:
                obj = obj.cut(ru.translate((x, y + yo, th)))
            if up and bottom:
                obj = obj.cut(ru.translate((x, y + yo, 0)))
            if down and top:
                obj = obj.cut(rd.translate((x, y - yo, th)))
            if down and bottom:
                obj = obj.cut(rd.translate((x, y - yo, 0)))
        return obj

    def render_length_filler(self, alignment_type="peg"):
        """Renders the centre filler element used along the front/back walls
        of the drawer."""
        if not self.deep_enough:
            return None
        r = (
            cq.Workplane("XY")
            .rect(self.length_fill, self.length_th)
            .extrude(self.thickness)
        )
        r = r.edges("|Z").fillet(self.fillet_rad)
        r = r.faces(">Z or <Z").chamfer(self.safe_chamfer_rad)
        if self.align_features and self.length_th > self.align_min:
            if alignment_type == "hole":
                ra = self.alignment_feature(as_cutter=True)
                r = r.cut(ra.translate((self.length_fill / 2, 0, 0)))
                r = r.cut(ra.translate((-self.length_fill / 2, 0, 0)))
            else:
                ra = self.alignment_feature(as_cutter=False)
                r = r.union(ra.translate((self.length_fill / 2, 0, 0)))
                r = r.union(ra.translate((-self.length_fill / 2, 0, 0)))
        return r

    def render_width_filler(self, arrows_top=True, arrows_bottom=True):
        """Renders the centre filler element used along the left/right walls
        of the drawer."""
        if not self.wide_enough:
            return None
        r = (
            cq.Workplane("XY")
            .rect(self.width_th, self.width_fill)
            .extrude(self.thickness)
        )
        r = r.edges("|Z").fillet(self.fillet_rad)
        r = r.faces(">Z or <Z").chamfer(self.safe_chamfer_rad)
        r = self.orientation_arrows(r, 0, 0, top=arrows_top, bottom=arrows_bottom)
        if self.align_features and self.width_th > self.align_min:
            ra = self.alignment_feature(horz=False, as_cutter=True)
            r = r.cut(ra.translate((0, self.width_fill / 2, 0)))
            r = r.cut(ra.translate((0, -self.width_fill / 2, 0)))
        return r

    def render_full_set(self, include_baseplate=False):
        """Renders a complete set of spacer components including the four corners plus
        left/right and front/back spacer pairs.  The components are placed in their 
        respective installed position in the drawer so that the resulting object can
        be used to preview final composition of components."""
        # Four corners top/bottom left + top/bottom right
        bl = self.render()
        tl = rotate_x(bl, 180).translate((0, self.size[1], self.thickness))
        br = rotate_y(bl, 180).translate((self.size[0], 0, self.thickness))
        tr = rotate_z(bl, 180).translate((*self.size, 0))
        r = bl.union(tl).union(br).union(tr)

        # 2x length-wise (drawer width) fillers
        if self.deep_enough:
            lf = self.render_length_filler()
            r = r.union(lf.translate((self.size[0] / 2, self.length_th / 2, 0)))
            r = r.union(
                lf.translate((self.size[0] / 2, self.size[1] - self.length_th / 2, 0))
            )
        # 2x width-wise (drawer depth) fillers
        if self.wide_enough:
            wf = self.render_width_filler()
            r = r.union(wf.translate((self.width_th / 2, self.size[1] / 2, 0)))
            r = r.union(
                wf.translate((self.size[0] - self.width_th / 2, self.size[1] / 2, 0))
            )
        if include_baseplate:
            bp = GridfinityBaseplate(*self.size_u)
            rb = bp.render().translate((self.size[0] / 2, self.size[1] / 2, 0))
            r = r.union(rb)
        return r

    def render_half_set(self):
        """Renders half of the full set of spacer components arranged for convenience
        for 3D printing.  This resulting compound object can then be printed twice to
        yield a complete set of spacer components for a drawer."""
        # one of each corner
        bl = self.render(arrows_bottom=False)
        br = self.render(arrows_top=False)
        if self.deep_enough:
            xo = self.length + 2.5 * self.width_th
            yo = 1.5 * self.length_th
        else:
            xo = 2.5 * self.width_th
            yo = 0
        br = rotate_y(br, 180).translate((xo, yo, self.thickness))
        r = bl.union(br)
        # length-wise (drawer width) filler
        if self.deep_enough:
            xl = self.length_fill / 2 - (
                self.length_fill - (self.length + self.width_th)
            )
            if self.length_th > self.align_min:
                xl -= self.align_l / 2
            if self.wide_enough:
                yt = self.width + self.length_th
                if self.width_th > self.align_min:
                    yt += self.align_l / 2
                yl = max(yt, self.width_fill)
                yl += max(self.length_th, self.align_l / 2)
            else:
                yl = 3.5 * self.length_th
            r = r.union(self.render_length_filler().translate((xl, yl, 0)))
        # width-wise (drawer depth) filler
        if self.wide_enough:
            r = r.union(
                self.render_width_filler(arrows_bottom=False).translate(
                    (-2 * self.width_th / 2, self.width_fill / 2, 0)
                )
            )
        return r
