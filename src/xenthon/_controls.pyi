from collections.abc import Callable
from enum import IntEnum
from typing import Any

from ._reconcile import El, ScrollPos

Msg = Any


class FlexAlign(IntEnum):
    AUTO: int
    START: int
    END: int
    CENTER: int
    STRETCH: int
    BASELINE: int


class FlexJustify(IntEnum):
    START: int
    END: int
    CENTER: int
    SPACE_BETWEEN: int
    SPACE_AROUND: int
    SPACE_EVENLY: int


class FlexWrap(IntEnum):
    NO_WRAP: int
    WRAP: int


class AppBarMode(IntEnum):
    COMPACT: int
    MINIMAL: int
    HIDDEN: int


class BadgeMode(IntEnum):
    DOT: int
    NUMBER: int
    ICON: int


class ButtonStyle(IntEnum):
    STANDARD: int
    SUBTLE: int
    TEXT: int
    ACCENT: int


class CalendarMode(IntEnum):
    SINGLE: int
    NONE: int
    MULTIPLE: int


class Clock(IntEnum):
    SYSTEM: int
    H12: int
    H24: int


class ElementLabel(IntEnum):
    DEFAULT: int
    COLLAPSED: int


class FontWeight(IntEnum):
    THIN: int
    EXTRA_LIGHT: int
    LIGHT: int
    REGULAR: int
    MEDIUM: int
    SEMI_BOLD: int
    BOLD: int
    EXTRA_BOLD: int
    BLACK: int


class ImageStretch(IntEnum):
    NONE: int
    FILL: int
    UNIFORM: int
    UNIFORM_TO_FILL: int


class InfoBarSeverity(IntEnum):
    INFORMATIONAL: int
    SUCCESS: int
    WARNING: int
    ERROR: int


class LabelPosition(IntEnum):
    BOTTOM: int
    RIGHT: int
    COLLAPSED: int


class ListSelMode(IntEnum):
    SINGLE: int
    NONE: int
    MULTIPLE: int
    EXTENDED: int


class OverflowButton(IntEnum):
    AUTO: int
    VISIBLE: int
    COLLAPSED: int


class PagerButtonVis(IntEnum):
    AUTO: int
    ALWAYS: int
    HIDDEN_EDGE: int
    NONE: int


class PagerDisplayMode(IntEnum):
    AUTO: int
    NUMBER_PANEL: int
    NUMBER_TEXT: int


class PipsNavVis(IntEnum):
    COLLAPSED: int
    VISIBLE: int
    ON_HOVER: int


class ProgressState(IntEnum):
    NORMAL: int
    PAUSED: int
    ERROR: int


class PullDirection(IntEnum):
    TOP_TO_BOTTOM: int
    LEFT_TO_RIGHT: int
    RIGHT_TO_LEFT: int
    BOTTOM_TO_TOP: int


class ScrollBarIndicator(IntEnum):
    NONE: int
    TOUCH: int
    MOUSE: int


class SliderSnap(IntEnum):
    STEP: int
    TICKS: int


class SortDirection(IntEnum):
    NONE: int
    ASCENDING: int
    DESCENDING: int


class Spectrum(IntEnum):
    HUE_SATURATION: int
    HUE_VALUE: int
    SATURATION_VALUE: int


class SplitViewDisplayMode(IntEnum):
    INLINE: int
    COMPACT_INLINE: int
    OVERLAY: int
    COMPACT_OVERLAY: int


class SplitViewPanePlacement(IntEnum):
    LEFT: int
    RIGHT: int


class StackDirection(IntEnum):
    COLUMN: int
    ROW: int


class TeachingTipPlacement(IntEnum):
    AUTO: int
    TOP: int
    BOTTOM: int
    LEFT: int
    RIGHT: int
    TOP_RIGHT: int
    TOP_LEFT: int
    BOTTOM_RIGHT: int
    BOTTOM_LEFT: int
    LEFT_TOP: int
    LEFT_BOTTOM: int
    RIGHT_TOP: int
    RIGHT_BOTTOM: int
    CENTER: int


class TeachingTipTail(IntEnum):
    AUTO: int
    VISIBLE: int
    COLLAPSED: int


class TextAlign(IntEnum):
    LEFT: int
    CENTER: int
    RIGHT: int
    JUSTIFY: int


class TextTrim(IntEnum):
    NONE: int
    CHAR: int
    CHAR_ELLIPSIS: int
    WORD: int
    WORD_ELLIPSIS: int
    PATH_ELLIPSIS: int


class TickPlacement(IntEnum):
    INLINE: int
    TOP_LEFT: int
    BOTTOM_RIGHT: int
    OUTSIDE: int
    NONE: int


def container(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def text(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    fontsize: float | None = None,
    fontweight: FontWeight | None = None,
    textalign: TextAlign | None = None,
    fg: int | None = None,
    maxlines: int | None = None,
    trim: TextTrim | None = None,
    textwrap: bool | None = None,
    selectable: bool | None = None,
) -> El: ...


def button(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    icon: str | None = None,
    style: ButtonStyle | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def toggle(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    checked: bool | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def checkbox(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    checked: bool | None = None,
    indeterminate: bool | None = None,
    threestate: bool | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
    on_state: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def radio(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    checked: bool | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def switch(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    checked: bool | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def slider(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    min: float | None = None,
    max: float | None = None,
    value: float | None = None,
    step: float | None = None,
    tick: float | None = None,
    tickplace: TickPlacement | None = None,
    snapsto: SliderSnap | None = None,
    smallchange: float | None = None,
    largechange: float | None = None,
    dir: StackDirection | None = None,
    range: bool | None = None,
    rangestart: float | None = None,
    rangeend: float | None = None,
    on_change: Msg | Callable[[float], Msg] | None = None,
    on_range: Msg | Callable[[float, float], Msg] | None = None,
) -> El: ...


def textbox(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    placeholder: str | None = None,
    multiline: bool | None = None,
    readonly: bool | None = None,
    on_change: Msg | Callable[[str], Msg] | None = None,
) -> El: ...


def scroll(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
    x: float | None = None,
    y: float | None = None,
    on_scroll: Msg | Callable[[ScrollPos], Msg] | None = None,
) -> El: ...


def image(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    src: int | None = None,
    fit: ImageStretch | None = None,
) -> El: ...


def progress(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    min: float | None = None,
    max: float | None = None,
    value: float | None = None,
    indeterminate: bool | None = None,
    state: ProgressState | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    border_width: float | None = None,
) -> El: ...


def list(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    ncol: int | None = None,
    mode: ListSelMode | None = None,
    first: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
    items: tuple[int, Callable[[int], El]] | None = None,
) -> El: ...


def tab(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
) -> El: ...


def card(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def divider(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
) -> El: ...


def canvas(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
) -> El: ...


def password(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    placeholder: str | None = None,
    on_change: Msg | Callable[[str], Msg] | None = None,
) -> El: ...


def number(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    value: float | None = None,
    min: float | None = None,
    max: float | None = None,
    step: float | None = None,
    hidespin: bool | None = None,
    on_change: Msg | Callable[[float], Msg] | None = None,
) -> El: ...


def link(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    url: str | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def repeat(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    icon: str | None = None,
    style: ButtonStyle | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def progressring(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    min: float | None = None,
    max: float | None = None,
    value: float | None = None,
    indeterminate: bool | None = None,
    state: ProgressState | None = None,
    active: bool | None = None,
) -> El: ...


def badge(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    badgemode: BadgeMode | None = None,
    value: int | None = None,
    icon: str | None = None,
) -> El: ...


def tooltip(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    open: bool | None = None,
    enabled: bool | None = None,
) -> El: ...


def flyout(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    open: bool | None = None,
    enabled: bool | None = None,
) -> El: ...


def menufly(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    open: bool | None = None,
    enabled: bool | None = None,
) -> El: ...


def dropdown(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    icon: str | None = None,
    style: ButtonStyle | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def split(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    icon: str | None = None,
    style: ButtonStyle | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def combo(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    placeholder: str | None = None,
    sel: int | None = None,
    text: str | None = None,
    editable: bool | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
    on_submit: Msg | Callable[[str], Msg] | None = None,
) -> El: ...


def expander(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    expanded: bool | None = None,
    contenth: float | None = None,
    on_toggle: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def exphead(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
) -> El: ...


def expbody(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def infobar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    message: str | None = None,
    tip: str | None = None,
    severity: InfoBarSeverity | None = None,
    closable: bool | None = None,
    on_close: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def dialog(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    primary: str | None = None,
    secondary: str | None = None,
    close: str | None = None,
    contenth: float | None = None,
    open: bool | None = None,
    on_close: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def dialogbody(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def menubar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
) -> El: ...


def menuitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def nav(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def navitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def tabs(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_close: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def tabitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def listitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def listbox(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    ncol: int | None = None,
    mode: ListSelMode | None = None,
    first: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
    items: tuple[int, Callable[[int], El]] | None = None,
) -> El: ...


def gridview(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    ncol: int | None = None,
    mode: ListSelMode | None = None,
    first: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
    items: tuple[int, Callable[[int], El]] | None = None,
) -> El: ...


def repeater(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    ncol: int | None = None,
    mode: ListSelMode | None = None,
    first: int | None = None,
    items: tuple[int, Callable[[int], El]] | None = None,
) -> El: ...


def itemsview(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    ncol: int | None = None,
    mode: ListSelMode | None = None,
    invoked: bool | None = None,
    first: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
    items: tuple[int, Callable[[int], El]] | None = None,
) -> El: ...


def flip(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    sel: int | None = None,
    dir: StackDirection | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def pips(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    dir: StackDirection | None = None,
    maxvisible: int | None = None,
    nav: PipsNavVis | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def suggest(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    placeholder: str | None = None,
    icon: str | None = None,
    on_change: Msg | Callable[[str], Msg] | None = None,
    on_query: Msg | Callable[[str, int], Msg] | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def togglesplit(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    checked: bool | None = None,
    on_invoke: Msg | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def radiogroup(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    ncol: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def rating(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    value: float | None = None,
    max: float | None = None,
    text: str | None = None,
    placeholder: float | None = None,
    initial: int | None = None,
    clear: bool | None = None,
    readonly: bool | None = None,
    on_rating: Msg | Callable[[float, int], Msg] | None = None,
) -> El: ...


def selector(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def selectoritem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def breadcrumb(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def crumb(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def teachtip(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    subtitle: str | None = None,
    icon: str | None = None,
    action: str | None = None,
    actionaccent: bool | None = None,
    close: str | None = None,
    placement: TeachingTipPlacement | None = None,
    untargeted: bool | None = None,
    lightdismiss: bool | None = None,
    tail: TeachingTipTail | None = None,
    placementmargin: float | None = None,
    open: bool | None = None,
    on_close: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def tree(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    itemh: float | None = None,
    on_invoke: Msg | None = None,
    on_expand: Msg | Callable[[int, bool], Msg] | None = None,
    on_select: Msg | Callable[[int, bool], Msg] | None = None,
) -> El: ...


def treeitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    selected: bool | None = None,
    expanded: bool | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def refresh(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    direction: PullDirection | None = None,
    visualizer: float | None = None,
    threshold: float | None = None,
    refreshing: bool | None = None,
    on_refresh: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def avatar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    initials: str | None = None,
    src: int | None = None,
    badgeglyph: str | None = None,
    badgevalue: int | None = None,
    group: bool | None = None,
) -> El: ...


def pager(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    sel: int | None = None,
    nitem: int | None = None,
    display: PagerDisplayMode | None = None,
    first: PagerButtonVis | None = None,
    prev: PagerButtonVis | None = None,
    next: PagerButtonVis | None = None,
    last: PagerButtonVis | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def splitview(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    open: bool | None = None,
    display: SplitViewDisplayMode | None = None,
    placement: SplitViewPanePlacement | None = None,
    openlen: float | None = None,
    compactlen: float | None = None,
) -> El: ...


def splitpane(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def splitbody(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    dir: StackDirection | None = None,
    items: FlexAlign | None = None,
    justify: FlexJustify | None = None,
    gap: float | None = None,
    pl: float | None = None,
    pt: float | None = None,
    pr: float | None = None,
    pb: float | None = None,
    fill: bool | None = None,
    fitw: bool | None = None,
    fith: bool | None = None,
    wrap: FlexWrap | None = None,
) -> El: ...


def titlebar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    subtitle: str | None = None,
    icon: str | None = None,
    showback: bool | None = None,
    backdisabled: bool | None = None,
    showtoggle: bool | None = None,
    integrate: bool | None = None,
    on_invoke: Msg | None = None,
    on_toggle: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def scrollbar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    dir: StackDirection | None = None,
    min: float | None = None,
    max: float | None = None,
    value: float | None = None,
    viewport: float | None = None,
    smallchange: float | None = None,
    largechange: float | None = None,
    indicator: ScrollBarIndicator | None = None,
    on_change: Msg | Callable[[float], Msg] | None = None,
) -> El: ...


def looping(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    nitem: int | None = None,
    sel: int | None = None,
    itemh: float | None = None,
    itemw: float | None = None,
    loop: bool | None = None,
    on_select: Msg | Callable[[int], Msg] | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def datepicker(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    header: str | None = None,
    date: int | None = None,
    minyear: int | None = None,
    maxyear: int | None = None,
    on_value: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def timepicker(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    header: str | None = None,
    time: int | None = None,
    clock: Clock | None = None,
    step: int | None = None,
    on_value: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def calendar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    date: int | None = None,
    mode: CalendarMode | None = None,
    mindate: int | None = None,
    maxdate: int | None = None,
    firstday: int | None = None,
    on_date: Msg | Callable[[int, bool], Msg] | None = None,
) -> El: ...


def colorpicker(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    color: int | None = None,
    alpha: bool | None = None,
    morebutton: bool | None = None,
    spectrum: Spectrum | None = None,
    on_value: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def colheader(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    shrink: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
) -> El: ...


def colitem(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    minw: float | None = None,
    maxw: float | None = None,
    text: str | None = None,
    tip: str | None = None,
    align: TextAlign | None = None,
    enabled: bool | None = None,
    resizable: bool | None = None,
    sort: SortDirection | None = None,
    on_invoke: Msg | None = None,
    on_resize: Msg | Callable[[float], Msg] | None = None,
    on_fit: Msg | None = None,
    on_reorder: Msg | Callable[[int], Msg] | None = None,
) -> El: ...


def commandbar(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    enabled: bool | None = None,
    open: bool | None = None,
    sticky: bool | None = None,
    mode: AppBarMode | None = None,
    labels: LabelPosition | None = None,
    more: OverflowButton | None = None,
    dynamic: bool | None = None,
    on_open: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def appbarbutton(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    labelpos: ElementLabel | None = None,
    accel: str | None = None,
    secondary: bool | None = None,
    order: int | None = None,
    on_invoke: Msg | None = None,
) -> El: ...


def appbartoggle(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    text: str | None = None,
    icon: str | None = None,
    enabled: bool | None = None,
    labelpos: ElementLabel | None = None,
    accel: str | None = None,
    checked: bool | None = None,
    secondary: bool | None = None,
    order: int | None = None,
    on_change: Msg | Callable[[bool], Msg] | None = None,
) -> El: ...


def appbarsep(
    *children: El,
    key: int | str | None = None,
    w: float | None = None,
    h: float | None = None,
    grow: float | None = None,
    self: FlexAlign | None = None,
    ml: float | None = None,
    mt: float | None = None,
    mr: float | None = None,
    mb: float | None = None,
    tip: str | None = None,
    secondary: bool | None = None,
    order: int | None = None,
) -> El: ...
