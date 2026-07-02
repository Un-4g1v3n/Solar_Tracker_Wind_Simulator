"""
========================================================================

Option Registry

========================================================================

Central dispatcher for editor drop-down lists.

This module NEVER owns engineering data.

Instead, it requests option lists from the subsystem that owns them.

========================================================================
"""

from core.template_library import template_names

from truth.tracker_sections import TRACKER_SECTIONS


# ======================================================================
# Registry Dispatch Table
# ======================================================================

_REGISTRIES = {

    #
    # Templates
    #

    "templates": template_names,

    #
    # Section Library
    #

    "tracker_sections": lambda: sorted(

        TRACKER_SECTIONS.keys()

    ),

}


# ======================================================================
# Register
# ======================================================================

def register_registry(

    name: str,

    callback,

):
    """
    Register a new option source.

    Example

        register_registry(
            "materials",
            material_names,
        )
    """

    _REGISTRIES[name] = callback


# ======================================================================
# Exists
# ======================================================================

def registry_exists(name: str):

    return name in _REGISTRIES


# ======================================================================
# Get Options
# ======================================================================

def get_options(name: str):
    """
    Return a sorted list of options.

    Raises KeyError if the registry
    does not exist.
    """

    if name not in _REGISTRIES:

        raise KeyError(

            f"Unknown option registry '{name}'."

        )

    options = _REGISTRIES[name]()

    return sorted(options)


# ======================================================================
# List Registries
# ======================================================================

def registry_names():
    """
    Return all registered registry names.
    """

    return sorted(

        _REGISTRIES.keys()

    )