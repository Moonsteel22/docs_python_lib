from docs_python_lib.src.services.functions import generate_request
from docs_python_lib.src.services.google_api_auth_service import GoogleApiServices
from docs_python_lib.src.services.types.base import DocumentRequest


class DocumentHandler:
    """
    The idea of methods of this class is
    return list of requests and end_index.

    After all methods executing, we just send
    list of requests to batchUpdate method and
    update document with 1 request to google docs api
    """

    def __init__(
        self,
        documentId: str,
        google_services: GoogleApiServices = GoogleApiServices(),
    ):
        self.documentId = documentId
        self.google_services = google_services

    def batchUpdate(self, requests: list[DocumentRequest]):

        self.google_services.docs_service.documents().batchUpdate(
            documentId=self.documentId,
            body={"requests": [generate_request(request) for request in requests]},
        ).execute()
