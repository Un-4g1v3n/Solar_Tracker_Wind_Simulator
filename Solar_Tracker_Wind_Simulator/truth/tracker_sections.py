"""
==============================================================
TRACKER SECTION TRUTH DOCUMENT
==============================================================

This file contains the geometric definitions for every
structural member used anywhere in the simulator.

NO calculations should ever be performed here.

Each entry is simply a definition of a real physical section.

Section properties are generated through

    section_factory.py

which converts these geometric definitions into complete
SectionProperties objects.

This file is the single source of truth for geometry.

==============================================================
"""

from dataclasses import dataclass
from typing import Optional

# -------------------------------------------------------------
# Material Density
# -------------------------------------------------------------

STEEL_DENSITY = 7850.0

# =============================================================
# Torque Tubes
# =============================================================

TRACKER_SECTIONS = {

    "TorqueTube_4in": {

        "shape": "rectangular_tube",

        "name": "4-inch Torque Tube",

        "width": 0.1016,
        "height": 0.1016,
        "thickness": 0.00370,

        "density": STEEL_DENSITY,
    },

    "TorqueTube_5in": {

        "shape": "rectangular_tube",

        "name": "5-inch Torque Tube",

        "width": 0.1270,
        "height": 0.1270,
        "thickness": 0.00476,

        "density": STEEL_DENSITY,
    },

    "TorqueTube_6in": {

        "shape": "rectangular_tube",

        "name": "6-inch Torque Tube",

        "width": 0.1524,
        "height": 0.1524,
        "thickness": 0.00476,

        "density": STEEL_DENSITY,
    },


    "Pipe_SCH40": {

        "shape": "circular_tube",

        "name": "6 inch Schedule 40 Pipe",

        "outside_diameter": 0.16828,
        "thickness": 0.00711,
        "density": STEEL_DENSITY,
    },
    
    "Channel_7p62": {

        "shape": "channel",

        "name": "7.62 in Channel",

        "depth": 0.193548,
        "flange_width": 0.114300,
        "web_thickness": 0.00381,
        "flange_thickness": 0.00381,
        "density": STEEL_DENSITY,
    },

    "CPile_4p5x7p62": {

        "shape": "channel",

        "name": "4.5 x 7.62 C-Pile",

        "depth": 0.193548,
        "flange_width": 0.114300,
        "web_thickness": 0.00381,
        "flange_thickness": 0.00381,
        "density": STEEL_DENSITY,
    },
}


# =============================================================
# Future Sections
# =============================================================

# Example placeholders

# TorqueTube_8in = ...

# W8x31 = ...

# HSS8x8x1/4 = ...

# AFrame_Leg = ...
