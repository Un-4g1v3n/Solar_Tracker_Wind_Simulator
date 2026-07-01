# core/tracker_mesh.py

#All geometry originates from tracker_definition.py.


from dataclasses import dataclass

import numpy as np

from core.tracker_definition import (
    num_spans,
    modules_per_span,
    modules_per_cantilever,
    span_length,
    cantilever_length,
)


# ============================================================
# DATA CLASS
# ============================================================

@dataclass(frozen=True)
class TrackerMesh:
    
    #Finite element representation of one tracker row.
    

    num_spans: int

    modules_per_span: int

    modules_per_cantilever: int

    span_length: float

    cantilever_length: float

    supported_length: float

    total_length: float

    num_elements: int

    num_nodes: int

    element_length: float

    support_nodes: list

    node_positions: np.ndarray

    connectivity: list

    span_elements: list

    cantilever_elements: list

    cantilever_start_element: int


# ============================================================
# MESH BUILDER
# ============================================================

def build_tracker_mesh() -> TrackerMesh:
    
    #Build a finite element mesh from tracker_definition.py.
    

    supported_length = (
        num_spans
        * span_length
    )

    total_length = (
        supported_length
        + cantilever_length
    )

 
    num_elements = (
        num_spans * modules_per_span
        + modules_per_cantilever
    )

    num_nodes = (
        num_elements + 1
    )

    element_length = (
        total_length
        / num_elements
    )

    #
    # Support locations
    #

    support_nodes = [

        i * modules_per_span

        for i in range(
            num_spans + 1
        )

    ]

    #
    # Node coordinates
    #

    node_positions = np.linspace(
        0.0,
        total_length,
        num_nodes
    )

    #
    # Connectivity
    #

    connectivity = [

        (i, i + 1)

        for i in range(
            num_elements
        )

    ]

    #
    # Span elements
    #

    span_elements = list(

        range(

            num_spans
            * modules_per_span

        )

    )

    #
    # Cantilever elements
    #

    cantilever_start = (

        num_spans
        * modules_per_span

    )

    cantilever_elements = list(

        range(

            cantilever_start,
            num_elements

        )

    )

    return TrackerMesh(

        num_spans=num_spans,

        modules_per_span=modules_per_span,

        modules_per_cantilever=modules_per_cantilever,

        span_length=span_length,

        cantilever_length=cantilever_length,

        supported_length=supported_length,

        total_length=total_length,

        num_elements=num_elements,

        num_nodes=num_nodes,

        element_length=element_length,

        support_nodes=support_nodes,

        node_positions=node_positions,

        connectivity=connectivity,

        span_elements=span_elements,

        cantilever_elements=cantilever_elements,

        cantilever_start_element=cantilever_start,

    )


# ============================================================
# DEFAULT SHARED INSTANCE
# ============================================================

mesh = build_tracker_mesh()