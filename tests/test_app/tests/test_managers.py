from django.test import TestCase

from tests.test_app.models import ExampleModel


class ManagerTest(TestCase):

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_managers.ManagerTest  --settings=tests.settings
    # =======================================================================

    def test_active_items(self):

        example = ExampleModel.objects.create()
        self.assertIn(example, ExampleModel.inactive_objects.all())

        example.set_active()

        self.assertIn(example, ExampleModel.active_objects.all())

        example2 = ExampleModel.objects.create(is_active=True)

        self.assertIn(example2, ExampleModel.active_objects.all())
        self.assertNotIn(example2, ExampleModel.inactive_objects.all())

    def test_inactive_items(self):
        example = ExampleModel.objects.create(is_active=True)
        self.assertIn(example, ExampleModel.active_objects.all())
        example.set_inactive()
        self.assertIn(example, ExampleModel.inactive_objects.all())
