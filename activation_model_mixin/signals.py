# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import logging

from django.dispatch.dispatcher import Signal

logger = logging.getLogger(__name__)

set_activated = Signal(providing_args=["instance", "explicit"])
set_deactivated = Signal(providing_args=["instance", "explicit"])
