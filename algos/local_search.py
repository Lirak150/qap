import itertools
import random
import typing as t

from tests.utils import Problem


class LocalSearch:
    def __init__(
        self,
        problem: Problem,
        max_iterations_local_search: int,
        max_no_improvements_count_local_search: int,
        max_iterations_iterated_local_search: t.Optional[int],
        max_no_improvements_count_iterated_local_search: t.Optional[int],
    ):
        self.problem = problem
        self.max_iterations_local_search = max_iterations_local_search
        self.max_no_improvements_count_local_search = (
            max_no_improvements_count_local_search
        )
        self.max_iterations_iterated_local_search = max_iterations_iterated_local_search
        self.max_no_improvements_count_iterated_local_search = (
            max_no_improvements_count_iterated_local_search
        )

    def count_delta_from_previous(
        self, solution: list[int], prev_delta: float, u: int, v: int, r: int, s: int
    ) -> float:
        return prev_delta + 2 * (
            self.problem.flows[r][u]
            - self.problem.flows[r][v]
            + self.problem.flows[s][v]
            - self.problem.flows[s][u]
        ) * (
            self.problem.distances[solution[s]][solution[u]]
            - self.problem.distances[solution[s]][solution[v]]
            + self.problem.distances[solution[r]][solution[v]]
            - self.problem.distances[solution[r]][solution[u]]
        )

    def count_delta(self, solution: list[int], r: int, s: int):
        delta = 0
        for k in range(self.problem.n):
            if k != r and k != s:
                delta += (self.problem.flows[k][r] + self.problem.flows[r][k]) * (
                    self.problem.distances[solution[s]][solution[k]]
                    - self.problem.distances[solution[r]][solution[k]]
                ) + (self.problem.flows[k][s] + self.problem.flows[s][k]) * (
                    self.problem.distances[solution[r]][solution[k]]
                    - self.problem.distances[solution[s]][solution[k]]
                )
        return delta

    def best_improvement(self, init_solution=None):
        no_improvements_count = 0
        prev_delta = None
        prev_swap = None
        if init_solution:
            solution = init_solution
        else:
            solution = list(range(self.problem.n))
            random.shuffle(solution)
        solution_improved = None
        for _ in range(self.max_iterations_local_search):
            if solution_improved is False:
                no_improvements_count += 1
            elif solution_improved is True:
                no_improvements_count = 0
            if no_improvements_count == self.max_no_improvements_count_local_search:
                break
            all_combinations = list(itertools.combinations(range(self.problem.n), 2))
            optimal_swap = None
            min_delta = prev_delta or 0
            solution_improved = False
            for swap in all_combinations:
                facility_1, facility_2 = swap
                if (
                    prev_swap is not None
                    and len(set(prev_swap).intersection({facility_1, facility_2})) == 0
                ):
                    delta = self.count_delta_from_previous(
                        solution, prev_delta, *prev_swap, facility_1, facility_2
                    )
                elif (
                    prev_swap is not None
                    and len(set(prev_swap).intersection({facility_1, facility_2})) != 0
                ):
                    continue
                else:
                    delta = self.count_delta(solution, *swap)
                if delta < min_delta:
                    min_delta = delta
                    optimal_swap = swap
            if optimal_swap:
                prev_swap = optimal_swap
                prev_delta = min_delta
                solution[facility_1], solution[facility_2] = (
                    solution[facility_2],
                    solution[facility_1],
                )
                solution_improved = True
        return solution, self.problem.cost(solution)

    def perturbation(self, solution: list[int]) -> list[int]:
        k = random.randint(2, self.problem.n)
        perturbation_indexes = random.sample(range(self.problem.n), k)
        shuffled_perturbation_indexes = perturbation_indexes.copy()
        random.shuffle(shuffled_perturbation_indexes)
        new_solution = solution.copy()
        for ind, shuffled_ind in zip(
            perturbation_indexes, shuffled_perturbation_indexes
        ):
            new_solution[ind] = solution[shuffled_ind]
        return new_solution

    def iterated_local_search(self):
        solution, cost = self.best_improvement()
        no_improvements_count = 0
        solution_improved = None
        for _ in range(self.max_iterations_iterated_local_search):
            if solution_improved is False:
                no_improvements_count += 1
            elif solution_improved is True:
                no_improvements_count = 0
            if (
                no_improvements_count
                == self.max_no_improvements_count_iterated_local_search
            ):
                break
            solution_improved = False
            perturbation = self.perturbation(solution)
            new_solution, new_solution_cost = self.best_improvement(perturbation)
            if new_solution_cost < cost:
                solution = new_solution
                cost = new_solution_cost
                solution_improved = True
        return solution, self.problem.cost(solution)
