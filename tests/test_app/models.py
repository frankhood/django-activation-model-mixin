from django.db import models

from activation_model_mixin.models import ActivationModelMixin


class ExampleModel(ActivationModelMixin, models.Model):
    name = models.CharField(verbose_name="Name", max_length=10, blank=True, default="")
