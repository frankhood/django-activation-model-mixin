from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage

from tests.test_app.admin import ExampleModelAdmin
from tests.test_app.models import ExampleModel


class ModelAdminTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        super_user = User.objects.create_superuser(
            username='super', email='super@email.org', password='pass'
        )
        self.request = RequestFactory().get('admin/test_app/examplemodel/')
        self.request.user = super_user
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    # =======================================================================
    # ./manage.py test tests.test_app.tests.test_admins.ModelAdminTest  --settings=tests.settings
    # =======================================================================
    def test_utility(self):
        example_model_admin = ExampleModelAdmin(model=ExampleModel, admin_site=AdminSite())
        self.assertIn('is_active', example_model_admin.list_display)
        self.assertIn('is_active', example_model_admin.list_filter)

        self.assertIn('make_active', example_model_admin.get_actions(request=self.request))
        self.assertIn('make_inactive', example_model_admin.get_actions(request=self.request))

        example = ExampleModel.objects.create()
        self.assertIn('is_active', example_model_admin.get_fieldsets(
                request=self.request,
                obj=example
            )[1][1].get('fields')[0]
        )
        self.assertIn('activation_date', example_model_admin.get_fieldsets(
                request=self.request,
                obj=example
            )[1][1].get('fields')[0]
        )

        self.assertIn('is_active', example_model_admin.get_readonly_fields(
                request=self.request,
                obj=example
            )
                      )
        self.assertIn('activation_date', example_model_admin.get_readonly_fields(
            request=self.request,
            obj=example
        ))

        example_model_admin.make_active(request=self.request, queryset=ExampleModel.inactive_objects.all())
        example.refresh_from_db()
        self.assertTrue(example.is_active)

        example_model_admin.make_inactive(request=self.request, queryset=ExampleModel.active_objects.all())
        example.refresh_from_db()
        self.assertFalse(example.is_active)


