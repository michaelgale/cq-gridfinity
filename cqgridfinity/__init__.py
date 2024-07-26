"""cqgridfinity - A python library to make Gridfinity compatible objects with CadQuery."""

import os

# fmt: off
__project__ = 'cqgridfinity'
__version__ = '0.5.7'
# fmt: on

VERSION = __project__ + "-" + __version__

script_dir = os.path.dirname(__file__)

from .constants import *
from .gf_obj import GridfinityObject
from .gf_baseplate import GridfinityBaseplate
from .gf_box import GridfinityBox, GridfinitySolidBox
from .gf_drawer import GridfinityDrawerSpacer
from .gf_ruggedbox import GridfinityRuggedBox
