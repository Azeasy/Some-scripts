def short_multiplication(first: int, second: int) -> int:
    first, second = min(first, second), max(first, second)
    out = 0
    for i in range(first):
        out += second
    return out


def normalize(digits: list):
    """
    Editing each digit with carrying over a digit in case of digit is > 9
    """
    n = len(digits)

    i = n - 1
    while i > 0:
        if digits[i] > 9:
            digits[i - 1] += 1
            digits[i] -= 10
        else:
            i -= 1

    return digits


def add_number(digits: list, number: int, position: int):
    """
    Adding a number at the specified position with the carrying over a digit
    """

    n = len(digits)
    s = str(number)
    for i in range(len(s)):
        digits[n - position - 1] += int(s[len(s) - i - 1])
        position += 1
    return digits


def long_multiplication(first: int, second: int) -> int:
    positive = (first > 0 and second > 0) or (first < 0 and second < 0)
    first, second = abs(first), abs(second)
    first, second = min(first, second), max(first, second)
    s1, s2 = str(first), str(second)

    answer = [0] * (len(s1) + len(s2))

    pointer1 = 0
    pointer2 = 0

    for i1 in s1[::-1]:
        for i2 in s2[::-1]:
            position = pointer1 + pointer2

            # two digits multiplication
            temp_value = short_multiplication(int(i1), int(i2))
            answer = add_number(answer, temp_value, position)

            pointer2 += 1
        pointer1 += 1
        pointer2 = 0

    answer = normalize(answer)

    str_ans = ""
    for i in answer:
        str_ans += str(i)
    int_ans = int(str_ans)

    if positive:
        return int_ans
    return -int_ans


if __name__ == "__main__":
    while s := input():
        a, b = [int(x) for x in s.split()]

        print(a / b, "true value")
        print()
        p = long_multiplication(a, b)
        print(p, "result")
