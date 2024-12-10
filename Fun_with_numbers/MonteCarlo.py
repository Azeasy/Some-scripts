import random


def estimate_phi(num_samples):

    phi_estimate = 0

    left = 0
    right = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)

        # we just count dots left and right to the point
        # where a / b = b / (a + b)
        ratio_1 = (1 - x) / (x)
        ratio_2 = (x) / 1

        if ratio_1 > ratio_2:
            left += 1
        else:
            right += 1

    phi_estimate = left / right
    return phi_estimate


def estimate_pi(num_samples, dim=2):

    pi_estimate = 0

    inside = 0
    outside = 0

    for _ in range(num_samples):
        r = 1  # radius of our N-sphere
        coef = 1  # coefficient in front of π in the area formula
        x = random.uniform(0, 1)
        if dim >= 2:
            coef = 1  # Area = 1 * π * r^2
            y = random.uniform(0, 1)
        if dim >= 3:
            coef = 4 / 3  # Area = (4/3) * π * r^3
            z = random.uniform(0, 1)
 
        distance = x**2
        if dim >= 2:
            distance += y**2
        if dim >= 3:
            distance += z**2

        if distance <= r**2:
            inside += 1
        else:
            outside += 1

    # we take the number of dots inside of the sphere,
    # divide by all dots, we get a ratio, then we adjust it to the
    # formula of the area (volume) by dividing by the coef
    # and multiply by number of symmetrical regions in the
    # n-dimensional cube with the side = r (1)
    if dim >= 1:
        pi_estimate = 2**dim / (coef) * inside / (inside + outside)
    if dim >= 2:
        pi_estimate = 2**dim / (coef) * inside / (inside + outside)
    if dim >= 3:
        pi_estimate = 2**dim / (coef) * inside / (inside + outside)
    return pi_estimate


if __name__ == "__main__":
    # Run the estimation
    num_samples = 1_000_000  # Number of random samples
    phi_estimate = estimate_phi(num_samples)
    print(f"Estimated value of φ: {phi_estimate}")

    pi_estimate = estimate_pi(num_samples, dim=1)
    print(f"Estimated value of π: {pi_estimate}")

    pi_estimate = estimate_pi(num_samples, dim=2)
    print(f"Estimated value of π: {pi_estimate}")

    pi_estimate = estimate_pi(num_samples, dim=3)
    print(f"Estimated value of π: {pi_estimate}")
