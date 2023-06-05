"""Basic Model that includes an auto incrmented id, info_timestamp, and info_modified_timestamp and some related functions"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, cast

from django.db import models

if TYPE_CHECKING:
    from typing import Optional

    from extended_path import ExtendedPath


class ModelWithIdAndTimestamp(models.Model):
    """Basic Model that includes an auto incrmented id, info_timestamp, and info_modified_timestamp and some related functions"""

    # Required to be able to subclass models.Model
    class _Meta:
        abstract = True

    # Fixes IncompatibleVariableOverride Pylance issues with Meta class
    # See: https://github.com/microsoft/pylance-release/issues/3814#issuecomment-1376276168
    Meta = cast(type[models.Model.Meta], _Meta)

    id = models.AutoField(primary_key=True)
    """Automatically generated unique ID"""

    info_timestamp = models.DateTimeField()
    """Timestamp representing when the information in the database was last pulled from an external source"""

    # If I modify information by hand I do not want the timestamp to auto-update
    # Therefore automatically updating timestamps is not appropriate and it must be updated manually
    info_modified_timestamp = models.DateTimeField()
    """Timestamp representing when the information in the database was last modified excluding modifications that are
    done by hand"""

    def is_up_to_date(
        self,
        minimum_info_timestamp: Optional[datetime] = None,
        minimum_modified_timestamp: Optional[datetime] = None,
    ) -> bool:
        """Check if the information in the database is up to date

        Args:
            minimum_info_timestamp (Optional[datetime], optional): The minimum timestamp that the information on the
            database was last pulled from an external source, if none is given just check if the entry exists. Defaults
            to None.
            minimum_modified_timestamp (Optional[datetime], optional): The minimum timestamp that the information on the
            database was last modified programmatically. If none is given jsut check if the entry exists. Defaults to
            None.

        Returns:
            bool: True if the information is up to date, False otherwise"""

        # If no timestamp is present the information has to be outdated
        if not self.info_timestamp or not self.info_modified_timestamp:
            return False

        # Check that minimum_info_timestamp is up to date
        if minimum_info_timestamp and minimum_info_timestamp > self.info_timestamp:
            return False

        # Check that minimum_modified_timestamp is up to date
        if minimum_modified_timestamp and minimum_modified_timestamp > self.info_modified_timestamp:
            return False

        # If other tests passed information is up to date
        return True

    def is_outdated(
        self,
        minimum_info_timestamp: Optional[datetime] = None,
        minimum_modified_timestamp: Optional[datetime] = None,
    ) -> bool:
        """Check if the information in the database is outdated

        Args:
            minimum_info_timestamp (Optional[datetime], optional): The minimum timestamp that the information on the
            database was last pulled from an external source, if none is given just check if the entry exists. Defaults
            to None.
            minimum_modified_timestamp (Optional[datetime], optional): The minimum timestamp that the information on the
            database was last modified programmatically. If none is given jsut check if the entry exists. Defaults to
            None.

        Returns:
            bool: True if the information is outdated, False otherwise"""

        return not self.is_up_to_date(minimum_info_timestamp, minimum_modified_timestamp)

    def add_timestamps_and_save(self, info_timestamp: ExtendedPath | datetime) -> None:
        """Add timestamps to the model and save it

        Args:
            info_timestamp (ExtendedPath | datetime): The timestamp representing when the information was last updated
            from an external source, if an ExtendedPath is given it will be converted to a datetime object."""
        self.add_timestamps(info_timestamp)
        self.save()

    def add_timestamps(self, info_timestamp: ExtendedPath | datetime) -> None:
        """Add timestamps to the model

        Args:
            info_timestamp (ExtendedPath | datetime): The timestamp representing when the information was last updated
            from an external source, if an ExtendedPath is given it will be converted to a datetime object."""
        if isinstance(info_timestamp, ExtendedPath):
            self.info_timestamp = info_timestamp.aware_mtime()
        else:
            self.info_timestamp = info_timestamp.astimezone()

        self.info_modified_timestamp = datetime.now().astimezone()
