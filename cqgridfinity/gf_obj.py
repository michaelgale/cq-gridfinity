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
# Gridfinity base object class

import math
import os

from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.StlAPI import StlAPI_Writer
import cadquery as cq
from cadquery import exporters

from cqgridfinity import *
from cqkit import export_step_file

# Special test to see which version of CadQuery is installed and
# therefore if any compensation is required for extruded zlen
# CQ versions < 2.4.0 typically require zlen correction, i.e.
# scaling the vertical extrusion extent by 1/cos(taper)
ZLEN_FIX = True
_r = cq.Workplane("XY").rect(2, 2).extrude(1, taper=45)
_bb = _r.vals()[0].BoundingBox()
if abs(_bb.zlen - 1.0) < 1e-3:
    ZLEN_FIX = False


class GridfinityObject:
    """Base Gridfinity object class

    This class bundles glabally relevant constants, properties, and methods
    for derived Gridfinity object classes.
    """

    def __init__(self, **kwargs):
        self.length_u = 1
        self.width_u = 1
        self.height_u = 1
        self._cq_obj = None
        self._obj_label = None
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

    @property
    def cq_obj(self):
        if self._cq_obj is None:
            return self.render()
        return self._cq_obj

    @property
    def length(self):
        return self.length_u * GRU

    @property
    def width(self):
        return self.width_u * GRU

    @property
    def height(self):
        return 3.8 + GRHU * self.height_u

    @property
    def int_height(self):
        h = self.height - GR_LIP_H - GR_BOT_H
        if self.lite_style:
            return h + self.wall_th
        return h

    @property
    def max_height(self):
        return self.int_height + GR_UNDER_H + GR_TOPSIDE_H

    @property
    def floor_h(self):
        if self.lite_style:
            return GR_FLOOR - self.wall_th
        return GR_FLOOR

    @property
    def lip_width(self):
        if self.no_lip:
            return self.wall_th
        return GR_UNDER_H + self.wall_th

    @property
    def outer_l(self):
        return self.length_u * GRU - GR_TOL

    @property
    def outer_w(self):
        return self.width_u * GRU - GR_TOL

    @property
    def outer_dim(self):
        return self.outer_l, self.outer_w

    @property
    def inner_l(self):
        return self.outer_l - 2 * self.wall_th

    @property
    def inner_w(self):
        return self.outer_w - 2 * self.wall_th

    @property
    def inner_dim(self):
        return self.inner_l, self.inner_w

    @property
    def half_l(self):
        return (self.length_u - 1) * GRU2

    @property
    def half_w(self):
        return (self.width_u - 1) * GRU2

    @property
    def half_dim(self):
        return self.half_l, self.half_w

    @property
    def half_in(self):
        return GRU2 - self.wall_th - GR_TOL / 2

    @property
    def outer_rad(self):
        return GR_RAD - GR_TOL / 2

    @property
    def inner_rad(self):
        return self.outer_rad - self.wall_th

    @property
    def under_h(self):
        return GR_UNDER_H - (self.wall_th - GR_WALL)

    @property
    def safe_fillet_rad(self):
        if not any([self.scoops, self.labels, self.length_div, self.width_div]):
            return GR_FILLET
        return min(GR_FILLET, (GR_UNDER_H + GR_WALL) - self.wall_th - 0.05)

    @property
    def grid_centres(self):
        return [
            (x * GRU, y * GRU)
            for x in range(self.length_u)
            for y in range(self.width_u)
        ]

    @property
    def hole_centres(self):
        return [
            (x * GRU - GR_HOLE_DIST * i, -(y * GRU - GR_HOLE_DIST * j))
            for x in range(self.length_u)
            for y in range(self.width_u)
            for i in (-1, 1)
            for j in (-1, 1)
        ]

    def safe_fillet(self, obj, selector, rad):
        if len(obj.edges(selector).vals()) > 0:
            return obj.edges(selector).fillet(rad)
        return obj

    def filename(self, prefix=None, path=None):
        """Returns a descriptive readable filename which represents a Gridfinity object.
        The filename can be optionally prefixed with arbitrary text and
        an optional path prefix can also be specified."""
        from cqgridfinity import (
            GridfinityBaseplate,
            GridfinityBox,
            GridfinityDrawerSpacer,
            GridfinityRuggedBox,
        )

        if prefix is not None:
            prefix = prefix
        elif isinstance(self, GridfinityBaseplate):
            prefix = "gf_baseplate_"
        elif isinstance(self, GridfinityBox):
            prefix = "gf_box_"
            if self.lite_style:
                prefix = prefix + "lite_"
        elif isinstance(self, GridfinityDrawerSpacer):
            prefix = "gf_drawer_"
        elif isinstance(self, GridfinityRuggedBox):
            prefix = "gf_ribbox_" if self.rib_style else "gf_ruggedbox_"
        else:
            prefix = ""
        fn = ""
        if path is not None:
            fn = fn.replace(os.sep, "")
            fn = path + os.sep
        fn = fn + prefix
        fn = fn + "%dx%d" % (self.length_u, self.width_u)
        if isinstance(self, GridfinityBox):
            fn = fn + "x%d" % (self.height_u)
            if self.length_div and not self.solid:
                fn = fn + "_div%d" % (self.length_div)
            if self.width_div and not self.solid:
                if self.length_div:
                    fn = fn + "x%d" % (self.width_div)
                else:
                    fn = fn + "_div_x%d" % (self.width_div)
            if abs(self.wall_th - GR_WALL) > 1e-3:
                fn = fn + "_%.2f" % (self.wall_th)
            if self.no_lip:
                fn = fn + "_basic"
            if self.holes:
                fn = fn + "_holes"
            if self.solid:
                fn = fn + "_solid"
            else:
                if self.scoops:
                    fn = fn + "_scoops"
                if self.labels:
                    fn = fn + "_labels"
        elif isinstance(self, GridfinityRuggedBox):
            fn = fn + "x%d" % (self.height_u)
            if self._obj_label is not None:
                fn = fn + "_%s" % (self._obj_label)
            if self.front_handle or self.front_label:
                fn = fn + "_fr-"
                if self.front_handle:
                    fn = fn + "h"
                if self.front_label:
                    fn = fn + "l"
            if self.side_handles or self.side_clasps:
                fn = fn + "_sd-"
                if self.side_handles:
                    fn = fn + "h"
                if self.side_clasps:
                    fn = fn + "c"
            if self.stackable:
                fn = fn + "_stack"
            if self.lid_baseplate:
                fn = fn + "_lidbp"
            if self.lid_window:
                fn = fn + "_win"
        elif isinstance(self, GridfinityDrawerSpacer):
            if self._obj_label is not None:
                fn = fn + "_%s" % (self._obj_label)
        elif isinstance(self, GridfinityBaseplate):
            if self.ext_depth > 0:
                fn = fn + "x%.1f" % (self.ext_depth)
            if self.corner_screws:
                fn = fn + "_screwtabs"
        return fn

    def save_step_file(self, filename=None, path=None, prefix=None):
        fn = (
            filename
            if filename is not None
            else self.filename(path=path, prefix=prefix)
        )
        if not fn.lower().endswith(".step"):
            fn = fn + ".step"
        if isinstance(self.cq_obj, cq.Assembly):
            self.cq_obj.save(fn)
        else:
            export_step_file(self.cq_obj, fn)

    def save_stl_file(
        self, filename=None, path=None, prefix=None, tol=1e-2, ang_tol=0.1
    ):
        fn = (
            filename
            if filename is not None
            else self.filename(path=path, prefix=prefix)
        )
        if not fn.lower().endswith(".stl"):
            fn = fn + ".stl"
        obj = self.cq_obj.val().wrapped
        mesh = BRepMesh_IncrementalMesh(obj, tol, True, ang_tol, True)
        mesh.Perform()
        writer = StlAPI_Writer()
        writer.Write(obj, fn)

    def save_svg_file(self, filename=None, path=None, prefix=None):
        fn = (
            filename
            if filename is not None
            else self.filename(path=path, prefix=prefix)
        )
        if not fn.lower().endswith(".svg"):
            fn = fn + ".svg"
        r = self.cq_obj.rotate((0, 0, 0), (0, 0, 1), 75)
        r = r.rotate((0, 0, 0), (1, 0, 0), -90)
        exporters.export(
            r,
            fn,
            opt={
                "width": 600,
                "height": 400,
                "showAxes": False,
                "marginTop": 20,
                "marginLeft": 20,
                "projectionDir": (1, 1, 1),
            },
        )

    def extrude_profile(self, sketch, profile, workplane="XY", angle=None):
        taper = profile[0][1] if isinstance(profile[0], (list, tuple)) else 0
        zlen = profile[0][0] if isinstance(profile[0], (list, tuple)) else profile[0]
        if abs(taper) > 0:
            if angle is None:
                zlen = zlen if ZLEN_FIX else zlen / SQRT2
            else:
                zlen = zlen / math.cos(math.radians(taper)) if ZLEN_FIX else zlen
        r = cq.Workplane(workplane).placeSketch(sketch).extrude(zlen, taper=taper)
        for level in profile[1:]:
            if isinstance(level, (tuple, list)):
                if angle is None:
                    zlen = level[0] if ZLEN_FIX else level[0] / SQRT2
                else:
                    zlen = (
                        level[0] / math.cos(math.radians(level[1]))
                        if ZLEN_FIX
                        else level[0]
                    )
                r = r.faces(">Z").wires().toPending().extrude(zlen, taper=level[1])
            else:
                r = r.faces(">Z").wires().toPending().extrude(level)
        return r

    @classmethod
    def to_step_file(
        cls,
        length_u,
        width_u,
        height_u=None,
        filename=None,
        prefix=None,
        path=None,
        **kwargs
    ):
        """Convenience method to create, render and save a STEP file representation
        of a Gridfinity object."""
        obj = GridfinityObject.as_obj(cls, length_u, width_u, height_u, **kwargs)
        obj.save_step_file(filename=filename, path=path, prefix=prefix)

    @classmethod
    def to_stl_file(
        cls,
        length_u,
        width_u,
        height_u=None,
        filename=None,
        prefix=None,
        path=None,
        **kwargs
    ):
        """Convenience method to create, render and save a STEP file representation
        of a Gridfinity object."""
        obj = GridfinityObject.as_obj(cls, length_u, width_u, height_u, **kwargs)
        obj.save_stl_file(filename=filename, path=path, prefix=prefix)

    @staticmethod
    def as_obj(cls, length_u=None, width_u=None, height_u=None, **kwargs):
        if "GridfinityBox" in cls.__name__:
            obj = GridfinityBox(length_u, width_u, height_u, **kwargs)
            if "GridfinitySolidBox" in cls.__name__:
                obj.solid = True
        elif "GridfinityBaseplate" in cls.__name__:
            obj = GridfinityBaseplate(length_u, width_u, **kwargs)
        elif "GridfinityDrawerSpacer" in cls.__name__:
            obj = GridfinityDrawerSpacer(**kwargs)
        return obj
