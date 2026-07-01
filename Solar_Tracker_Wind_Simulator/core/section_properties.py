"""
===============================================================================
section_properties.py

Canonical section property library for the Solar Tracker Wind Simulator.

Purpose
-------
This module computes geometric properties for structural cross-sections.
It is intended to be the single source of truth for all finite element,
mass, stiffness, and structural calculations.

All dimensions are SI units.

    Length      meters
    Area        m²
    Inertia     m⁴
    Torsion     m⁴
    Density     kg/m³
    Weight      N/m
    Mass        kg/m

No FE code should ever compute section properties directly.

===============================================================================
"""


from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Optional, Tuple

import numpy as np
# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

STANDARD_GRAVITY = 9.80665

# -----------------------------------------------------------------------------
# Dataclass
# -----------------------------------------------------------------------------


@dataclass
class SectionProperties:
    """
    Generic structural section properties.

    All dimensions are SI.
    """

    # ---------------------------------------------------------
    # Shape Properties
    # ---------------------------------------------------------
    
    name: str


    # ---------------------------------------------------------
    # Required geometric properties
    # ---------------------------------------------------------

    area: float

    Ix: float
    Iy: float
    J: float
    Cw: float
    density: Optional[float] = None
    mass_per_meter: Optional[float] = None
    weight_per_meter: Optional[float] = None
    radius_gyration_x: Optional[float] = None
    radius_gyration_y: Optional[float] = None
    section_modulus_x: Optional[float] = None
    section_modulus_y: Optional[float] = None
    centroid_x: Optional[float] = None
    centroid_y: Optional[float] = None
    
    
    
    width: Optional[float] = None
    height: Optional[float] = None
    outside_diameter: Optional[float] = None
    inside_diameter: Optional[float] = None
    web_thickness: Optional[float] = None
    flange_thickness: Optional[float] = None
    lip_length: Optional[float] = None
    corner_radius: Optional[float] = None
    thickness: Optional[float] = None


    def pretty_print(self) -> None:
        """
        Print all section properties in a readable engineering format.
        """

        print("=" * 70)
        print(self.name)
        print("=" * 70)

        print(f"Area               : {self.area:.8e} m²")
        print(f"Ix                 : {self.Ix:.8e} m⁴")
        print(f"Iy                 : {self.Iy:.8e} m⁴")
        print(f"J                  : {self.J:.8e} m⁴")
        
        if self.Cw is not None:
            print(f"Cw                 : {self.Cw:.8e} m⁶")
        if self.section_modulus_x is not None:
            print(f"section_modulus_x  : {self.section_modulus_x:.8e} m³")
        if self.section_modulus_y is not None:
            print(f"section_modulus_y  : {self.section_modulus_y:.8e} m³")

        if self.radius_gyration_x is not None:
            print(f"radius_gyration_x  : {self.radius_gyration_x:.8e} m")
        if self.radius_gyration_y is not None:
            print(f"radius_gyration_y  : {self.radius_gyration_y:.8e} m")
        
        if self.width is not None:
             print(f"width              : {self.width} m")
        if self.height is not None:
             print(f"height             : {self.height} m")
        if self.outside_diameter is not None:
             print(f"outside_diameter   : {self.outside_diameter} m")
        if self.inside_diameter is not None:
             print(f"inside_diameter    : {self.inside_diameter:.8e} m")
        if self.web_thickness is not None:
             print(f"web_thickness      : {self.web_thickness} m")
        if self.flange_thickness is not None:
             print(f"flange_thickness  : {self.flange_thickness} m")
        if self.lip_length is not None:
             print(f"lip_length        : {self.lip_length} m")
        if self.corner_radius is not None:
             print(f"corner_radius     : {self.corner_radius} m")
        if self.thickness is not None:
             print(f"thickness         : {self.thickness} m")
             
        print()

        print(f"Density            : {self.density:.3f} kg/m³")
        print(f"Mass / meter       : {self.mass_per_meter:.5f} kg/m")
        print(f"Weight / meter     : {self.weight_per_meter:.5f} N/m")

        print("=" * 70)

        

# ============================================================
# INTERNAL GEOMETRY HELPERS
# ============================================================

def _combine_rectangles(rectangles):
    """
    Combine an arbitrary number of rectangles into a single section.

    Each rectangle is defined as

        (
            width,
            height,
            centroid_x,
            centroid_y
        )

    All dimensions are in meters.

    Returns
    -------
    dict containing

        area
        centroid_x
        centroid_y
        Ix
        Iy

    using the Parallel Axis Theorem.
    """

    if len(rectangles) == 0:
        raise ValueError("At least one rectangle is required.")

    # --------------------------------------------------------
    # AREA
    # --------------------------------------------------------

    total_area = 0.0

    for width, height, _, _ in rectangles:

        total_area += width * height

    # --------------------------------------------------------
    # GLOBAL CENTROID
    # --------------------------------------------------------

    centroid_x = 0.0
    centroid_y = 0.0

    for width, height, x, y in rectangles:

        area = width * height

        centroid_x += area * x
        centroid_y += area * y

    centroid_x /= total_area
    centroid_y /= total_area

    # --------------------------------------------------------
    # SECOND MOMENTS OF AREA
    # --------------------------------------------------------

    Ix = 0.0
    Iy = 0.0

    for width, height, x, y in rectangles:

        area = width * height

        # local centroidal inertias

        Ix_local = width * height**3 / 12.0
        Iy_local = height * width**3 / 12.0

        dx = x - centroid_x
        dy = y - centroid_y

        Ix += Ix_local + area * dy**2
        Iy += Iy_local + area * dx**2

    return {
        
        "area": total_area,

        "centroid_x": centroid_x,
        "centroid_y": centroid_y,

        "Ix": Ix,
        "Iy": Iy
    }

# ============================================================
# COMMON SECTION DERIVED PROPERTIES
# ============================================================

def _derive_section_properties(
    area,
    Ix,
    Iy,
    density,
    g=9.80665
):
    """
    Compute common derived section properties.

    Returns
    -------
    dict containing

        
        radius_gyration_x
        radius_gyration_y
        mass_per_meter
        weight_per_meter
    """

    return {

       

        "radius_gyration_x":
            np.sqrt(Ix / area),

        "radius_gyration_y":
            np.sqrt(Iy / area),

        "mass_per_meter":
            area * density,

        "weight_per_meter":
            area * density * g
    }

# -----------------------------------------------------------------------------
# Internal utility functions
# -----------------------------------------------------------------------------


def _mass_per_meter(area: float, density: float) -> float:
    """
    Computes linear mass.
    """
    return area * density


def _weight_per_meter(mass_per_meter: float) -> float:
    """
    Computes linear weight.
    """
    return mass_per_meter * STANDARD_GRAVITY


def _radius_of_gyration(I: float, area: float) -> float:
    """
    Radius of gyration.

    r = sqrt(I/A)
    """

    if area <= 0:
        raise ValueError("Area must be positive.")

    return sqrt(I / area)


def _section_modulus(I: float, c: float) -> float:
    """
    Elastic section modulus.

    S = I / c
    """

    if c <= 0:
        raise ValueError("Extreme fiber distance must be positive.")

    return I / c


# -----------------------------------------------------------------------------
# Validation helpers
# -----------------------------------------------------------------------------


def require_positive(**values) -> None:
    """
    Ensures every supplied value is positive.

    Example

        require_positive(width=b,
                         height=h,
                         thickness=t)
    """

    for name, value in values.items():

        if value <= 0:

            raise ValueError(
                f"{name} must be positive "
                f"(received {value})"
            )


# -----------------------------------------------------------------------------
# Built Shapes Section
# -----------------------------------------------------------------------------

###Solid Rectangle
 
def rectangle(
    width: float,
    height: float,
    density: float = 7850.0,
    name: str = "Rectangle",
):

    require_positive(
        width=width,
        height=height,
        density=density,
    )

    # -------------------------------------------------------------
    # Geometry represented as one rectangle
    # -------------------------------------------------------------

    rectangles = [
        (
            width,
            height,
            width / 2,
            height / 2,
        )
    ]

    props = _combine_rectangles(rectangles)

    area = props["area"]

    centroid_x = props["centroid_x"]
    centroid_y = props["centroid_y"]

    Ix = props["Ix"]
    Iy = props["Iy"]

    # -------------------------------------------------------------
    # Saint-Venant torsion constant
    # -------------------------------------------------------------

    a = max(width, height)
    b = min(width, height)

    beta = b / a

    J = (
        a
        * b**3
        * (
            1.0 / 3.0
            - 0.21 * beta * (1.0 - beta**4 / 12.0)
        )
    )

    # -------------------------------------------------------------
    # Warping constant
    # -------------------------------------------------------------

    Cw = 0.0

    # -------------------------------------------------------------
    # Derived engineering properties
    # -------------------------------------------------------------

    derived = _derive_section_properties(
        area=area,
        Ix=Ix,
        Iy=Iy,
        density=density,
        )
   
    # -------------------------------------------------------------
    # Section Modulus
    # -------------------------------------------------------------
    section_modulus_x = Ix / (height / 2)
    section_modulus_y = Iy / (width / 2)

    # -------------------------------------------------------------
    # Build object
    # -------------------------------------------------------------

    return SectionProperties(

        name=name,

        area=area,

        Ix=Ix,
        Iy=Iy,
        J=J,
        Cw=Cw,

        section_modulus_x=section_modulus_x,
        section_modulus_y=section_modulus_y,

        radius_gyration_x=derived["radius_gyration_x"],
        radius_gyration_y=derived["radius_gyration_y"],

        mass_per_meter=derived["mass_per_meter"],
        weight_per_meter=derived["weight_per_meter"],

        density=density,

        centroid_x=centroid_x,
        centroid_y=centroid_y,
    )

### Hollow Rectangle

def rectangular_tube(width: float,
    height: float,
    thickness: float,
    density: float = 7850.0,
    name: str = "Rectangular_Tube",
):

    require_positive(
        width=width,
        height=height,
        density=density,
    )

    # -------------------------------------------------------------
    # Geometry represented as rectangles
    # -------------------------------------------------------------

    rectangles = [

    (
        width,
        thickness,
        width/2,
        height-thickness/2
    ),

    (
        width,
        thickness,
        width/2,
        thickness/2
    ),

    (
        thickness,
        height-2*thickness,
        thickness/2,
        height/2
    ),

    (
        thickness,
        height-2*thickness,
        width-thickness/2,
        height/2
    )

]
    props = _combine_rectangles(rectangles)

    area = props["area"]

    centroid_x = props["centroid_x"]
    centroid_y = props["centroid_y"]

    Ix = props["Ix"]
    Iy = props["Iy"]
    
    # -------------------------------------------------------------
    # Thin-wall torsional constant
    #
    # Roark / AISC approximation
    #
    # Accurate for ordinary HSS members.
    # -------------------------------------------------------------

    mid_width = width - thickness
    mid_height = height - thickness

    perimeter_mid = 2.0 * (mid_width + mid_height)

    enclosed_area = mid_width * mid_height

    J = (
        4.0
        * enclosed_area**2
        * thickness
        / perimeter_mid
    )

    # -------------------------------------------------------------
    # Warping constant
    #
    # Closed sections exhibit very small warping.
    # We keep Cw = 0 until the advanced torsional solver
    # is implemented.
    # -------------------------------------------------------------

    Cw = 0.0

    # -------------------------------------------------------------
    # Derived engineering properties
    # -------------------------------------------------------------

    derived = _derive_section_properties(
        area=area,
        Ix=Ix,
        Iy=Iy,
        density=density,
        )
   
    # -------------------------------------------------------------
    # Section Modulus
    # -------------------------------------------------------------
    section_modulus_x = Ix / (height / 2)
    section_modulus_y = Iy / (width / 2)
   
    # -------------------------------------------------------------
    # Build object
    # -------------------------------------------------------------


    return SectionProperties(

        name=name,

        area=area,

        Ix=Ix,
        Iy=Iy,
        J=J,
        Cw=Cw,

        section_modulus_x=section_modulus_x,
        section_modulus_y=section_modulus_y,

        radius_gyration_x=derived["radius_gyration_x"],
        radius_gyration_y=derived["radius_gyration_y"],

        mass_per_meter=derived["mass_per_meter"],
        weight_per_meter=derived["weight_per_meter"],

        density=density,

        
        centroid_x=centroid_x,
        centroid_y=centroid_y,
    )


def circular_tube(
    outside_diameter: float,
    thickness: float,
    density: float = 7850.0,
    name: str = "Circular Tube",
) -> SectionProperties:
 

    require_positive(
        outside_diameter=outside_diameter,
        thickness=thickness,
        density=density,
    )

    if thickness >= outside_diameter / 2:
        raise ValueError(
            "Wall thickness is larger than tube radius."
        )

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    D = outside_diameter
    d = D - 2.0 * thickness

    area = np.pi / 4.0 * (D**2 - d**2)

    centroid_x = D / 2.0
    centroid_y = D / 2.0

    # ---------------------------------------------------------
    # Second moments
    # ---------------------------------------------------------

    Ix = np.pi / 64.0 * (D**4 - d**4)

    Iy = Ix

    # ---------------------------------------------------------
    # Polar torsion constant
    #
    # For circular sections:
    # J = Ix + Iy
    # (this is exact)
    # ---------------------------------------------------------

    J = np.pi / 32.0 * (D**4 - d**4)

    # ---------------------------------------------------------
    # Warping constant
    #
    # Closed circular tubes do not develop
    # restrained warping in Saint-Venant torsion.
    # ---------------------------------------------------------

    Cw = 0.0
    
    # -------------------------------------------------------------
    # Derived engineering properties
    # -------------------------------------------------------------

    derived = _derive_section_properties(
        area=area,
        Ix=Ix,
        Iy=Iy,
        density=density,
        )
   
    # -------------------------------------------------------------
    # Section Modulus
    # -------------------------------------------------------------
    section_modulus_x = Ix / (outside_diameter / 2)
    section_modulus_y = section_modulus_x

    # -------------------------------------------------------------
    # Build object
    # -------------------------------------------------------------
     
      
    return SectionProperties(

        name=name,

        area=area,

        Ix=Ix,
        Iy=Iy,
        J=J,
        Cw=Cw,

        section_modulus_x=section_modulus_x,
        section_modulus_y=section_modulus_y,

        radius_gyration_x=derived["radius_gyration_x"],
        radius_gyration_y=derived["radius_gyration_y"],

        mass_per_meter=derived["mass_per_meter"],
        weight_per_meter=derived["weight_per_meter"],

        density=density,

        
        centroid_x=centroid_x,
        centroid_y=centroid_y,
    )

def circular_bar(
    outside_diameter: float,
    density: float = 7850.0,
    name: str = "Circular Bar",
) -> SectionProperties:
 

    require_positive(
        outside_diameter=outside_diameter,
        density=density,
    )

    # ---------------------------------------------------------
    # Geometry
    # ---------------------------------------------------------

    D = outside_diameter

    area = np.pi / 4.0 * (D**2)

    centroid_x = D / 2.0
    centroid_y = D / 2.0

    # ---------------------------------------------------------
    # Second moments
    # ---------------------------------------------------------

    Ix = np.pi / 64.0 * (D**4)

    Iy = Ix

    # ---------------------------------------------------------
    # Polar torsion constant
    #
    # For circular sections:
    # J = Ix + Iy
    # (this is exact)
    # ---------------------------------------------------------

    J = np.pi / 32.0 * (D**4)

    # ---------------------------------------------------------
    # Warping constant
    #
    # Closed circular tubes do not develop
    # restrained warping in Saint-Venant torsion.
    # ---------------------------------------------------------

    Cw = 0.0
    
    # -------------------------------------------------------------
    # Derived engineering properties
    # -------------------------------------------------------------

    derived = _derive_section_properties(
        area=area,
        Ix=Ix,
        Iy=Iy,
        density=density,
        )
   
    # -------------------------------------------------------------
    # Section Modulus
    # -------------------------------------------------------------
    section_modulus_x = Ix / (outside_diameter / 2)
    section_modulus_y = section_modulus_x

    # -------------------------------------------------------------
    # Build object
    # -------------------------------------------------------------
     
      
    return SectionProperties(

        name=name,

        area=area,

        Ix=Ix,
        Iy=Iy,
        J=J,
        Cw=Cw,

        section_modulus_x=section_modulus_x,
        section_modulus_y=section_modulus_y,

        radius_gyration_x=derived["radius_gyration_x"],
        radius_gyration_y=derived["radius_gyration_y"],

        mass_per_meter=derived["mass_per_meter"],
        weight_per_meter=derived["weight_per_meter"],

        density=density,

        
        centroid_x=centroid_x,
        centroid_y=centroid_y,
    )

# ============================================================
# CHANNEL SECTION
# ============================================================

def channel(
    depth,
    flange_width,
    web_thickness,
    flange_thickness,
    density=7850.0,
    name="Channel Section",
):
    require_positive(
        depth=depth,
        flange_width=flange_width,
        web_thickness=web_thickness,
        flange_thickness=flange_thickness,
        density=density,
    )

    # -------------------------------------------------------------
    # Geometry represented as one rectangle
    # -------------------------------------------------------------
    rectangles = [

    (
        flange_width,
        flange_thickness,
        flange_width/2,
        depth-flange_thickness/2
    ),

    (
        flange_width,
        flange_thickness,
        flange_width/2,
        flange_thickness/2
    ),

    (
        web_thickness,
        depth-2*flange_thickness,
        web_thickness/2,
        depth/2
    )
]


    props = _combine_rectangles(rectangles)
    area = props["area"]

    centroid_x = props["centroid_x"]
    centroid_y = props["centroid_y"]

    Ix = props["Ix"]
    Iy = props["Iy"]

    # --------------------------------------------------------
    # APPROXIMATE TORSION CONSTANT
    #
    # Saint-Venant thin-wall approximation
    # --------------------------------------------------------

    J = (
       (2.0 * flange_width * flange_thickness**3)
        + (
            (depth - 2.0 * flange_thickness)
            * web_thickness**3
        )
    ) / 3.0

    # -------------------------------------------------------------
    # Warping constant
    # -------------------------------------------------------------

    Cw = 0.0

    # -------------------------------------------------------------
    # Derived engineering properties
    # -------------------------------------------------------------

    derived = _derive_section_properties(
        area=area,
        Ix=Ix,
        Iy=Iy,
        density=density,
       )
 
    # -------------------------------------------------------------
    # Section Modulus
    # -------------------------------------------------------------
    section_modulus_x = Ix / (depth / 2)
    section_modulus_y = Iy / (flange_width / 2)
    
 
 
    # --------------------------------------------------------
    # Build object
    # --------------------------------------------------------
    
    
    return SectionProperties(

        name=name,

        area=area,

        Ix=Ix,
        Iy=Iy,
        J=J,
        Cw=Cw,

        section_modulus_x=section_modulus_x,
        section_modulus_y=section_modulus_y,

        radius_gyration_x=derived["radius_gyration_x"],
        radius_gyration_y=derived["radius_gyration_y"],

        mass_per_meter=derived["mass_per_meter"],
        weight_per_meter=derived["weight_per_meter"],

        density=density,

        
        centroid_x=centroid_x,
        centroid_y=centroid_y,
    )
    
# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("SECTION PROPERTIES LIBRARY")
    print("=" * 70)

    rect = rectangle(
            width=0.100,
            height=0.050,
            
    )

    rect.pretty_print()


    tube = rectangular_tube(
        width=0.1016,
        height=0.1016,
        thickness=0.0037,
        name="4-inch Torque Tube",
    )

    tube.pretty_print()


    pipe = circular_tube(
        outside_diameter=0.1683,
        thickness=0.00711,
        name="6 inch Sch40 Pipe",
    )

    pipe.pretty_print()

    bar = circular_bar(
        outside_diameter=0.1683,
        name="6 inch bar",
    )

    bar.pretty_print()

    print("\n=== Channel Test ===")

    channel = channel(
        depth=0.193548,
        flange_width=0.1143,
        web_thickness=0.00381,
        flange_thickness=0.00381,
    )

    channel.pretty_print()