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
EPS = 1e-5
M2_DIAM = 1.8
M2_CLR_DIAM = 2.5
M3_DIAM = 3
M3_CLR_DIAM = 3.5
M3_CB_DIAM = 5.5
M3_CB_DEPTH = 3.5

GRU = 42
GRU2 = GRU / 2
GRHU = 7

GRU_CUT = 42.2  # base extrusion width
GR_WALL = 1.0  # nominal exterior wall thickness
GR_DIV_WALL = 1.2  # width of dividing walls
GR_TOL = 0.5  # nominal tolerance

GR_RAD = 4  # nominal exterior filleting radius
GR_BASE_CLR = 0.25  # clearance above the nominal base height
GR_BASE_HEIGHT = 4.75  # nominal base height

# baseplate extrusion profile
GR_BASE_CHAMF_H = 0.98994949 / SQRT2
GR_STR_H = 1.8
GR_BASE_TOP_CHAMF = GR_BASE_HEIGHT - GR_BASE_CHAMF_H - GR_STR_H
GR_BASE_PROFILE = (
    (GR_BASE_TOP_CHAMF * SQRT2, 45),
    GR_STR_H,
    (GR_BASE_CHAMF_H * SQRT2, 45),
)
GR_STR_BASE_PROFILE = (
    (GR_BASE_TOP_CHAMF * SQRT2, 45),
    GR_STR_H + GR_BASE_CHAMF_H,
)

GR_BOT_H = 7  # bin nominal floor height
GR_FILLET = 1.1  # inside filleting radius
GR_FLOOR = GR_BOT_H - GR_BASE_HEIGHT  # floor offset

# box/bin extrusion profile
GR_BOX_CHAMF_H = 1.1313708 / SQRT2
GR_BOX_TOP_CHAMF = GR_BASE_HEIGHT - GR_BOX_CHAMF_H - GR_STR_H + GR_BASE_CLR
GR_BOX_PROFILE = (
    (GR_BOX_TOP_CHAMF * SQRT2, 45),
    GR_STR_H,
    (GR_BOX_CHAMF_H * SQRT2, 45),
)

# bin mating lip extrusion profile
GR_UNDER_H = 1.6
GR_TOPSIDE_H = 1.2
GR_LIP_PROFILE = (
    (GR_UNDER_H * SQRT2, 45),
    GR_TOPSIDE_H,
    (0.7 * SQRT2, -45),
    1.8,
    (1.3 * SQRT2, -45),
)
GR_LIP_H = 0
for h in GR_LIP_PROFILE:
    if isinstance(h, tuple):
        GR_LIP_H += h[0] / SQRT2
    else:
        GR_LIP_H += h
GR_NO_PROFILE = (GR_LIP_H,)

# bottom hole nominal dimensions
GR_HOLE_D = 6.5
GR_HOLE_H = 2.4
GR_BOLT_D = 3.0
GR_BOLT_H = 3.6 + GR_HOLE_H
GR_HOLE_DIST = 26 / 2
GR_HOLE_SLICE = 0.25

# Rugged Box constant parameters
GR_RBOX_WALL = 2.5
GR_RBOX_FLOOR = 1.2
GR_RBOX_CWALL = 10.0
GR_RBOX_CORNER_W = 56
GR_RBOX_BACK_L = 66
GR_RBOX_FRONT_L = 56
GR_RBOX_RAD = 3.745
GR_RBOX_CRAD = 14

GR_RBOX_CHAN_W = 20
GR_RBOX_CHAN_D = GR_RBOX_CWALL - GR_RBOX_WALL
GR_RBOX_VCUT_D = 1

GR_CLASP_SLIDE_D = 39
GR_CLASP_SLIDE_W = 4

GR_RIB_W = 2
GR_RIB_L = 5
GR_RIB_GAP = 1
GR_RIB_H = 3.5
GR_RIB_SEP = 4
GR_RIB_CTR = 10

GR_REG_L = 5
GR_REG_W = 2.5
GR_REG_H = 2.5
GR_REG_R0 = 10.75
GR_REG_R1 = 8.25
GR_BREG_R0 = GR_REG_R0 + 0.25
GR_BREG_R1 = GR_REG_R1 - 0.25

GR_HANDLE_L1 = 12
GR_HANDLE_L2 = 28
GR_HANDLE_H = 7.5
GR_HANDLE_W = 5
GR_HANDLE_SEP = 12.5
GR_HANDLE_OFS = 61.5
GR_HANDLE_SZ = 30
GR_HANDLE_TH = 7
GR_HANDLE_RAD = 11

GR_LID_HANDLE_W = 70
GR_SIDE_HANDLE_W = 60

GR_HINGE_SZ = 32
GR_HINGE_D = 3
GR_HINGE_W1 = 5.5
GR_HINGE_H1 = 2.7
GR_HINGE_W2 = 2.1
GR_HINGE_H2 = 9
GR_HINGE_CTR = 30.625
GR_HINGE_W3 = 2
GR_HINGE_SEP = 1
GR_HINGE_OFFS = 2.65
GR_HINGE_SKEW = 0.15
GR_HINGE_RAD = 3.5
GR_HINGE_TOL = 0.4
GR_HEX_H = 3
GR_HEX_W = 4
GR_HEX_D = 1.3
GR_LID_WINDOW_H = 6.5

GR_LABEL_SLOT_TH = 2.5
GR_LABEL_TH = 0.8
GR_LABEL_H = 31

GR_LATCH_L = 32.5
GR_LATCH_W = 19.6
GR_LATCH_H = 7
GR_LATCH_IW = 14.75
GR_LATCH_IL = 5.2
