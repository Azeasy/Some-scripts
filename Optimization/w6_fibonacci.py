from math import cos, pi


def func(x):
    return cos(x) ** 2


def get_fib(limit):
    output = [1, 1]

    i = 1
    while output[i] <= limit:
        output.append(output[i] + output[i - 1])

        i += 1

    return output


def main():
    # The realization of the golden section method of finding the min value
    # of the given convex function

    start = 0
    end = pi

    delta = 0.01

    fib = get_fib((end - start) / delta)

    h = ((end - start) / fib[-1])
    j = len(fib) - 1

    left = start + fib[j - 2] * h
    right = start + fib[j - 1] * h

    left_value = func(left)
    right_value = func(right)

    j -= 1
    while j >= 2:
        if left_value < right_value:
            end = right

            right = left
            right_value = left_value

            left = start + fib[j - 2] * h
            left_value = func(left)
        else:
            start = left

            left = right
            left_value = right_value

            right = start + fib[j - 1] * h
            right_value = func(right)

        j -= 1

    print(left, right, pi / 2 - left)


if __name__ == '__main__':
    main()
