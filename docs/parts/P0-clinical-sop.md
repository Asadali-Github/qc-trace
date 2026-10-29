# P0 — Clinical review and SOP freeze
**Owner: Asad only. Nobody else can do this part.** Blocks P1 and P2.

## Goal
Turn `sop-draft.md` into a frozen `SOP.md` in the repo, with every clinical decision
confirmed by someone who has worked a bench.

## Why it matters
`qc_rules.py` implements the SOP exactly. Every gold verdict in the eval derives from it.
If a clinical decision is wrong, the eval is wrong — and the project's whole advantage is
that its author has real laboratory experience.

## Decisions to confirm (SOP §3.1)
1. 4-1s and 10-x applied **ungated** — no 1-2s breach required first. **This is
   load-bearing**: task family 5 has no point beyond 2 SD, so under classic gated Westgard
   the correct answer flips from REJECT to ACCEPT.
2. Does 2-2s span consecutive runs, or within-run only? The published source is silent.
3. Do 4-1s and 10-x span control materials? Westgard's site says they often do; the draft
   says they do not here.
4. The rule → error-category mapping (RANDOM / SYSTEMATIC). The authoritative source does
   not assign these, so the SOP must define them.
5. Is "no partial release of a bracket" realistic?
6. When a control is repeated, does the LIS retain the original?

## Acceptance
- `SOP.md` committed, every clause numbered, each annotated with its CLIA / CAP / ISO /
  CLSI source where one exists
- Any changed decision reflected in `qc_rules.py`, and `python -m pytest tests -q` green
- If a change alters expected verdicts, `tasks.py` expectations updated and the mutation
  tests still catch 7/7

## Do not
Do not soften a clause to make a task work. If a clinical decision kills a task family,
drop the family. Nine is already above the recommended minimum.
