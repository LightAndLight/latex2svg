syscmd(`truncate --size 0 output.txt')dnl
define(`equation_count', `0')dnl
define(`allocate_equation', `define(`equation_count', incr(equation_count))equation_count')dnl
define(`equation_texs', `')dnl
define(`equation_dvis', `')dnl
define(`equation_svgs_in', `')dnl
define(`equation_svgs_out', `')dnl
define(`append', `define(`$1', $1` $2')')dnl
dnl
define(`temp_dir', esyscmd(`mktemp --tmpdir -d "latex2svg-XXXXXX" | tr -d "\n"'))dnl
dnl
define(
  `m4_eq',
  `dnl
define(`equation_number', allocate_equation)dnl
define(`equation_name', `equation-'equation_number)dnl
syscmd(`cat <<EOF > 'temp_dir`/'equation_name`.tex
\documentclass[margin=0.5pt]{standalone}
\usepackage{amsmath,amssymb}
\begin{document}
\($1\)
\end{document}
EOF')dnl
append(`equation_texs', temp_dir`/'equation_name`.tex')dnl
append(`equation_dvis', temp_dir`/'equation_name`.dvi')dnl
append(`equation_svgs_in', temp_dir`/'equation_name`.svg')dnl
append(`equation_svgs_out', `./'equation_name`.svg')dnl
<img src="'equation_name`.svg" alt="equation content here" role="img" />dnl
')dnl
define(
  `m4_generate_equation_svgs',
  `dnl
syscmd(`/usr/bin/env time parallel latex -output-directory='temp_dir` --'equation_texs` >> output.txt 2>&1')dnl
syscmd(`/usr/bin/env time parallel dvisvgm --no-fonts --exact --scale=2 --bbox=papersize -o 'temp_dir`/%f.svg --'equation_dvis` >> output.txt 2>&1')dnl
syscmd(`/usr/bin/env time svgo -i'equation_svgs_in` -o'equation_svgs_out` >> output.txt 2>&1')dnl
')dnl
