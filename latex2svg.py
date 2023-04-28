import os
import subprocess
import sys
import tempfile

def latex_to_svg(math_string, output_file):
    latex_document = f"""
\\documentclass[preview, border={{0pt 0pt 0pt 0pt}}]{{standalone}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\begin{{document}}
\\({math_string}\\)
\\end{{document}}
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file_path = os.path.join(temp_dir, "texput.tex")
        dvi_file_path = os.path.join(temp_dir, "texput.dvi")
        svg_file_path = os.path.join(temp_dir, "texput.svg")

        with open(tex_file_path, "w") as tex_file:
            tex_file.write(latex_document)
        
        latex_result = subprocess.run(
            ["latex", "-output-directory", temp_dir],
            input=latex_document,
            capture_output=True,
            text=True,
        )
        if latex_result.returncode != 0:
            print(latex_result.stdout)
            print(latex_result.stderr, file=sys.stderr)
            sys.exit(1)
        
        svg_result = subprocess.run(
            ["dvisvgm", "--no-fonts", "--exact", "--scale=2", "-o", svg_file_path, dvi_file_path],
            capture_output=True,
            text=True,
        )
        if svg_result.returncode != 0:
            print(svg_result.stdout)
            print(svg_result.stderr, file=sys.stderr)
            sys.exit(1)
        
        with open(svg_file_path, "r") as svg_file:
            svg_content = svg_file.read()

        with open(output_file, "w") as output_svg_file:
            output_svg_file.write(svg_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python latex_to_svg.py <latex_math_string> <output_svg_file>")
        sys.exit(1)

    math_string = sys.argv[1]
    output_file = sys.argv[2]

    latex_to_svg(math_string, output_file)
