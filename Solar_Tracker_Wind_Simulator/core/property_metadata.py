"""
========================================================================

Property Metadata

========================================================================

Utilities for displaying engineering metadata.

This module performs NO editing.

It simply formats and displays metadata in a consistent way.

========================================================================
"""


# ======================================================================
# Small Helper
# ======================================================================

def show(label, value, formatter=str):
    """
    Display a metadata item only if it has a value.

    Parameters
    ----------
    label
        Display label.

    value
        Metadata value.

    formatter
        Optional formatting function.
    """

    if value is None:
        return

    if value == "":
        return

    if value == []:
        return

    print(f"{label:<12}: {formatter(value)}")


# ======================================================================
# Helper Formatters
# ======================================================================

def yes_no(value):

    return "Yes" if value else "No"


def format_range(metadata):

    minimum = metadata.get("min")

    maximum = metadata.get("max")

    if minimum is None and maximum is None:

        return None

    if minimum is None:

        return f"≤ {maximum}"

    if maximum is None:

        return f"≥ {minimum}"

    return f"{minimum} → {maximum}"


def registry_name(metadata):

    options = metadata.get("options")

    if isinstance(options, str):

        return options

    return None


# ======================================================================
# Display Metadata
# ======================================================================

def display_metadata(field):

    metadata = field.metadata

    print("-" * 60)

    show("Units", metadata.get("units"))

    show("Default", metadata.get("default"))

    show("Range", format_range(metadata))

    show("Required",
         metadata.get("required"),
         yes_no)

    show("Editable",
         metadata.get("editable", True),
         yes_no)

    show("Precision",
         metadata.get("precision"),
         lambda p: f"{p} decimals")

    show("Registry",
         registry_name(metadata))

    print("-" * 60)