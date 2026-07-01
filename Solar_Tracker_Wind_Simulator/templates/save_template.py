"""
========================================================================

Save Tracker Template

========================================================================

Saves the currently active tracker template.

All filesystem operations are performed by template_library.py

========================================================================
"""

from menus.registry import register

from core.project_state import project_state
from core.template_library import (
    list_templates,
    save_template,
)


# ============================================================
# Helpers
# ============================================================

def overwrite_existing():

    templates = list_templates()

    if len(templates) == 0:

        print()
        print("No existing templates found.")
        print()

        save_as()

        return

    print()
    print("Existing Templates")
    print("------------------")
    print()

    for i, template in enumerate(templates, start=1):

        print(f"{i}. {template.stem}")

    print()

    choice = input("Overwrite which template? : ").strip()

    try:

        filename = templates[int(choice) - 1].name

    except Exception:

        print()
        print("Invalid selection.")
        print()

        return

    save_template(

        project.current_template,

        filename,

    )

    project.template_filename = filename

    project.modified = False

    print()
    print("Template saved.")
    print(filename)
    print()


def save_as():

    default = "New_Template"

    if project.current_template is not None:

        default = project.current_template.name.replace(" ", "_")

    print()

    filename = input(

        f"Filename [{default}] : "

    ).strip()

    if filename == "":

        filename = default

    save_template(

        project.current_template,

        filename,

    )

    if not filename.endswith(".yaml"):

        filename += ".yaml"

    project.template_filename = filename

    project.modified = False

    print()
    print("Template saved.")
    print(filename)
    print()


# ============================================================
# Main Entry
# ============================================================

def run():

    if project.current_template is None:

        print()
        print("No active tracker template.")
        print()

        return

    print()
    print("=" * 70)
    print("SAVE TEMPLATE")
    print("=" * 70)
    print()

    print(f"Current Template : {project.current_template.name}")

    if project.template_filename:

        print(f"Current File     : {project.template_filename}")

    else:

        print("Current File     : <Unsaved>")

    print()

    print("1. Overwrite Existing")

    print("2. Save As")

    print("0. Cancel")

    print()

    choice = input("Selection : ").strip()

    if choice == "0":

        return

    elif choice == "1":

        overwrite_existing()

    elif choice == "2":

        save_as()

    else:

        print()
        print("Invalid selection.")
        print()


# ============================================================
# Registry
# ============================================================

register(

    category="Templates",

    name="Save Template",

    description="Save the current tracker template",

    callback=run,

)


# ============================================================

if __name__ == "__main__":

    run()