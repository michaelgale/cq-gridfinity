<!-- <img src=./images/logo.png width=320> -->
![cq-gridfinity Logo](./images/logo.png)

# cq-gridfinity

![python version](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=blue&style=flat&logo=python)
![https://github.com/CadQuery/cadquery](https://img.shields.io/static/v1?label=dependencies&message=CadQuery%202.0%2B&color=blue&style=flat)
![https://github.com/michaelgale/cq-kit/blob/master/LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>


This repository contains a python library to build [Gridfinity](https://gridfinity.xyz) boxes, baseplates, and other objects based on the [CadQuery](https://github.com/CadQuery/cadquery) python library.  The Gridfinity system was created by [Zach Freedman](https://www.youtube.com/c/ZackFreedman) as a versatile system of modular organization and storage modules.  A vibrant community of user contributed modules and utilities has grown around the Gridfinity system.  This repository contains python classes to create gridfinity compatible parameterized components such as baseplates and boxes.

## Installation

**cq-gridfinity** has the following installation dependencies:
- [CadQuery](https://github.com/CadQuery/cadquery)
- [cq-kit](https://github.com/michaelgale/cq-kit)

Assuming these dependencie are installed, you can install **cq-gridfinity** using a [PyPI package](https://pypi.org/project/cqgridfinity/) as follows:

```bash
$ pip install cqgridfinity
```

The **cq-gridfinity** package can be installed directly from the source code:

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
    import cadquery as cq
    from cqgridfinity import *

    # make a simple box
    box = GridfinityBox(3, 2, 5, holes=True, no_lip=False, scoops=True, labels=True)
    fn = box.filename() + ".stl"
    exporters.export(r, fn, tolerance=1e-2, angularTolerance=0.15)
    # Output a STL file of box named:
    #   gf_box_3x2x5_holes_scoops_labels.svg
```

## Baseplates (`GridfinityBaseplate`)

Gridfinity baseplates can be made with the `GridfinityBaseplate` class.  The baseplate style is the basic style initially proposed by Zach Freedman.  Therefore, it does not have magnet or mounting holes.  An example usage is as follows:

```python
   # Create 4 x 3 baseplate
   baseplate = GridfinityBaseplate(4, 3)
   baseplate.save_step_file()
```

## Boxes (`GridfinityBox`)

Gridfinity boxes with many optional features can be created with the `GridfinityBox` class.  As a minimum, this class is initialized with basic 3D unit dimensions for length, width, and height.  The length and width are multiples of 42 mm Gridfinity intervals and height represents multiples of 7 mm.

### Simple Box

```python
    # Create a simple 3 x 2 box, 5U high
    box = GridfinityBox(3, 2, 5)
    box.save_step_file()
    # Output a STEP file of box named:
    #   gf_box_3x2x5.step
``` 
<img src=./images/basic_box.png width=400>

### Magnet Holes

```python
    # add magnet holes to the box
    box = GridfinityBox(3, 2, 5, holes=True)
    box.save_step_file()
    # gf_box_3x2x5_holes.step
```
<img src=./images/box_holes.png width=400>

### Simple Box with No Top Lip

```python
    # remove top mounting lip
    box = GridfinityBox(3, 2, 5, no_lip=True)
    box.save_step_file()
    # gf_box_3x2x5_basic.step
```
<img src=./images/box_nolip.png width=400>

### Scoops and Labels

```python
    # add finger scoops and label top flange
    box = GridfinityBox(3, 2, 5, scoops=True, labels=True)
    box.save_step_file()
    # gf_box_3x2x5_scoops_labels.step
```
<img src=./images/box_options.png width=400>

### Dividing Walls

```python
    # add dividing walls
    box = GridfinityBox(3, 2, 5, length_div=2, width_div=1)
    box.save_step_file()
    # gf_box_3x2x5_div2x1.step
```
<img src=./images/box_div.png width=400>

### Solid Box

```python
    # make a partially solid box
    box = GridfinityBox(3, 2, 5, solid=True, solid_ratio=0.7)
    box.save_step_file()
    # gf_box_3x2x5_solid.step
```
<img src=./images/box_solid.png width=400>

## Drawer Spacer (`GridfinityDrawerSpacer`)

The `GridfinityDrawerSpacer` class can be used to make spacer components to fit a drawer with any arbitrary dimensions.  With a specified width and depth of the drawer, the best fit of integer gridfinity baseplate units is computed.  Rarely, integer multiples of 42 mm gridfinity baseplates fit perfectly inside a drawer; therefore, spacers are required to secure the baseplate snuggly inside the drawer.  Spacers consist of 4x identical corner sections, 2x spacers for the left and right sides and 2x spacers for the front and back edges.

```python
    spacer = GridfinityDrawerSpacer()
    spacer.best_fit_to_dim(582, 481, verbose=True)
    # Best fit for 582.00 x 481.00 mm is 13U x 11U
    # with 18.00 mm margin each side and 9.50 mm margin front and back
    # Corner spacers     : 4U wide x 3U deep
    # Front/back spacers : 5U wide x 9.25 mm +0.25 mm tolerance
    # Left/right spacers : 5U deep x 17.75 mm +0.25 mm tolerance
```

A full set of components (optionally including a full baseplate) can be rendered with the `render_full_set()` method.  This method is mostly used to verify the fit and placement of the spacers.

<img src=./images/full_set.png width=400>


Normally, the `render_half_set()` method used to render half of the components compactly arranged conveniently for 3D printing.  This set can be printed twice to make a full set for a single drawer.

<img src=./images/half_set.png width=400>

## Releases

- v.0.1.0 - First release on PyPI

## Authors

**cq-gridfinity** was written by [Michael Gale](https://github.com/michaelgale)

