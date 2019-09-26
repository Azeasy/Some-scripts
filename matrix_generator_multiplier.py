from random import randint


def generate_matrix(m=3, n=3, range_=(-5, 10)):
    # The function that generates a random matrix
    a = []

    for i in range(m):
        b = []
        for j in range(n):
            b.append(randint(range_[0], range_[1]))
        a.append(b)
    return a


def print_matrix(a):
    # The function that pretty prints a matrix
    spaces = 3

    for i in range(len(a)):
        for j in range(len(a[0])):
            a_ij = str(a[i][j]) + " " * (spaces - len(str(a[i][j])))

            print(a_ij, end=' ')
        print()
    print()


def miltiple_matrices(a, b):
    c = []
    for i in range(len(a)):
        temp = []
        for j in range(len(b[0])):
            s = 0
            for k1 in range(len(b)):
                s += a[i][k1] * b[k1][j]
            temp.append(s)
        c.append(temp)

    return c


a = generate_matrix(3, 3)
b = generate_matrix(3, 3)

print_matrix(a)
print_matrix(b)

print_matrix(miltiple_matrices(a, b))
print_matrix(miltiple_matrices(b, a))
