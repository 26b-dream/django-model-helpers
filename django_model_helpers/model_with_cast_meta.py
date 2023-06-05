from __future__ import annotations

from typing import cast

from django.db import models


class ModelWithCastMeta(models.Model):
    """Model in which Meta is cast to the correct type to fix Pylance issues"""

    # Required to be able to subclass models.Model
    class _Meta:
        abstract = True

    # Fixes IncompatibleVariableOverride Pylance issues with Meta class
    # See: https://github.com/microsoft/pylance-release/issues/3814#issuecomment-1376276168
    Meta = cast(type[models.Model.Meta], _Meta)
