import re
from typing import Optional
from typing import Union

from src.services.functions import generate_request
from src.services.google_api_auth_service import GoogleApiServices
from src.services.types.base import DocumentRequest
from src.services.types.classes import Location
from src.services.types.classes import Range
from src.services.types.classes import TableCellLocation
from src.services.types.classes import TextStyle
from src.services.types.requests import InsertTableRow
from src.services.types.requests import InsertText
from src.services.types.requests import UpdateTextStyle


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

    def get_doc_json(self) -> dict:
        return (
            self.google_services.docs_service.documents()
            .get(documentId=self.documentId)
            .execute()
        )

    def get_path(
        self,
        regex: str,
        is_many: bool = False,
    ) -> Optional[Union[dict, list[dict]]]:
        """
        Return dict with all struct of provided regex
        is_many:
            if True, function finds all matched texts and
            return all structs
        """

        content = self.get_doc_json()["body"]["content"]

        def _is_here(node) -> Optional[bool]:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "content" and isinstance(value, str):
                        if re.search(regex, value):
                            return True
                    elif not _is_here(value):
                        continue
                    else:
                        return True
            if isinstance(node, list):
                for element in node:
                    return _is_here(element)
            return False

        if is_many:
            elements: list = []
            for element in content:
                if _is_here(element):
                    elements.append(element)
            return elements
        else:
            for element in content:
                if _is_here(element):
                    return element
        return None
