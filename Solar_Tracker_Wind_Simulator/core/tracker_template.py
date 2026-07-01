"""
========================================================================

Tracker Template

========================================================================

Defines the complete configurable geometry of a tracker.

This file contains NO calculations.

It is simply the editable definition used to build tracker instances.

========================================================================
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class TrackerTemplate:

    # ==========================================================
    # General Information
    # ==========================================================

    name: str = field(
        default="New Tracker",
        metadata={

    "group": "General",

    "description": "Template Name",

    "units": "",

    "editable": True,

    "choices": None,

    "min": None,

    "max": None,

    "precision": 3

}
    )

    description: str = field(
        default="",
        metadata={

    "group": "General",

    "description": "Description",

    "units": "",

    "editable": True,

    "choices": None,

    "min": None,

    "max": None,

    "precision": 3

}
    )

    manufacturer: str = field(
        default="",
        metadata={

    "group": "General",

    "description": "Manufacturer",

    "units": "",

    "editable": True,

    "choices": ["OMCO STAR" ,"P4Q"], 

    "min": None,

    "max": None,

    "precision": 3

}
    )

    version: str = field(
        default="1.0",
        metadata={
            "group": "General",
            "description": "Template version"
        }
    )

    # ==========================================================
    # Overall Geometry
    # ==========================================================

    tracker_length: float = field(
        default=90.0,
        metadata={
            "group": "Overall Geometry",
            "units": "m",
            "min": 1.0,
            "max": 300.0,
            "description": "Overall tracker length"
        }
    )

    support_count: int = field(
        default=7,
        metadata={
            "group": "Overall Geometry",
            "min": 2,
            "description": "Number of support posts"
        }
    )

    # ==========================================================
    # Span Geometry
    # ==========================================================

    span_lengths: List[float] = field(
        default_factory=lambda: [15.0] * 6,
        metadata={
            "group": "Span Geometry",
            "units": "m",
            "description": "Distance between supports"
        }
    )

    modules_per_span: List[float] = field(
        default_factory=lambda: [5.0] * 6,
        metadata={
            "group": "Span Geometry",
            "description": "Modules within each span"
        }
    )

    # ==========================================================
    # Torque Tubes
    # ==========================================================

    torque_tube_sections: List[str] = field(
        default_factory=lambda: [
            "TorqueTube_4in",
            "TorqueTube_4in",
            "TorqueTube_4in",
            "TorqueTube_4in",
            "TorqueTube_4in",
            "TorqueTube_4in",
        ],
        metadata={
            "group": "Torque Tubes",
            "description": "Section used for each torque tube segment"
        }
    )

    tube_segment_lengths: List[float] = field(
        default_factory=lambda: [15.0] * 6,
        metadata={
            "group": "Torque Tubes",
            "units": "m",
            "description": "Length of each tube segment"
        }
    )

    # ==========================================================
    # Solar Modules
    # ==========================================================

    module_width: float = field(
        default=1.30,
        metadata={
            "group": "Solar Modules",
            "units": "m",
            "description": "Module width"
        }
    )

    module_height: float = field(
        default=2.30,
        metadata={
            "group": "Solar Modules",
            "units": "m",
            "description": "Module height"
        }
    )

    module_gap: float = field(
        default=0.02,
        metadata={
            "group": "Solar Modules",
            "units": "m",
            "description": "Gap between modules"
        }
    )

    # ==========================================================
    # Supports
    # ==========================================================

    support_section: str = field(
        default="CPile_4p5x7p62",
        metadata={
            "group": "Supports",
            "description": "Support section type"
        }
    )

    foundation_type: str = field(
        default="Driven Pile",
        metadata={
            "group": "Supports",
            "description": "Foundation type"
        }
    )

    embedment_depth: float = field(
        default=2.5,
        metadata={
            "group": "Supports",
            "units": "m",
            "description": "Foundation embedment"
        }
    )

    # ==========================================================
    # Bearings
    # ==========================================================

    bearing_offset: float = field(
        default=0.0,
        metadata={
            "group": "Bearings",
            "units": "m",
            "description": "Bearing offset from support"
        }
    )

    # ==========================================================
    # Drive
    # ==========================================================

    drive_location: int = field(
        default=3,
        metadata={
            "group": "Drive",
            "description": "Support containing drive"
        }
    )

    motor_name: str = field(
        default="Default Drive",
        metadata={
            "group": "Drive",
            "description": "Drive motor"
        }
    )

    # ==========================================================
    # Cantilevers
    # ==========================================================

    cantilever_left: float = field(
        default=3.0,
        metadata={
            "group": "Cantilevers",
            "units": "m",
            "description": "Left cantilever"
        }
    )

    cantilever_right: float = field(
        default=3.0,
        metadata={
            "group": "Cantilevers",
            "units": "m",
            "description": "Right cantilever"
        }
    )

    # ==========================================================
    # GPS Layout
    # ==========================================================

    latitude_start: float = field(
        default=0.0,
        metadata={
            "group": "GPS Layout",
            "units": "deg",
            "description": "Starting latitude"
        }
    )

    longitude_start: float = field(
        default=0.0,
        metadata={
            "group": "GPS Layout",
            "units": "deg",
            "description": "Starting longitude"
        }
    )

    latitude_end: float = field(
        default=0.0,
        metadata={
            "group": "GPS Layout",
            "units": "deg",
            "description": "Ending latitude"
        }
    )

    longitude_end: float = field(
        default=0.0,
        metadata={
            "group": "GPS Layout",
            "units": "deg",
            "description": "Ending longitude"
        }
    )