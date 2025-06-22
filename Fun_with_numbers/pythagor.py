# Pythagorean triples


def generate(a, b):
    return abs(a ** 2 - b ** 2), 2 * a * b, abs(a ** 2 + b ** 2)


for i in range(1, 10):
    for j in range(1, 10):
        print(generate(i, j))
