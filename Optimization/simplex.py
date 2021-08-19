import numpy as np
# a = [
#     [-2.0,  3.0, -7.0,  0.0,  0.0,  0.0,   0.0],
#     [ 5.0,  3.0,  1.0,  1.0,  0.0,  0.0,  20.0],
#     [ 2.0, 10.0,  4.0,  0.0,  1.0,  0.0,  15.0],
#     [ 8.0,  5.0,  2.0,  0.0,  0.0,  1.0,  14.0],
# ]

a = [
    [-3.0, -2.0,  5.0,  0.0,  0.0,   0.0],
    [ 4.0, -2.0,  2.0,  1.0,  0.0,   4.0],
    [ 2.0, -1.0,  1.0,  0.0,  1.0,   1.0],
]

a = np.array(a)

def min_neg(arr):
    idx = arr.argmin()
    el = arr[idx]
    if el >= 0:
        return 0
    else:
        return el, idx


def min_pos(arr_of_arrays, min_neg_col_idx):
    min_idx = 1
    min_val = arr_of_arrays[1][min_neg_col_idx]
    for line_idx in range(1, len(a)):
        line = a[line_idx]
        if line[min_neg_col_idx] == 0:
            continue
        coef = line[-1] / line[min_neg_col_idx]
        if coef < min_val and coef > 0:
            min_val = coef
            min_idx = line_idx
    return min_val, min_idx


def kill_sultans(a, exc, col):
    for i in range(len(a)):
        if i == exc:
            continue

        coef = -a[i][col]

        a[i] = a[i] + coef * a[exc]
    return a

iters = 0
while el_idx := min_neg(a[0]):
    el, min_neg_col_idx = el_idx

    min_pos_val, min_pos_row_idx = min_pos(a, min_neg_col_idx)
    if min_pos_val < 0:
        break

    a[min_pos_row_idx] = a[min_pos_row_idx] / a[min_pos_row_idx][min_neg_col_idx]

    a = kill_sultans(a, min_pos_row_idx, min_neg_col_idx)

    print(a)
    # break

    iters += 1
    if iters >= 1000:
        break

ans = a[0][-1]
print(ans)