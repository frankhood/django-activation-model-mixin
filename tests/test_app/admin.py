from django.contrib import admin

from activation_model_mixin.admin import ActivationModelMixinAdmin
from tests.test_app.models import ExampleModel


class ExampleModelAdmin(ActivationModelMixinAdmin, admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {"fields": (("name",),)},
        ),
    )

    # fields = None


admin.site.register(ExampleModel, ExampleModelAdmin)
