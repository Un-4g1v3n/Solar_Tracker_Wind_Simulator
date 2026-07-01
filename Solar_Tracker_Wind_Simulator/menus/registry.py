"""
==============================================================

Plugin Registry

Every executable module registers itself here.

The application never imports engineering modules directly.

==============================================================
"""

from dataclasses import dataclass
from typing import Callable


# ============================================================
# MENU ITEM
# ============================================================

@dataclass
class MenuItem:

    category: str
    name: str
    description: str
    callback: Callable


# ============================================================
# GLOBAL REGISTRY
# ============================================================

_registry = []


# ============================================================
# REGISTER
# ============================================================

def register(category: str,
             name: str,
             description: str,
             callback):

    _registry.append(

        MenuItem(

            category=category,
            name=name,
            description=description,
            callback=callback

        )

    )


# ============================================================
# GET ALL
# ============================================================

def get_all():

    return sorted(

        _registry,

        key=lambda item: (

            item.category,

            item.name

        )

    )


# ============================================================
# GET CATEGORY
# ============================================================

def get_categories():

    return sorted(

        {

            item.category

            for item in _registry

        }

    )


def get_category(category):

    return sorted(

        [

            item

            for item in _registry

            if item.category == category

        ],

        key=lambda x: x.name

    )