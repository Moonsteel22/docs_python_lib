from docs_lib.settings.base import *
from docs_lib.settings.google import *

DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}
