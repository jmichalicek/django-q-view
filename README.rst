=============================
Django Q View
=============================

.. image:: https://badge.fury.io/py/django-q-view.png
    :target: https://badge.fury.io/py/django-q-view

.. image:: https://github.com/jmichalicek/django-q-view/workflows/Python%20package/badge.svg
    :target: https://github.com/jmichalicek/django-q-view/actions?query=workflow%3A%22Python+package%22

View emails in development without actually sending them.

Documentation
-------------

The full documentation is at https://django-q-view.readthedocs.io.

Quickstart
----------

Install Django Q View::

    pip install django-q-view

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


TODO
-----


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
