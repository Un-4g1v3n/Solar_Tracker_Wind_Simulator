"""
========================================================================

Delete Tracker Template

========================================================================
"""

from menus.registry import register

from core.project_state import project_state

from core.template_library import (

    delete_template,

    template_names,

)


def run():

    names = template_names()

    if not names:

        print()

        print("No templates exist.")

        return

    print()

    print("=" * 70)
    print("DELETE TEMPLATE")
    print("=" * 70)
    print()

    for i, name in enumerate(names, start=1):

        current = ""

        if project_state.current_template_name == name:

            current = " (CURRENT)"

        print(f"{i}. {name}{current}")

    print()

    print("0. Cancel")
    print()

    choice = input("Selection : ").strip()

    if choice == "0":

        return

    try:

        filename = names[int(choice)-1]

    except Exception:

        print()

        print("Invalid selection.")

        return

    print()

    confirm = input(

        f'Delete "{filename}"? (y/n): '

    ).lower()

    if confirm != "y":

        print()

        print("Cancelled.")

        return

    delete_template(filename)

    #
    # If current template deleted
    #

    if project_state.current_template_name == filename:

        project_state.current_template = None

        project_state.current_template_name = None

    print()

    print(f'"{filename}" deleted.')


register(

    category="Templates",

    name="Delete Template",

    description="Delete a tracker template",

    callback=run,

)


if __name__ == "__main__":

    run()