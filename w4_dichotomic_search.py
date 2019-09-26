from math import cos, pi


def f(x):
    return cos(x)**2


def main():
    # The realization of the dichotomic method of finding the min value
    # of the given convex function
    start = 0
    end = pi

    delta = 0.01
    e = delta / 10

    while abs(end - start) > delta:
        left = (start + end) / 2 - e
        left_value = f(left)

        right = (start + end) / 2 + e
        right_value = f(right)

        if right_value > left_value:
            end = right
            continue
        else:
            start = left
            continue

    print(start, end, abs(end - start))


if __name__ == '__main__':
    main()
