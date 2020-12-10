from Matrix import Matrix
from math import exp


def f(m: Matrix) -> float:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return 16 * x1 - 0.4 * x2 + exp(2.56 * x1**2 + 2.6 * x2**2)


def diff(m: Matrix) -> Matrix:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return Matrix([[16 + 2.56 * 2 * x1 * exp(2.56 * x1**2 + 2.6 * x2**2)],
                   [-0.4 + 2.6 * 2 * x2 * exp(2.56 * x1**2 + 2.6 * x2**2)]])


def diff_2(m: Matrix) -> Matrix:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    f11 = 2.56 * 2 * exp(2.56 * x1**2 + 2.6 * x2**2) + \
        2.56**2 * 4 * x1**2 * exp(2.56 * x1**2 + 2.6 * x2**2)

    f12 = 2.56 * 2 * x1 * 2.6 * 2 * x2 * exp(2.56 * x1**2 + 2.6 * x2**2)
    f22 = -0.4 + 2.6 * 2 * exp(2.56 * x1**2 + 2.6 * x2**2) + \
        2.6**2 * 4 * x2**2 * exp(2.56 * x1**2 + 2.6 * x2**2)

    return Matrix([[f11, f12],
                   [f12, f22]])


def len_of_vector(m):
    v = m.matrix
    sum_ = 0
    for i in range(len(v)):
        sum_ += v[i][0]**2

    return sum_**(1 / 2)


x0 = Matrix([[0], [0]])

e = 0.002

J0 = diff(x0)

# print(J0)
# print(lenOfMatrix(J0))

step_size = 1

F0 = f(x0)
while len_of_vector(J0) > e:

    x1 = x0 - Matrix([[step_size * J0.matrix[0][0]],
                      [step_size * J0.matrix[1][0]]])

    F1 = f(x1)

    if F1 >= F0:
        step_size = step_size / 2
        continue
    # print(x0)

    x0 = x1
    F0 = F1
    J0 = diff(x0)
    # print(lenOfMatrix(J0))

print(x0)
print(J0)
