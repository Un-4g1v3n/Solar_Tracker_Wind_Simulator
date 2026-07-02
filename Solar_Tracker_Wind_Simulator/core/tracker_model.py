"""
========================================================================

Tracker Model

========================================================================

The TrackerModel is the fully assembled engineering representation of a
solar tracker.

It is created exclusively by tracker_builder.py.

Analysis modules SHALL operate on TrackerModel objects and never directly
on TrackerTemplate objects.

This object contains resolved geometry and engineering definitions but
performs no calculations.

========================================================================
"""

from dataclasses import dataclass, field

from core.section_properties import SectionProperties


# ======================================================================
# Geometry
# ======================================================================

@dataclass
class SupportLocation:
    """
    One tracker support.
    """

    index: int

    station: float

    section_name: str

    section: SectionProperties


# ======================================================================

@dataclass
class TorqueTubeSegment:
    """
    One continuous torque tube segment.
    """

    index: int

    start_station: float

    end_station: float

    length: float

    section_name: str

    section: SectionProperties


# ======================================================================

@dataclass
class ModuleGroup:
    """
    Modules contained within a span.
    """

    span_index: int

    module_count: float


# ======================================================================
# Tracker Model
# ======================================================================

@dataclass
class TrackerModel:
    """
    Fully assembled tracker.
    """

    #
    # Metadata
    #

    template_name: str = ""

    manufacturer: str = ""

    model: str = ""

    version: str = ""

    #
    # Overall Geometry
    #

    tracker_length: float = 0.0

    cantilever_start: float = 0.0

    cantilever_end: float = 0.0

    #
    # Derived Geometry
    #

    support_locations: list[SupportLocation] = field(
        default_factory=list
    )

    span_lengths: list[float] = field(
        default_factory=list
    )

    #
    # Structural Members
    #

    torque_tubes: list[TorqueTubeSegment] = field(
        default_factory=list
    )

    #
    # Modules
    #

    module_groups: list[ModuleGroup] = field(
        default_factory=list
    )

    total_module_count: float = 0.0

    #
    # Global Properties
    #

    total_mass: float = 0.0

    center_of_gravity: float = 0.0

    #
    # Future Analysis Objects
    #

    nodes: list = field(
        default_factory=list
    )

    beam_elements: list = field(
        default_factory=list
    )

    shell_elements: list = field(
        default_factory=list
    )