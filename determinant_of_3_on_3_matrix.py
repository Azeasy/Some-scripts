# a = [[1, 2, -3], [4, 1, 7], [-5, 6, 0]]
a = []
for i in range(3):
    a.append([int(x) for x in input().split()])


def minor(a, i, j):
    n = len(a)
    r = []
    for i_ in range(n):
        if i_ != i:
            b = []
            for j_ in range(n):
                if j_ != j:
                    b.append(a[i_][j_])
            r.append(b)

    # print(r)
    return r[0][0] * r[1][1] - r[0][1] * r[1][0]


def det(a):
    # Laplace method to find determinant
    n = len(a)
    sum_ = 0
    for i in range(n):
        b = a[i][0]

        element = (-1) ** (i) * b * (minor(a, i, 0))

        sum_ += element
    return sum_


print(det(a))

# TODO: make the general determinant calculator
# that will count it with time complexity O(n^3)
