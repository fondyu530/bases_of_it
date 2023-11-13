import math
import pandas as pd
import plotly.express as px


def f(x: float) -> float:
    return math.sqrt(x) - math.cos(x) ** 2


def f_antiderivative(x: float) -> float:
    return 2 / 3 * x ** 1.5 - 0.5 * x - math.sin(2 * x) / 4


def f_integral_computation_part(x_mid: float, hi: float) -> tuple[float, float]:
    x1 = x_mid - hi * 0.5773502692 / 2
    x2 = x_mid + hi * 0.5773502692 / 2
    return f(x1), f(x2)


start = 5
end = 8
m_values = [10, 20, 40]
integral_value = f_antiderivative(end) - f_antiderivative(start)

res_table = {"m": m_values, "integral_value": [integral_value] * len(m_values),
             "integral_computed_value": [], "residuals": []}
for m in m_values:
    h = (end - start) / m
    x_interval_middles = [start + h * (i + 0.5) for i in range(m)]
    integral_computed = sum([sum(f_integral_computation_part(x_mid, h)) for x_mid in x_interval_middles]) * h / 2
    res_table["integral_computed_value"].append(integral_computed)
    res_table["residuals"].append(abs(integral_computed - integral_value))


res_table = pd.DataFrame(res_table)
print(res_table)
