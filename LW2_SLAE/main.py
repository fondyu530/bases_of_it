import numpy as np


def read_equations_matrix(file_path: str) -> np.array:
    matrix = []
    with open(file_path, "r") as f:
        for matrix_row in f.readlines():
            matrix_row = [float(el) for el in matrix_row.split(" ")]
            matrix.append(matrix_row)
    return np.array(matrix)


def compute_roots(matrix: np.array) -> np.array:
    # forward propagation
    for i in range(1, len(matrix)):
        tmp_a = matrix[i][i] - matrix[i][i - 1] * matrix[i - 1][i] / matrix[i - 1][i - 1]
        tmp_b = matrix[i][-1] - matrix[i][i - 1] * matrix[i - 1][-1] / matrix[i - 1][i - 1]
        matrix[i][i - 1] = 0
        matrix[i][i] = tmp_a
        matrix[i][-1] = tmp_b

    # backward propagation
    roots = [matrix[-1][-1] / matrix[-1][-2]]
    for roots_ind, i in enumerate(range(len(matrix) - 2, -1, -1)):
        tmp_root = (matrix[i][-1] - matrix[i][i + 1] * roots[roots_ind]) / matrix[i][i]
        roots.append(tmp_root)

    roots.reverse()
    return np.array(roots)


def compute_residual(matrix: np.array, roots: np.array) -> float:
    matrix_left = np.array([row[:-1] for row in equations_matrix])
    matrix_right = np.array([row[-1] for row in equations_matrix])
    matrix_right_computed = np.dot(matrix_left, roots)
    residuals = np.abs(matrix_right - matrix_right_computed)
    return np.max(residuals)


equations_matrix = read_equations_matrix("input_matrix.txt")
equations_roots = compute_roots(equations_matrix.copy())
residual = compute_residual(equations_matrix, equations_roots)


# make output
print("SLAE:")
for i, row in enumerate(equations_matrix):
    row_str = [f"{el} * X{j + 1}" if el >= 0 else f"({el} * X{j + 1})" for j, el in enumerate(row[:-1])]
    row_str = " + ".join(row_str) + f" = {row[-1]}"
    print(row_str)

print("\nRoots:")
for i, root in enumerate(equations_roots):
    print(f"X{i + 1} = {root}")

print(f"\nResidual: {residual}")
