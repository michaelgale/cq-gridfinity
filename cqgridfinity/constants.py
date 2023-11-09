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
# Globally useful constants representing Gridfinity geometry

from math import sqrt

SQRT2 = sqrt(2)

GRU = 42
GRU2 = GRU / 2
GRHU = 7
GRU_CUT = 42.71
GR_WALL = 1.0
GR_DIV_WALL = 1.2

GR_RAD = 4
GR_BASE_HEIGHT = 5
GR_BASE_CHAMF_H = 0.985 / SQRT2
GR_STR_H = 1.8
GR_BASE_TOP_CHAMF = GR_BASE_HEIGHT - GR_BASE_CHAMF_H - GR_STR_H

GR_HOLE_D = 6.5
GR_HOLE_H = 2.4
GR_BOLT_D = 3.0
GR_BOLT_H = 3.6 + GR_HOLE_H
GR_HOLE_DIST = 26 / 2

GR_BOT_H = 7.2
GR_FILLET = 1.2
GR_FLOOR = GR_BOT_H - GR_BASE_HEIGHT

GR_BOX_CHAMF_H = 1.13 / SQRT2
GR_BOX_TOP_CHAMF = GR_BASE_HEIGHT - GR_BOX_CHAMF_H - GR_STR_H
GR_TOL = 0.5

GR_UNDER_H = 1.6
GR_TOPSIDE_H = 1.2
GR_LIP_PROFILE = (
    (GR_UNDER_H * SQRT2, 45),
    GR_TOPSIDE_H,
    (0.7 * SQRT2, -45),
    1.8,
    (1.3 * SQRT2, -45),
)
GR_LIP_H = GR_UNDER_H + GR_TOPSIDE_H + 0.7 + 1.8 + 1.3
GR_NO_PROFILE = (GR_LIP_H,)
