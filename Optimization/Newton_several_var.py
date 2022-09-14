from Matrix import Matrix
from math import exp


def f(m: Matrix) -> float:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return 16 * x1 - 0.4 * x2 + exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)


def diff(m: Matrix) -> Matrix:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return Matrix([[16 + 2.56 * 2 * x1 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)],
                   [-0.4 + 2.6 * 2 * x2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)]])


def diff_2(m: Matrix) -> Matrix:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    f11 = 2.56 * 2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2) + \
          2.56 ** 2 * 4 * x1 ** 2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)

    f12 = 2.56 * 2 * x1 * 2.6 * 2 * x2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)
    f22 = -0.4 + 2.6 * 2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2) + \
          2.6 ** 2 * 4 * x2 ** 2 * exp(2.56 * x1 ** 2 + 2.6 * x2 ** 2)

    return Matrix([[f11, f12],
                   [f12, f22]])


def len_of_vector(m):
    v = m.matrix
    sum_ = 0
    for i in range(len(v)):
        sum_ += v[i][0] ** 2

    return sum_ ** (1 / 2)


x0 = Matrix([[1], [1]])

e = 0.0002

J0 = diff(x0)

# print(J0)

while len_of_vector(J0) > e:
    J_prime_inv = diff_2(x0)
    J_prime_inv.inverseMatrix()

    tmp = x0
    x0 = J_prime_inv * diff(x0)
    x0 = tmp - x0
    # print(x0)

    J0 = diff(x0)

print(x0)
print(J0)
