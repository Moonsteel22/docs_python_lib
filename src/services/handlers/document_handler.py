from docs_python_lib.src.services.functions import generate_request
from docs_python_lib.src.services.google_api_auth_service import GoogleApiServices
from docs_python_lib.src.services.types.base import DocumentRequest
from docs_python_lib.src.services.types.classes import Location
from docs_python_lib.src.services.types.classes import Range
from docs_python_lib.src.services.types.classes import TableCellLocation
from docs_python_lib.src.services.types.classes import TextStyle
from docs_python_lib.src.services.types.requests import InsertTableRow
from docs_python_lib.src.services.types.requests import InsertText
from docs_python_lib.src.services.types.requests import UpdateTextStyle


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

    def insert_text(
        self,
        text: str,
        location: Location,
        text_style: TextStyle = None,
    ) -> tuple[int, list[DocumentRequest]]:
        end_index = location.index + len(text)
        requests = [InsertText(text=text, location=location)]
        if text_style:
            requests.append(
                UpdateTextStyle(
                    text_style=text_style,
                    range=Range(
                        start_index=location.index,
                        end_index=end_index,
                        segment_id="",
                    ),
                ),
            )
        return end_index, requests

    def insert_table_row(
        self,
        columns: int,
        table_cell_location: TableCellLocation,
    ) -> tuple[int, list[DocumentRequest]]:

        return 1 + 2 * columns, [
            InsertTableRow(table_cell_location=table_cell_location, insert_below=True),
        ]
