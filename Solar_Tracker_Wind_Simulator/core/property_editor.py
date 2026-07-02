"""
========================================================================

Property Editor

========================================================================

Public API for editing dataclass objects.

Responsibilities

    • Present grouped editing menus
    • Display engineering metadata
    • Coordinate parsing
    • Coordinate formatting
    • Coordinate validation
    • Coordinate option registries

All parsing, formatting, validation and grouping logic lives in
their own modules.

Public API

    edit_object(obj)

========================================================================
"""

from dataclasses import fields

from core.property_groups import (
    group_names,
    fields_in_group,
)

from core.property_formatter import (
    format_display,
)

from core.property_parser import (
    parse_value,
)

from core.property_validation import (
    validate,
)

from core.option_registry import (
    get_options,
)
from core.property_metadata import display_metadata

# ======================================================================
# Helpers
# ======================================================================

def _display_choices(options):
    """
    Display a numbered list of available options.

    Returns
    -------
    selected_value or None
    """

    print()

    for i, value in enumerate(options, start=1):

        print(f"{i:2d}. {value}")

    print()

    selection = input("Selection : ").strip()

    if selection == "":

        return None

    try:

        index = int(selection) - 1

        return options[index]

    except Exception:

        print()

        print("Invalid selection.")

        input("Press ENTER...")

        return None


# ======================================================================
# Edit One Field
# ======================================================================

def _edit_field(obj, field):
    """
    Edit a single dataclass field.

    Returns
    -------
    bool

        True if the field changed.
    """

    metadata = field.metadata

    current = getattr(obj, field.name)

    print()

    print("=" * 70)
    print(field.name)
    print("=" * 70)
    print()

    #
    # Description
    #

    description = metadata.get("description")

    if description:

        print(description)
        print()

    #
    # Current value
    #

    print("Current Value")

    print(

        format_display(

            current,

            metadata.get("units"),

            metadata.get("precision"),

        )

    )

    print()

    #
    # Engineering metadata
    #

    display_metadata(field)

    #
    # Option list?
    #

    options = metadata.get("options")

    #
    # Registry-backed list
    #

    if isinstance(options, str):

        options = get_options(options)

    #
    # Menu selection
    #

    if isinstance(options, list):

        print()

        print("Available Options")

        print("-----------------")

        for i, option in enumerate(options, start=1):

            print(f"{i:2d}. {option}")

        print()

        selection = input(
            "Selection (ENTER to cancel): "
        ).strip()

        if selection == "":

            return False

        try:

            parsed = options[int(selection) - 1]

        except Exception:

            print()

            print("Invalid selection.")

            input("Press ENTER...")

            return False

    #
    # Free-text entry
    #

    else:

        print()

        text = input(
            "New Value (ENTER to keep current): "
        )

        if text == "":

            return False

        try:

            parsed = parse_value(

                current,

                field.type,

                text,

            )

        except Exception as ex:

            print()

            print(ex)

            input("Press ENTER...")

            return False

    #
    # Validate
    #

    valid, reason = validate(

        parsed,

        metadata,

    )

    if not valid:

        print()

        print(reason)

        input("Press ENTER...")

        return False

    #
    # No change?
    #

    if parsed == current:

        return False

    #
    # Store
    #

    setattr(

        obj,

        field.name,

        parsed,

    )

    print()

    print("Value updated.")

    input("Press ENTER...")

    return True
# ======================================================================
# Edit One Group
# ======================================================================

def _edit_group(obj, group_name):
    """
    Edit all fields within a single property group.

    Returns
    -------
    bool
        True if any property was modified.
    """

    modified = False

    group = fields_in_group(

        obj,

        group_name,

    )

    while True:

        print()

        print("=" * 70)

        print(group_name)

        print("=" * 70)

        print()

        #
        # Display all properties
        #

        for index, field in enumerate(group, start=1):

            metadata = field.metadata

            value = getattr(

                obj,

                field.name,

            )

            display = format_display(

                value,

                metadata.get("units"),

                metadata.get("precision"),

            )

            print(

                f"{index:2d}. "

                f"{field.name:<32}"

                f"{display}"

            )

            description = metadata.get(

                "description"

            )

            if description:

                print(

                    f"      {description}"

                )

        print()

        print("0. Back")

        print()

        selection = input(

            "Property : "

        ).strip()

        #
        # Return to previous menu
        #

        if selection == "0":

            return modified

        #
        # Lookup field
        #

        try:

            field = group[

                int(selection) - 1

            ]

        except Exception:

            print()

            print(

                "Invalid selection."

            )

            input(

                "Press ENTER..."

            )

            continue

        #
        # Edit selected field
        #

        changed = _edit_field(

            obj,

            field,

        )

        modified = (

            modified or changed

        )
        
# ======================================================================
# Public API
# ======================================================================

def edit_object(obj):
    """
    Edit any dataclass using metadata.

    Parameters
    ----------
    obj
        Dataclass instance to edit.

    Returns
    -------
    bool

        True if one or more properties changed.

        False otherwise.
    """

    modified = False

    while True:

        print()

        print("=" * 70)

        print(type(obj).__name__)

        print("=" * 70)

        print()

        groups = group_names(obj)

        #
        # Show available groups
        #

        for index, group in enumerate(groups, start=1):

            print(f"{index}. {group}")

        print()

        print("0. Done")

        print()

        selection = input("Section : ").strip()

        #
        # Finished editing
        #

        if selection == "0":

            return modified

        #
        # Select group
        #

        try:

            group = groups[int(selection) - 1]

        except Exception:

            print()

            print("Invalid selection.")

            input("Press ENTER...")

            continue

        #
        # Edit selected group
        #

        changed = _edit_group(

            obj,

            group,

        )

        modified = (

            modified or changed

        )