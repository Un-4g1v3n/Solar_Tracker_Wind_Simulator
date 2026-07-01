"""
========================================================================

Property Editor

========================================================================

Generic dataclass editor.

Features

    • Automatic grouping using metadata["group"]
    • Units display
    • Descriptions
    • Primitive types
    • List editing
    • Works with ANY dataclass

========================================================================
"""

from dataclasses import fields
from collections import OrderedDict
from typing import get_origin, get_args


# ======================================================================
# Helpers
# ======================================================================

def _format_value(value):

    if isinstance(value, list):

        if not value:
            return "[]"

        return ", ".join(str(v) for v in value)

    return str(value)


# ======================================================================

def _parse_value(current, annotation, text):

    origin = get_origin(annotation)

    args = get_args(annotation)

    #
    # Leave unchanged
    #

    if text == "":

        return current

    #
    # Lists
    #

    if origin is list:

        subtype = args[0]

        values = [

            item.strip()

            for item in text.split(",")

            if item.strip() != ""

        ]

        if subtype is float:

            return [float(v) for v in values]

        if subtype is int:

            return [int(v) for v in values]

        return values

    #
    # Primitive types
    #

    if annotation is float:

        return float(text)

    if annotation is int:

        return int(text)

    if annotation is bool:

        return text.lower() in (

            "true",
            "yes",
            "y",
            "1",

        )

    return text


# ======================================================================

def _field_groups(obj):

    """
    Returns

        OrderedDict

    group_name -> list(field)
    """

    groups = OrderedDict()

    for f in fields(obj):

        group = f.metadata.get(

            "group",

            "General",

        )

        groups.setdefault(

            group,

            []

        ).append(f)

    return groups


# ======================================================================

def _edit_group(obj, group_name, group_fields):

    """
    Edit one metadata group.
    """

    modified = False

    while True:

        print()

        print("=" * 70)

        print(group_name)

        print("=" * 70)

        print()

        for i, f in enumerate(group_fields, start=1):

            value = getattr(obj, f.name)

            units = f.metadata.get("units", "")

            description = f.metadata.get(

                "description",

                ""

            )

            print(

                f"{i:2d}. "

                f"{f.name:<30}"

                f"{_format_value(value)}"

                f" {units}"

            )

            if description:

                print(f"      {description}")

        print()

        print("0. Back")

        print()

        selection = input("Property : ").strip()

        if selection == "0":

            return modified

        try:

            field = group_fields[int(selection) - 1]

        except Exception:

            print()

            print("Invalid selection.")

            continue

        current = getattr(obj, field.name)

        print()

        print(field.name)

        print("-" * len(field.name))

        print()

        print("Current Value")

        print(current)

        units = field.metadata.get("units")

        if units:

            print(f"Units : {units}")

        minimum = field.metadata.get("min")

        maximum = field.metadata.get("max")

        if minimum is not None:

            print(f"Minimum : {minimum}")

        if maximum is not None:

            print(f"Maximum : {maximum}")

        print()

        new_value = input("New Value : ")

        try:

            parsed = _parse_value(

                current,

                field.type,

                new_value,

            )

        except Exception as ex:

            print()

            print(ex)

            continue

        #
        # Range validation
        #

        if minimum is not None:

            if isinstance(parsed, (int, float)):

                if parsed < minimum:

                    print()

                    print(

                        f"Value must be >= {minimum}"

                    )

                    continue

        if maximum is not None:

            if isinstance(parsed, (int, float)):

                if parsed > maximum:

                    print()

                    print(

                        f"Value must be <= {maximum}"

                    )

                    continue

        setattr(

            obj,

            field.name,

            parsed,

        )

        modified = True


# ======================================================================
# Public Editor
# ======================================================================

def edit_object(obj):

    """
    Generic grouped editor.

    Returns

        True if modified.

        False otherwise.
    """

    modified = False

    groups = _field_groups(obj)

    group_names = list(groups.keys())

    while True:

        print()

        print("=" * 70)

        print(type(obj).__name__)

        print("=" * 70)

        print()

        for i, group in enumerate(group_names, start=1):

            print(f"{i}. {group}")

        print()

        print("0. Done")

        print()

        selection = input("Section : ").strip()

        if selection == "0":

            return modified

        try:

            group = group_names[int(selection) - 1]

        except Exception:

            print()

            print("Invalid selection.")

            continue

        changed = _edit_group(

            obj,

            group,

            groups[group],

        )

        modified = modified or changed