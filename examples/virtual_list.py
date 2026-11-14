from dataclasses import dataclass, replace

import xenthon as xtk


@dataclass(frozen=True)
class Select:
    index: int


@dataclass(frozen=True)
class Model:
    selected: int = -1


def update(model: Model, msg: Select) -> Model:
    match msg:
        case Select(index):
            return replace(model, selected=index)


def row(i: int) -> xtk.El:
    return xtk.container(
        xtk.text(text=str(i), w=72, fontsize=12),
        xtk.text(text=f"Item number {i}", fontsize=14),
        dir=xtk.StackDirection.ROW, gap=12, items=xtk.FlexAlign.CENTER,
    )


def view(model: Model) -> xtk.El:
    status = f"Selected row: {model.selected}" if model.selected >= 0 else "Nothing selected yet."
    return xtk.container(
        xtk.text(text="100,000 rows", fontsize=28, fontweight=xtk.FontWeight.SEMI_BOLD),
        xtk.text(text=status),
        xtk.list(grow=1, itemh=40, mode=xtk.ListSelMode.SINGLE, sel=model.selected, on_select=Select,
               items=(100_000, row)),
        dir=xtk.StackDirection.COLUMN, grow=1, gap=12, pl=32, pt=32, pr=32, pb=32,
    )


if __name__ == "__main__":
    raise SystemExit(xtk.run(Model(), update, view, title="xenthon virtual list"))
