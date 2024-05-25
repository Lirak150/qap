from pathlib import Path

import pandas as pd

from algos.local_search import LocalSearch
from tests import utils
from collections import defaultdict

TESTS_PATH = Path(__file__).parent / "tests"
SOLUTION_PATH = Path(__file__).parent / "solutions"
TESTS = ["tai20a", "tai40a", "tai60a", "tai80a", "tai100a"]
READER = utils.Reader()
ls_metrics = defaultdict(list)
lsit_metrics = defaultdict(list)


for test in TESTS:
    n_iter = 1000
    current_test = TESTS_PATH / test
    problem = READER.read(current_test)
    local_search = LocalSearch(problem, n_iter, int(0.2 * n_iter), None, None)
    local_search_iterated = LocalSearch(
        problem, int(0.1 * n_iter), int(0.1 * 0.5 * n_iter), n_iter, int(0.2 * n_iter)
    )
    local_search_timing = utils.timing(3, local_search.best_improvement)
    local_search_iterated_timing = utils.timing(
        3, local_search_iterated.iterated_local_search
    )
    time_ls, (solution_ls, cost_ls) = local_search_timing
    time_lsit, (solution_lsit, cost_lsit) = local_search_iterated_timing

    with (SOLUTION_PATH / "local_search" /f'{test}.sol').open(mode="w") as ls_fd:
        ls_fd.write(" ".join([str(item) for item in solution_ls]))
    with (SOLUTION_PATH / "iterated_local_search" /f'{test}.sol').open(mode="w") as lsit_fd:
        lsit_fd.write(" ".join([str(item) for item in solution_lsit]))

    ls_metrics["time"].append(f'{time_ls:.{2}}')
    lsit_metrics["time"].append(f'{time_lsit:.{2}}')

    ls_metrics["cost"].append(cost_ls)
    lsit_metrics["cost"].append(cost_lsit)

    print(ls_metrics)
    print(lsit_metrics)

df_ls = pd.DataFrame.from_dict(ls_metrics, columns=TESTS, orient='index')
df_lsit = pd.DataFrame.from_dict(lsit_metrics, columns=TESTS, orient='index')


print(df_ls.to_markdown())
print()
print(df_lsit.to_markdown())



