from Matrix import Matrix


def f(m: Matrix) -> float:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return 10 * x1 ** 2 + x2 ** 2


def diff(m: Matrix) -> Matrix:
    x1 = m.matrix[0][0]
    x2 = m.matrix[1][0]
    return Matrix([[20 * x1],
                   [2 * x2]])


def len_of_vector(m: Matrix) -> float:
    v = m.matrix
    sum_ = 0
    for i in range(len(v)):
        sum_ += v[i][0]**2

    return sum_**(1 / 2)


def is_inside(m: Matrix, radius: float, center: Matrix) -> bool:
    v = m.matrix
    c = (center.matrix[0][0], center.matrix[1][0])
    radius = 5
    return c[0] * v[0][0] + c[1] * v[1][0] <= radius


def get_projection(m: Matrix) -> Matrix:
    y = 5
    c = Matrix([[1], [2]])

    if is_inside(m, y, c):
        return m

    dir_ = c - m
    temp = dir_.matrix
    len_dir = len_of_vector(dir_)
    temp[0][0] = temp[0][0] * y / len_dir
    temp[1][0] = temp[1][0] * y / len_dir
    dir_.matrix = temp

    return c + dir_


x0 = Matrix([[170], [6000]])

e = 0.002
delta = 0.001

J0 = diff(x0)

# print(J0)
# print(lenOfMatrix(J0))

step_size = 1
F0 = f(x0)
while len_of_vector(J0) > e:
    step = Matrix([[step_size * J0.matrix[0][0]],
                   [step_size * J0.matrix[1][0]]])

    x1 = x0 - step
    x1 = get_projection(x1)
    F1 = f(x1)
    # print(step)
    # print((F1), (F0))

    if F1 >= F0:
        step_size = step_size / 2
        if step_size < delta:
            break
        continue
    # print(x0)

    x0 = x1
    F0 = F1
    J0 = diff(x0)

print(x0)
print(J0)
print(F1)
