=====
Usage
=====

To use Django Activation Model Mixin in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'activation_model_mixin.apps.ActivationModelMixinConfig',
        ...
    )

Add Django Activation Model Mixin's URL patterns:

.. code-block:: python

    from activation_model_mixin import urls as activation_model_mixin_urls


    urlpatterns = [
        ...
        url(r'^', include(activation_model_mixin_urls)),
        ...
    ]
