"""
The solution of the Poisson 2D equation
using Jacobi method and MPI library
for the parallel calculating.

Requirements:
python 3.
mpi4py
numpy
matplotlib
MPI


Variables you may want to change:
Grid:
N, M

Accuracy:
accuracy

Function:
f

Boundary conditions:
outlets - von Neumann's conditions
inlets - Dirichlet's conditions

Partition:
By default it is square, if possible,
if not, it is the nearest values to the root, for example:
50 -> 10 x 5
30 -> 6 x 5
etc.
Above, the left side is the number of the columns (horizontal partition)

Of course, you can set any other partition, you just add two numbers - columns and rows on the execution.

Running (windows):
mpiexec -n 6 python poisson_2D_topology.py
or with custom partition:
mpiexec -n 6 python poisson_2D_topology.py 6 1

6 after -n is the number of processors
"""

from mpi4py import MPI
from time import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Horizontal grid
N = 30
# Vertical grid
M = 30

accuracy = 0.0001


# Define your f here:
# Pxx + Pyy = -f
def f(x, y):
    return x**2


# Define your boundary conditions here:
left_outlets = []
right_outlets = [(0, 0.2), (0.4, 0.6), (0.7, 0.9)]
up_outlets = []
down_outlets = []

left_inlets = [(0, 0.3), (0.6, 0.8)]
right_inlets = []
up_inlets = []
down_inlets = [(0.3, 0.6)]


l_outlet = []
r_outlet = []
u_outlet = []
d_outlet = []

l_inlet = []
r_inlet = []
u_inlet = []
d_inlet = []

for item in left_outlets:
    l_outlet += [(i, 0) for i in range(int(item[0] * M), int(item[1] * M))]
for item in right_outlets:
    r_outlet += [(i, N - 1) for i in range(int(item[0] * M), int(item[1] * M))]
for item in up_outlets:
    u_outlet += [(0, j) for j in range(int(item[0] * N), int(item[1] * N))]
for item in down_outlets:
    d_outlet += [(M - 1, j) for j in range(int(item[0] * N), int(item[1] * N))]

for item in left_inlets:
    l_inlet += [(i, 0) for i in range(int(item[0] * M), int(item[1] * M))]
for item in right_inlets:
    r_inlet += [(i, N - 1) for i in range(int(item[0] * M), int(item[1] * M))]
for item in up_inlets:
    u_inlet += [(0, j) for j in range(int(item[0] * N), int(item[1] * N))]
for item in down_inlets:
    d_inlet += [(M - 1, j) for j in range(int(item[0] * N), int(item[1] * N))]

inlet = r_inlet + l_inlet + u_inlet + d_inlet


border_x = 1
for i in range(int(size ** 0.5), 0, -1):
    if size % i == 0:
        border_x = i
        break

border_y = size // border_x

if len(sys.argv) >= 2:
    try:
        border_y = int(sys.argv[1])
        border_x = int(sys.argv[2])
    except ValueError as e:
        raise e
    except IndexError:
        raise IndexError("Make sure that you gave two parameters for the grid")

is_grid_ok = (N % border_y == 0, M % border_x == 0, border_x * border_y == size)

if rank == 0:
    print(f"The partition is {border_y} by {border_x}")

    if not all(is_grid_ok):
        text_1 = f"\nN - grid ({N}) is not divisible by {border_y} - partition coefficient" \
            if not is_grid_ok[0] else ''
        text_2 = f"\nM - grid variable with value of {M} is not divisible by {border_x} - partition coefficient" \
            if not is_grid_ok[1] else ''
        text_3 = f"\nInvalid grid {N} by {M} for the processors count {size}" if not is_grid_ok[2] else ''
        raise IndexError(text_1 + text_2 + text_3)

if all(is_grid_ok):
    steps_x = N // border_y
    steps_y = M // border_x
else:
    exit()

dx = 1 / N
dy = 1 / M

# This is to create default communicator and get the rank
cartesian2d = comm.Create_cart(dims=[border_y, border_x], periods=[False, False], reorder=True)
coord2d = cartesian2d.Get_coords(rank)

left_rank, right_rank = cartesian2d.Shift(direction=0, disp=1)
top_rank, bottom_rank = cartesian2d.Shift(direction=1, disp=1)
#
#
# print()
# print(border_x, border_y)
# print(rank, left_rank, right_rank, top_rank, bottom_rank)
# exit()

# print(f"Rank {rank}; coord {coord2d}")
# print(f" my rank is {rank}; left is {left_rank}; right is {right_rank}; roses are red;")
# print(f" my rank is {rank}; top is {top_rank}; bottom is {bottom_rank}; violets are blue;")
# exit()

"""
+++++++++
+ 0 + 2 +
+++++++++
+ 1 + 3 +
+++++++++
"""

global_arr = np.zeros((M, N))

left, top = coord2d
right, bottom = left + 1, top + 1

left *= steps_x
right *= steps_x
top *= steps_y
bottom *= steps_y

# left = (rank // int(size ** 0.5)) * steps
# right = (rank // int(size ** 0.5) + 1) * steps
# top = (rank % int(size ** 0.5)) * steps
# bottom = (rank % int(size ** 0.5) + 1) * steps

rank_arr = []
if coord2d == [0, 0]:
    rank_arr = global_arr[top: bottom + 1, left: right + 1]
elif coord2d == [0, border_x - 1]:
    rank_arr = global_arr[top - 1: bottom, left: right + 1]
elif coord2d == [border_y - 1, 0]:
    rank_arr = global_arr[top: bottom + 1, left - 1: right]
elif coord2d == [border_y - 1, border_x - 1]:
    rank_arr = global_arr[top - 1: bottom, left - 1: right]
elif coord2d[0] == 0:
    rank_arr = global_arr[top - 1: bottom + 1, left: right + 1]
elif coord2d[0] == border_y - 1:
    rank_arr = global_arr[top - 1: bottom + 1, left - 1: right]
elif coord2d[1] == 0:
    rank_arr = global_arr[top: bottom + 1, left - 1: right + 1]
elif coord2d[1] == border_x - 1:
    rank_arr = global_arr[top - 1: bottom, left - 1: right + 1]
else:
    rank_arr = global_arr[top - 1: bottom + 1, left - 1: right + 1]

# print(rank, left_rank, right_rank, top_rank, bottom_rank, rank_arr.shape)
# print('  ', left, right, top, bottom, coord2d)
#
# exit()


def normalize(input_arr, input_coord2d):
    if input_coord2d == [0, 0]:
        input_arr = input_arr[:-1, :-1]
    elif input_coord2d == [0, border_x - 1]:
        input_arr = input_arr[1:, left:-1]
    elif input_coord2d == [border_y - 1, 0]:
        input_arr = input_arr[:-1, 1:]
    elif input_coord2d == [border_y - 1, border_x - 1]:
        input_arr = input_arr[1:, 1:]
    elif input_coord2d[0] == 0:
        input_arr = input_arr[1:-1, :-1]
    elif input_coord2d[0] == border_y - 1:
        input_arr = input_arr[1:-1, 1:]
    elif input_coord2d[1] == 0:
        input_arr = input_arr[:-1, 1:-1]
    elif input_coord2d[1] == border_x - 1:
        input_arr = input_arr[1:, 1:-1]
    else:
        input_arr = input_arr[1:-1, 1:-1]
    return input_arr


def poisson_iter(arr):
    j_shift, i_shift = 0, 0
    if coord2d[0] != 0:
        j_shift = -1
    if coord2d[1] != 0:
        i_shift = -1

    tmp = arr.copy()
    for i in range(1, len(arr) - 1):
        for j in range(1, len(arr[0]) - 1):
            tmp[i][j] = ((arr[i][j + 1] + arr[i][j - 1]) / dx**2 +
                         (arr[i + 1][j] + arr[i - 1][j]) / dy**2 +
                         f((top + i + i_shift) * dx, (left + j + j_shift) * dy)) / (2 / dx**2 + 2 / dy**2)
    return tmp


def boundaries(arr):
    if coord2d[0] != 0 and coord2d[1] != 0:
        tmp_arr = arr[1:, 1:]
    elif coord2d[0] != 0:
        tmp_arr = arr[:, 1:]
    elif coord2d[1] != 0:
        tmp_arr = arr[1:, :]
    else:
        tmp_arr = arr

    for i in range(len(tmp_arr)):
        for j in range(len(tmp_arr[0])):
            if (top + i, left + j) in r_outlet:
                tmp_arr[i][j] = tmp_arr[i][j - 1]
            elif (top + i, left + j) in l_outlet:
                tmp_arr[i][j] = tmp_arr[i][j + 1]
            elif (top + i, left + j) in u_outlet:
                tmp_arr[i][j] = tmp_arr[i + 1][j]
            elif (top + i, left + j) in d_outlet:
                tmp_arr[i][j] = tmp_arr[i - 1][j]
            elif (top + i, left + j) in inlet:
                tmp_arr[i][j] = 1

    # if coord2d[0] != 0 and coord2d[1] != 0:
    #     arr[1:, 1:] = tmp_arr
    # elif coord2d[0] != 0:
    #     arr[:, 1:] = tmp_arr
    # elif coord2d[1] != 0:
    #     arr[1:, :] = tmp_arr
    # else:
    #     arr = tmp_arr

    return arr


def get_err(arr1, arr2):
    err = 0
    for i in range(len(arr1)):
        for j in range(len(arr1[0])):
            diff = abs(arr1[i][j] - arr2[i][j])
            if diff > err:
                err = diff
    return err


iters = 0

ok = True
start = time()
while ok:
    new_arr = poisson_iter(rank_arr)
    new_arr = boundaries(new_arr)
    error = get_err(new_arr, rank_arr)

    if left_rank != -1:
        cartesian2d.send(new_arr[:, 1], tag=1, dest=left_rank)
        new_arr[:, 0] = cartesian2d.recv(tag=1, source=left_rank)
    if right_rank != -1:
        cartesian2d.send(new_arr[:, -2], tag=1, dest=right_rank)
        new_arr[:, -1] = cartesian2d.recv(tag=1, source=right_rank)
    if top_rank != -1:
        cartesian2d.send(new_arr[1, :], tag=1, dest=top_rank)
        new_arr[0, :] = cartesian2d.recv(tag=1, source=top_rank)
    if bottom_rank != -1:
        cartesian2d.send(new_arr[-2, :], tag=1, dest=bottom_rank)
        new_arr[-1, :] = cartesian2d.recv(tag=1, source=bottom_rank)

    rank_arr = new_arr.copy()

    run = True
    if rank != 0:
        comm.send(error, tag=0, dest=0)
    else:
        outer_err = error
        # combining all rows together
        for i in range(1, size):
            res = comm.recv(tag=0, source=i)
            if res > outer_err:
                outer_err = res
        if outer_err < accuracy:
            run = False
            end = time()
    ok = comm.bcast(run, root=0)

    iters += 1

if rank != 0:
    comm.send(rank_arr, tag=2, dest=0)
else:
    rank_arr = normalize(rank_arr, coord2d)

    to_concat = [[0 for i in range(border_y)] for j in range(border_x)]
    to_concat[0][0] = rank_arr
    for i in range(1, size):
        x, y = cartesian2d.Get_coords(i)
        to_concat[y][x] = normalize(comm.recv(tag=2, source=i),
                                    [x, y])

    line_to_concat = [to_concat[i][0] for i in range(border_x)]

    for i in range(border_x):
        for j in range(1, border_y):
            line_to_concat[i] = np.concatenate((line_to_concat[i], to_concat[i][j]), axis=1)

    for i in range(1, border_x):
        line_to_concat[0] = np.concatenate((line_to_concat[0], line_to_concat[i]), axis=0)

    P = line_to_concat[0]

    # print(P)
    print(f"Time is {end - start}")
    plt.pcolormesh(P, cmap=cm.jet)
    plt.show()
