"""Seeded task generator. Every task MUST fire exactly its intended rule set.
Rejection sampling on the padding history guarantees no accidental rule fires.
"""
import random
from typing import List, Tuple
from qc_rules import QCEvent, evaluate, all_fired

def _pad(rng, n, lo=-0.85, hi=0.85, alternate=True):
    """Benign history. Alternating signs prevents accidental 10_x / 4_1s."""
    out = []
    for i in range(n):
        mag = rng.uniform(lo if lo > 0 else 0.05, hi)
        sign = (1 if i % 2 == 0 else -1) if alternate else rng.choice([1, -1])
        out.append(round(sign * mag, 2))
    return out

def _mk(prefix, z1s, z2s, **kw):
    assert len(z1s) == len(z2s)
    return [QCEvent(f"{prefix}-{i:02d}", z1s[i], z2s[i], timestamp=1000 + i * 60, **kw)
            for i in range(len(z1s))]

def _jit(rng, v, lo, hi):
    """Jitter a value, keeping it inside (lo, hi) so the intended rule still fires."""
    return round(min(hi, max(lo, v + rng.uniform(-0.08, 0.08))), 2)

def build(family: int, seed: int, variant: str = "auto"):
    """Returns (history, expected_verdict, expected_rule, expected_fired_set).
    variant: "fire" = the rule triggers; "near_miss" = one point short, so ACCEPT.
    "auto" = odd seeds fire, even seeds are near-misses (families 5 and 7 only),
    so a model cannot learn "this family always rejects" and must actually count."""
    rng = random.Random(seed * 1000 + family)
    if variant == "auto":
        variant = "fire" if (family not in (5, 7) or seed % 2 == 1) else "near_miss"

    for _attempt in range(4000):
        if family == 1:                      # clean
            n = 6
            h = _mk("T1", _pad(rng, n, 0.05, 0.75), _pad(rng, n, 0.05, 0.75))
            want, rule, fired = "ACCEPT", "NONE", []

        elif family == 2:                    # 1_3s random spike
            n = 5
            z1 = _pad(rng, n, 0.05, 0.8) + [_jit(rng, 3.4, 3.05, 3.9)]
            z2 = _pad(rng, n + 1, 0.05, 0.8)
            h = _mk("T2", z1, z2)
            want, rule, fired = "REJECT", "1_3s", ["1_3s"]

        elif family == 3:                    # 2_2s within event, across levels
            n = 5
            z1 = _pad(rng, n, 0.05, 0.8) + [_jit(rng, 2.2, 2.05, 2.9)]
            z2 = _pad(rng, n, 0.05, 0.8) + [_jit(rng, 2.3, 2.05, 2.9)]
            h = _mk("T3", z1, z2)
            want, rule, fired = "REJECT", "2_2s", ["2_2s"]

        elif family == 4:                    # 1_2s warning only -> ACCEPT
            n = 5
            z1 = _pad(rng, n, 0.05, 1.6) + [_jit(rng, -2.3, -2.9, -2.05)]
            z2 = _pad(rng, n + 1, 0.05, 0.8)
            h = _mk("T4", z1, z2)
            want, rule, fired = "ACCEPT", "1_2s_WARN", []

        elif family == 5:                    # 4_1s drift, never crosses 2SD
            if variant == "fire":
                drift = [_jit(rng, v, 1.02, 1.95) for v in (1.15, 1.30, 1.40, 1.25)]
                want, rule, fired = "REJECT", "4_1s", ["4_1s"]
            else:                            # BOUNDARY: exactly 3 points beyond 1SD
                drift = [_jit(rng, v, 1.02, 1.95) for v in (1.18, 1.33, 1.27)]
                want, rule, fired = "ACCEPT", "NONE", []
            n = 4
            z1 = _pad(rng, n, 0.05, 0.9) + drift
            z2 = _pad(rng, n + len(drift), 0.05, 0.9)
            h = _mk("T5", z1, z2)

        elif family == 6:                    # R_4s within event, opposite sides
            n = 5
            z1 = _pad(rng, n, 0.05, 0.8) + [_jit(rng, 2.2, 2.05, 2.9)]
            z2 = _pad(rng, n, 0.05, 0.8) + [_jit(rng, -2.1, -2.9, -2.05)]
            h = _mk("T6", z1, z2)
            want, rule, fired = "REJECT", "R_4s", ["R_4s"]

        elif family == 7:                    # 10_x same side, all under 1SD
            k = 10 if variant == "fire" else 9     # BOUNDARY: 9 points is one short
            run = [round(rng.uniform(0.25, 0.95), 2) for _ in range(k)]
            z1 = _pad(rng, 2, 0.05, 0.8) + run
            z2 = _pad(rng, 2 + k, 0.05, 0.9)
            h = _mk("T7", z1, z2)
            if variant == "fire":
                want, rule, fired = "REJECT", "10_x", ["10_x"]
            else:
                want, rule, fired = "ACCEPT", "NONE", []

        elif family == 8:                    # the Mirage -> ACCEPT (warning only)
            n = 4
            a = _jit(rng, 2.15, 2.05, 2.6)
            b = -_jit(rng, 2.15, 2.05, 2.6)
            z1 = _pad(rng, n, 0.05, 0.8) + [a, b]
            z2 = _pad(rng, n + 1, 0.05, 0.8) + [_jit(rng, -0.4, -0.9, -0.1)]
            h = _mk("T8", z1, z2)
            want, rule, fired = "ACCEPT", "1_2s_WARN", []

        elif family == 9:                    # lack of data: L2 not measured
            n = 5
            z1 = _pad(rng, n, 0.05, 0.8) + [round(rng.uniform(-0.9, 0.9), 2)]
            z2 = _pad(rng, n, 0.05, 0.8) + [None]
            h = _mk("T9", z1, z2)
            want, rule, fired = "INDETERMINATE_LACK_OF_DATA", "INCOMPLETE_DATA", []
        else:
            raise ValueError(family)

        v, r, _cat, _z = evaluate(h)
        if v == want and r == rule and all_fired(h) == fired:
            return h, want, rule, fired
    raise RuntimeError(f"family {family} seed {seed}: no valid instance in 4000 attempts")
