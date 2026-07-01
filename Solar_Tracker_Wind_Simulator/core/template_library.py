"""
========================================================================

Template Library

========================================================================

Single interface for all tracker template file operations.

No menus.
No project state.
No user interaction.

Only filesystem operations.

========================================================================
"""

from pathlib import Path
from dataclasses import asdict, fields, dataclass
from datetime import datetime
import yaml

from core.tracker_template import TrackerTemplate


# ============================================================
# Template Folder
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"
TEMPLATE_FOLDER = DATA_FOLDER / "templates"

TEMPLATE_FOLDER.mkdir(parents=True, exist_ok=True)


# ============================================================
# Template Information
# ============================================================

@dataclass
class TemplateInfo:

    name: str

    filename: str

    modified: datetime


# ============================================================
# List Templates
# ============================================================

def list_templates() -> list[TemplateInfo]:
    """
    Return every template in the template folder.

    Sorted alphabetically by template name.
    """

    templates = []

    for path in TEMPLATE_FOLDER.glob("*.yaml"):

        templates.append(

            TemplateInfo(

                name=path.stem,

                filename=path.name,

                modified=datetime.fromtimestamp(
                    path.stat().st_mtime
                )

            )

        )

    templates.sort(key=lambda t: t.name.lower())

    return templates


# ============================================================
# Template Names
# ============================================================

def template_names() -> list[str]:
    """
    Convenience function.

    Returns only template names.
    """

    return [

        template.name

        for template in list_templates()

    ]


# ============================================================
# Exists
# ============================================================

def template_exists(filename: str) -> bool:

    if not filename.endswith(".yaml"):

        filename += ".yaml"

    return (TEMPLATE_FOLDER / filename).exists()


# ============================================================
# Save
# ============================================================

def save_template(
    template: TrackerTemplate,
    filename: str,
):

    if not filename.endswith(".yaml"):

        filename += ".yaml"

    filepath = TEMPLATE_FOLDER / filename

    with open(filepath, "w", encoding="utf-8") as outfile:

        yaml.safe_dump(

            asdict(template),

            outfile,

            sort_keys=False,

            default_flow_style=False,

        )

    return filepath


# ============================================================
# Load
# ============================================================

def load_template(filename: str) -> TrackerTemplate:

    if not filename.endswith(".yaml"):

        filename += ".yaml"

    filepath = TEMPLATE_FOLDER / filename

    with open(filepath, "r", encoding="utf-8") as infile:

        data = yaml.safe_load(infile)

    valid_fields = {

        field.name

        for field in fields(TrackerTemplate)

    }

    filtered = {

        key: value

        for key, value in data.items()

        if key in valid_fields

    }

    return TrackerTemplate(**filtered)


# ============================================================
# Delete
# ============================================================

def delete_template(filename: str):

    if not filename.endswith(".yaml"):

        filename += ".yaml"

    filepath = TEMPLATE_FOLDER / filename

    if filepath.exists():

        filepath.unlink()


# ============================================================
# Rename
# ============================================================

def rename_template(
    old_name: str,
    new_name: str,
):

    if not old_name.endswith(".yaml"):

        old_name += ".yaml"

    if not new_name.endswith(".yaml"):

        new_name += ".yaml"

    old_path = TEMPLATE_FOLDER / old_name

    new_path = TEMPLATE_FOLDER / new_name

    old_path.rename(new_path)

    return new_path


# ============================================================
# Duplicate
# ============================================================

def duplicate_template(
    old_name: str,
    new_name: str,
):

    template = load_template(old_name)

    save_template(template, new_name)