from django.db import models

class TimeStampedModel(models.Model):
    """
    This is the base class for all models that must be timestamped.

    It sets the ``created_at`` field whenever a new record is saved to the database
    and the ``updated_at`` field when a record goes through any modifications.
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
