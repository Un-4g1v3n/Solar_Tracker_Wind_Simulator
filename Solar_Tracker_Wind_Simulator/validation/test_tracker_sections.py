from menus.registry import register
from truth.tracker_sections import TRACKER_SECTIONS


def run():

    print()

    print("Tracker Sections")

    print("----------------")

    for name, section in TRACKER_SECTIONS.items():

        print(name)

        for key, value in section.items():

            print(f"    {key}: {value}")

        print()
        
register(
    
    description="Geometry definitions for Trackers",

    category="Validation",

    name="Section Library",

    callback=run

)


if __name__ == "__main__":

    run()