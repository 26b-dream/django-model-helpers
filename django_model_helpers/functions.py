"""Useful functions for creating Django models."""

from __future__ import annotations

import inspect

from django.db import models


def auto_unique(*fields: str) -> models.UniqueConstraint:
    """Automatically generate a unique constraint for the given fields

    When using models.UniqueConstraint one of the required parameters is the name of the constraint. It is simpler to
    have this name automatically generated to decrease the possibility of accidently making two constraints with the
    same name.

    Args:
        *fields: The names of the fields that should be unique together.

    Returns:
        A `UniqueConstraint` instance that can be used to enforce uniqueness on the specified fields.
    Raises:
        `ValueError`: If the function is not called from within the `Meta` class of a model."""

    # This function may not be reliable because it relies on undocumented behavior of the inspect module
    # See: https://stackoverflow.com/questions/900392/getting-the-caller-function-name-inside-another-function-in-python
    # To help ensure the function fails gracefully check if the Meta class is the caller because it should always be
    # first caller followed by the actual model class
    if inspect.stack()[1].function != "Meta":
        raise ValueError("sketchy_lazy_namer has lived up to it's name and somethign went wrong")
    print(f"{inspect.stack()[2].function}_{'_'.join(fields)}")

    return models.UniqueConstraint(fields=fields, name=f"{inspect.stack()[2].function}_{'_'.join(fields)}")
