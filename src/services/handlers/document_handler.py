import re
from typing import Optional
from typing import Union

from services.types.enum import BulletGlyphPreset

from src.services.functions import generate_request
from src.services.google_api_auth_service import GoogleApiServices
from src.services.types.base import DocumentRequest
from src.services.types.classes import Location
from src.services.types.classes import ParagraphStyle
from src.services.types.classes import Range
from src.services.types.classes import SubstringMatchCriteria
from src.services.types.classes import TableCellLocation
from src.services.types.classes import TextStyle
from src.services.types.requests import CreateParagraphBullets
from src.services.types.requests import InsertTableRow
from src.services.types.requests import InsertText
from src.services.types.requests import ReplaceAllText
from src.services.types.requests import UpdateParagraphStyle
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

    def fill_tag(
        self,
        tag: str,
        value: str,
    ) -> tuple[int, list[DocumentRequest]]:
        """
        Allows to fill tags in document.
        Tag - text in document, which define
        some pattern

        Parameters
        ----------
        tag: str
            text to be replaced
        value: str
            text to replace
        """
        return -1, [
            ReplaceAllText(
                replace_text=value,
                contains_text=SubstringMatchCriteria(text=tag, match_case=True),
            ),
        ]

    def fill_tags(
        self,
        replacements: dict[str, str],
    ) -> tuple[int, list[DocumentRequest]]:
        """
        For multi-replacing tags

        Parameters
        ----------
        replacements: dict[str,str]
            Dict of pairs {'tag':'value'}
        """
        requests = []
        for tag, value in replacements.items():
            _, request = self.fill_tag(tag, value)
            requests += request
        return -1, requests

    def insert_list_element(
        self,
        location: Location,
        text: str,
        bullet: BulletGlyphPreset,
        bullet_style: TextStyle,
        text_style: TextStyle,
        bullet_paragraph_style: ParagraphStyle,
    ) -> tuple[int, list[DocumentRequest]]:
        """
        Allows to insert list element to document

        Also it can be used to add element with
        bullet style and text style. This feature
        is supported via extra space between text
        and bullet.

        Parameters
        ----------
        location: Location
            position of text in document
        text: str
            text to be placed in list element
        bullet: BulletGlyphPreset
            bullet type
        bullet_style: TextStyle
            bullet style (color for example)
        text_style: TextStyle
            text style
        bullet_paragraph_style: ParagraphStyle
            bullet style as paragraph (size, space between text, etc.)
        """

        text = " " + text + "\n"
        end_index = location.index + len(text)

        bullet_range = Range(
            start_index=location.index,
            end_index=end_index,
            segment_id="",
        )

        text_range = Range(
            start_index=location.index + 1,
            end_index=end_index,
            segment_id="",
        )

        return end_index, [
            InsertText(text=text, location=location),
            CreateParagraphBullets(range=bullet_range, bullet_preset=bullet),
            UpdateParagraphStyle(
                paragraph_style=bullet_paragraph_style,
                range=bullet_range,
            ),
            UpdateTextStyle(text_style=bullet_style, range=bullet_range),
            UpdateTextStyle(text_style=text_style, range=text_range),
        ]

    def insert_list(
        self,
        start_location: Location,
        header: str,
        header_style: TextStyle,
        text_style: TextStyle,
        paragraph_style: ParagraphStyle,
        bullet_style: TextStyle,
        bullet_glyph: BulletGlyphPreset,
        elements: list[str],
    ) -> tuple[int, list[DocumentRequest]]:
        """Create list with header and elements

        Parameters
        ----------
        start_index: int
            index, where we want to put element
        header: str
            Title of list

        elements: List[str]
            list of text

        bullet_preset: str
            type of bullet_preset, which will be used for list elements

        Returns
        -------
            int
                end index of added element
            list[DocumentRequest]
                list of requests to update
        """

        requests = []
        header += "\n"

        requests.append(InsertText(text=header, location=start_location))
        requests.append(
            UpdateTextStyle(
                text_style=header_style,
                range=Range(
                    start_index=start_location.index,
                    end_index=start_location.index + len(header),
                    segment_id="",
                ),
            ),
        )

        next_element_index = start_location.index + len(header)

        for text in elements:
            next_element_index, element_requests = self.insert_list_element(
                location=Location(segment_id="", index=next_element_index),
                text=text,
                bullet=bullet_glyph,
                bullet_style=bullet_style,
                text_style=text_style,
                bullet_paragraph_style=paragraph_style,
            )
            requests += element_requests

        return next_element_index, requests
