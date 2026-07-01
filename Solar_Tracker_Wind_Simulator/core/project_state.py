"""
========================================================================

Project State

========================================================================

This module stores the active engineering objects currently loaded
by the application.

The application should NEVER pass engineering objects directly between
menus.

Instead, every tool reads and writes the active project state.

This behaves similarly to professional CAD/CAE software where there is
one active project loaded at a time.

========================================================================
"""

from dataclasses import dataclass
from typing import Optional, Any

from core.tracker_template import TrackerTemplate


@dataclass
class ProjectState:

    current_template: Optional[TrackerTemplate] = None
    current_template_name: Optional[str] = None
    current_tracker: Any = None
    current_mesh: Any = None
    current_results: Any = None

    # ---------------------------------------------------------
    # Active File Names
    # ---------------------------------------------------------

    template_filename: str | None = None

    project_filename: str | None = None

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    modified: bool = False

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def clear(self):

        self.current_template = None
        self.current_tracker = None
        self.current_mesh = None
        self.current_results = None

        self.template_filename = None
        self.project_filename = None

        self.modified = False

    # ---------------------------------------------------------

    def has_template(self):

        return self.current_template is not None

    # ---------------------------------------------------------

    def has_tracker(self):

        return self.current_tracker is not None

    # ---------------------------------------------------------

    def has_mesh(self):

        return self.current_mesh is not None

    # ---------------------------------------------------------

    def has_results(self):

        return self.current_results is not None


# ======================================================================
# SINGLE GLOBAL PROJECT
# ======================================================================

project_state = ProjectState()