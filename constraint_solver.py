from sympy import S, Symbol
from sympy.solvers.solveset import linsolve


layout = [
    {
        "type": "Rect",
        "id": "parent",
        "x": "0",
        "y": "0",
        "w": "800",
        "h": "600",
        "color": (255, 0, 0, 255),

        "children": [
            {
                "type": "Rect",
                "id": "rect1",
                "x": "0",
                "y": "0",
                "w": "parent.w / 2",
                "h": "parent.h",
                "color": (0, 255, 0, 255)
            },
            {
                "type": "Rect",
                "id": "rect2",
                "x": "rect1.right",
                "y": "0",
                # "w": "parent.w / 2",
                "right": "parent.right",
                "h": "parent.h / 2",
                "color": (0, 0, 255, 255)
            },
            {
                "type": "Rect",
                "id": "rect3",
                "x": "rect2.x",
                "y": "rect2.bottom",
                "w": "rect2.w",
                "bottom": "parent.bottom",
                "color": (0, 0, 255, 255)
            }
        ]
    }
]


def _build_eqn(element, key):
    if key not in element:
        return None
    expr = element[key].replace('.', '__')
    return S("-{}__{} + {}".format(element['id'], key, expr))


def get_equations(elements):
    eqns = []

    if not elements:
        return eqns

    for e in elements:
        eqns += [
            _build_eqn(e, 'x'),  # TODO: Relative to parent
            _build_eqn(e, 'y'),  # TODO: Relative to parent
            _build_eqn(e, 'w'),
            _build_eqn(e, 'h'),
            _build_eqn(e, 'right'),
            _build_eqn(e, 'bottom'),
            # TODO: Convenience anchors, such as right, left, top, bottom,
            # horizontal_center, vertical_center
            S("-{0}__right + {0}__x + {0}__w".format(e['id'])),
            S("-{0}__bottom + {0}__y + {0}__h".format(e['id'])),
        ]
        eqns += get_equations(e.get('children'))
    return [e for e in eqns if e]


def main():
    equations = get_equations(layout)
    symbols = set()
    for eqn in equations:
        symbols = symbols.union(eqn.atoms(Symbol))
    symbols = list(symbols)
    solve = list(linsolve(equations, *symbols))[0]
    print(list(zip(symbols, solve)))


if __name__ == "__main__":
    main()
