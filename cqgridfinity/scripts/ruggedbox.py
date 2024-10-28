#! /usr/bin/env python3
"""
command line script to make a rugged Gridfinity box
"""
import argparse

import cqgridfinity
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
The minimum box size is 3U x 3U x 4U.
"""

EPILOG = """
example usage:

  5 x 4 x 6 rugged box shell and lid saved to STL files:
  $ ruggedbox 5 4 6 --box --lid -f stl
"""


def save_asset(box, argsd, prefix=None):
    if argsd["output"] is not None:
        fn = argsd["output"]
        if box._obj_label is not None:
            for ext in (".stl", ".step", ".svg"):
                if fn.lower().endswith(ext):
                    fn = fn.replace(ext, "_%s%s" % (box._obj_label, ext))
                    break
    else:
        fn = box.filename(prefix=prefix)
    s = ["Component generated and saved as"]
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
        "+w",
        "--lidwindow",
        action="store_true",
        default=False,
        help="Add window slot to the lid",
    )
    parser.add_argument(
        "-w",
        "--nolidwindow",
        action="store_true",
        default=False,
        help="Do not add window slot to the lid",
    )
    parser.add_argument(
        "-wt",
        "--windowthickness",
        action="store",
        default=None,
        help="Thickness of lid windows (mm)",
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
        "-r",
        "--normalstyle",
        action="store_true",
        default=False,
        help="Make normal style box",
    )
    parser.add_argument(
        "+r",
        "--ribstyle",
        action="store_true",
        default=False,
        help="Make rib style box with exposed vertical ribs",
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
        help="Generate box",
    )
    parser.add_argument(
        "-gl",
        "--lid",
        action="store_true",
        default=False,
        help="Generate lid",
    )
    parser.add_argument(
        "-ga",
        "--acc",
        action="store_true",
        default=False,
        help="Generate accessory components",
    )
    parser.add_argument(
        "-gh",
        "--hinge",
        action="store_true",
        default=False,
        help="Generate hinge element",
    )
    parser.add_argument(
        "-ge",
        "--genlabel",
        action="store_true",
        default=False,
        help="Generate label panel insert",
    )
    parser.add_argument(
        "-gn",
        "--genhandle",
        action="store_true",
        default=False,
        help="Generate front handle",
    )
    parser.add_argument(
        "-gt",
        "--genlatch",
        action="store_true",
        default=False,
        help="Generate latch component",
    )
    parser.add_argument(
        "-gw",
        "--genwindow",
        action="store_true",
        default=False,
        help="Generate lid window component",
    )

    args = parser.parse_args()
    argsd = vars(args)
    box = GridfinityRuggedBox(
        length_u=int(argsd["length"]),
        width_u=int(argsd["width"]),
        height_u=int(argsd["height"]),
    )
    if argsd["lidbaseplate"]:
        box.lid_baseplate = True
    if argsd["nolidbaseplate"]:
        box.lid_baseplate = False
    if argsd["lidwindow"]:
        box.lid_window = True
    if argsd["nolidwindow"]:
        box.lid_window = False
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
    if argsd["ribstyle"]:
        box.rib_style = True
    if argsd["normalstyle"]:
        box.rib_style = False
    if argsd["windowthickness"] is not None:
        box.window_th = float(argsd["windowthickness"])

    print(title)
    print("Version: %s" % (cqgridfinity.__version__))
    print(
        "Gridfinity rugged box: %dU x %dU x %dU"
        % (
            box.length_u,
            box.width_u,
            box.height_u,
        )
    )
    print(
        "  Exterior dim: %.1f mm x %.1f mm x %.1f mm"
        % (
            box.box_length + 2 * (GR_RBOX_CWALL - GR_RBOX_WALL),
            box.box_width + 2 * (GR_RBOX_CWALL - GR_RBOX_WALL),
            box.box_height + box.lid_height,
        )
    )
    print(
        "  Interior dim: %.1f mm x %.1f mm x %.1f mm"
        % (
            box.length,
            box.width,
            box.height,
        )
    )
    print("  Internal volume: %.3f L" % (box.length * box.width * box.height / 1e6))
    if box.lid_window:
        print(
            "  Lid window dimensions: %.2f x %.2f mm, %.2f mm thickness"
            % (*box.lid_window_size(), box.window_th)
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
        "rib_style",
    ]
    for opt in opts:
        opt_name = opt.replace("_", " ").title()
        val = "Y" if box.__dict__[opt] else "N"
        print("  %-19s: %s" % (opt_name, val))
    print("  %-19s: %s" % ("Lid Window", "Y" if box.lid_window else "N"))

    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = box.filename()
    g = False
    if argsd["box"]:
        print("Rendering box...")
        box.render()
        save_asset(box, argsd)
        g = True
    if argsd["lid"]:
        print("Rendering lid...")
        box.render_lid()
        save_asset(box, argsd)
        g = True
    if argsd["acc"]:
        print("Rendering accessory components...")
        r = box.render_accessories()
        save_asset(box, argsd)
        g = True
    if argsd["hinge"]:
        print("Rendering hinge components...")
        r = box.render_hinge()
        save_asset(box, argsd)
        g = True
    if argsd["genlabel"]:
        print("Rendering label panel...")
        r = box.render_label()
        save_asset(box, argsd)
        g = True
    if argsd["genhandle"]:
        print("Rendering front handle...")
        r = box.render_handle()
        save_asset(box, argsd)
        g = True
    if argsd["genlatch"]:
        print("Rendering latch component...")
        r = box.render_latch()
        save_asset(box, argsd)
        g = True
    if argsd["genwindow"]:
        print(
            "Rendering lid window (%.2f x %.2f mm, %.2f mm thickness)..."
            % (*box.lid_window_size(), box.window_th)
        )
        r = box.render_lid_window()
        save_asset(box, argsd)
        g = True
    if not g:
        print("Rendering full assembly...")
        a = box.render_assembly()
        if argsd["output"] is not None:
            fn = argsd["output"]
        else:
            fn = box.filename()
        if not fn.endswith(".step"):
            fn = fn + ".step"
        a.save(fn)


if __name__ == "__main__":
    main()
