"""
========================================================================

Property Parser

========================================================================

Parsing utilities used by the Property Editor.

Responsibilities

    • Convert user-entered text into Python objects
    • Support primitive types
    • Support lists
    • Preserve existing values on blank input

This module performs NO validation and NO user interaction.

========================================================================
"""

from typing import Any
from typing import get_args
from typing import get_origin


# ======================================================================
# Primitive Parsers
# ======================================================================

_TRUE_VALUES = {

    "true",
    "t",
    "yes",
    "y",
    "1",
    "on",

}

_FALSE_VALUES = {

    "false",
    "f",
    "no",
    "n",
    "0",
    "off",

}


def parse_bool(text: str) -> bool:
    """
    Convert text into a boolean.
    """

    value = text.strip().lower()

    if value in _TRUE_VALUES:

        return True

    if value in _FALSE_VALUES:

        return False

    raise ValueError(
        f"'{text}' is not a valid boolean."
    )


# ======================================================================
# List Parser
# ======================================================================

def parse_list(
    text: str,
    subtype,
):
    """
    Convert comma-separated text into a list.

    Example

        1,2,3

        1.2, 5.4

        abc,def
    """

    items = [

        item.strip()

        for item in text.split(",")

        if item.strip()

    ]

    if subtype is int:

        return [

            int(item)

            for item in items

        ]

    if subtype is float:

        return [

            float(item)

            for item in items

        ]

    if subtype is bool:

        return [

            parse_bool(item)

            for item in items

        ]

    return items


# ======================================================================
# Generic Parser
# ======================================================================

def parse_value(
    current_value: Any,
    annotation,
    text: str,
):
    """
    Parse text into the supplied type.

    Blank input returns the current value unchanged.
    """

    #
    # Keep current value
    #

    if text.strip() == "":

        return current_value

    origin = get_origin(annotation)

    args = get_args(annotation)

    #
    # List
    #

    if origin is list:

        subtype = args[0]

        return parse_list(

            text,

            subtype,

        )

    #
    # Primitive
    #

    if annotation is str:

        return text

    if annotation is int:

        return int(text)

    if annotation is float:

        return float(text)

    if annotation is bool:

        return parse_bool(text)

    #
    # Fallback
    #

    return text