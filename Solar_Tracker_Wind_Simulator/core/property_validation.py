"""
========================================================================

Property Validation

========================================================================

Validation utilities used by the Property Editor.

Responsibilities

    • Validate numeric ranges
    • Validate required fields
    • Validate list lengths
    • Validate choice selections
    • Return readable error messages

This module performs NO user interaction.

========================================================================
"""

from typing import Any


# ======================================================================
# Numeric Range Validation
# ======================================================================

def validate_numeric(value, metadata):
    """
    Validate minimum and maximum limits.

    Returns

        (True, "")

    or

        (False, reason)
    """

    minimum = metadata.get("min")
    maximum = metadata.get("max")

    if minimum is not None:

        if value < minimum:

            return (

                False,

                f"Value must be >= {minimum}",

            )

    if maximum is not None:

        if value > maximum:

            return (

                False,

                f"Value must be <= {maximum}",

            )

    return True, ""


# ======================================================================
# Choice Validation
# ======================================================================

def validate_choice(value, metadata):
    """
    Validate enumerated choices.

    If no choices are supplied,
    validation automatically succeeds.
    """

    choices = metadata.get("options")

    if not choices:

        return True, ""

    #
    # String registry lookup handled elsewhere.
    #

    if isinstance(choices, str):

        return True, ""

    if value not in choices:

        return (

            False,

            "Value must be one of:\n"

            + ", ".join(str(v) for v in choices),

        )

    return True, ""


# ======================================================================
# List Validation
# ======================================================================

def validate_list(value, metadata):
    """
    Validate list length.
    """

    minimum = metadata.get("min_items")
    maximum = metadata.get("max_items")

    length = len(value)

    if minimum is not None:

        if length < minimum:

            return (

                False,

                f"Requires at least {minimum} entries.",

            )

    if maximum is not None:

        if length > maximum:

            return (

                False,

                f"Maximum {maximum} entries.",

            )

    return True, ""


# ======================================================================
# Required Field Validation
# ======================================================================

def validate_required(value, metadata):
    """
    Validate required fields.
    """

    if not metadata.get("required", False):

        return True, ""

    if value is None:

        return False, "Value is required."

    if isinstance(value, str):

        if value.strip() == "":

            return False, "Value is required."

    if isinstance(value, list):

        if len(value) == 0:

            return False, "At least one value is required."

    return True, ""


# ======================================================================
# Master Validator
# ======================================================================

def validate(value: Any, metadata):
    """
    Master validation function.

    Returns

        (True, "")

    or

        (False, reason)
    """

    #
    # Required
    #

    ok, reason = validate_required(

        value,

        metadata,

    )

    if not ok:

        return ok, reason

    #
    # Choices
    #

    ok, reason = validate_choice(

        value,

        metadata,

    )

    if not ok:

        return ok, reason

    #
    # Lists
    #

    if isinstance(value, list):

        return validate_list(

            value,

            metadata,

        )

    #
    # Numbers
    #

    if isinstance(value, (int, float)):

        return validate_numeric(

            value,

            metadata,

        )

    return True, ""