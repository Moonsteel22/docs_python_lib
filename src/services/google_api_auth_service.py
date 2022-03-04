import os.path

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class GoogleApiServices(Singleton):
    """
    Singleton class service for accessing Google resources
    """

    def _refresh(self):
        if self.creds and self.creds.expired:
            self.creds.refresh(Request())

    def __init__(self):
        self._docs_service: Resource = None
        self._drive_service: Resource = None
        if os.path.exists(settings.CREDENTIALS_SERVICE):
            creds: service_account.Credentials = (
                service_account.Credentials.from_service_account_file(
                    settings.CREDENTIALS_SERVICE,
                    scopes=settings.SCOPES,
                )
            )
            self._creds = creds

    @property
    def docs_service(self):
        self._refresh()
        if not self._docs_service:
            self._docs_service = build("docs", "v1", credentials=self._creds)
        return self._docs_service

    @property
    def drive_service(self):
        self._refresh()
        if not self._drive_service:
            self._drive_service = build("drive", "v3", credentials=self._creds)
        return self._drive_service

    @property
    def creds(self):
        return self._creds
