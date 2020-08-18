def short_division(dividend: int, divisor: int) -> (int, int):
    """
    This function returns a digit - remainder of the division
    Note that it is called only for the short division.
    """
    remainder = dividend
    quotient = 0
    while remainder >= divisor:
        remainder -= divisor
        quotient += 1
    return quotient, remainder


def long_division(dividend: int, divisor: int) -> (int, int):
    """
    Long division function
    """
    if divisor == 0:
        raise ZeroDivisionError("The divisor must be non-zero integer")

    positive = (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0)

    # We are finding a quotient that closer to 0 than others,
    # not the least remainder (according to the Euclidean function) case
    absdividend = abs(dividend)
    absdivisor = abs(divisor)

    # initially the quotient is 0
    quotient = "0"
    # the point, from which we append a digit to the temporary divisor
    pointer = 0
    s = str(absdividend)
    # remainder is the result of substraction at the last step
    remainder = 0

    while pointer < len(s):
        postfix = s[pointer:pointer + 1]
        remainder = int(str(remainder) + postfix)

        # we are multiplying the quotint by 10
        if remainder < absdivisor:
            quotient += "0"
            pointer += 1
            continue

        # just substruction-based division max value of quotint is 9
        temp_quotient, temp_remainder = short_division(remainder, absdivisor)
        quotient += str(temp_quotient)
        remainder = temp_remainder

        pointer += 1
    if positive:
        return int(quotient), remainder
    return -int(quotient), -remainder


if __name__ == "__main__":
    while s := input():
        a, b = [int(x) for x in s.split()]

        print(a // b, a % b, "true value")
        print()
        p = long_division(a, b)
        print(p, "result")
