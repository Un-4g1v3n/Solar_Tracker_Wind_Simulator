"""
========================================================================

Load Tracker Template

========================================================================

Loads a tracker template from disk into the current project.

Filesystem operations are handled by template_library.py.

========================================================================
"""

from menus.registry import register

from core.project_state import project_state

from core.template_library import (
    load_template,
    template_names,
)


# ======================================================================

def run():

    names = template_names()

    if not names:

        print()
        print("No templates exist.")
        return

    print()
    print("=" * 70)
    print("LOAD TEMPLATE")
    print("=" * 70)
    print()

    for i, name in enumerate(names, start=1):

        print(f"{i}. {name}")

    print()
    print("0. Cancel")
    print()

    choice = input("Selection : ").strip()

    if choice == "0":

        return

    try:

        index = int(choice) - 1

        filename = names[index]

    except Exception:

        print()
        print("Invalid selection.")
        return

    #
    # Read YAML
    #

    template = load_template(filename)

    #
    # Make current project template
    #

    project_state.current_template = template

    project_state.current_template_name = filename

    print()
    print(f'Loaded "{filename}"')
    print()


# ======================================================================

register(

    category="Templates",

    name="Load Template",

    description="Load a tracker template",

    callback=run,

)


# ======================================================================

if __name__ == "__main__":

    run()