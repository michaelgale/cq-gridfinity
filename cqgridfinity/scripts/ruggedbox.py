#! /usr/bin/env python3
"""
command line script to make a rugged Gridfinity box
"""
import argparse

from cqgridfinity import *

title = """
 ____                             _ ____
|  _ \ _   _  __ _  __ _  ___  __| | __ )  _____  __
| |_) | | | |/ _` |/ _` |/ _ \\/ _` |  _ \\ / _ \\ \\/ /
|  _ <| |_| | (_| | (_| |  __/ (_| | |_) | (_) >  <
|_| \\_\\\\__,_|\\__, |\\__, |\\___|\\__,_|____/ \\___/_/\\_\\
             |___/ |___/
"""

DESC = """
Make a customized/parameterized Gridfinity compatible rugged box enclosure.
"""

EPILOG = """
example usage:

  5 x 4 x 6 rugged box saved to STL file:
  $ ruggedbox 5 4 6 -f stl
"""


def save_asset(box, argsd, prefix=None):
    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = box.filename(prefix=prefix)
    s = ["\nBox generated and saved as"]
    if argsd["format"].lower() == "stl" or fn.lower().endswith(".stl"):
        if not fn.endswith(".stl"):
            fn = fn + ".stl"
        box.save_stl_file(filename=argsd["output"], prefix=prefix)
        s.append("%s in STL format" % (fn))
    elif argsd["format"].lower() == "svg" or fn.lower().endswith(".svg"):
        if not fn.endswith(".svg"):
            fn = fn + ".svg"
        box.save_svg_file(filename=argsd["output"], prefix=prefix)
        s.append("%s in SVG format" % (fn))
    else:
        if not fn.endswith(".step"):
            fn = fn + ".step"
        box.save_step_file(filename=argsd["output"], prefix=prefix)
        s.append("%s in STEP format" % (fn))
    print(" ".join(s))


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
        "+l",
        "--label",
        action="store_true",
        default=False,
        help="Add label window across the front wall",
    )
    parser.add_argument(
        "-l",
        "--nolabel",
        action="store_true",
        default=False,
        help="Remove label window across the front wall",
    )
    parser.add_argument(
        "+p",
        "--lidbaseplate",
        action="store_true",
        default=False,
        help="Add baseplate to top of the lid",
    )
    parser.add_argument(
        "-p",
        "--nolidbaseplate",
        action="store_true",
        default=False,
        help="Smooth/plain lid",
    )
    parser.add_argument(
        "+a",
        "--handle",
        action="store_true",
        default=False,
        help="Add front handle",
    )
    parser.add_argument(
        "-a",
        "--nohandle",
        action="store_true",
        default=False,
        help="No front handle",
    )
    parser.add_argument(
        "+c",
        "--clasps",
        action="store_true",
        default=False,
        help="Add clasps to the left and right side walls",
    )
    parser.add_argument(
        "-c",
        "--noclasps",
        action="store_true",
        default=False,
        help="No clasps on the left and right side walls",
    )
    parser.add_argument(
        "+s",
        "--stackable",
        action="store_true",
        default=False,
        help="Add stackable mating features to top and bottom",
    )
    parser.add_argument(
        "-s",
        "--notstackable",
        action="store_true",
        default=False,
        help="Non-stackable box",
    )
    parser.add_argument(
        "+v",
        "--veegroove",
        action="store_true",
        default=False,
        help="Add v-cut grooves to side walls",
    )
    parser.add_argument(
        "-v",
        "--noveegroove",
        action="store_true",
        default=False,
        help="No v-cut grooves (plain) side walls",
    )
    parser.add_argument(
        "+e",
        "--sidehandle",
        action="store_true",
        default=False,
        help="Add handles to side walls",
    )
    parser.add_argument(
        "-e",
        "--nosidehandle",
        action="store_true",
        default=False,
        help="No handles on side walls",
    )
    parser.add_argument(
        "+b",
        "--backfeet",
        action="store_true",
        default=False,
        help="Add standing feet to back wall",
    )
    parser.add_argument(
        "-b",
        "--nobackfeet",
        action="store_true",
        default=False,
        help="No standing feet added to back wall",
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
    parser.add_argument(
        "-gb",
        "--box",
        action="store_true",
        default=False,
        help="Generate box only",
    )
    parser.add_argument(
        "-gl",
        "--lid",
        action="store_true",
        default=False,
        help="Generate lid only",
    )
    parser.add_argument(
        "-ga",
        "--acc",
        action="store_true",
        default=False,
        help="Generate accessory components only",
    )
    args = parser.parse_args()
    argsd = vars(args)
    box = GridfinityRuggedBox(
        length_u=int(argsd["length"]),
        width_u=int(argsd["width"]),
        height_u=int(argsd["height"]),
    )
    if argsd["lidbaseplate"]:
        box.inside_baseplate = True
    if argsd["nolidbaseplate"]:
        box.inside_baseplate = False
    if argsd["handle"]:
        box.front_handle = True
    if argsd["nohandle"]:
        box.front_handle = False
    if argsd["label"]:
        box.front_label = True
    if argsd["nolabel"]:
        box.front_label = False
    if argsd["clasps"]:
        box.side_clasps = True
    if argsd["noclasps"]:
        box.side_clasps = False
    if argsd["stackable"]:
        box.stackable = True
    if argsd["notstackable"]:
        box.stackable = False
    if argsd["veegroove"]:
        box.wall_vgrooves = True
    if argsd["noveegroove"]:
        box.wall_vgrooves = False
    if argsd["sidehandle"]:
        box.side_handles = True
    if argsd["nosidehandle"]:
        box.side_handles = False
    if argsd["backfeet"]:
        box.back_feet = True
    if argsd["nobackfeet"]:
        box.back_feet = False

    print(title)
    print(
        "Gridfinity rugged box: %dU x %dU x %dU (%.1f mm x %.1f mm x %.1f mm)"
        % (
            box.length_u,
            box.width_u,
            box.height_u,
            box.length,
            box.width,
            box.height,
        )
    )
    s = []
    opts = [
        "wall_vgrooves",
        "front_handle",
        "stackable",
        "side_clasps",
        "lid_baseplate",
        "inside_baseplate",
        "side_handles",
        "front_label",
        "back_feet",
    ]
    for opt in opts:
        opt_name = opt.replace("_", " ").title()
        val = "Y" if box.__dict__[opt] else "N"
        print("  %-19s: %s" % (opt_name, val))

    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = box.filename()
    g = False
    if argsd["box"]:
        print("Rendering box...")
        r = box.render()
        save_asset(box, argsd)
        g = True
    if argsd["lid"]:
        print("Rendering lid...")
        r = box.render_lid()
        save_asset(box, argsd, prefix="lid_")
        g = True
    if argsd["acc"]:
        print("Rendering accessory components...")
        r = box.render_accessories()
        save_asset(box, argsd, prefix="acc_")
        g = True
    if not g:
        print("Rendering full assembly...")
        a = box.render_assembly()
        if not fn.endswith(".step"):
            fn = fn + ".step"
        a.save(fn)


if __name__ == "__main__":
    main()
