import threading
import time
from dataclasses import dataclass, replace

import xenthon as xtk


@dataclass(frozen=True)
class Edit:
    text: str


@dataclass(frozen=True)
class Submit:
    text: str


@dataclass(frozen=True)
class Checked:
    text: str
    length: int


@dataclass(frozen=True)
class Model:
    text: str = ""
    busy: bool = False
    round: int = 0
    results: tuple[str, ...] = ()


def check(text: str) -> None:
    time.sleep(0.5)
    xtk.post(Checked(text, len(text)))


def update(model: Model, msg) -> Model:
    match msg:
        case Edit(text):
            return replace(model, text=text)
        case Submit(text) if text and not model.busy:
            threading.Thread(target=check, args=(text,), daemon=True).start()
            return replace(model, busy=True)
        case Checked(text, length):
            line = f"{text!r} has {length} characters"
            return replace(model, text="", busy=False, round=model.round + 1, results=(line, *model.results))
    return model


def view(model: Model) -> xtk.El:
    status = "Checking on a worker thread…" if model.busy else "Type a word and press Enter."
    return xtk.container(
        xtk.text(text="Focus and post", fontsize=28, fontweight=xtk.FontWeight.SEMI_BOLD),
        xtk.text(text=status),
        xtk.container(
            xtk.suggest(key="input", text=model.text, w=280, enabled=not model.busy, focus=model.round,
                        on_change=Edit, on_query=lambda text, index: Submit(text)),
            xtk.progressring(w=20, h=20) if model.busy else None,
            dir=xtk.StackDirection.ROW, gap=12, items=xtk.FlexAlign.CENTER,
        ),
        *(xtk.text(text=line, fontsize=13) for line in model.results[:8]),
        dir=xtk.StackDirection.COLUMN, grow=1, gap=12, pl=32, pt=32, pr=32, pb=32, items=xtk.FlexAlign.START,
    )


if __name__ == "__main__":
    raise SystemExit(xtk.run(Model(), update, view, title="xenthon focus and post"))
