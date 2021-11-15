from unittest.mock import patch

from django.test import TestCase

from tests.test_app.models import ExampleModel


class SignalTest(TestCase):

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_signals.SignalTest  --settings=tests.settings
    # =======================================================================
    @patch("activation_model_mixin.signals.set_activated.send")
    def test_set_accepted_signal(self, mock):

        example = ExampleModel.objects.create()
        example.set_active()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

    @patch("activation_model_mixin.signals.set_deactivated.send")
    def test_set_rejected_signal(self, mock):

        example = ExampleModel.objects.create(is_active=True)
        example.set_inactive()
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)
