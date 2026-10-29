# P4 — Analysis and pre-registration
Depends on **P3**'s output format only. Branch `p4-analysis`.

## Build
1. **`HYPOTHESES.md`, git-committed BEFORE any frontier run.** Record: direction of each
   claim, the test, the minimum detectable effect from power analysis, the **primary
   endpoint**, the random-effects specification, temperature, scaffold level.
   Point predictions go in a separate section labelled predictions — **never as success
   criteria**. A real, significant 12-point effect must not read as a failed
   pre-registration. Pre-register two-sided: the prior literature points both ways.
   **Primary endpoint:** the G1-vs-G3 paired difference in pass rate on actionable tasks
   under condition A.
2. **`analyze_results.py`** generating every table automatically:
   - Omnibus first (repeated-measures ANOVA, task as blocking unit, or Friedman), then
     **Holm** correction. Never rank from uncorrected pairwise tests
   - Exact McNemar on discordant pairs (already in `stats.py`)
   - Cluster bootstrap by task family (already in `stats.py`)
   - pass@1 and pass^3; worst case, CVaR@0.2, Reliability@0.9
   - Trivial baselines and prevalence printed alongside every score
   - Naive and corrected results side by side
3. **Severity rollup.** Count patient results at S4 or above under a false pass. Label it
   a **severity weight, not a harm estimate** — these are synthetic samples.

## Acceptance
- Every number in the README is produced by this script, not typed by hand
- Re-running it on the same `frontier_runs.jsonl` reproduces every figure exactly
- `HYPOTHESES.md` commit timestamp precedes the first frontier run commit

## Do not
Do not add a test after seeing the data and present it as planned. If an analysis was
added post hoc, label it post hoc.
