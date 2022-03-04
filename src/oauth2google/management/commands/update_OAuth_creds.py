import json
import logging

from allauth.socialaccount.models import SocialApp
from django.conf import settings
from django.core.management import BaseCommand
from dotenv import find_dotenv
from dotenv import load_dotenv

load_dotenv(find_dotenv())


class Command(BaseCommand):
    help = "This command update Social App in database by provided creds"

    def handle(self, *args, **options):

        with open(settings.CREDENTIALS_AUTH) as j:
            creds = json.load(j)["web"]

        app: SocialApp = SocialApp.objects.first()
        app.secret = creds["client_secret"]
        app.client_id = creds["client_id"]

        app.save()

        logging.info(msg="Replaced client_id anf client_secret in Social App")
