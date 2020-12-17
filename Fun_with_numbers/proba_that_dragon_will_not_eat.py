# Python program for nth Catalan Number
# Returns value of Binomial Coefficient C(n, k)


def binomialCoefficient(n, k):

    # since C(n, k) = C(n, n - k)
    if (k > n - k):
        k = n - k

    # initialize result
    res = 1

    # Calculate value of [n * (n-1) *---* (n-k + 1)]
    # / [k * (k-1) *----* 1]
    for i in range(k):
        res = res * (n - i)
        res = res / (i + 1)
    return res


# A Binomial coefficient based function to
# find nth catalan number in O(n) time
def catalan(n):
    c = binomialCoefficient(2 * n, n)
    return int(c / (n + 1))


# The code above was contributed by Aditi Sharma

"""
The problem:
    There is a very scary dragon living in Almaty city near KBTU.
    Everyday he needs to eat several young students for a launch. He usually
    kidnaps them one by one in the morning and eats at a launch time,
    having put them in a line at a cell in his prison. But sometimes he has
    problems with his launch, because students vanish! He still doesn’t know
    that pair of boy and a girl (B-G) can disappear if they stand together
    exactly in this order (B-G) due to the magic of love. After that line
    becomes smaller. So, there is a possibility that no one will be left for a
    dragon launch!
"""
# The following part counts a probability that
# boys and girls from the problem disappear
for i in range(100):
    print(catalan(i) / 2 ** (2 * i))
