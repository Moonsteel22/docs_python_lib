import os

from base import BASE_URL

# Social Account Settings

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}


ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

LOGIN_REDIRECT_URL = BASE_URL + "/profile"

LOGOUT_REDIRECT_URL = BASE_URL

GENERATED_CVS_FOLDER = os.environ.get("GENERATED_CVS_FOLDER", "default_folder")
