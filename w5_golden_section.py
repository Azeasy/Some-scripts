from math import cos, pi, sqrt


def f(x):
    return cos(x)**2


def main():
    # The realization of the golden section method of finding the min value
    # of the given convex function

    start = 0
    end = pi

    gr = 2 / (1 + sqrt(5))

    delta = 0.01

    left = end - (end - start) * gr
    left_value = f(left)

    right = start + (end - start) * gr
    right_value = f(right)

    while abs(end - start) > delta:
        if right_value > left_value:
            end = right
            right = left
            right_value = left_value

            left = end - (end - start) * gr
            left_value = f(left)
        else:
            start = left
            left = right
            left_value = right_value

            right = start + (end - start) * gr
            right_value = f(right)

    print(start, end, abs(end - start))


if __name__ == '__main__':
    main()
