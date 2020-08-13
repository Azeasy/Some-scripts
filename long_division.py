def short_division(dividend: int, divisor: int) -> int:
    """
    This function returns a digit - reminder of the division
    Note that it is called only for the short division.
    """
    reminder = dividend
    quotient = 0
    while reminder >= divisor:
        reminder -= divisor
        quotient += 1
    return quotient, reminder


def long_division(dividend: int, divisor: int) -> int:
    """
    Long division function
    """
    positive = (dividend > 0 and divisor > 0) or (dividend < 0 and divisor < 0)

    # We are finding a quotient that closer to 0 than others,
    # not the least reminder (according to the Euclidean function) case
    absdividend = abs(dividend)
    absdivisor = abs(divisor)

    # initially the quotient is 0
    quotient = "0"
    # the point, from which we append a digit to the temporary divisor
    pointer = 0
    s = str(absdividend)
    # reminder is the result of substraction at the last step
    reminder = 0

    while pointer < len(s):
        postfix = s[pointer:pointer + 1]
        reminder = int(str(reminder) + postfix)

        if reminder < absdivisor:
            quotient += "0"
            pointer += 1
            continue
        temp_quotient, temp_reminder = short_division(reminder, absdivisor)
        quotient += str(temp_quotient)
        reminder = temp_reminder

        pointer += 1
    if positive:
        return int(quotient), reminder
    return -int(quotient), -reminder
