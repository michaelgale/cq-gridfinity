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

import os

from cadquery import exporters

from cqgridfinity import *
from cqkit import export_step_file


class GridfinityObject:
    """Base Gridfinity object class

    This class bundles glabally relevant constants, properties, and methods
    for derived Gridfinity object classes.
    """

    def __init__(self, **kwargs):
        self.length_u = 1
        self.width_u = 1
        self.height_u = 1
        for k, v in kwargs.items():
            if k in self.__dict__:
                self.__dict__[k] = v

    @property
    def cq_obj(self):
        return self.render()

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
    def box_height(self):
        return self.height - GR_BASE_HEIGHT

    @property
    def int_height(self):
        return self.height - GR_LIP_H - GR_BOT_H

    @property
    def max_height(self):
        return self.int_height + GR_UNDER_H + GR_TOPSIDE_H

    @property
    def lip_width(self):
        if self.no_lip:
            return GR_WALL
        return GR_UNDER_H + GR_WALL

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
        return self.outer_l - 2 * GR_WALL

    @property
    def inner_w(self):
        return self.outer_w - 2 * GR_WALL

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
        return GRU2 - GR_WALL - GR_TOL / 2

    @property
    def inner_rad(self):
        return GR_RAD - GR_WALL

    def filename(self, prefix=None, path=None):
        """Returns a descriptive readable filename which represents a Gridfinity object.
        The filename can be optionally prefixed with arbitrary text and 
        an optional path prefix can also be specified."""
        from cqgridfinity import (
            GridfinityBaseplate,
            GridfinityBox,
            GridfinityDrawerSpacer,
        )

        if prefix is not None:
            prefix = prefix
        elif isinstance(self, GridfinityBaseplate):
            prefix = "gf_baseplate_"
        elif isinstance(self, GridfinityBox):
            prefix = "gf_box_"
        elif isinstance(self, GridfinityDrawerSpacer):
            prefix = "gf_corner_"
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
        return fn

    def save_step_file(self, filename=None, path=None, prefix=None):
        fn = (
            filename
            if filename is not None
            else self.filename(path=path, prefix=prefix)
        )
        if not fn.lower().endswith(".step"):
            fn = fn + ".step"

        # exporters.export(self.cq_obj, fn)
        export_step_file(self.cq_obj, fn)

    def save_stl_file(self, filename=None, path=None, prefix=None):
        fn = (
            filename
            if filename is not None
            else self.filename(path=path, prefix=prefix)
        )
        if not fn.lower().endswith(".stl"):
            fn = fn + ".stl"
        exporters.export(self.cq_obj, fn, tolerance=1e-2, angularTolerance=0.15)

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
