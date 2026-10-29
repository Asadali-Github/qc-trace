# P5 — Evidence and packaging
**No dependencies. Can run any time.** Branch `p5-evidence`.

## Build
1. **BetterBench self-scorecard** (`docs/betterbench-scorecard.md`). Score the eval against
   all 46 criteria across Design, Implementation, Documentation and Maintenance; mark each
   pass / fail / not applicable with one line of evidence. Known gaps to close while doing
   it: per-instance UUIDs, a CI badge, release requirements, a contact person, a feedback
   channel, a licence file.
2. **Croissant file with Responsible AI metadata**, validated with the official validator.
   NeurIPS 2026's Evaluations & Datasets track requires it and rejects submissions without
   one. Shipping it lets the README say the eval meets a top venue's submission bar.
3. **Validity card** (`docs/validity-card.md`): every check marked pass / fail /
   not-probed — trivial baselines, prevalence, scaffold reporting, forged-probe results,
   positional baselines, specificity alongside any F1, scope-of-claim statement.
4. **Generator card**: seeds, how instances are produced, contamination notes.
5. **Canary wiring.** `CANARY.md` exists; make every emitted JSONL record carry
   `evaluation_only`, `do_not_train` and `benchmark_canary`.
6. **Licence files.** MIT for code, CC BY 4.0 for data and SOP.

## Acceptance
- Croissant file passes the official validator
- Scorecard covers all 46 criteria with evidence, including honest failures
- Every record in `results/*.jsonl` carries the canary fields

## Do not
Do not mark a BetterBench criterion as passed without a line of evidence. An honest
"fail" is worth more than an unsupported "pass".
