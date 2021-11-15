from django.test import TestCase

from activation_model_mixin.querysets import ActivationQuerySet
from tests.test_app.models import ExampleModel


class QuerySetTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.activation_queryset = ActivationQuerySet(ExampleModel)

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_querysets.QuerySetTest  --settings=tests.settings
    # =======================================================================

    def test_active_items(self):

        example = ExampleModel.objects.create()
        self.assertIn(example, self.activation_queryset.inactive_items())

        example.set_active()

        self.assertIn(example, self.activation_queryset.active_items())
        self.assertNotIn(example, self.activation_queryset.inactive_items())

        example2 = ExampleModel.objects.create(is_active=True)

        self.assertIn(example2, self.activation_queryset.active_items())
        self.assertNotIn(example2, self.activation_queryset.inactive_items())

    def test_inactive_items(self):
        example = ExampleModel.objects.create()
        example.set_active()
        self.assertIn(example, self.activation_queryset.active_items())
        self.assertNotIn(example, self.activation_queryset.inactive_items())

        example.set_inactive()

        self.assertIn(example, self.activation_queryset.inactive_items())
        self.assertNotIn(example, self.activation_queryset.active_items())

        example2 = ExampleModel.objects.create(is_active=True)

        self.assertIn(example2, self.activation_queryset.active_items())
        self.assertNotIn(example2, self.activation_queryset.inactive_items())

        example2.set_inactive()

        self.assertIn(example2, self.activation_queryset.inactive_items())
        self.assertNotIn(example2, self.activation_queryset.active_items())
