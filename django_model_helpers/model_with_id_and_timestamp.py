from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from typing import Optional

    from extended_path import ExtendedPath


class ModelWithIdAndTimestamp(models.Model):
    """Basic Model that includes an auto incrmented id, info_timestamp, and info_modified_timestamp and some related functions"""

    class Meta:  # type: ignore - Abstract Meta classes always throw type errors
        abstract = True  # Required to be able to subclass models.Model

    # Automatically genenrated ID
    id = models.AutoField(primary_key=True)

    # Timestamps
    info_timestamp = models.DateTimeField()
    # If I modify information by hand I do not want the timestamp to auto-update
    # Therefore this timestamp needs to be manually updated
    info_modified_timestamp = models.DateTimeField()

    def is_up_to_date(
        self,
        minimum_info_timestamp: Optional[datetime] = None,
        minimum_modified_timestamp: Optional[datetime] = None,
    ) -> bool:
        """Check if the model is up to date using minimum_info_timestamp and minimum_modified_timestamp"""

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
        """Check if the model is outdated using minimum_info_timestamp and minimum_modified_timestamp"""
        return not self.is_up_to_date(minimum_info_timestamp, minimum_modified_timestamp)

    def add_timestamps_and_save(self, info_timestamp: ExtendedPath | datetime) -> None:
        self.add_timestamps(info_timestamp)
        self.save()

    def add_timestamps(self, info_timestamp: ExtendedPath | datetime) -> None:
        if isinstance(info_timestamp, ExtendedPath):
            self.info_timestamp = info_timestamp.aware_mtime()
        else:
            self.info_timestamp = info_timestamp.astimezone()

        self.info_modified_timestamp = datetime.now().astimezone()
