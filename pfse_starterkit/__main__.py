"""
A module to designed to perform package installations, and verification of install,
in preparation for the StructuralPython "Python for Structural Engineers" ("pfse")
course.
"""
__version__ = "0.0.1"

import importlib.util
import importlib
import pathlib
import platform
import psutil
import subprocess
import time
import warnings
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, track
from rich.markdown import Markdown
from rich.text import Text

console = Console()


def check_installs():
    """
    Runs various mini-scripts to validate that certain packages
    are installed correctly. Offers suggestions for remediation if not.
    """
    header = Markdown("# Python for Structural Engineers ('PfSE')")
    addl_installs = Markdown("## Installing additional package for Linux...")
    addl_installs.style = "yellow"
    console.print(header)
    console.print(addl_installs)

    install_extra()
    validating = Markdown("## Validating installed packages...")
    validating.style = "yellow"
    console.print(validating)

    funcs = [
        check_streamlit,
        check_vtk,
        check_numpy,
        check_shapely,
        check_sectionproperties,
        check_openpyxl,
    ]
    msgs = []
    for func in track(funcs):
        msg = func()
        if msg is not None:
            msgs.append(msg)
        time.sleep(0.2)

    if len(msgs) != 0:
        for msg in msgs:
            if msg is not None:
                console.print(msg)
        notify = Markdown("# Inconsistencies encoutered")
        notify.style = "red"
        instructions = Markdown(
            "### Please use Ctrl-Shift-C to copy the above error messages and email them to connor@structuralpython.com"
        )
        instructions.style = "red"
        console.print(notify)
        console.print(instructions)
    else:
        verified = Markdown("# PfSE installation seems ok")
        verified.style = "green"
        close_windows = Markdown(
            "## You can now close any windows that have opened as a result of the test."
        )
        close_windows.style = "green"
        console.print(verified)
        console.print(close_windows)


def check_streamlit():
    st_file = pathlib.Path(__file__).parent / "streamlit_test.py"
    try:
        proc = subprocess.Popen(
            ["streamlit", "run", str(st_file)], stdout=subprocess.PIPE
        )
        # proc.communicate("\n")
        time.sleep(4)
        proc.kill()

    except ValueError:
        err_msg = Text("Streamlit did not run properly.")
        err_msg.stylize("bold magenta")
        return err_msg


def check_vtk():
    try:
        import vtkmodules.vtkInteractionStyle

        # noinspection PyUnresolvedReferences
        import vtkmodules.vtkRenderingOpenGL2
        from vtkmodules.vtkCommonColor import vtkNamedColors
        from vtkmodules.vtkFiltersSources import vtkCylinderSource
        from vtkmodules.vtkRenderingCore import (
            vtkActor,
            vtkPolyDataMapper,
            vtkRenderWindow,
            vtkRenderWindowInteractor,
            vtkRenderer,
        )

        colors = vtkNamedColors()
        # Set the background color.
        bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
        colors.SetColor("BkgColor", *bkg)

        # This creates a polygonal cylinder model with eight circumferential
        # facets.
        cylinder = vtkCylinderSource()
        cylinder.SetResolution(8)

        # The mapper is responsible for pushing the geometry into the graphics
        # library. It may also do color mapping, if scalars or other
        # attributes are defined.
        cylinderMapper = vtkPolyDataMapper()
        cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

        # The actor is a grouping mechanism: besides the geometry (mapper), it
        # also has a property, transformation matrix, and/or texture map.
        # Here we set its color and rotate it -22.5 degrees.
        cylinderActor = vtkActor()
        cylinderActor.SetMapper(cylinderMapper)
        cylinderActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))
        cylinderActor.RotateX(30.0)
        cylinderActor.RotateY(-45.0)

        # Create the graphics structure. The renderer renders into the render
        # window. The render window interactor captures mouse events and will
        # perform appropriate camera or actor manipulation depending on the
        # nature of the events.
        ren = vtkRenderer()
        renWin = vtkRenderWindow()
        renWin.AddRenderer(ren)
        iren = vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # Add the actors to the renderer, set the background and size
        ren.AddActor(cylinderActor)
        ren.SetBackground(colors.GetColor3d("BkgColor"))
        renWin.SetSize(300, 300)
        renWin.SetWindowName("CylinderExample")

        # This allows the interactor to initalize itself. It has to be
        # called before an event loop.
        iren.Initialize()

        # We'll zoom in a little by accessing the camera and invoking a "Zoom"
        # method on it.
        ren.ResetCamera()
        ren.GetActiveCamera().Zoom(1.5)
        renWin.Render()

    except Exception as err:
        err_msgs = Text("\nvtk example did not run properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold red")
        return err_msgs


def check_numpy():
    try:
        import numpy as np
    except Exception as err:
        err_msgs = Text("\nnumpy did not import properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold green")
        return err_msgs


def check_shapely():
    try:
        from shapely.geometry import Polygon
    except Exception as err:
        err_msgs = Text("\nshapely did not import properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold cyan")
        return err_msgs


def check_sectionproperties():
    try:
        import sectionproperties.pre.library.primitive_sections as sections
        from sectionproperties.analysis.section import Section

        geometry = sections.circular_section(d=50, n=64)
        geometry.create_mesh(mesh_sizes=[2.5])
    except Exception as err:
        err_msgs = Text("\nsectionproperties example did not run properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold cyan")
        return err_msgs


def check_openpyxl():
    try:
        from openpyxl import Workbook

        wb = Workbook()
        dest_filename = "empty_book.xlsx"
        saved_file = pathlib.Path.home() / dest_filename
        wb.save(filename=saved_file)
        if not saved_file.exists():
            raise Exception(f"No file found: {saved_file}")
        else:
            saved_file.unlink()
    except Exception as err:
        err_msgs = Text("\nopenpyxl example did not run properly:\n")
        for err_arg in err.args:
            err_msgs.append("\t" + err_arg + "\n")
        err_msgs.stylize("bold yellow")
        return err_msgs


def install_extra():
    if platform.system() == "Linux":
        # conda install that package for vtk on linux if platform is linux
        proc = subprocess.Popen(
            ["conda", "install", "-c", "conda-forge", "libstdcxx-ng"],
            stdin=subprocess.PIPE,
            text=True,
        )
        proc.communicate("y\n")
    else:
        msg = Text("No additional installations necessary. Ok.")
        msg.stylize("bold green")
        console.print(msg)


if __name__ == "__main__":
    install_extra()
    check_installs()
