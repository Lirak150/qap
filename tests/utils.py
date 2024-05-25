import pathlib
from time import time


class Problem:
    def __init__(self, n, distances, flows):
        self.n = n
        self.distances = distances
        self.flows = flows

    def cost(self, sol: list[list[int]]):
        cost_ = 0
        for i in range(self.n):
            for j in range(self.n):
                cost_ += self.flows[i][j] * self.distances[sol[i]][sol[j]]

        return cost_


class Reader:
    def read(self, file: pathlib.Path) -> Problem:
        distances = []
        flows = []
        with file.open(mode="r") as problem_fd:
            n = int(problem_fd.readline().strip())
            for _ in range(n):
                distances.append(list(map(int, problem_fd.readline().split())))
            problem_fd.readline()
            for _ in range(n):
                flows.append(list(map(int, problem_fd.readline().split())))

        return Problem(n=n, distances=distances, flows=flows)


def timing(times, func, *args, **kwargs):
    experiments = []
    for _ in range(times):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        experiments.append(end - start)
    return sum(experiments) / len(experiments), result
