<!-- <img src=./images/logo.png width=320> -->
![cq-gridfinity Logo](./images/logo.png)

# cq-gridfinity

[![](https://img.shields.io/pypi/v/cqgridfinity.svg)](https://pypi.org/project/cqgridfinity/)
![python version](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=blue&style=flat&logo=python)
[![](https://img.shields.io/static/v1?label=dependencies&message=CadQuery%202.0%2B&color=blue&style=flat)](https://github.com/CadQuery/cadquery)
[![](https://img.shields.io/badge/CQ--kit-blue)](https://github.com/michaelgale/cq-kit)
![https://github.com/michaelgale/cq-kit/blob/master/LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)
[![](https://img.shields.io/badge/code%20style-black-black.svg)](http://github.com/psf/black)

This repository contains a python library to build [Gridfinity](https://gridfinity.xyz) boxes, baseplates, and other objects based on the [CadQuery](https://github.com/CadQuery/cadquery) python library.  The Gridfinity system was created by [Zach Freedman](https://www.youtube.com/c/ZackFreedman) as a versatile system of modular organization and storage modules.  A vibrant community of user contributed modules and utilities has grown around the Gridfinity system.  This repository contains python classes to create gridfinity compatible parameterized components such as baseplates and boxes.

Examples of how I am starting to use Gridfinity to organize my tools are shown below using components built with this python library:

<img src=./images/examples.png width=800>

# Quick Links

- [Installation / Usage](#installation)
- [Shell Command Scripts](#shell-command-scripts)
  - [gridfinitybox](#gridfinitybox)
  - [gridfinitybase](#gridfinitybase)
  - [ruggedbox](#ruggedbox)
- [Classes](#classes)
  - [GridfinityBaseplate](#gridfinitybaseplate)
  - [GridfinityBox](#gridfinitybox-1)
  - [GridfinityDrawerSpacer](#gridfinitydrawerspacer)
  - [GridfinityRuggedBox](#gridfinityruggedbox)
  - [GridfinityObject](#gridfinityobject)
- [References](#references)

## Installation

**cq-gridfinity** has the following installation dependencies:
- [CadQuery](https://github.com/CadQuery/cadquery)
- [cq-kit](https://github.com/michaelgale/cq-kit)

Assuming these dependencie are installed, you can install **cq-gridfinity** using a [PyPI package](https://pypi.org/project/cqgridfinity/) as follows:

```bash
$ pip install cqgridfinity
```

Alternatively, the **cq-gridfinity** package can be installed directly from the source code:

```bash
$ git clone https://github.com/michaelgale/cq-gridfinity.git
$ cd cq-gridfinity
$ pip install .
```

## Basic Usage

After installation, the package can imported:

```shell
$ python
>>> import cqgridfinity
>>> cqgridfinity.__version__
```

An example of the package can be seen below:

```python
from cqgridfinity import *

# make a simple box
box = GridfinityBox(3, 2, 5, holes=True, no_lip=False, scoops=True, labels=True)
box.save_stl_file()
# Output a STL file of box:
#   gf_box_3x2x5_holes_scoops_labels.stl
```

# Shell Command Scripts

- [gridfinitybox](#gridfinitybox)
- [gridfinitybase](#gridfinitybase)
- [ruggedbox](#ruggedbox)

This package can be used to make your own python scripts to generate Gridfinity objects.  This gives the flexibility to customize the object and combine with other code to add custom cutouts, add text labels, etc.

However, for simple generation of standard objects such as baseplates and boxes, console scripts can be used for quick command line usage.  These console scripts are installed automatically into the path of your python environment and should be accessible from your terminal shell.

## `gridfinitybox`

<img src=./images/box_script.png width=600>

Make a customized/parameterized Gridfinity compatible box with many optional features.

```
usage: gridfinitybox [-h] [-m] [-u] [-n] [-s] [-l] [-e] [-d] [-r RATIO] [-ld LENGTHDIV] [-wd WIDTHDIV] [-wt WALL]
                     [-f FORMAT] [-o OUTPUT]
                     length width height

Make a customized/parameterized Gridfinity compatible box with many optional features.

positional arguments:
  length                Box length in U (1U = 42 mm)
  width                 Box width in U (1U = 42 mm)
  height                Box height in U (1U = 7 mm)

options:
  -h, --help            show this help message and exit
  -m, --magnetholes     Add bottom magnet/mounting holes
  -u, --unsupported     Add bottom magnet holes with 3D printer friendly strips without support
  -n, --nolip           Do not add mating lip to the top perimeter
  -s, --scoops          Add finger scoops against each length-wise back wall
  -l, --labels          Add label strips against each length-wise front wall
  -e, --ecolite         Make economy / lite style box with no elevated floor
  -d, --solid           Make solid (filled) box for customized storage
  -r RATIO, --ratio RATIO
                        Solid box fill ratio 0.0 = minimum, 1.0 = full height
  -ld LENGTHDIV, --lengthdiv LENGTHDIV
                        Split box length-wise with specified number of divider walls
  -wd WIDTHDIV, --widthdiv WIDTHDIV
                        Split box width-wise with specified number of divider walls
  -wt WALL, --wall WALL
                        Wall thickness (default=1 mm)
  -f FORMAT, --format FORMAT
                        Output file format (STEP, STL, SVG) default=STEP
  -o OUTPUT, --output OUTPUT
                        Output filename (inferred output file format with extension)

```

Examples:

```shell
# 2x3x5 box with magnet holes saved to STL file with default filename:
$ gridfinitybox 2 3 5 -m -f stl
# gf_box_2x3x5_holes.stl

# 1x3x4 box with scoops, label strip, 3 internal partitions and specified name:
$ gridfinitybox 1 3 4 -s -l -ld 3 -o MyBox.step
# MyBox.step

# Solid 3x3x3 box with 50% fill, unsupported magnet holes and no top lip:
$ gridfinitybox 3 3 3 -d -r 0.5 -u -n
# gf_box_3x3x3_basic_holes_solid.step

# Lite style box 3x2x3 with label strip, partitions, output to default SVG file:
$ gridfinitybox 3 2 3 -e -l -ld 2 -f svg
# gf_box_lite_3x2x3_div2_labels.svg
```

## `gridfinitybase`

<img src=./images/base_script.png width=600>

Make a customized/parameterized Gridfinity compatible simple baseplate.

```
usage: gridfinitybase [-h] [-f FORMAT] [-s] [-d DEPTH] [-hd HOLEDIAM] [-hc CSKDIAM] [-ca CSKANGLE] [-o OUTPUT]
                      length width

Make a customized/parameterized Gridfinity compatible simple baseplate.

positional arguments:
  length                Box length in U (1U = 42 mm)
  width                 Box width in U (1U = 42 mm)

options:
  -h, --help            show this help message and exit
  -f FORMAT, --format FORMAT
                        Output file format (STEP, STL, SVG) default=STEP
  -s, --screws          Add screw mounting tabs to the corners (adds +5 mm to depth)
  -d DEPTH, --depth DEPTH
                        Extrude extended depth under baseplate by this amount
  -hd HOLEDIAM, --holediam HOLEDIAM
                        Corner mounting screw hole diameter (default=5)
  -hc CSKDIAM, --cskdiam CSKDIAM
                        Corner mounting screw countersink diameter (default=10)
  -ca CSKANGLE, --cskangle CSKANGLE
                        Corner mounting screw countersink angle (deg) (default=82)
  -o OUTPUT, --output OUTPUT
                        Output filename (inferred output file format with extension)
```

Examples:

```shell
# 7 x 4 baseplate with screw corners to default STL file:
$ gridfinitybase 7 4 -s -f stl
# gf_baseplate_7x4x5.0_screwtabs.stl
```

## `ruggedbox`

<img src=./images/rugged_box.png width=600>

Make a parameterized rugged storage box compatible with gridfinity. This box is based on the [superb design by Pred on Printables](https://www.printables.com/model/543553-gridfinity-storage-box-by-pred-now-parametric).  This implementation makes a few improvements and additions to Pred's design in addition to making almost all of the box's features optional and tunable.  Using either the `ruggedbox` console script or the `GridfinityRuggedBox` class, you can make vast variety of different boxes of various sizes and features.  By default, almost all of the boxes features are enabled, but by using the desired command line options you can customize your desired feature set.

```
usage: ruggedbox [-h] [+l] [-l] [+p] [-p] [+w] [-w] [-wt WINDOWTHICKNESS] [+a] [-a] [+c] [-c] [+s] [-s] [+v] [-v]
                 [+e] [-e] [+b] [-b] [-r] [+r] [-f FORMAT] [-o OUTPUT] [-gb] [-gl] [-ga] [-gh] [-ge] [-gn] [-gt]
                 [-gw]
                 length width height

Make a customized/parameterized Gridfinity compatible rugged box enclosure.
The minimum box size is 3U x 3U x 4U.

positional arguments:
  length                Box length in U (1U = 42 mm)
  width                 Box width in U (1U = 42 mm)
  height                Box height in U (1U = 7 mm)

options:
  -h, --help            show this help message and exit
  +l, --label           Add label window across the front wall
  -l, --nolabel         Remove label window across the front wall
  +p, --lidbaseplate    Add baseplate to top of the lid
  -p, --nolidbaseplate  Smooth/plain lid
  +w, --lidwindow       Add window slot to the lid
  -w, --nolidwindow     Do not add window slot to the lid
  -wt WINDOWTHICKNESS, --windowthickness WINDOWTHICKNESS
                        Thickness of lid windows (mm)
  +a, --handle          Add front handle
  -a, --nohandle        No front handle
  +c, --clasps          Add clasps to the left and right side walls
  -c, --noclasps        No clasps on the left and right side walls
  +s, --stackable       Add stackable mating features to top and bottom
  -s, --notstackable    Non-stackable box
  +v, --veegroove       Add v-cut grooves to side walls
  -v, --noveegroove     No v-cut grooves (plain) side walls
  +e, --sidehandle      Add handles to side walls
  -e, --nosidehandle    No handles on side walls
  +b, --backfeet        Add standing feet to back wall
  -b, --nobackfeet      No standing feet added to back wall
  -r, --normalstyle     Make normal style box
  +r, --ribstyle        Make rib style box with exposed vertical ribs
  -f FORMAT, --format FORMAT
                        Output file format (STEP, STL, SVG) default=STEP
  -o OUTPUT, --output OUTPUT
                        Output filename (inferred output file format with extension)
  -gb, --box            Generate box
  -gl, --lid            Generate lid
  -ga, --acc            Generate accessory components
  -gh, --hinge          Generate hinge element
  -ge, --genlabel       Generate label panel insert
  -gn, --genhandle      Generate front handle
  -gt, --genlatch       Generate latch component
  -gw, --genwindow      Generate lid window component

example usage:

  5 x 4 x 6 rugged box shell and lid saved to STL files:
  $ ruggedbox 5 4 6 --box --lid -f stl
```
Examples:

5 x 4 x 6 rugged box component saved to STL file:

```shell
$ ruggedbox 5 4 6 -gb -f stl
 ____                             _ ____
|  _ \ _   _  __ _  __ _  ___  __| | __ )  _____  __
| |_) | | | |/ _` |/ _` |/ _ \/ _` |  _ \ / _ \ \/ /
|  _ <| |_| | (_| | (_| |  __/ (_| | |_) | (_) >  <
|_| \_\\__,_|\__, |\__, |\___|\__,_|____/ \___/_/\_\
             |___/ |___/

Version: 0.5.7
Gridfinity rugged box: 5U x 4U x 6U
  Exterior dim: 230.0 mm x 188.0 mm x 55.0 mm
  Interior dim: 210.0 mm x 168.0 mm x 45.8 mm
  Internal volume: 1.616 L
  Wall Vgrooves      : Y
  Front Handle       : Y
  Stackable          : Y
  Side Clasps        : Y
  Lid Baseplate      : Y
  Inside Baseplate   : Y
  Side Handles       : Y
  Front Label        : Y
  Back Feet          : Y
  Rib Style          : N
  Lid Window         : N
Rendering box...
Component generated and saved as gf_ruggedbox_5x4x6_body_fr-hl_sd-hc_stack_lidbp.stl in STL format
$
```

```shell
# same 5 x 4 x 6 rugged box with the lid saved to STL file:
$ ruggedbox 5 4 6 --lid -f stl
# gf_ruggedbox_5x4x6_lid_fr-hl_sd-hc_stack_lidbp.stl

# 5 x 5 x 9 rugged box, smooth lid, non-stackable, and no handle; full assembly saved to STEP file
$ ruggedbox 5 5 9 --nohandle --nolidbaseplate --notstackable
# gf_ruggedbox_5x5x9_fr-l_sd-hc.step

# Render the box, lid, and hinge for a 5x4x6 rugged box all at once:
$ ruggedbox 5 4 6 --box --lid --hinge
# gf_ruggedbox_5x4x6_fr-hl_sd-hc_stack_lidbp.step
# gf_ruggedbox_5x4x6_lid_fr-hl_sd-hc_stack_lidbp.step
# gf_ruggedbox_5x4x6_hinge_fr-hl_sd-hc_stack_lidbp.step

# Then render the latches and handle components for the same box:
$ ruggedbox 5 4 6 --acc
# gf_ruggedbox_5x4x6_acc_fr-hl_sd-hc_stack_lidbp.step

# Or render individual components as STL files with your preferred name:
$ ruggedbox 5 4 6 --genhandle --genlatch -o orange.stl
# orange_handle.stl
# orange_latch.stl
```

# Classes

- [GridfinityBaseplate](#gridfinitybaseplate)
- [GridfinityBox](#gridfinitybox-1)
- [GridfinityDrawerSpacer](#gridfinitydrawerspacer)
- [GridfinityRuggedBox](#gridfinityruggedbox)
- [GridfinityObject](#gridfinityobject)
  

## `GridfinityBaseplate`

Gridfinity baseplates can be made with the `GridfinityBaseplate` class.  The baseplate style is the basic style initially proposed by Zach Freedman.  Therefore, it does not have magnet or mounting holes.  An example usage is as follows:

```python
# Create 4 x 3 baseplate
baseplate = GridfinityBaseplate(4, 3)
baseplate.save_step_file()
# gf_baseplate_4x3.step
```
<img src=./images/baseplate4x3.png width=512>

Baseplates can be rendered with extra depth to make a taller overall baseplate using the `ext_depth` attribute.  Furthermore, mounting screws corner tabs can be added to the baseplate with the `corner_screws` attribute.  A baseplate with this feature is shown below.

<img src=./images/baseplate6x3.png width=512>

### Optional Keyword Arguments

```python
ext_depth = 0            # extended depth to extrude below baseplate
straight_bottom = False  # add/remove 0.8 mm chamfer on bottom of baseplate
corner_screws = False    # add corner mounting screw tabs
corner_tab_size = 21     # size of screw mounting tab (mm)
csk_hole = 5.0           # hole diameter of countersink mounting screw (mm)
csk_diam = 10.0          # countersink diameter (mm)
csk_angle = 82           # countersink angle (deg)
```

## `GridfinityBox`

Gridfinity boxes with many optional features can be created with the `GridfinityBox` class.  As a minimum, this class is initialized with basic 3D unit dimensions for length, width, and height.  The length and width are multiples of 42 mm Gridfinity intervals and height represents multiples of 7 mm.

### Simple Box

```python
# Create a simple 3 x 2 box, 5U high
box = GridfinityBox(3, 2, 5)
box.save_step_file()
# Output a STEP file of box named:
#   gf_box_3x2x5.step
``` 
<img src=./images/basic_box.png width=512>

### Lite Style Box

"Lite" style boxes are simplified for faster 3D printing with less material.  They remove the continuous floor at 7.2 mm and the box becomes a homogenous 1 mm thick walled shell. "lite" style boxes can include labels and dividers; however, the number of dividers must correspond to the same bottom partition ridges, i.e. `length_div` must be `length_u - 1` and `width_div` must be `width_u - 1`.  "lite" style cannot be combined with solid boxes, finger scoops, or magnet holes.

```python
# Create a "lite" style 3 x 2 box, 5U high
box = GridfinityBox(3, 2, 5, lite_style=True)
box.save_step_file()
# Output a STEP file of box named:
#   gf_box_lite_3x2x5.step
``` 
<img src=./images/box_lite.png width=512>

### Magnet Holes

```python
# add magnet holes to the box
box = GridfinityBox(3, 2, 5, holes=True)
box.save_step_file()
# gf_box_3x2x5_holes.step
```
<img src=./images/box_holes.png width=512>

The `unsupported_holes` attribute can specify either regular holes or modified/unsupported holes which are more suitable for 3D-printing.  These modified holes include thin filler strips which allow the slicer to avoid using supports to render the underside holes.

```python
# add magnet holes to the box
box = GridfinityBox(1, 1, 5, holes=True, unsupported_holes=True)
box.save_step_file()
# gf_box_1x1x5_holes.step
```
<img src=./images/box_holetypes.png width=512>

### Simple Box with No Top Lip

```python
# remove top mounting lip
box = GridfinityBox(3, 2, 5, no_lip=True)
box.save_step_file()
# gf_box_3x2x5_basic.step
```
<img src=./images/box_nolip.png width=512>

### Scoops and Labels

```python
# add finger scoops and label top flange
box = GridfinityBox(3, 2, 5, scoops=True, labels=True)
box.save_step_file()
# gf_box_3x2x5_scoops_labels.step
```
<img src=./images/box_options.png width=512>

### Dividing Walls

```python
# add dividing walls
box = GridfinityBox(3, 2, 5, length_div=2, width_div=1, scoops=True, labels=True)
box.save_step_file()
# gf_box_3x2x5_div2x1_scoops_labels.step
```
<img src=./images/box_div.png width=512>

### Solid Box

```python
# make a partially solid box
box = GridfinityBox(3, 2, 5, solid=True, solid_ratio=0.7)
box.save_step_file()
# gf_box_3x2x5_solid.step
```
<img src=./images/box_solid.png width=512>

### Optional Keyword Arguments

```python
length_div=0            # add dividing walls along length
width_div=0             # add dividing walls along width
holes=False             # add magnet holes to bottom
unsupported_holes=False # 3D-printer friendly hole style requiring no supports
no_lip=False            # remove top mating lip feature
scoops=False            # add finger scoops
scoop_rad=11            # radius of optional interior scoops
labels=False            # add a label flange to the top
label_width=12          # width of the label strip
label_height=10         # thickness height of label overhang
label_lip_height=0.8    # thickness of label vertical lip
lite_style=False        # make a "lite" version of box without elevated floor
solid=False             # make a solid box
solid_ratio=1.0         # ratio of solid height range 0.0 to 1.0 (max height)
wall_th=1.0             # wall thickness (0.5-2.5 mm)
fillet_interior=True    # enable/disable internal fillet edges
```

## `GridfinityDrawerSpacer`

The `GridfinityDrawerSpacer` class can be used to make spacer components to fit a drawer with any arbitrary dimensions.  Initialize with specified width and depth of the drawer (in mm) and the best fit of integer gridfinity baseplate units is computed.  Rarely, integer multiples of 42 mm gridfinity baseplates fit perfectly inside a drawer; therefore, spacers are required to secure the baseplate snuggly inside the drawer.  Spacers consist of 4x identical corner sections, 2x spacers for the left and right sides and 2x spacers for the front and back edges.

If the computed spacer width falls below a configurable threshold (default 4 mm), then no spacer component is made in that dimension.  The spacer components are made by default with interlocking "jigsaw" type features to assist with assembly and to secure the spacers within the drawer.  Also, alignment arrows (default but optional) are placed on the components to indicate the installation orientation in the direction of the drawer movement.

```python
# make drawer spacers for Craftsman tool chest drawer 23" wide x 19" deep
spacer = GridfinityDrawerSpacer(582, 481, verbose=True)
# Best fit for 582.00 x 481.00 mm is 13U x 11U
# with 18.00 mm margin each side and 9.50 mm margin front and back
# Corner spacers     : 4U wide x 3U deep
# Front/back spacers : 5U wide x 9.25 mm +0.25 mm tolerance
# Left/right spacers : 5U deep x 17.75 mm +0.25 mm tolerance
```
<img src=./images/drawer_photo.png width=600>


A full set of components (optionally including a full baseplate) can be rendered with the `render_full_set()` method.  This method is mostly used to verify the fit and placement of the spacers.

<img src=./images/full_set.png width=600>


Normally, the `render_half_set()` method used to render half of the components compactly arranged conveniently for 3D printing.  This set can be printed twice to make a full set for a single drawer.

<img src=./images/half_set.png width=600>

### Optional Keyword Arguments

```python
thickness=GR_BASE_HEIGHT # thickness of spacers, default=5 mm
chamf_rad=1.0            # chamfer radius of spacer top/bottom edges
show_arrows=True         # show orientation arrows indicating drawer in/out direction
align_features=True      # add "jigsaw" interlocking feautures
align_tol=0.15           # tolerance of the interlocking joint
align_min=8              # minimum spacer width for adding interlocking feature
min_margin=4             # minimum size to make a spacer, nothing is made for smaller gaps
tolerance=GR_TOL         # overall tolerance for spacer components, default=0.5 mm
```
### Example with IKEA ALEX narrow drawer

An example use case to make a set of spacer components for a typical IKEA narrow ALEX drawer is as follows:

```python
spacers = GridfinityDrawerSpacer(INCHES(11.5), INCHES(20.5), verbose=True)
spacers.render_full_set(include_baseplate=True)
spacers.save_step_file("ikea_alex_full_set.step")
# make a half set for 3D printing
spacers.render_half_set()
spacers.save_stl_file("ikea_alex_half_set.stl")
```

<img src=./images/alexdrawer.png width=600>

## `GridfinityRuggedBox`

<img src=./images/rugged_box.png width=600>

The `GridfinityRuggedBox` class can be used to make gridfinity compatible rugged storage boxes. This box is based on the [superb design by Pred on Printables](https://www.printables.com/model/543553-gridfinity-storage-box-by-pred-now-parametric).

The **cq-gridfinity** derivative version of Pred's box is completely parameterized and generated completely with code in the `GridfinityRuggedBox` class.  This lets you render the most minimalist box configuration with no added features up to a full-featured box as shown below:

<img src=./images/min_rugged_box.png width=600>

The desired box size and features are specified with keyword arguments/attributes such as the ones illustrated below:

<img src=./images/rugged_box_features.png width=600>

A alternative "rib style" rugged box is also available.  This adds vertical rib stiffeners around the perimeter of the box and it is recommended to disable the side handles to allow for ribs to be generated on all sides.

<img src=./images/ribstylebox.png width=600>

Lastly, the lid baseplate can be substituted with a lid window which makes the contents of the box visible.  The window consists of a seperately prepared 1 mm thick transparent acrylic sheet cut to the required dimensions.  These dimensions can be queried with the `lid_window_size()` method or will be printed to the console when using the `ruggedbox` shell script.

<img src=./images/lid_window.png width=600>

After the lid has been printed the process to install the lid window is as follows:
1. Cut the lid window to the required dimensions.  It is recommended to chamfer or round off the leading edge corners with a file prior to insertion.
2. Slide the window into the lid starting from the back and along the tapered window groove slot around the inside perimeter of the lid.
3. The window should be inserted just past the retention slots for the hinges.
4. Secure the lid with 3x M2 screws along the back of the lid. Carefully drill 2.5 mm clearance holes into the window in situ prior to  installation of the screws. Alternatively, the lid can be secured with a few drops of super glue along the rear edge.
5. Install the lid hinges.  The hinges must be installed last since they act as a physical retainer along the back edge of the window.
  
The lid window should nominally be 1 mm thick; however if it necessary to use a different thickness material, the `window_th` attribute can be set.  It recommended to keep the window thickness in the range of 0.8 to 1.6 mm.

The rugged box can be rendered either as a complete assembly or as individual components.  This is useful for making individual asset files for 3D printing.  The  render methods include the `render_assembly()` method as shown above for the complete assembly, as well as individual render methods summarized below:

`render()` - renders just the main box body shell:

<img src=./images/rugged_box_shell.png width=600>

`render_lid()` - renders the lid:

<img src=./images/rugged_box_lid.png width=600>

`render_accessories()` - renders the accessory component elements as a group in the quantities required for the desired box:

<img src=./images/rugged_box_acc.png width=600>

Lastly, each individual component has an individual render method.

- `render_hinge()`
- `render_latch()`
- `render_label()`
- `render_handle()`
  
### Optional Keyword Arguments

```python
lid_height = 10            # lid height (should be multiple of 10 mm for stacking)
wall_vgrooves = True       # enable horizontal v-grooves to body shell
front_handle = True        # enable front handle
stackable = True           # add mating stackable features
side_clasps = True         # add extra side latching clasps
lid_baseplate = True       # enable top/lid baseplate
inside_baseplate = True    # enable interior baseplate
side_handles = True        # enable side handles to box
front_label = True         # enable front label panel
label_length = None        # length of front label panel, None=auto size
label_height = None        # height of front label panel, None=auto size
label_th = GR_LABEL_TH     # thickness of label panel, default=0.5 mm
back_feet = True           # add rear back feet matching hinges to allow the stand box vertically
hinge_width = GR_HINGE_SZ  # Size of hinge, default=32 mm
hinge_bolted = False       # printed or bolted hinge construction
box_color = cq.Color(0.25, 0.25, 0.25)    # colors for the assembly STEP file
lid_color = cq.Color(0.25, 0.5, 0.75)
handle_color = cq.Color(0.75, 0.5, 0.25)
latch_color = cq.Color(0.75, 0.5, 0.25)
hinge_color = cq.Color(0.75, 0.5, 0.25)
label_color = cq.Color(0.7, 0.7, 0.7)
```

## `GridfinityObject`

The `GridfinityObject` is the base class for `GridfinityBox`, `GridfinityBaseplate`, etc. It has several useful methods and attributes including:

### File export and naming

`obj.filename(self, prefix=None, path=None)` returns a filename string with descriptive attributes such as the object size and enabled features.

```python
box = GridfinityBox(3, 2, 5, holes=True)
box.filename()
# gf_box_3x2x5_holes
box.filename(prefix="MyBox")
# MyBox_3x2x5_holes
box.filename(path="./outputfiles")
# ./outputfiles/gf_box_3x2x5_holes
box2 = GridfinityBox(4, 3, 3, holes=True, length_div=2, width_div=1)
box2.filename()
# gf_box_4x3x3_holes_div2x1
```

```python
# Export object to STEP, STL, or SVG file
obj.save_step_file(filename=None, path=None, prefix=None)
obj.save_stl_file(filename=None, path=None, prefix=None)
obj.save_svg_file(filename=None, path=None, prefix=None)
```

The automatic filename assignment is aware of the last object generated with a particular class's render method.  Therefore, you can call any render method and then call any of the `save_step_file`, `save_stl_file`, `save_svg_file` methods and the filename will adapt to the last object rendered.  For example:

```python
b1 = GridfinityRuggedBox(5, 4, 6)
b1.render_accessories()
b1.save_step_file()
# saved as "gf_ruggedbox_5x4x6_acc_fr-hl_sd-hc_stack_lidbp.step"
b1.render_handle()
b1.save_stl_file()
# saved as "gf_ruggedbox_5x4x6_handle_fr-hl_sd-hc_stack_lidbp.stl"
b1.render_hinge()
b1.save_svg_file(path="./mystuff")
# saved as "./mystuff/gf_ruggedbox_5x4x6_hinge_fr-hl_sd-hc_stack_lidbp.svg"
b1.render_assembly()
b1.save_step_file()
# saved as "gf_ruggedbox_5x4x6_assembly_fr-hl_sd-hc_stack_lidbp.step"
```

### Useful properties

```obj.cq_obj``` returns a rendered CadQuery Workplane object  
```obj.length``` returns length in mm  
```obj.width``` returns width in mm  
```obj.height``` returns height in mm  
```obj.top_ref_height``` returns the height of the top surface of a solid box or the floor height of an empty box.  This can be useful for making custom boxes with cutouts since the reference height can be used to orient the cutting solid to the correct height.

# To-do

- add more example scripts
- improve documentation

# Releases

- v.0.1.0 - First release on PyPI
- v.0.1.1 - Fixed release
- v.0.2.0 - Added new "lite" style box
- v.0.2.1 - Added new unsupported magnet hole types
- v.0.2.2 - Added SVG export and integrated STL exporter
- v.0.2.3 - Updated to python build tools to make distribution
- v.0.3.0 - Added console generator scripts: `gridfinitybox` and `gridfinitybase`
- v.0.4.0 - Added `GridfinityRuggedBox` class and `ruggedbox` console script. Various other improvements.
- v.0.4.1 - Fixed docstring in `__init__.py`
- v.0.4.2 - Improved script automatic renaming
- v.0.4.3 - Fixed regression bug with using multilevel extrusion functions from cq-kit
- v.0.4.4 - IMPORTANT FIX: generated geometry breaks using CadQuery v.2.4+ due to changes in CadQuery's `extrude` method.  This version should work with any CQ version since it detects which CQ extrusion implementation is used at runtime.
- v.0.4.5 - IMPORTANT FIX: fixes error in v.0.4.4 for extrusion angle
- v.0.5.0 - Improved rugged box to make viable boxes down to 3U x 3U x 4U
- v.0.5.1 - Increased the resolution of the gridfinity extruded base profile
- v.0.5.2 - Adjusted geometry of box/bin floor/lip heights to exactly 7.00 mm intervals
- v.0.5.3 - Removed a potential namespace collision for computing the height of boxes
- v.0.5.4 - Optimized the geometry of the baseplate top height
- v.0.5.5 - Added underside bin clearance and variable wall thickness interior radiusing
- v.0.5.6 - Added adjustable magnet hole diameter to box. Prevent drawer spacers being rendered which fall below minimum size
- v.0.5.7 - Added scoops to lite-style boxes. Added new "rib style" rugged box. Added a lid window feature to the rugged box.

# References

- [Zach Freedman's YouTube Channel](https://www.youtube.com/c/ZackFreedman)
- [The video that started it all!](https://youtu.be/ra_9zU-mnl8?si=EOT1LFV65VZfiepi)
- [Gridfinity Documentation repo](https://github.com/Stu142/Gridfinity-Documentation)
- [Gridfinity Unofficial wiki](https://gridfinity.xyz)
- Catalogs
  - [gridfinity-catalog](https://github.com/jeffbarr/gridfinity-catalog)
  - [Master Collection on Printables](https://www.printables.com/model/242711-gridfinity-master-collection)
- Software/Tools
  - [Online Gridfinity Creator](https://gridfinity.bouwens.co)
  - [Gridfinity rebuilt OpenSCAD library](https://github.com/kennetek/gridfinity-rebuilt-openscad)
  - [Gridfinity Fusion360 generator plugin](https://github.com/Le0Michine/FusionGridfinityGenerator)
  - [FreeCAD Gridfinity Parametric Files (on Printables)](https://www.printables.com/@Stu142_524934/collections/969910)
  - [Gridfinity eco (low-cost Gridfinity resources)](https://github.com/jrymk/gridfinity-eco)
  - [Another CadQuery based Gridfinity script](https://github.com/kmeisthax/gridfinity-cadquery)
- Videos
  - [Zach Freedman's follow-up Jul 2022](https://youtu.be/Bd4NnHvTRAY?si=rvgb9geXnq83mhOv)
  - [Zach Freedman's follow-up Dec 2022](https://youtu.be/7FCwMq-rVsY?si=tdqAe8MthGjfWEbR)
  - [The Next Layer tips video](https://youtu.be/KtbKwAuwv9s?si=1hYPjOvqf8tb5NO9)

## Authors

**cq-gridfinity** was written by [Michael Gale](https://github.com/michaelgale)

