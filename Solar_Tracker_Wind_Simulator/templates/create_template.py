"""
========================================================================

Create Tracker Template

========================================================================

Creates a new tracker template.

The generic Property Editor is used to edit all fields.

========================================================================
"""

from menus.registry import register

from core.tracker_template import TrackerTemplate
from core.property_editor import edit_object
from core.template_library import save_template


# ============================================================
# Create Template
# ============================================================

def run():

    print()
    print("=" * 70)
    print("CREATE TRACKER TEMPLATE")
    print("=" * 70)

    #
    # Start with a blank/default template.
    #

    template = TrackerTemplate()

    print()
    print(
        "A new tracker template has been created."
    )
    print(
        "Fill in the desired values below."
    )

    #
    # Launch the generic property editor.
    #

    modified = edit_object(template)

    if not modified:

        print()
        print("Template creation cancelled.")
        return

    #
    # Ask to save.
    #

    print()

    answer = input(
        "Save this template? (Y/N) : "
    ).strip().lower()

    if answer not in ("y", "yes"):

        print()
        print("Template discarded.")
        return

    #
    # Suggest filename from template name.
    #

    default_filename = template.name.replace(" ", "_")

    print()

    filename = input(
        f"Filename [{default_filename}] : "
    ).strip()

    if filename == "":

        filename = default_filename

    save_template(

        template,

        filename,

    )

    print()
    print("Template saved successfully.")
    print(f"Name     : {template.name}")
    print(f"Filename : {filename}.yaml")
    print()


# ============================================================
# Register
# ============================================================

register(

    category="Templates",

    name="Create Template",

    description="Create a new tracker template.",

    callback=run,

)


# ============================================================

if __name__ == "__main__":

    run()