#! /usr/bin/env python3
"""
command line script to make a Gridfinity box
"""
import argparse

import cqgridfinity
from cqgridfinity import *

title = """
  _____      _     _  __ _       _ _           ____
 / ____|    (_)   | |/ _(_)     (_) |         |  _ \\
| |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |_) | _____  __
| | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | |  _ < / _ \\ \\/ /
| |__| | |  | | (_| | | | | | | | | |_| |_| | | |_) | (_) >  <
 \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, | |____/ \\___/_/\\_\\
                                        __/ |
                                       |___/
"""

DESC = """
Make a customized/parameterized Gridfinity compatible box with many optional features.
"""

EPILOG = """
example usages:

  2x3x5 box with magnet holes saved to STL file with default filename:
  $ gridfinitybox 2 3 5 -m -f stl

  1x3x4 box with scoops, label strip, 3 internal partitions and specified name:
  $ gridfinitybox 1 3 4 -s -l -ld 3 -o MyBox.step

  Solid 3x3x3 box with 50% fill, unsupported magnet holes and no top lip:
  $ gridfinitybox 3 3 3 -d -r 0.5 -u -n
 
  Lite style box 3x2x3 with label strip, partitions, output to default SVG file:
  $ gridfinitybox 3 2 3 -e -l -ld 2 -f svg
"""


def main():
    parser = argparse.ArgumentParser(
        description=DESC,
        epilog=EPILOG,
        prefix_chars="-+",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "length", metavar="length", type=str, help="Box length in U (1U = 42 mm)"
    )
    parser.add_argument(
        "width", metavar="width", type=str, help="Box width in U (1U = 42 mm)"
    )
    parser.add_argument(
        "height", metavar="height", type=str, help="Box height in U (1U = 7 mm)"
    )
    parser.add_argument(
        "-m",
        "--magnetholes",
        action="store_true",
        default=False,
        help="Add bottom magnet/mounting holes",
    )
    parser.add_argument(
        "-u",
        "--unsupported",
        action="store_true",
        default=False,
        help="Add bottom magnet holes with 3D printer friendly strips without support",
    )
    parser.add_argument(
        "-n",
        "--nolip",
        action="store_true",
        default=False,
        help="Do not add mating lip to the top perimeter",
    )
    parser.add_argument(
        "-s",
        "--scoops",
        action="store_true",
        default=False,
        help="Add finger scoops against each length-wise back wall",
    )
    parser.add_argument(
        "-l",
        "--labels",
        action="store_true",
        default=False,
        help="Add label strips against each length-wise front wall",
    )
    parser.add_argument(
        "-e",
        "--ecolite",
        action="store_true",
        default=False,
        help="Make economy / lite style box with no elevated floor",
    )
    parser.add_argument(
        "-d",
        "--solid",
        action="store_true",
        default=False,
        help="Make solid (filled) box for customized storage",
    )
    parser.add_argument(
        "-r",
        "--ratio",
        action="store",
        default=1.0,
        help="Solid box fill ratio 0.0 = minimum, 1.0 = full height",
    )
    parser.add_argument(
        "-ld",
        "--lengthdiv",
        action="store",
        default=0,
        help="Split box length-wise with specified number of divider walls",
    )
    parser.add_argument(
        "-wd",
        "--widthdiv",
        action="store",
        default=0,
        help="Split box width-wise with specified number of divider walls",
    )
    parser.add_argument(
        "-wt",
        "--wall",
        action="store",
        default=1.0,
        help="Wall thickness (default=1 mm)",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="step",
        help="Output file format (STEP, STL, SVG) default=STEP",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output filename (inferred output file format with extension)",
    )
    args = parser.parse_args()
    argsd = vars(args)
    solid_ratio = float(argsd["ratio"])
    length_div = int(argsd["lengthdiv"])
    width_div = int(argsd["widthdiv"])
    wall = float(argsd["wall"])
    box = GridfinityBox(
        length_u=int(argsd["length"]),
        width_u=int(argsd["width"]),
        height_u=int(argsd["height"]),
        holes=argsd["magnetholes"] or argsd["unsupported"],
        unsupported_holes=argsd["unsupported"],
        no_lip=argsd["nolip"],
        scoops=argsd["scoops"],
        labels=argsd["labels"],
        lite_style=argsd["ecolite"],
        solid=argsd["solid"],
        solid_ratio=solid_ratio,
        length_div=length_div,
        width_div=width_div,
        wall_th=wall,
    )
    if argsd["ecolite"]:
        bs = "lite "
    elif argsd["solid"]:
        bs = "solid "
    else:
        bs = ""
    print(title)
    print("Version: %s" % (cqgridfinity.__version__))

    print(
        "Gridfinity %sbox: %dU x %dU x %dU (%.1f mm x %.1f mm x %.1f mm), %.2f mm walls"
        % (
            bs,
            box.length_u,
            box.width_u,
            box.height_u,
            box.length,
            box.width,
            box.height,
            box.wall_th,
        )
    )
    if argsd["solid"]:
        print(
            "  solid height ratio: %.2f  top height: %.2f mm / %.2f mm"
            % (solid_ratio, box.top_ref_height, box.max_height + GR_BOT_H)
        )
    s = []
    if argsd["unsupported"]:
        s.append("holes with no support")
    elif argsd["magnetholes"]:
        s.append("holes")
    if argsd["nolip"]:
        s.append("no lip")
    if argsd["scoops"]:
        s.append("scoops")
    if argsd["labels"]:
        s.append("label strips")
    if length_div:
        s.append("%d length-wise walls" % (length_div))
    if width_div:
        s.append("%d width-wise walls" % (width_div))
    if len(s):
        print("  with options: %s" % (", ".join(s)))
    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = box.filename()
    s = ["\nBox generated and saved as"]
    if argsd["format"].lower() == "stl" or fn.lower().endswith(".stl"):
        if not fn.endswith(".stl"):
            fn = fn + ".stl"
        box.save_stl_file(filename=argsd["output"])
        s.append("%s in STL format" % (fn))
    elif argsd["format"].lower() == "svg" or fn.lower().endswith(".svg"):
        if not fn.endswith(".svg"):
            fn = fn + ".svg"
        box.save_svg_file(filename=argsd["output"])
        s.append("%s in SVG format" % (fn))
    else:
        if not fn.endswith(".step"):
            fn = fn + ".step"
        box.save_step_file(filename=argsd["output"])
        s.append("%s in STEP format" % (fn))
    print(" ".join(s))


if __name__ == "__main__":
    main()
