r"""
.. _ref_ex_simple:
Simple Example
--------------
Calculate section properties of a circle.
The following example calculates the geometric, warping and plastic properties
of a 50 mm diameter circle. The circle is discretised with 64 points and a mesh
size of 2.5 mm\ :sup:`2`.
The geometry and mesh are plotted, and the mesh information printed to the terminal
before the analysis is carried out. Detailed time information is printed to the
terminal during the cross-section analysis stage. Once the analysis is complete,
the cross-section properties are printed to the terminal. The centroidal
axis second moments of area and torsion constant are saved to variables and it
is shown that, for a circle, the torsion constant is equal to the sum of the
second moments of area.
"""

# sphinx_gallery_thumbnail_number = 1

import sectionproperties.pre.library.primitive_sections as sections
from sectionproperties.analysis.section import Section

from rich.console import Console
from rich.text import Text

console = Console()


def main():
    # %%
    # Create a 50 diameter circle discretised by 64 points
    geometry = sections.circular_sections(d=50, n=64)

    # %%
    # Create a mesh with a mesh size of 2.5 and display information about it
    geometry.create_mesh(mesh_sizes=[2.5])

    section = Section(geometry)


try:
    main()
except Exception as err:
    for arg in err.args:
        err_arg = Text("\n" + arg)
        err_arg.stylize("bold red")
        console.print(err_arg)
