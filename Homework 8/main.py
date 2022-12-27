import random as r
import numpy as np


class equation:
    def __init__(self, arguments, sum):

        self.sum = sum
        self.arguments = np.array(arguments)
        self.args = np.zeros(len(arguments))

    def try_a(self, args):
        return np.dot(self.arguments, np.array(args).transpose())

    def mistake(self, args):
        return abs(self.try_a(args) - self.sum)

    def solution(self, generation=6):
        e = 0
        length = len(self.arguments)

        genomes = [[r.randint(1, self.sum) for i in range(length)] for i in range(generation)]
        bin = lambda: r.randint(0, 1)

        def parent(a):
            rt = r.randint(0, 10000)
            if rt < a[0]:
                return 0
            for i in range(1, len(a)):
                if a[i - 1] < rt < a[i]:
                    return i

        while True:
            mistakes = [self.mistake(i) for i in genomes]
            sum = 0.0
            for m in range(len(mistakes)):
                if mistakes[m] == 0:
                    self.args = np.array(genomes[m])
                    return genomes[m]
                sum += 1 / mistakes[m]
            al = [int((1 / m) / sum * 10000) for m in mistakes]
            res = [0 for i in range(generation)]
            res[0] = al[0]

            for i in range(1, len(al)):
                res[i] = res[i - 1] + al[i]
            parents = []
            for i in range(generation):

                first = parent(res)
                while first is None:
                    first = parent(res)
                second = first
                while second == first:
                    second = parent(res)
                    while second is None:
                        second = parent(res)

                parents.append((first, second))

            s = genomes[np.argmax(al)]
            genomes = [[genomes[f[j % 2]][j] for j in range(length)] for f in parents]

            for v in genomes:
                if bin() == 1:
                    v[r.randint(0, length - 1)] = r.randint(1, self.sum)

            genomes[0] = s
            e += 1

if __name__ == '__main__':
    dga = equation([1, 2, 3, 4, 5], 196)
    print("1a+2b+3c+4d+5e=196 = ", dga.solution())