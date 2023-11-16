#! /usr/bin/env python3
"""
command line script to make a Gridfinity baseplate
"""
import argparse

from cqgridfinity import *

title = """
  _____      _     _  __ _       _ _           ____
 / ____|    (_)   | |/ _(_)     (_) |         |  _ \\
| |  __ _ __ _  __| | |_ _ _ __  _| |_ _   _  | |_) | __ _ ___  ___
| | |_ | '__| |/ _` |  _| | '_ \\| | __| | | | |  _ < / _` / __|/ _ \\
| |__| | |  | | (_| | | | | | | | | |_| |_| | | |_) | (_| \\__ \\  __/
 \\_____|_|  |_|\\__,_|_| |_|_| |_|_|\\__|\\__, | |____/ \\__,_|___/\\___|
                                        __/ |
                                       |___/
"""

DESC = """
Make a customized/parameterized Gridfinity compatible simple baseplate.
"""

EPILOG = """
example usage:

  6 x 3 baseplate to default STL file:
  $ gridfinitybase 6 3 -f stl
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
    base = GridfinityBaseplate(
        length_u=int(argsd["length"]), width_u=int(argsd["width"]),
    )
    print(title)
    print(
        "Gridfinity baseplate: %dU x %dU (%.1f mm x %.1f mm)"
        % (base.length_u, base.width_u, base.length, base.width,)
    )
    if argsd["output"] is not None:
        fn = argsd["output"]
    else:
        fn = base.filename()
    s = ["\nBaseplate generated and saved as"]
    if argsd["format"].lower() == "stl" or fn.lower().endswith(".stl"):
        if not fn.endswith(".stl"):
            fn = fn + ".stl"
        base.save_stl_file(filename=argsd["output"])
        s.append("%s in STL format" % (fn))
    elif argsd["format"].lower() == "svg" or fn.lower().endswith(".svg"):
        if not fn.endswith(".svg"):
            fn = fn + ".svg"
        base.save_svg_file(filename=argsd["output"])
        s.append("%s in SVG format" % (fn))
    else:
        if not fn.endswith(".step"):
            fn = fn + ".step"
        base.save_step_file(filename=argsd["output"])
        s.append("%s in STEP format" % (fn))
    print(" ".join(s))


if __name__ == "__main__":
    main()
