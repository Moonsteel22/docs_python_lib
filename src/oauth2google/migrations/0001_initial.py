import os

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import migrations
from django.db import transaction
from dotenv import find_dotenv
from dotenv import load_dotenv

PROVIDER_ID = "google"
APP_NAME = "google-oauth2"
SITE_DOMAIN = "example.com"
SITE_NAME = "example"

load_dotenv(find_dotenv())


def set_application(apps, schema_editor):
    with transaction.atomic():
        app = SocialApp(
            provider=PROVIDER_ID,
            name=APP_NAME,
            secret=os.environ.get("GOOGLE_AUTH_CLIENT_SECRET"),
            client_id=os.environ.get("GOOGLE_AUTH_CLIENT_ID"),
        )
        app.save()
        site = Site(domain=SITE_DOMAIN, name=SITE_NAME)
        site.save()
        app = SocialApp.objects.get(name=APP_NAME)
        app.sites.add(site)
        app.save()


class Migration(migrations.Migration):
    dependencies = [
        ("socialaccount", "__latest__"),
    ]

    operations = [migrations.RunPython(set_application)]
