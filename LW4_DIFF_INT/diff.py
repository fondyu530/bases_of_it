import math
import pandas as pd
import plotly.express as px


def f(x: float) -> float:
    return math.sqrt(x) - math.cos(x) ** 2


def f_dif_1(x: float) -> float:
    return 1 / (2 * math.sqrt(x)) + math.sin(2 * x)


def f_dif_2(x: float) -> float:
    return 2 * math.cos(2 * x) - 1 / (4 * x ** 1.5)


def f_dif_1_computed(x: float, h: float, position: int):
    if position == 1:
        x1, x2, x3 = x, x + h, x + 2 * h
        y1, y2, y3 = f(x1), f(x2), f(x3)
        return - (3 * y1 - 4 * y2 + y3) / (2 * h)
    elif position == 2:
        x1, x3 = x - h, x + h
        return (f(x3) - f(x1)) / (2 * h)
    elif position == 3:
        x1, x2, x3 = x - 2 * h, x - h, x
        y1, y2, y3 = f(x1), f(x2), f(x3)
        return (y1 - 4 * y2 + 3 * y3) / (2 * h)


def f_dif_2_computed(x: float, h: float):
    x1, x3 = x - h, x + h
    y1, y2, y3 = f(x1), f(x), f(x3)
    return (y1 - 2 * y2 + y3) / h ** 2


start = 5
end = 8
h_values = [0.2, 0.1, 0.05]

results_table_all = None
for h_p in h_values:
    results_table = dict()
    results_table["h"] = [h_p] * 21
    results_table["x"] = [start + (i - 1) * (end - start) / 20 for i in range(1, 22)]
    results_table["f(x)"] = [f(el) for el in results_table["x"]]
    results_table["f'(x)"] = [f_dif_1(el) for el in results_table["x"]]
    results_table["f'(x)_computed"] = [f_dif_1_computed(start, h_p, position=1)] + \
                                      [f_dif_1_computed(el, h_p, position=2) for el in results_table["x"][1:-1]] + \
                                      [f_dif_1_computed(end, h_p, position=3)]
    results_table["f''(x)"] = [f_dif_2(el) for el in results_table["x"]]
    results_table["f''(x)_computed"] = [None] + [f_dif_2_computed(el, h_p) for el in results_table["x"][1:-1]]
    results_table["f''(x)_computed"] += [None]

    results_table = pd.DataFrame(results_table)
    results_table_all = results_table if results_table_all is None else pd.concat([results_table_all, results_table])


h_display = 0.05
print(f"Results table for h = {h_display}\n")
print(results_table_all[results_table_all["h"] == h_display])

results_table_all["diff_1_residuals"] = abs(results_table_all["f'(x)"] - results_table_all["f'(x)_computed"])
results_table_all["diff_2_residuals"] = abs(results_table_all["f''(x)"] - results_table_all["f''(x)_computed"])

fig = px.line(results_table_all, x="x", y="diff_2_residuals", color="h")
fig.show()
