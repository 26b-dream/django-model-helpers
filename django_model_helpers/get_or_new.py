"""A mixin that adds a get_or_new method to a model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

from .model_with_cast_meta import ModelWithCastMeta

if TYPE_CHECKING:
    from typing import Self


class GetOrNew(ModelWithCastMeta):
    """A mixin that adds a get_or_new method to a model"""

    def get_or_new(self, **values: str | int | models.Model) -> tuple[Self, bool]:
        """Inspired by get_or_create, but with some differences

        get_or_create will immediatly attempt to create an object even if it doesn't have all the required information,
        get_or_new will not save the object, and instead must be saved manually when all of the information has been
        added to the object

        This is useful for when creating a new object but not all of the information is easily avaialble at the time of
        object initialization

        Argss:
            **values: The keyword arguments used to filter the objects. Must at least include unique fields
        Returns:
            A `tuple` containing the existing object that matches the given values and a boolean indicating whether a new object was created.
        """
        try:
            return (self.__class__.objects.get(**values), False)
        except self.DoesNotExist:
            return (self.__class__(**values), True)
