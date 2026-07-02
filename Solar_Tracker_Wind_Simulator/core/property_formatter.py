"""
========================================================================

Property Formatter

========================================================================

Formatting utilities used by the Property Editor.

Responsibilities

    • Convert Python values into readable strings
    • Apply precision formatting
    • Format lists
    • Format booleans

This module performs NO validation and NO user interaction.

========================================================================
"""

from typing import Any


# ======================================================================
# Primitive Formatter
# ======================================================================

def format_value(
    value: Any,
    precision: int | None = None,
) -> str:
    """
    Convert a Python value into a readable string.

    Parameters
    ----------
    value
        Value to format.

    precision
        Optional decimal precision for floats.

    Returns
    -------
    str
    """

    #
    # None
    #

    if value is None:

        return ""

    #
    # Boolean
    #

    if isinstance(value, bool):

        return "Yes" if value else "No"

    #
    # Float
    #

    if isinstance(value, float):

        if precision is None:

            return str(value)

        return f"{value:.{precision}f}"

    #
    # List
    #

    if isinstance(value, list):

        return format_list(
            value,
            precision,
        )

    #
    # Default
    #

    return str(value)


# ======================================================================
# List Formatter
# ======================================================================

def format_list(
    values: list,
    precision: int | None = None,
) -> str:
    """
    Format a list for display.
    """

    if not values:

        return "[]"

    formatted = [

        format_value(
            value,
            precision,
        )

        for value in values

    ]

    return ", ".join(formatted)


# ======================================================================
# Display Formatter
# ======================================================================

def format_display(
    value: Any,
    units: str | None = None,
    precision: int | None = None,
) -> str:
    """
    Format a value together with engineering units.

    Example

        17.500 m

        5

        True

    """

    text = format_value(
        value,
        precision,
    )

    if units:

        return f"{text} {units}"

    return text