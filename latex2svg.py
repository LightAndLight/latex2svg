import os
import subprocess
import sys
import tempfile
import re


def latex_to_svg(math_string, output_file):
    latex_document = (
        "\\documentclass[margin=0.5pt]{standalone}"
        "\\usepackage{amsmath,amssymb}"
        "\\begin{document}"
        f"\\({math_string}\\)"
        "\\end{document}"
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        dvi_file = os.path.join(temp_dir, "texput.dvi")
        svg_file = os.path.join(temp_dir, "texput.svg")

        latex_result = subprocess.run(
            ["latex", "-output-directory", temp_dir],
            input=latex_document,
            capture_output=True,
            text=True,
        )
        if latex_result.returncode != 0:
            print(latex_document)
            print(latex_result.stdout)
            print(latex_result.stderr, file=sys.stderr)
            sys.exit(1)

        svg_result = subprocess.run(
            ["dvisvgm", "--no-fonts", "--exact", "--scale=2", "--bbox=papersize", "-o", svg_file, dvi_file],
            capture_output=True,
            text=True,
        )
        if svg_result.returncode != 0:
            print(svg_result.stdout)
            print(svg_result.stderr, file=sys.stderr)
            sys.exit(1)

        min_svg_result = subprocess.run(
            ["svgo", "-i", svg_file, output_file],
            capture_output=True,
            text=True,
        )
        if min_svg_result.returncode != 0:
            print(min_svg_result.stdout)
            print(min_svg_result.stderr, file=sys.stderr)
            sys.exit(1)
        
        with open(output_file, 'r') as output_file:
            dimensions = re.search(r"width=['\"]([\d.]+)['\"] height=['\"]([\d.]+)['\"]", output_file.read())
            if dimensions:
                width, height = float(dimensions.group(1)), float(dimensions.group(2))
                print(f"Width: {width} pixels, Height: {height} pixels")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert LaTeX math string to SVG')
    parser.add_argument('latex_math_string', type=str, help='LaTeX math string to be converted')
    parser.add_argument('output_svg_file', type=str, help='output SVG file name')

    args = parser.parse_args()

    latex_to_svg(args.latex_math_string, args.output_svg_file)

