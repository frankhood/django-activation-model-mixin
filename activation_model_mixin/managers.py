from django.db import models

from activation_model_mixin.querysets import ActivationQuerySet


class ActivationEntryManager(models.Manager):
    def get_queryset(self):
        return ActivationQuerySet(self.model, using=self._db)


class ActiveActivationEntryManager(ActivationEntryManager):
    def get_queryset(self):
        return super(ActiveActivationEntryManager, self).get_queryset().active_items()


class InactiveActivationEntryManager(ActivationEntryManager):
    def get_queryset(self):
        return (
            super(InactiveActivationEntryManager, self).get_queryset().inactive_items()
        )
