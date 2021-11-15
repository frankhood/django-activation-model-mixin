from django.test import TestCase

from tests.test_app.models import ExampleModel


class ModelTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_models.ModelTest  --settings=tests.settings
    # =======================================================================
    def test_unit(self):
        example = ExampleModel.objects.create()
        self.assertEqual(example.is_active, False)
        self.assertEqual(example.activation_date, None)
        self.assertTrue(example.is_activable())
        self.assertFalse(example.is_deactivable())

        example.set_active()
        self.assertEqual(example.is_active, True)
        self.assertNotEqual(example.activation_date, None)
        self.assertTrue(example.is_deactivable())
        self.assertFalse(example.is_activable())

        example.set_inactive()
        self.assertEqual(example.is_active, False)
        self.assertEqual(example.activation_date, None)
        self.assertTrue(example.is_activable())
        self.assertFalse(example.is_deactivable())
