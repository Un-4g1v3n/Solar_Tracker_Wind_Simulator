"""
========================================================================

Solar Tracker Wind Simulator
Application Launcher

========================================================================

Responsibilities

    • Verify project structure
    • Display current project state
    • Discover registered tools
    • Execute selected tool

No engineering calculations occur here.

========================================================================
"""

from pathlib import Path
import sys

#
# Import menus
# (registration happens automatically)
#

from menus import validation
from menus import templates

from menus.registry import (
    get_categories,
    get_category,
)

from core.project_state import project_state


# ============================================================
# Project Structure
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

REQUIRED_FOLDERS = [

    "core",
    "truth",
    "validation",
    "templates",
    "menus",
    "results",
    "docs",

]


# ============================================================
# Startup
# ============================================================

def startup():

    print()
    print("=" * 70)
    print("SOLAR TRACKER WIND SIMULATOR")
    print("=" * 70)
    print()

    for folder in REQUIRED_FOLDERS:

        path = PROJECT_ROOT / folder

        if path.exists():

            print(f"[ OK ] {folder}")

        else:

            print(f"[MISSING] {folder}")

    print()


# ============================================================
# Project Status
# ============================================================

def show_status():

    print("=" * 70)
    print("CURRENT PROJECT")
    print("=" * 70)

    print(
        f"Template    : "
        f"{project_state.current_template_name or '(none)'}"
    )

    print(
        f"Farm        : "
        f"{getattr(project_state,'current_farm_name',None) or '(none)'}"
    )

    print(
        f"Simulation  : "
        f"{getattr(project_state,'current_simulation_name',None) or '(none)'}"
    )

    print()


# ============================================================
# Main Menu
# ============================================================

def main_menu():

    categories = get_categories()

    while True:

        show_status()

        print("=" * 70)
        print("MAIN MENU")
        print("=" * 70)
        print()

        for i, category in enumerate(categories, start=1):

            print(f"{i}. {category}")

        print()
        print("0. Exit")
        print()

        choice = input("Selection : ").strip()

        if choice == "0":

            return

        try:

            category = categories[int(choice)-1]

        except Exception:

            print("\nInvalid selection.\n")

            continue

        submenu(category)


# ============================================================
# Sub Menu
# ============================================================

def submenu(category):

    items = get_category(category)

    while True:

        show_status()

        print("=" * 70)
        print(category)
        print("=" * 70)
        print()

        for i, item in enumerate(items, start=1):

            print(f"{i}. {item.name}")

            if item.description:

                print(f"    {item.description}")

        print()

        print("0. Back")
        print()

        choice = input("Selection : ").strip()

        if choice == "0":

            return

        try:

            tool = items[int(choice)-1]

        except Exception:

            print("\nInvalid selection.\n")

            continue

        print()

        try:

            tool.callback()

        except Exception as ex:

            print()
            print(ex)

        input("\nPress ENTER...")


# ============================================================
# Main
# ============================================================

def main():

    startup()

    main_menu()

    print()
    print("Goodbye.")


# ============================================================

if __name__ == "__main__":

    main()