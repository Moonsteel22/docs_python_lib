from dataclasses import dataclass
from dataclasses import field

from services.types.base import DocumentRequest
from services.types.classes import EndOfSegmentation
from services.types.classes import Location
from services.types.classes import ParagraphStyle
from services.types.classes import Range
from services.types.classes import SubstringMatchCriteria
from services.types.classes import TableCellLocation
from services.types.classes import TextStyle
from services.types.enum import BulletGlyphPreset


@dataclass
class CreateParagraphBullets(DocumentRequest):
    range: Range = field()
    bullet_preset: BulletGlyphPreset = field(
        default=BulletGlyphPreset.BULLET_DISC_CIRCLE_SQUARE,
    )


@dataclass
class UpdateTextStyle(DocumentRequest):
    text_style: TextStyle = field()
    range: Range = field()
    fields: str = field(default="*")


@dataclass
class InsertText(DocumentRequest):
    end_of_segmentation: EndOfSegmentation = field(init=False)
    text: str = field()
    location: Location = field()


@dataclass
class UpdateParagraphStyle(DocumentRequest):
    paragraph_style: ParagraphStyle = field()
    range: Range = field()
    fields: str = field(default="*")


@dataclass
class DeleteParagraphBullets(DocumentRequest):
    range: Range = field()


@dataclass
class InsertTable(DocumentRequest):
    location: Location = field()
    end_of_segmentation: EndOfSegmentation = field(init=False)
    rows: int = field(default=1)
    columns: int = field(default=1)


@dataclass
class InsertTableRow(DocumentRequest):
    table_cell_location: TableCellLocation = field()
    insert_below: bool = field(default=True)


@dataclass
class ReplaceAllText(DocumentRequest):
    replace_text: str = field()
    contains_text: SubstringMatchCriteria = field()


@dataclass
class DeleteContentRange(DocumentRequest):
    range: Range = field()
