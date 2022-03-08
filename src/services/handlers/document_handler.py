from docs_python_lib.src.services.google_api_auth_service import GoogleApiServices


class DocumentHandler:
    def __init__(
        self,
        documentId: str,
        google_services: GoogleApiServices = GoogleApiServices(),
    ):
        self.documentId = documentId
        self.google_services = google_services
