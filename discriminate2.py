"""Clean discrimination test: each wrong engine is the FULL correct engine with
exactly ONE mutation. Differences are therefore attributable to that mutation alone.
"""
import qc_rules as R
from qc_rules import QCEvent
from tasks import build
from typing import List
import copy, functools

def run_with(patches, h):
    """Temporarily patch qc_rules internals, evaluate, restore."""
    saved = {k: getattr(R, k) for k in patches}
    try:
        for k, v in patches.items(): setattr(R, k, v)
        v_, r_, _c, _z = R.evaluate(h)
        return (v_, r_)
    finally:
        for k, v in saved.items(): setattr(R, k, v)

# --- MUTATION 1: 2-2s drops the same-side requirement -------------------------
def m_two_2s_nosign(history):
    cur = history[-1]
    if cur.z1 is not None and cur.z2 is not None:
        if abs(cur.z1) > 2.0 and abs(cur.z2) > 2.0: return True
    for level in (1, 2):
        s = R._series(history, level)
        if len(s) >= 2 and abs(s[-2]) > 2.0 and abs(s[-1]) > 2.0: return True
    return False

# --- MUTATION 2: R-4s evaluated across consecutive events, not within-event ---
def m_r4s_across(ev):  # signature matches _r_4s(ev) but we need history; handled below
    return False
def m_two_2s_keep(history): return R._two_2s(history)
def m_r4s_across_hist(history):
    for level in (1, 2):
        s = R._series(history, level)
        if len(s) >= 2:
            a, b = s[-2], s[-1]
            if (a > 2.0 and b < -2.0) or (a < -2.0 and b > 2.0): return True
    return False

# --- MUTATION 3: classic 1-2s gating on 4-1s and 10-x ------------------------
def gated_eval(h):
    v, r, _c, _z = R.evaluate(h)
    cur = h[-1]
    if r in ("4_1s", "10_x"):
        if not any(z is not None and abs(z) > 2.0 for z in (cur.z1, cur.z2)):
            return ("ACCEPT", "NONE")
    return (v, r)

# --- MUTATION 4: manufacturer SD (z scaled by in_house_sd/mfr_sd = 2.0/5.0) ---
def mfr_eval(h):
    scaled = [QCEvent(e.run_id,
                      None if e.z1 is None else round(e.z1 * 0.4, 2),
                      None if e.z2 is None else round(e.z2 * 0.4, 2),
                      e.established_stats, e.timestamp) for e in h]
    v, r, _c, _z = R.evaluate(scaled)
    return (v, r)

# --- MUTATION 5: 1-2s treated as a REJECTION rule (over-cautious) -------------
def over_cautious_eval(h):
    v, r, _c, _z = R.evaluate(h)
    if v == "ACCEPT" and r == "1_2s_WARN": return ("REJECT", "1_2s_WARN")
    return (v, r)

# --- MUTATION 6: 4-1s needs only 3 consecutive (off-by-one) -------------------
def m_four_1s_three(history):
    for level in (1, 2):
        s = R._series(history, level)
        if len(s) >= 3:
            last = s[-3:]
            if all(z > 1.0 for z in last) or all(z < -1.0 for z in last): return True
    return False

# --- MUTATION 7: 10-x needs only 8 consecutive (short lookback) ---------------
def m_ten_x_eight(history):
    for level in (1, 2):
        s = R._series(history, level)
        if len(s) >= 8:
            last = s[-8:]
            if all(z > 0 for z in last) or all(z < 0 for z in last): return True
    return False

ENGINES = {
    "2-2s ignores same-side":   lambda h: run_with({"_two_2s": m_two_2s_nosign}, h),
    "R-4s across runs":         lambda h: run_with({"_r_4s": lambda ev: False,
                                                    "_two_2s": lambda hh: R._two_2s(hh) or m_r4s_across_hist(hh) and False}, h) if False else _r4s_variant(h),
    "classic 1-2s gating":      gated_eval,
    "manufacturer SD used":     mfr_eval,
    "1-2s treated as reject":   over_cautious_eval,
    "4-1s off-by-one (3 pts)":  lambda h: run_with({"_four_1s": m_four_1s_three}, h),
    "10-x short lookback (8)":  lambda h: run_with({"_ten_x": m_ten_x_eight}, h),
}

def _r4s_variant(h):
    """R-4s across events instead of within-event: replace _r_4s with a history-aware version."""
    saved_r, saved_eval = R._r_4s, None
    try:
        # within-event disabled; across-event enabled, injected via _r_4s closure over h
        R._r_4s = lambda ev, _h=h: m_r4s_across_hist(_h)
        v, r, _c, _z = R.evaluate(h)
        return (v, r)
    finally:
        R._r_4s = saved_r

SEEDS = range(1, 26)
names = list(ENGINES)
print("Each column = the correct engine with ONE mutation. 'n/25' = that task caught it.\n")
hdr = f"{'task':<5}" + "".join(f"{n[:24]:<26}" for n in names)
print(hdr); print("-" * len(hdr))
catch = {n: [] for n in names}
for fam in range(1, 10):
    row = f"T{fam:<4}"
    for n in names:
        fn = ENGINES[n]; diff = 0
        for s in SEEDS:
            h, want, rule, _ = build(fam, s)
            if fn(h) != (want, rule): diff += 1
        if diff: catch[n].append((fam, diff))
        row += f"{(f'{diff}/25' if diff else '—'):<26}"
    print(row)
print()
for n in names:
    if catch[n]:
        print(f"  {n:<26} caught by " + ", ".join(f"T{f}({d}/25)" for f, d in catch[n]))
    else:
        print(f"  {n:<26} *** NOT CAUGHT BY ANY TASK ***")
