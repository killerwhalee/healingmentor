"""
Utilities

This file defines utilities for general use.
Add any functions to call from any applications.

"""


def uuid_filepath(instance, filename):
    """
    Generate filepath regarding instance

    File name is renamed into uuid

    """

    import os
    from uuid import uuid4

    app_name = instance.__class__._meta.app_label.lower()
    model_name = instance.__class__.__name__.lower()
    uuid_name = uuid4().hex
    _, ext = os.path.splitext(filename)

    return f"{app_name}/{model_name}/{uuid_name}{ext.lower()}"
