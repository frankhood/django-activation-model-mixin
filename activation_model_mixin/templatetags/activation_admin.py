# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals
import logging

from django import template
from django.utils.translation import ugettext, ugettext_lazy as _

register = template.Library()

logger = logging.getLogger(__name__)


@register.inclusion_tag("admin/activation/submit_line.html", takes_context=True)
def activation_submit_row(context):

    opts = context["opts"]
    change = context["change"]
    is_popup = context["is_popup"]
    save_as = context["save_as"]
    ctx = {
        "opts": opts,
        "show_delete_link": (
            not is_popup
            and context["has_delete_permission"]
            and change
            and context.get("show_delete", True)
        ),
        "show_save_as_new": not is_popup and change and save_as,
        "show_save_and_add_another": (
            context["has_add_permission"]
            and not is_popup
            and (not save_as or context["add"])
        ),
        "show_save_and_continue": not is_popup and context["has_change_permission"],
        "is_popup": is_popup,
        "show_save": True,
        "preserved_filters": context.get("preserved_filters"),
        # nuovi bottoni
        "show_set_active": (
            not is_popup
            and context["original"]
            and context["original"].is_activable()
            and context.get("original", None)
            and not is_popup
            and context["has_change_permission"]
        ),
        "show_set_inactive": (
            not is_popup
            and context["original"]
            and context["original"].is_deactivable()
            and context.get("original", None)
            and not is_popup
            and context["has_change_permission"]
        ),
    }
    if context.get("original") is not None:
        ctx["original"] = context["original"]
    return ctx
