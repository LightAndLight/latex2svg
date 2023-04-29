# `latex2svg`

My blog currently uses [MathJax](https://www.mathjax.org/) to display equations, and I realised that's a little bit silly
considering it's a statically generated site. What if I could render the equations during site generation, instead having
each viewer's browser do it? Here's where I play around with ideas to that effect.

* `latex2svg.py` - a Python script that renders an equation as an SVG
* `latex2svg.m4` - a GNU M4 script for converting all equations in a document to SVGs and including them via `<img>` tags
