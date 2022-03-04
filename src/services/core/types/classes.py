from dataclasses import dataclass
from dataclasses import field

from services.core.types.base import DocumentObject
from services.core.types.enum import Alignment
from services.core.types.enum import BaselineOffset
from services.core.types.enum import ContentDirection
from services.core.types.enum import DashStyle
from services.core.types.enum import NamedStyleType
from services.core.types.enum import SpacingMode
from services.core.types.enum import TabStopAlignment
from services.core.types.enum import Unit


# COMMON CLASSES


@dataclass
class WeightedFontFamily(DocumentObject):
    font_family: str = field()
    weight: int = field()


@dataclass
class Range(DocumentObject):
    start_index: int = field()
    end_index: int = field()
    segment_id: str = field(default="")


@dataclass
class Location(DocumentObject):
    index: int = field()
    segment_id: str = field(default="")


@dataclass
class Dimension(DocumentObject):
    magnitude: int = field(default=10)
    unit: Unit = field(default=Unit.PT)


@dataclass
class Link(DocumentObject):
    url: str = field()
    bookmarkId: str = field()
    headingId: str = field()


# STYLE CLASSES


@dataclass
class RgbColor(DocumentObject):
    red: float = field(default=0)
    green: float = field(default=0)
    blue: float = field(default=0)


@dataclass
class Color(DocumentObject):
    rgb_color: RgbColor = field(default=RgbColor())


@dataclass
class OptionalColor(DocumentObject):
    color: Color = field(default=Color())


@dataclass
class ParagraphBorder(DocumentObject):
    color: OptionalColor = field(init=False)
    width: Dimension = field(init=False)
    padding: Dimension = field(init=False)
    dash_style: DashStyle = field(init=False)


@dataclass
class TextStyle(DocumentObject):
    bold: bool = field(init=False)
    italic: bool = field(init=False)
    underline: bool = field(init=False)
    strikethrough: bool = field(init=False)
    small_caps: bool = field(init=False)
    background_color: OptionalColor = field(init=False)
    foreground_color: OptionalColor = field(init=False)
    font_size: Dimension = field(init=False)
    weighted_font_family: WeightedFontFamily = field(
        default=WeightedFontFamily(font_family="Noto Sans Symbols", weight=400),
    )
    baseline_offset: BaselineOffset = field(init=False)
    link: Link = field(init=False)


@dataclass
class TabStop(DocumentObject):
    offset: Dimension = field(init=False)
    alignment: TabStopAlignment = field(
        default=TabStopAlignment.TAB_STOP_ALIGNMENT_UNSPECIFIED,
    )


@dataclass
class Shading(DocumentObject):
    background_color: OptionalColor = field(init=False)


@dataclass
class ParagraphStyle(DocumentObject):
    heading_id: str = field(init=False)
    named_style_type: NamedStyleType = field(init=False)
    alignment: Alignment = field(init=False)
    line_spacing: float = field(init=False)
    direction: ContentDirection = field(
        default=ContentDirection.CONTENT_DIRECTION_UNSPECIFIED,
    )
    spacing_mode: SpacingMode = field(default=SpacingMode.SPACING_MODE_UNSPECIFIED)
    space_above: Dimension = field(init=False)
    space_below: Dimension = field(init=False)
    border_between: ParagraphBorder = field(init=False)
    border_top: ParagraphBorder = field(init=False)
    border_bottom: ParagraphBorder = field(init=False)
    border_left: ParagraphBorder = field(init=False)
    border_right: ParagraphBorder = field(init=False)
    indent_first_line: Dimension = field(init=False)
    indent_start: Dimension = field(init=False)
    indent_end: Dimension = field(init=False)
    tab_stops: TabStop = field(init=False)
    keep_lines_together: bool = field(init=False)
    keep_with_next: bool = field(init=False)
    avoid_widow_and_orphan: bool = field(init=False)
    shading: Shading = field(init=False)


@dataclass
class EndOfSegmentation(DocumentObject):
    segment_id: str = field(default="")


@dataclass
class TableCellLocation(DocumentObject):
    table_start_location: Location = field()
    row_index: int = field()
    column_index: int = field()


@dataclass
class SubstringMatchCriteria(DocumentObject):
    text: str = field()
    match_case: bool = field()
