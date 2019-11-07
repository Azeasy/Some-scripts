import math
PI = math.pi
sin = math.sin
interval_start = -PI / 2
interval_end = PI / 2
N = 1000

h = (interval_end - interval_start) / N
e = h / 100


def func(u):
    return sin(u)**2


def main():
    # The realization of the unifomr search method of finding the min value
    # of the given convex function
    u = interval_start
    min_value = func(u)
    min_parameter = u

    for i in range(N):
        u = interval_start + (i + 1) * h
        current_value = func(u)

        if current_value < min_value:
            min_value = current_value
            min_parameter = u

    left_parameter = min_parameter - e
    left_value = func(left_parameter)

    right_parameter = min_parameter + e
    right_value = func(right_parameter)

    if left_value < min_value:
        min_value = left_value
        min_parameter = left_parameter

    if right_value < min_value:
        min_value = right_value
        min_parameter = right_parameter

    print(min_parameter, min_value)


if __name__ == '__main__':
    main()
