"""
This code takes six-digit number from console and verboses it
"""

import re


def main():
    pass
    a = 563412

    # Dictionaries for the switch-case logic
    decs_dict = {
        "0": "",
        "1": "ten",
        "2": "twenty",
        "3": "thirty",
        "4": "fourty",
        "5": "fifty",
        "6": "sixty",
        "7": "seventy",
        "8": "eighty",
        "9": "ninety"
    }

    units = {
        "0": "",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine"
    }

    ten_to_nineteen = {
        "0": "ten",
        "1": "eleven",
        "2": "twelve",
        "3": "thirteen",
        "4": "fourteen",
        "5": "fifteen",
        "6": "sixteen",
        "7": "seventeen",
        "8": "eighteen",
        "9": "nineteen"
    }

    while a:
        s = str(a)
        ans = ''

        # First three digits verbosing
        ans += units.get(s[0]) + " hundred "

        if s[1] != "1":
            ans += decs_dict.get(s[1]) + ' '
            ans += units.get(s[2]) + ' '
        else:
            ans += ten_to_nineteen.get(s[2]) + ' '

        ans += "thousand "

        # Last three digits verbosing
        if units.get(s[3]):
            ans += units.get(s[3]) + " hundred "

        if s[4] != "1":
            ans += decs_dict.get(s[4]) + ' '
            ans += units.get(s[5]) + ' '
        else:
            ans += ten_to_nineteen.get(s[5])

        ans = re.sub("\s+", " ", ans)

        print(ans)

        # input for the next value of a
        a = input()


if __name__ == "__main__":
    main()
