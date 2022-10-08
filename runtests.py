import sys
from pathlib import Path

try:
    from django.conf import settings
    from django.test.utils import get_runner
    root_dir = Path(__file__).resolve().parent

    settings.configure(
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
        DEBUG=True,
        USE_TZ=True,
        # TODO: test on multiple database backends?
        DATABASES={"default": {
            "ENGINE": "django.db.backends.sqlite3",
        }},
        ROOT_URLCONF="django_q_view.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django_q_view",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': []
            }
        }],
        EMAIL_BACKEND='django_q_view.backends.locmem.EmailBackend',
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },
        MEDIA_ROOT=str(root_dir / '.test_media_root/')
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    msg = "To fix this error, run: pip install -r requirements_test.txt"
    raise ImportError(msg)


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
