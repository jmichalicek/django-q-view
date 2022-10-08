=====
Usage
=====

To use Django Q View in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_q_view',
        ...
    )

Add Django Q View's URL patterns:

.. code-block:: python

    # You may want to only include this in development environments

    urlpatterns = [
        ...
        path('', include('django_q_view.urls')),
        ...
    ]

