"""
========================================================================

Edit Tracker Template

========================================================================

Loads an existing tracker template, edits it using the generic property
editor, and optionally saves the changes.

========================================================================
"""

from menus.registry import register

from core.template_library import (
    list_templates,
    load_template,
    save_template,
)

from core.property_editor import edit_object


# ============================================================
# Edit Template
# ============================================================

def run():

    templates = list_templates()

    if not templates:

        print()
        print("No templates exist.")
        return

    print()
    print("=" * 70)
    print("EDIT TEMPLATE")
    print("=" * 70)
    print()

    for i, template in enumerate(templates, start=1):

        print(f"{i}. {template.name}")

    print()
    print("0. Cancel")
    print()

    choice = input("Template : ").strip()

    if choice == "0":

        return

    try:

        template_info = templates[int(choice) - 1]

    except Exception:

        print()
        print("Invalid selection.")
        return

    template = load_template(template_info.filename)

    print()
    print(f"Editing: {template_info.name}")

    modified = edit_object(template)

    if not modified:

        print()
        print("No changes made.")
        return

    print()
    answer = input("Save changes? (Y/N) : ").strip().lower()

    if answer not in ("y", "yes"):

        print()
        print("Changes discarded.")
        return

    save_template(template, template_info.filename)

    print()
    print("Template saved.")


# ============================================================
# Register
# ============================================================

register(

    category="Templates",

    name="Edit Template",

    description="Modify an existing tracker template.",

    callback=run,

)


# ============================================================

if __name__ == "__main__":

    run()