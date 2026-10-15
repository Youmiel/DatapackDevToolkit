"""Shared helpers for the patches of a project.

Copy this package into the project root. Patches are imported as modules whose
dotted name starts at the project root, so a helper placed there is importable
from any patch with an absolute import:

    from patch_lib import mcmeta

A .py file placed inside a version directory is treated as a patch instead, and
the framework will try to run it.
"""
