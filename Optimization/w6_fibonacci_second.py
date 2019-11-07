from math import cos, pi


def func(x):
    return cos(x)**2


def get_fib(limit):
    b, c = 1, 2

    i = 1
    while b + c <= limit:
        b, c = c, b + c

        i += 1

    return b, c


def reduce_fib(a, b, c):
    return b - a, a, b


def main():
    # The realization of the golden section method of finding the min value
    # of the given convex function

    start = 0
    end = pi

    delta = 0.01

    pre_last, last_fib = get_fib((end - start) / delta)

    h = ((end - start) / last_fib)

    left = start + (last_fib - pre_last) * h
    right = start + pre_last * h

    left_value = func(left)
    right_value = func(right)

    pre_last, last_fib = last_fib - pre_last, pre_last

    while last_fib >= 2:
        if left_value < right_value:
            end = right

            right = left
            right_value = left_value

            left = start + (last_fib - pre_last) * h
            left_value = func(left)
        else:
            start = left

            left = right
            left_value = right_value

            right = start + pre_last * h
            right_value = func(right)

        pre_last, last_fib = last_fib - pre_last, pre_last

    print(left, right, pi / 2 - left)


if __name__ == '__main__':
    main()
