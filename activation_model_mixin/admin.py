# -*- coding: utf-8 -*-
import logging
from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlquote

from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class ActivationModelMixinAdmin(admin.ModelAdmin):
    change_form_template = "admin/activation/activation_change_form.html"

    actions = ["make_active", "make_inactive"]
    SHOW_ACTIVATION = True
    SHOW_ACTIVATION_FILTER = True
    SHOW_ACTIVATION_FIELDSETS = True

    fieldsets_moderation = (
        (_("Activation"), {"fields": (("is_active", "activation_date"),)}),
    )

    def __init__(self, *args, **kwargs):
        super(ActivationModelMixinAdmin, self).__init__(*args, **kwargs)
        if self.SHOW_ACTIVATION and "is_active" not in self.list_display:
            self.list_display = list(self.list_display) + ["is_active"]
        if self.SHOW_ACTIVATION_FILTER and "is_active" not in self.list_filter:
            self.list_filter = list(self.list_filter) + ["is_active"]
        if (
            (not self.SHOW_ACTIVATION)
            and self.change_form_template
            == ActivationModelMixinAdmin.change_form_template
        ):
            logger.warning(
                "Pay Attention! You have to set change_form_template=None "
                "if SHOW_ACTIVATION = False, elsewher set SHOW_ACTIVATION=True "
                "in this ModelAdmin"
            )

    def get_actions(self, request):
        actions = super(ActivationModelMixinAdmin, self).get_actions(request)
        try:
            if not self.SHOW_ACTIVATION:
                actions.pop("make_active")
                actions.pop("make_inactive")
        except KeyError:
            pass
        return actions

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ActivationModelMixinAdmin, self).get_fieldsets(
            request, obj=obj
        )
        if self.SHOW_ACTIVATION_FIELDSETS:
            fieldsets = tuple(list(fieldsets) + list(self.fieldsets_moderation))
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(ActivationModelMixinAdmin, self).get_readonly_fields(
            request, obj
        )
        return list(readonly_fields) + ["is_active", "activation_date"]

    def response_change(self, request, obj):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        msg_dict = {
            "name": force_text(opts.verbose_name),
            "obj": format_html('<a href="{0}">{1}</a>', urlquote(request.path), obj),
        }
        if "_setactive" in request.POST:
            obj.set_active(commit=True, request=request)
            msg = format_html(
                _(
                    'The {name} "{obj}" was set as "active" \
                successfully'
                ),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        if "_setinactive" in request.POST:
            obj.set_inactive(commit=True, request=request)
            msg = format_html(
                _(
                    'The {name} "{obj}" was set as "inactive" \
                successfully'
                ),
                **msg_dict
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        return super(ActivationModelMixinAdmin, self).response_change(request, obj)

    def make_active(self, request, queryset):
        updated_objects = 0
        for obj in queryset:
            if obj.is_activable():
                obj.set_active(commit=True, request=request)
                updated_objects += 1
        message = "{updated_objects} Entry sono state attivate".format(
            **{"updated_objects": updated_objects}
        )
        messages.info(request, message)

    make_active.short_description = _("Activate selected Entries")

    def make_inactive(self, request, queryset):
        updated_objects = 0
        for obj in queryset:
            if obj.is_deactivable():
                obj.set_inactive(commit=True, request=request)
                updated_objects += 1
        message = "{updated_objects} Entry sono state disattivate".format(
            **{"updated_objects": updated_objects}
        )
        messages.info(request, message)

    make_inactive.short_description = _("Deactivate selected Entries")
