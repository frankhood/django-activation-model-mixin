# -*- coding: utf-8 -*-

import logging

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.db import models
from activation_model_mixin import managers, signals

logger = logging.getLogger(__name__)


class ActivationModelMixin(models.Model):
    SEND_ACTIVATION_SIGNAL_ON_SAVE = True

    objects = managers.ActivationEntryManager()
    active_objects = managers.ActiveActivationEntryManager()
    inactive_objects = managers.InactiveActivationEntryManager()

    activation_date = models.DateTimeField(_("Activation Date"), blank=True, null=True)
    is_active = models.BooleanField(_("Is Active"), default=False)

    class Meta:
        abstract = True

    def is_activable(self):
        return not self.is_active

    def is_deactivable(self):
        return self.is_active

    def save(self, *args, **kwargs):
        if self.is_active and not self.activation_date:
            self.activation_date = timezone.now()
        elif not self.is_active and self.activation_date:
            self.activation_date = None

        _send_signals = (
            kwargs.pop("send_signal", True) and self.SEND_ACTIVATION_SIGNAL_ON_SAVE
        )
        if _send_signals:
            is_active_modified = False
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                if old_instance.is_active != self.is_active:
                    is_active_modified = True
            except self.__class__.DoesNotExist:
                pass
            super(ActivationModelMixin, self).save(*args, **kwargs)
            if is_active_modified:
                if self.is_active:
                    signals.set_activated.send(
                        sender=self.__class__, instance=self, explicit=False
                    )
                else:
                    signals.set_deactivated.send(
                        sender=self.__class__, instance=self, explicit=False
                    )
        else:
            super(ActivationModelMixin, self).save(*args, **kwargs)

    def set_active(self, commit=True, **kwargs):
        self.is_active = True
        if commit:
            self.save(send_signal=False)
            signals.set_activated.send(
                sender=self.__class__, instance=self, explicit=True
            )

    set_active.alters_data = True

    def set_inactive(self, commit=True, **kwargs):
        self.is_active = False
        if commit:
            self.save(send_signal=False)
            signals.set_deactivated.send(
                sender=self.__class__, instance=self, explicit=True
            )

    set_inactive.alters_data = True
