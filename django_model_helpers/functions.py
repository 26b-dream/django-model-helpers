import inspect

from django.db import models


def auto_unique(*fields: str) -> models.UniqueConstraint:
    """Automatically generate a unique constraint for the given fields

    By default the constraint requires a name, to avoid name collisions it's easier if the name is automatically generated

    This is done using stack inspection and may not work correctly or consistently"""

    if inspect.stack()[1].function != "Meta":
        raise ValueError("sketchy_lazy_namer has lived up to it's name and somethign went wrong")
    print(f"{inspect.stack()[2].function}_{'_'.join(fields)}")

    return models.UniqueConstraint(fields=fields, name=f"{inspect.stack()[2].function}_{'_'.join(fields)}")
