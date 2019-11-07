from random import randint


class Matrix():
    def __init__(self, matrix=None):
        if matrix is None:
            self.matrix = Matrix.generateRandomMatrix()
        else:
            self.matrix = matrix

    @staticmethod
    def generateRandomMatrix(m=3, n=3, range_=(-5, 10)):
        # The function that generates a random matrix
        a = []

        for i in range(m):
            b = []
            for j in range(n):
                b.append(randint(range_[0], range_[1]))
            a.append(b)
        return a

    @staticmethod
    def getIdentityMatrix(m=3):
        # The function that generates an identity matrix matrix
        a = []
        for i in range(m):
            b = []
            for j in range(m):
                if i == j:
                    b.append(1)
                else:
                    b.append(0)
            a.append(b)
        return a

    def __str__(self):
        # The function that pretty prints a matrix
        spaces = 3
        a = self.matrix
        s = ""
        for i in range(len(a)):
            for j in range(len(a[0])):
                a_ij = str(a[i][j]) + " " * (spaces - len(str(a[i][j])))

                s += a_ij + " "
            s = s[:-1]
            s += "\n"
        return s

    def __sub__(self, other):
        a = self.matrix
        b = other.matrix
        c = []
        for i in range(len(a)):
            temp = []
            for j in range(len(a[i])):
                temp.append(a[i][j] - b[i][j])
            c.append(temp)
        return Matrix(c)

    def __add__(self, other):
        a = self.matrix
        b = other.matrix
        c = []
        for i in range(len(a)):
            temp = []
            for j in range(len(a[i])):
                temp.append(a[i][j] + b[i][j])
            c.append(temp)
        return Matrix(c)

    def __mul__(self, other):
        a = self.matrix
        b = other.matrix

        if len(a[0]) != len(b):
            raise Exception("Number of columns is not " +
                            "equal to the number of rows")

        c = []
        for i in range(len(a)):
            temp = []
            for j in range(len(b[0])):
                s = 0
                for k1 in range(len(b)):
                    s += a[i][k1] * b[k1][j]
                temp.append(s)
            c.append(temp)

        return Matrix(c)

    def transposeMatrix(self):
        a = self.matrix
        if len(a) != len(a[0]):
            raise Exception("Matrix should be squared")

        transposed_a = []
        for j in range(len(a)):
            b = []
            for i in range(len(a[j])):
                b.append(a[i][j])
            transposed_a.append(b)
        self.matrix = transposed_a

    def getTransposedMatrix(self):
        a = self.matrix
        if len(a) != len(a[0]):
            raise Exception("Matrix should be squared")

        transposed_a = []
        for j in range(len(a)):
            b = []
            for i in range(len(a[j])):
                b.append(a[i][j])
            transposed_a.append(b)
        return Matrix(transposed_a)

    def getMatrixMinor(self, i, j):
        m = self.matrix
        return Matrix([row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])])

    def getMatrixDeternminant(self):
        m = self.matrix
        # base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c) * m[0][c] \
                * (self.getMatrixMinor(0, c)).getMatrixDeternminant()
        return determinant

    def getInverseMatrix(self):
        m = self.matrix
        determinant = self.getMatrixDeternminant()
        # special case for 2x2 matrix:
        if len(m) == 2:
            return Matrix([[m[1][1] / determinant, -1 * m[0][1] / determinant],
                           [-1 * m[1][0] / determinant, m[0][0] / determinant]])

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(r, c)
                cofactorRow.append(((-1)**(r + c)) *
                                   minor.getMatrixDeternminant())
            cofactors.append(cofactorRow)
        cofactors = Matrix(cofactors)
        cofactors.transposeMatrix()
        for r in range(len(cofactors.matrix)):
            for c in range(len(cofactors.matrix)):
                cofactors.matrix[r][c] = cofactors.matrix[r][c] / determinant
        return cofactors

    def inverseMatrix(self):
        m = self.matrix
        determinant = self.getMatrixDeternminant()
        # special case for 2x2 matrix:
        if len(m) == 2:
            self.matrix = [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                           [-1 * m[1][0] / determinant, m[0][0] / determinant]]
            return

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(r, c)
                cofactorRow.append(((-1)**(r + c)) *
                                   minor.getMatrixDeternminant())
            cofactors.append(cofactorRow)
        cofactors = Matrix(cofactors)
        cofactors.transposeMatrix()
        for r in range(len(cofactors.matrix)):
            for c in range(len(cofactors.matrix)):
                cofactors.matrix[r][c] = cofactors.matrix[r][c] / determinant
        self.matrix = cofactors.matrix


def main():
    a = Matrix()
    # b = generate_matrix(3, 3)

    print(a)
    # a.transposeMatrix()
    print(a.getTransposedMatrix())

    inv_a = a.getInverseMatrix()

    print(inv_a)
    print(a * inv_a)


if __name__ == "__main__":
    main()
