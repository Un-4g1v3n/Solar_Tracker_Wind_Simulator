"""
========================================================================

Property Groups

========================================================================

Utilities for organizing dataclass fields into editor groups.

Responsibilities

    • Read field metadata
    • Build ordered property groups
    • Filter editable fields

This module performs NO user interaction.

========================================================================
"""

from collections import OrderedDict
from dataclasses import fields


# ======================================================================
# Editable Fields
# ======================================================================

def editable_fields(obj):
    """
    Return every editable dataclass field.

    Fields are editable unless

        metadata["editable"] == False
    """

    result = []

    for field in fields(obj):

        if field.metadata.get("editable", True):

            result.append(field)

    return result


# ======================================================================
# Field Groups
# ======================================================================

def field_groups(obj):
    """
    Build ordered property groups.

    Returns

        OrderedDict

    Example

        Geometry
            width
            height

        Supports
            support_count
            support_spacing
    """

    groups = OrderedDict()

    for field in editable_fields(obj):

        group = field.metadata.get(

            "group",

            "General",

        )

        if group not in groups:

            groups[group] = []

        groups[group].append(field)

    return groups


# ======================================================================
# Group Names
# ======================================================================

def group_names(obj):
    """
    Return the ordered group names.
    """

    return list(

        field_groups(obj).keys()

    )


# ======================================================================
# Fields In Group
# ======================================================================

def fields_in_group(
    obj,
    group_name,
):
    """
    Return all editable fields
    belonging to one group.
    """

    return field_groups(obj).get(

        group_name,

        [],

    )


# ======================================================================
# Has Editable Fields
# ======================================================================

def has_editable_fields(obj):
    """
    True if the object contains
    at least one editable property.
    """

    return len(

        editable_fields(obj)

    ) > 0