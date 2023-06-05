from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from typing import Self


class GetOrNew(models.Model):
    # Required to be able to subclass models.Model
    class Meta:  # type: ignore - Abstract Meta classes always throw type errors
        abstract = True

    def get_or_new(self, **values: str | int | models.Model) -> tuple[Self, bool]:
        """This is different than get_or_create but very similiar

        get_or_create will create and save a new object if it doesn't exist

        get_or_new will make a new object that is not saved to the database if it doesn't exist

        This is useful when creating a new entry, but you only have some of the required information required initially

        get_or_create does not support this workflow because it will throw errors for objects missing required values"""
        try:
            return (self.__class__.objects.get(**values), False)
        except self.DoesNotExist:
            return (self.__class__(**values), True)
