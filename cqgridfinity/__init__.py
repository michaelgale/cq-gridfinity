"""cq-kit - A python library of CadQuery tools and helpers for building 3D CAD models."""

import os

# fmt: off
__project__ = 'cqgridfinity'
__version__ = '0.1.0'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .constants import *
from .gf_obj import GridfinityObject
from .gf_baseplate import GridfinityBaseplate
from .gf_box import GridfinityBox, GridfinitySolidBox
from .gf_drawer import GridfinityDrawerSpacer
