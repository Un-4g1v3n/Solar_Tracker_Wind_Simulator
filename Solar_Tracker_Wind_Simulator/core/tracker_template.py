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

    name: str = field(default="New Tracker",
        metadata={
    "group": "General",
    "description": "Template Name",
    "editable": True,
    "required": True,
    "default" :"New Tracker",
}
    )

    description: str = field(default= "",
        metadata={
    "group": "General",
    "description": "Description",
    "editable": True,
    "required": True,
    "default": None,
}
    )

    manufacturer: str = field(default= "OMCO STAR",
    metadata={
        "group": "General",
        "description": "Tracker manufacturer",
        "editable": True,
        "options": [
            "OMCO STAR",
            "P4Q",
        ], 
        "default": "OMCO STAR",
        "required": True,
    }
)

    version: str = field(default= "1.0",
        metadata={
            "group": "General",
            "description": "Template version",
            "default": "1.0",
            "required": True, 
        }
    )

    # ==========================================================
    # Overall Geometry
    # ==========================================================

    tracker_length: float = field(default= 90,
        metadata={
            "group": "Overall Geometry",
            "description": "Overall tracker length",
            "units": "m",
            "min": 1.0,
            "max": 400.0,
            "editable": True,
            "precision": 3,
            "default": 90, 
            "required": True,
            
        }
    )

    support_count: int = field(default= 7,
        metadata={
            "group": "Overall Geometry",
            "description": "Number of support posts",
            "units": "",
            "editable": True,
            "min": 1,
            "max": None,
            "default": 7, 
            "required": True,
        }
    )

    # ==========================================================
    # Span Geometry
    # ==========================================================

    span_lengths: List[float] = field(default= lambda: [15.0] * 6,
        metadata={
            "group": "Span Geometry",
            "description": "Distance between Support posts",
            "units": "m",
            "editable": True,
            "min": 5,
            "max": 50,
            "precision": 3, 
            "default": lambda: [15.0] * 6,
            "required": True, 
        }
    )

    modules_per_span: List[float] = field(default= lambda: [5.0] * 6, 
        metadata={
            "group": "Span Geometry",
            "description": "Modules within each span",
            "units": "",
            "editable": True,
            "min": 1,
            "max": None,
            "precision": 3, 
            "default": lambda: [5.0] * 6,
            "required": True, 
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
            "description": "Section used for each torque tube segment",
            "units": "",
            "editable": True,
            "default": None, 
            "required": True, 
        }
    )

    tube_segment_lengths: List[float] = field(default= lambda: [15.0] * 6, 
        metadata={
            "group": "Torque Tubes",
            "description": "Length of each tube segment",
            "units": "m",
            "editable": True,
            "min": 1,
            "max": 20,
            "precision": 3, 
            "default": lambda: [15.0] * 6,
            "required": True, 
        }
    )

    # ==========================================================
    # Solar Modules
    # ==========================================================

    module_width: float = field(default= 1.3, 
        metadata={
            "group": "Solar Modules",
            "description": "Module width",
            "units": "m",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 3,
            "default": 1.3,
            "required": True,
        }
    )

    module_height: float = field(default= 2.3, 
        metadata={
            "group": "Solar Modules",
            "description": "Module height",
            "units": "m",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 3,
            "default": 2.3,
            "required": True,
        }
    )

    module_gap: float = field(default= 0.2, 
        metadata={
            "group": "Solar Modules",
            "description": "Gap between modules",
            "units": "m",
            "editable": True,
            "min": 0,
            "max": None,
            "precision": 3, 
            "default": 0.2,
            "required": True,
        }
    )

    # ==========================================================
    # Supports
    # ==========================================================

    support_section: str = field(
        default="CPile_4p5x7p62",
        metadata={
            "group": "Supports",
            "description": "Support section type",
            "editable": True,
            "options": None,
            "default": "CPile_4p5x7p62",
            "required": True,
        }
    )

    foundation_type: str = field(default= "driven pile", 
        metadata={
            "group": "Supports",
            "description": "Foundation type",
            "editable": True,
            "options": None,
            "default": "Driven Pile",
            "required": True,
        }
    )

    embedment_depth: float = field(default= 2.5, 
        metadata={
            "group": "Supports",
            "description": "Foundation embedment",
            "units": "m",
            "editable": True,
            "min": 0,
            "max": None,
            "precision": 3,
            "default": 2.5,
            "required": True,
        }
    )

    # ==========================================================
    # Bearings
    # ==========================================================

    bearing_offset: float = field(default= 0.0, 
        metadata={
            "group": "Bearings",
            "description": "Bearing offset from support",
            "units": "m",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 3,
            "default": 0.0,
            "required": True,
        }
    )

    # ==========================================================
    # Drive
    # ==========================================================

    drive_location: int = field(default= 3, 
        metadata={
            "group": "Drive",
            "description": "Support containing drive",
            "editable": True,
            "default": 3,
            "required": True,
        }
    )

    motor_name: str = field(default= "Kinematics", 
        metadata={
            "group": "Drive",
            "description": "Drive motor",
            "editable": True,
            "options": None,
            "default": "Kinematics",
            "required": True,
        }
    )

    # ==========================================================
    # Cantilevers
    # ==========================================================

    cantilever_left: float = field(default= 3.0, 
        metadata={
            "group": "Cantilevers",
            "description": "Left cantilever",
            "units": "m",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 3,
            "default": 3.0,
            "required": True,
        }
    )

    cantilever_right: float = field(default= 3.0, 
        metadata={
            "group": "Cantilevers",
            "description": "Right cantilever",
            "units": "m",
            "editable": True,
            "options": None,
            "min": None,
            "max": None,
            "precision": 3, 
            "default": 3.0,
            "required": True,
        }
    )

    # ==========================================================
    # GPS Layout
    # ==========================================================

    latitude_start: float = field(default= 0.0, 
        metadata={
            "group": "GPS Layout",
            "description": "Starting latitude",
            "units": "deg",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 5, 
            "default": 0.0,
            "required": True,
        }
    )

    longitude_start: float = field(default= 0.0,
        metadata={
            "group": "GPS Layout",
            "description": "Starting longitude",
            "units": "deg",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 5,
            "default": 0.0,
            "required": True,
        }
    )

    latitude_end: float = field(default= 0.0,
        metadata={
            "group": "GPS Layout",
            "description": "Ending latitude",
            "units": "",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 5, 
            "default": 0.0,
            "required": True,
        }
    )

    longitude_end: float = field(default= 0.0,
        metadata={
            "group": "GPS Layout",
            "description": "Ending longitude",
            "units": "deg",
            "editable": True,
            "min": None,
            "max": None,
            "precision": 5, 
            "default": 0.0,
            "required": True,
        }
    )