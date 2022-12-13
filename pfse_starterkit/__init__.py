"""
A module to designed to perform package installations, and verification of install,
in preparation for the StructuralPython "Python for Structural Engineers" ("pfse")
course.
"""
__version__ = "0.0.1"

# import pathlib
import platform
import subprocess
from subprocess import PIPE
from rich.console import Console
from rich.text import Text

console = Console()



