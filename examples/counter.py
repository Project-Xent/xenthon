from dataclasses import dataclass, replace
from enum import Enum, auto

import xenthon as xtk


class Msg(Enum):
    INC = auto()
    DEC = auto()
    RESET = auto()


@dataclass(frozen=True)
class Model:
    n: int = 0


def update(model: Model, msg: Msg) -> Model:
    match msg:
        case Msg.INC:
            return replace(model, n=model.n + 1)
        case Msg.DEC:
            return replace(model, n=model.n - 1)
        case Msg.RESET:
            return replace(model, n=0)


def view(model: Model) -> xtk.El:
    return xtk.container(
        xtk.text(text="Counter", fontsize=28, fontweight=xtk.FontWeight.SEMI_BOLD),
        xtk.text(text=f"Value: {model.n}", fontsize=20),
        xtk.container(
            xtk.button(text="−", w=48, on_invoke=Msg.DEC),
            xtk.button(text="+", w=48, style=xtk.ButtonStyle.ACCENT, on_invoke=Msg.INC),
            xtk.button(text="Reset", style=xtk.ButtonStyle.SUBTLE, on_invoke=Msg.RESET),
            dir=xtk.StackDirection.ROW, gap=8, items=xtk.FlexAlign.CENTER,
        ),
        dir=xtk.StackDirection.COLUMN, grow=1, gap=16, pl=32, pt=32, pr=32, pb=32, items=xtk.FlexAlign.START,
    )


if __name__ == "__main__":
    raise SystemExit(xtk.run(Model(), update, view, title="xenthon counter"))
