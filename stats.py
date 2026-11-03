"""Statistics, pure standard library so the core path has zero dependencies.
Protocol follows "Adding Error Bars to Evals" (2411.00640) and
"Statistical Methods for Multiple Language Model Comparison" (2608.22659).
"""
from math import comb
from random import Random
from typing import List, Tuple, Dict

def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar on discordant pairs: binomial(b+c, 0.5).
    b = passed by A, failed by B.  c = failed by A, passed by B."""
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)

def paired_diff(pairs: List[Tuple[int, int]]) -> float:
    """Mean of (a_i - b_i) over matched runs."""
    return sum(a - b for a, b in pairs) / len(pairs) if pairs else 0.0

def cluster_bootstrap_ci(by_cluster: Dict[int, List[Tuple[int, int]]],
                         reps: int = 10000, seed: int = 7,
                         alpha: float = 0.05) -> Tuple[float, float]:
    """Resample CLUSTERS (task families) with replacement, not individual runs.
    Clustered SEs ran up to 3.05x naive in 2411.00640, so this matters."""
    rng = Random(seed)
    keys = list(by_cluster)
    draws = []
    for _ in range(reps):
        picked = [rng.choice(keys) for _ in keys]
        pool = [p for k in picked for p in by_cluster[k]]
        draws.append(paired_diff(pool))
    draws.sort()
    lo = draws[int((alpha / 2) * reps)]
    hi = draws[int((1 - alpha / 2) * reps) - 1]
    return lo, hi

def pass_hat_k(successes_by_task: Dict[str, List[int]], k: int) -> float:
    """pass^k (tau-bench): fraction of tasks succeeding in ALL k trials."""
    vals = [1 if all(v[:k]) and len(v) >= k else 0 for v in successes_by_task.values()]
    return sum(vals) / len(vals) if vals else 0.0

def pass_at_k(successes_by_task: Dict[str, List[int]], k: int) -> float:
    """pass@k: fraction of tasks with AT LEAST ONE success in the first k trials."""
    vals = [1 if any(v[:k]) else 0 for v in successes_by_task.values()]
    return sum(vals) / len(vals) if vals else 0.0

def pass_at_1(successes_by_task: Dict[str, List[int]]) -> float:
    flat = [x for v in successes_by_task.values() for x in v]
    return sum(flat) / len(flat) if flat else 0.0

def worst_case_and_cvar(scores: List[float], alpha: float = 0.2) -> Tuple[float, float]:
    """Reliability beyond the mean (2609.09218): worst case and CVaR@alpha."""
    if not scores: return 0.0, 0.0
    s = sorted(scores)
    m = max(1, int(alpha * len(s)))
    return s[0], sum(s[:m]) / m

def reliability_at(scores: List[float], tau: float = 0.9) -> float:
    return sum(1 for x in scores if x >= tau) / len(scores) if scores else 0.0
