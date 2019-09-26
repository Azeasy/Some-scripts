def get_valid_sudoku():
    return [[7, 3, 5, 6, 1, 4, 8, 9, 2],
            [8, 4, 2, 9, 7, 3, 5, 6, 1],
            [9, 6, 1, 2, 8, 5, 3, 7, 4],
            [2, 8, 6, 3, 4, 9, 1, 5, 7],
            [4, 1, 3, 8, 5, 7, 9, 2, 6],
            [5, 7, 9, 1, 2, 6, 4, 3, 8],
            [1, 5, 7, 4, 9, 2, 6, 8, 3],
            [6, 9, 4, 7, 3, 8, 2, 1, 5],
            [3, 2, 8, 5, 6, 1, 7, 4, 9]]


def squares(a, i_, j_):
    """
    This function
    """
    r = []
    for i in range(9):
        for j in range(9):
            if i // 3 == i_ and j // 3 == j_:
                r.append(a[i][j])
    return r


def sudoku(a):
    # Check whether or not there are unique elemets in the each row
    for i in range(9):
        if len(set(a[i])) < 9:
            return False

    # Transpose matrix to check the columns as well as the rows
    transposed_a = []
    for j in range(9):
        b = []
        for i in range(9):
            b.append(a[i][j])
        transposed_a.append(b)

    for i in range(9):
        if len(set(transposed_a[i])) < 9:
            return False

    # Partition of the each square to the rows
    for i in range(3):
        for j in range(3):
            square_in_row = squares(a, i, j)
            if len(set(square_in_row)) < 9:
                return False

    return True


def main():
    a = []
    print(sudoku(get_valid_sudoku()))

    for i in range(9):
        a.append([int(x) for x in input().split()])
    print(sudoku(a))

if __name__ == "__main__":
    main()
