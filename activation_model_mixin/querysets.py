from django.db import models


class ActivationQuerySet(models.QuerySet):
    def active_items(self):
        return self.filter(is_active=True)

    def inactive_items(self):
        return self.filter(is_active=False)
