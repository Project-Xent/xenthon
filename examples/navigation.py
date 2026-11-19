from dataclasses import dataclass, replace

import xenthon as xtk

K = xtk.NavKind
PAGES = [(K.ITEM, "Home", "Home"), (K.ITEM, "List", "Library"), K.SEPARATOR, (K.FOOTER, "Help", "About")]
TITLES = {0: "Home", 1: "Library", 3: "About"}


@dataclass(frozen=True)
class Model:
    page: int = 0
    view: int = 0
    fruit: str = ""


def update(model: Model, msg) -> Model:
    match msg:
        case ("page", i):
            return replace(model, page=i)
        case ("view", i):
            return replace(model, view=i)
        case ("fruit", text):
            return replace(model, fruit=text)
    return model


def view(model: Model) -> xtk.El:
    page = xtk.container(
        xtk.text(text=TITLES.get(model.page, ""), fontsize=28, fontweight=xtk.FontWeight.SEMI_BOLD),
        xtk.selector(items=[("List", "List"), ("Edit", "Grid"), (None, "Disabled", True)], sel=model.view,
                     on_select=lambda i: ("view", i)),
        xtk.suggest(w=280, text=model.fruit, placeholder="Fruit", items=["apple", "banana", "cherry"],
                    on_change=lambda t: ("fruit", t)),
        dir=xtk.StackDirection.COLUMN, grow=1, gap=16, pl=36, pt=28, pr=36, pb=28,
    )
    return xtk.nav(page, items=PAGES, titlebar=True, title="xenthon navigation", sel=model.page, grow=1,
                   on_select=lambda i: ("page", i))


if __name__ == "__main__":
    raise SystemExit(xtk.run(Model(), update, view, title="xenthon navigation"))
