class Partition():
    def __init__(self, n):
        self.number = n
        self.partition = Partition.partition_func(n)
        self.count = Partition.partition_count_func(self.number, self.number)

    def __str__(self):
        out = ''
        for _partitions_ in self.partition:
            temp = []
            for _partition_ in _partitions_:
                _partition_ = [str(x) for x in _partition_]
                temp.append(" + ".join(_partition_))
            for sum_ in temp:
                out += f'{self.number} = {sum_}\n'
        return out

    @staticmethod
    def get_var(n, k):
        temp = []
        for i in range(k):
            temp.append(f'v{i}')
        return ", ".join(temp)

    @staticmethod
    def get_cycles(n, k):
        temp = []
        for i in range(k):
            if i == 0:
                temp.append(f'for v{i} in range(1, {(n//k) + 1})')
            else:
                temp.append(f'for v{i} in range(v{i-1}, {n})')
        return ' '.join(temp)

    @staticmethod
    def get_sum_of_variables(n, k):
        temp = []
        for i in range(k):
            temp.append(f'v{i}')
        return "+".join(temp)

    @staticmethod
    def partition_n_k(n, k):
        a = [1] * k
        if n == k:
            return [tuple(a)]
        elif k + 1 == n:
            return [tuple(a[:-1] + [2])]
        elif k + 2 == n and n > 3:
            return [tuple(a[:-1] + [3]), tuple(a[:-2] + [2, 2])]

        variables = Partition.get_var(n, k)
        cycles = Partition.get_cycles(n, k)
        sum_of_variables = Partition.get_sum_of_variables(n, k)

        magic_line = f'[({variables},) {cycles} if {sum_of_variables} == {n}]'
        # print(magic_line)

        # Note that we use eval func. That's not safe but fast way to make
        # n times nested loop
        return eval(magic_line)

    @staticmethod
    def partition_func(n):
        if n == 0:
            return [[(0,)]]
        return [Partition.partition_n_k(n, k) for k in range(n, 0, -1)]

    @staticmethod
    def partition_count_func(n, m):
        # This function return a partition of the number n
        # to the m or less parts
        if n == m:
            return 1 + Partition.partition_count_func(n, m - 1)
        if m == 0 or n < 0:
            return 0
        if n == 0 or m == 1:
            return 1

        return Partition.partition_count_func(n, m - 1) + \
            Partition.partition_count_func(n - m, m)

    # TODO: think about making a partition based on the above recursion.
    # It can reduce the time complexity

# for i in range(17):
    # b = Partition.partition_count_func(i, i)
    # b = Partition(i)
    # print(b)
