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


def long_division(dividend: int,
                  divisor: int,
                  number_of_digits=214748364) -> (int, int):
    """
    Long division function
    """
    if divisor == 0:
        raise ZeroDivisionError("The divisor must be non-zero integer")

    if dividend == 0:
        return "0"

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

    # max lenght of the period is equal to divisor by Dirichlet's principle
    period_length = absdivisor
    # the counter for the decimal separator
    # it's an analogue to the pointer variable but for the fractional step
    period_step = 0
    is_periodic = True

    # Determine whether the fractional part started or not
    if absdividend >= absdivisor:
        period_started = False
        remainder = 0
    else:
        remainder = absdividend
        period_started = True

    # end if our fractional part become too long.
    # Unfortunately, we can't go forever

    true_period = 0
    is_periodic = False
    some_set = []

    while period_step <= period_length and period_step < number_of_digits:
        if period_started:
            postfix = "0"
        else:
            postfix = s[pointer:pointer + 1]

        # the postfix is an empty string in case of complete division
        if not postfix:
            break

        remainder = int(str(remainder) + postfix)
        if period_started:
            if remainder in some_set:
                true_period = some_set.index(remainder)
                true_period = len(some_set) - true_period
                is_periodic = True
                break
            some_set.append(remainder)
        if remainder < absdivisor and not period_started:
            quotient += "0"
            pointer += 1
            continue
        elif remainder < absdivisor and period_started:
            quotient += "0"
            period_step += 1
            continue

        # just substruction-based division max value of quotint is 9
        temp_quotient, temp_remainder = short_division(remainder, absdivisor)
        quotient += str(temp_quotient)
        remainder = temp_remainder

        if remainder == 0 and period_started:
            period_step += 1
            break
        elif remainder == 0 and not period_started:
            # the code will break, if pointer will exceed the dividend
            pointer += 1
            continue

        if period_started:
            period_step += 1
        else:
            pointer += 1

        # three conditions to start the fractional part
        if remainder < absdivisor and not period_started and pointer >= len(s):
            period_started = True

    if period_step != 0:
        slice_index = len(quotient) - period_step
        quotient = f"{quotient[:slice_index:]}." + \
                   f"{quotient[slice_index:]}"

        if is_periodic:
            slice_index = len(quotient) - true_period
            quotient = f"{quotient[:slice_index]}" + \
                       f"({quotient[slice_index:]})"

    quotient = quotient.lstrip("0")
    if quotient[0] == ".":
        quotient = "0" + quotient

    if positive:
        return quotient
    return "-" + quotient


if __name__ == "__main__":
    # an interesting example is a = 1, b = 998001
    while s := input():
        a, b = [int(x) for x in s.split()]

        print(a / b, "true value")
        print()
        p = long_division(a, b, 3000)
        print(p, "result")
