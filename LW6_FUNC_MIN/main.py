import math
import pandas as pd
import plotly.express as px


def f(x: float) -> float:
    return math.sqrt(x) - math.cos(x)


def f_diff_1(x: float) -> float:
    return 1 / (2 * math.sqrt(x)) + math.sin(x)


def find_local_min(x1, h, eps_arg):
    d1 = f_diff_1(x1)
    h = -h if d1 < 0 else h
    x2 = x1 + h
    d2 = f_diff_1(x2)
    counter = 0
    if (d2 - d1) / h > 0:
        y1, y2 = f(x1), f(x2)
        zm = 100
        while abs(zm) >= eps_arg:
            z1 = x1 - x2
            p = (d1 - d2 - 2 * (y1 - y2 - d2 * z1) / z1) / z1 ** 2
            q = (d2 - d1 + 3 * (y1 - y2 - d2 * z1) / z1) / z1
            r = d2
            zm = (-q + math.sqrt(q ** 2 - 3 * p * r)) / (3 * p)
            x1, y1, d1 = x2, y2, d2
            x2 += zm
            y2, d2 = f(x2), f_diff_1(x2)
            counter += 1
        return x2 + zm, counter
    print("Wrong initial approximation")
    return None, counter


start, end = 4, 20
m = 1000
h_t = (end - start) / m
e = 10e-15

x_initial_values = [5, 11.5, 17.5]
x_min_values = []

values_table = pd.DataFrame({"x": [start + h_t * i for i in range(m + 1)],
                             "f(x)": [f(start + h_t * i) for i in range(m + 1)]})
fig = px.line(values_table, x="x", y="f(x)")
for i, x_init in enumerate(x_initial_values):
    local_min, operations_count = find_local_min(x1=x_init, h=-0.1, eps_arg=e)
    fig.add_vline(local_min, annotation_text=f"Local min X_{i + 1} = {round(local_min, 3)} ♡",
                  line_dash="dot", line_color="purple", annotation_font_size=15)
    print(f"Local_min: {local_min}\nOperations count: {operations_count}")
fig.show()


epsilon_results = {"epsilon_degrees": list(range(2, 16)), "operations_count": []}
for degree in epsilon_results["epsilon_degrees"]:
    eps_operations_count = 0
    eps = 10 ** (-degree)
    for x_init in x_initial_values:
        local_min, operations_count = find_local_min(x1=x_init, h=-0.1, eps_arg=eps)
        eps_operations_count += operations_count
    epsilon_results["operations_count"].append(eps_operations_count)

fig = px.line(epsilon_results, x="epsilon_degrees", y="operations_count")
fig.show()
