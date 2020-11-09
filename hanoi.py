def hanoi(h, start, dest):
    # We only have 3 rods
    start, dest = start % 3, dest % 3

    # This rod is used to move h - 1 disks
    if (start + 1) % 3 != dest:
        free_rod = (start + 1) % 3
    else:
        free_rod = (start - 1) % 3

    # Simply move first disk
    if h == 1:
        print(1, start, dest)
    else:
        # Free the biggest disk by moving h - 1 disks
        hanoi(h - 1, start, free_rod)

        # Move the biggest disk
        print(h, start, dest)

        # Move h - 1 disks to the highest disk. The tower was moved.
        hanoi(h - 1, free_rod, dest)


if __name__ == "__main__":
    msg = "Enter three numbers: tower height, start and destination rods\n"
    while s := input(msg):
        height, start, dest = [int(x) for x in s.split()]
        hanoi(height, start, dest)
