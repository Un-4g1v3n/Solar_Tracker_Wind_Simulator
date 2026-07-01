from truth.tracker_sections import TRACKER_SECTIONS



SECTION_BUILDERS = {
    "rectangle": rectangle,
    "rectangular_tube": rectangular_tube,
    "circular_tube": circular_tube,
    "circular_bar": circular_bar,
    "channel": channel,
    #"lipped_channel": lipped_channel,
}


def build_section(name: str):

    definition = TRACKER_SECTIONS[name]

    shape = definition["shape"]

    builder = SECTION_BUILDERS[shape]

    kwargs = {
        k: v
        for k, v in definition.items()
        if k != "shape"
    }

    return builder(**kwargs)


###############################################################################
# Utility
###############################################################################

def available_sections() -> list[str]:
    

    return sorted(SECTION_BUILDERS.keys())


###############################################################################
# Self Test
###############################################################################

def run():

    print("SECTION PROPERTIES SELF TEST")

if __name__ == "__main__":

    run()

    print("=" * 72)
    print("SECTION FACTORY")
    print("=" * 72)

    print("\nAvailable Sections")

    for section in available_sections():
        print("  •", section)

    print("\nBuilding Example Section\n")

    tube = build_section(
        "rectangular_tube",
        width=0.1016,
        height=0.1016,
        thickness=0.0037,
        density=7850,
        name="Factory Test Tube",
    )

    tube.pretty_print()