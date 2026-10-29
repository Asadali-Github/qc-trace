"""SOP-CHEM-QC-01 rule engine. Implements section 3 exactly as drafted.
This is the oracle: it decides the gold verdict for a task, and later backs grader G3.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class QCEvent:
    """One QC event: both control levels measured. z = (value - in_house_mean)/in_house_sd."""
    run_id: str
    z1: Optional[float]          # Level 1 z-score; None = not measured
    z2: Optional[float]          # Level 2 z-score; None = not measured
    established_stats: bool = True   # in-house mean/SD exist for this lot
    timestamp: Optional[int] = None  # None = missing timestamp

# Rejection rules in SOP section 3 order (precedence = lowest row first)
REJECT_RULES = ["1_3s", "2_2s", "R_4s", "4_1s", "10_x"]
CATEGORY = {"1_3s": "RANDOM", "2_2s": "SYSTEMATIC", "R_4s": "RANDOM",
            "4_1s": "SYSTEMATIC", "10_x": "SYSTEMATIC"}

def _series(history: List[QCEvent], level: int) -> List[float]:
    """z-scores for one control level, oldest -> newest, over events with that level measured."""
    out = []
    for e in history:
        z = e.z1 if level == 1 else e.z2
        if z is not None:
            out.append(z)
    return out

def _one_3s(ev: QCEvent) -> bool:
    return any(z is not None and abs(z) > 3.0 for z in (ev.z1, ev.z2))

def _r_4s(ev: QCEvent) -> bool:
    """Within one event, one level >+2 and the other <-2. SOP 3.1(c): within-event only."""
    if ev.z1 is None or ev.z2 is None:
        return False
    return (ev.z1 > 2.0 and ev.z2 < -2.0) or (ev.z2 > 2.0 and ev.z1 < -2.0)

def _two_2s(history: List[QCEvent]) -> bool:
    """SOP 3.1(b): two consecutive beyond the SAME limit, within a level across events,
    OR within a single event across the two levels."""
    cur = history[-1]
    # within current event, across levels, same side
    if cur.z1 is not None and cur.z2 is not None:
        if (cur.z1 > 2.0 and cur.z2 > 2.0) or (cur.z1 < -2.0 and cur.z2 < -2.0):
            return True
    # across consecutive events within a level
    for level in (1, 2):
        s = _series(history, level)
        if len(s) >= 2:
            a, b = s[-2], s[-1]
            if (a > 2.0 and b > 2.0) or (a < -2.0 and b < -2.0):
                return True
    return False

def _four_1s(history: List[QCEvent]) -> bool:
    """SOP 3.1(d): within a single level, 4 consecutive beyond the SAME 1SD limit."""
    for level in (1, 2):
        s = _series(history, level)
        if len(s) >= 4:
            last4 = s[-4:]
            if all(z > 1.0 for z in last4) or all(z < -1.0 for z in last4):
                return True
    return False

def _ten_x(history: List[QCEvent]) -> bool:
    """SOP 3.1(d): within a single level, 10 consecutive on the same side of the mean."""
    for level in (1, 2):
        s = _series(history, level)
        if len(s) >= 10:
            last10 = s[-10:]
            if all(z > 0 for z in last10) or all(z < 0 for z in last10):
                return True
    return False

def _one_2s_warn(ev: QCEvent) -> bool:
    return any(z is not None and abs(z) > 2.0 for z in (ev.z1, ev.z2))

def evaluate(history: List[QCEvent]) -> Tuple[str, str, str, float]:
    """history oldest->newest; the last element is the current QC event.
    Returns (verdict, triggered_rule, error_category, max_abs_z)."""
    cur = history[-1]

    # INDETERMINATE_LACK_OF_DATA takes precedence (SOP section 4)
    if (not cur.established_stats) or cur.z1 is None or cur.z2 is None or cur.timestamp is None:
        zs = [abs(z) for z in (cur.z1, cur.z2) if z is not None]
        return ("INDETERMINATE_LACK_OF_DATA", "INCOMPLETE_DATA", "UNVERIFIABLE",
                max(zs) if zs else float("nan"))

    max_abs_z = max(abs(cur.z1), abs(cur.z2))

    fired = []
    if _one_3s(cur):            fired.append("1_3s")
    if _two_2s(history):        fired.append("2_2s")
    if _r_4s(cur):              fired.append("R_4s")
    if _four_1s(history):       fired.append("4_1s")
    if _ten_x(history):         fired.append("10_x")

    if fired:
        rule = min(fired, key=lambda r: REJECT_RULES.index(r))   # SOP 3.1(e)
        return ("REJECT", rule, CATEGORY[rule], max_abs_z)

    if _one_2s_warn(cur):       # SOP 3.1(f)
        return ("ACCEPT", "1_2s_WARN", "NONE", max_abs_z)

    return ("ACCEPT", "NONE", "NONE", max_abs_z)

def all_fired(history: List[QCEvent]) -> List[str]:
    """Every rule that fires, for design verification (we want exactly one per task)."""
    cur = history[-1]
    f = []
    if _one_3s(cur):      f.append("1_3s")
    if _two_2s(history):  f.append("2_2s")
    if _r_4s(cur):        f.append("R_4s")
    if _four_1s(history): f.append("4_1s")
    if _ten_x(history):   f.append("10_x")
    return f
