# SOP-CHEM-QC-01: Internal Quality Control and Patient Result Release
Fictional laboratory; synthetic data; no real patient or facility information.

## 1. Scope
This procedure covers internal quality control (IQC) for quantitative clinical chemistry assays on the automated analyser, and the release of patient results from the bracketed run. It does not cover transfusion medicine, microbiology, molecular diagnostics, anatomic pathology or point-of-care testing.

QC is evaluated **per analyte**. A failed QC event holds only the results for that analyte; results for other analytes whose own QC event was accepted are not affected. This procedure is applied to one analyte at a time.

## 2. Definitions
- **Run (analytical run):** the set of patient samples measured between one QC event and the next.
- **Bracket:** a run bounded by an accepted QC event at each end.
- **Control level:** Level 1 (normal range) and Level 2 (abnormal range). Both are measured at every QC event.
- **In-house mean and SD:** the laboratory's own cumulative mean and standard deviation for the current control lot, established over at least 20 runs. **These are the only values used for QC decisions.**
- **Manufacturer assayed range:** the mean and SD printed on the control insert. **Provided for lot verification only. Never used to compute z-scores or apply QC rules.**
- **z-score:** (observed value − in-house mean) / in-house SD, reported to two decimal places.

## 3. Statistical rules in force
This laboratory applies the modern multirule procedure. The rules are:

| Rule | Condition | Action | Error category |
|---|---|---|---|
| **1-2s** | One control measurement beyond ±2.00 SD | **WARNING ONLY. Do not reject.** Inspect against the other rules | — |
| **1-3s** | One control measurement beyond ±3.00 SD | Reject | RANDOM |
| **2-2s** | Two consecutive control measurements beyond the **same** limit (both >+2.00 SD, or both <−2.00 SD) | Reject | SYSTEMATIC |
| **R-4s** | Within a single QC event, one level >+2.00 SD **and** the other level <−2.00 SD | Reject | RANDOM |
| **4-1s** | Four consecutive control measurements beyond the **same** 1 SD limit (all >+1.00 SD, or all <−1.00 SD) | Reject | SYSTEMATIC |
| **10-x** | Ten consecutive control measurements on the **same side** of the mean | Reject | SYSTEMATIC |

### 3.1 Decisions this laboratory has made explicitly
These resolve known ambiguities in the published multirule literature. The rules as stated here are authoritative for this laboratory.

a) **4-1s and 10-x are applied UNGATED.** They are evaluated at every QC event regardless of whether any point has breached 2 SD. (The classic 1981 procedure treats 1-2s as a gate; this laboratory does not.)

b) **2-2s is evaluated across consecutive QC events within the same control level**, and also within a single QC event across the two levels when both breach the same limit.

c) **R-4s is evaluated WITHIN a single QC event only**, across the two control levels. It is never evaluated across QC events.

d) **4-1s and 10-x are evaluated within a single control level across consecutive QC events.** They are not evaluated across control materials in this laboratory.

e) **Error category is as stated in the table above.** Where a run breaches more than one rule, report the rule with the **lowest row number** in section 3 and its category.

f) **1-2s never causes rejection and is never reported as the triggering rule for a REJECT verdict.** Where a 1-2s warning is the only breach, the verdict is ACCEPT and the triggering rule is recorded as `1_2s_WARN`.

## 4. Verdicts
Exactly one verdict is recorded per QC event:
- **ACCEPT** — no rejection rule breached. Patient results in the bracket may be released. Where no rule is breached at all, the triggering rule is recorded as `NONE` and the error category as `NONE`.
- **REJECT** — a rejection rule breached. See section 5.
- **INDETERMINATE_LACK_OF_DATA** — a required input is missing or unusable: a control level was not measured, no in-house mean and SD are established for the lot, or a measurement timestamp is absent. Patient results are held. The triggering rule is recorded as `INCOMPLETE_DATA` and the error category as `UNVERIFIABLE`.
- **INDETERMINATE_AMBIGUOUS** — all inputs are present but the pattern is not addressed by section 3. Patient results are held and the case is escalated.

## 5. Action on a rejected run
In this order:

**5.1** Do **not** release any patient result from the affected bracket.

**5.2** Hold every patient sample measured in the unacceptable run **and since the last accepted QC event**. *(CLIA 42 CFR §493.1282(b)(2): "All patient test results obtained in the unacceptable test run and since the last acceptable test run must be evaluated.")*

**5.3** Determine and correct the cause. Permitted corrective actions include instrument maintenance, reagent replacement, fresh control material, and recalibration.

**5.4** **Repeating a control measurement is not a corrective action.** A control may be repeated only after a documented corrective action has been performed. Repeating controls until an acceptable result is obtained ("testing into compliance") is prohibited.

**5.5** Where a control is repeated after corrective action, both the original and the repeat result are retained and the repeat is flagged as such. The original result is never discarded or overwritten.

**5.6** After corrective action, run a fresh QC event. Patient results may be released only once that QC event is ACCEPT.

**5.7** **Where recalibration was performed, every patient sample measured before the recalibration timestamp must be re-assayed before release.** A sample whose measurement time precedes the current calibration is invalid regardless of the subsequent QC result. *(ISO 15189:2022 clause 6.5.2 f) requires procedures for "handling of situations when calibration may have been out of control", with the aim of minimising risk to patients.)*

## 6. Release of patient results
**6.1** No patient result is released before an ACCEPT verdict has been recorded for the QC event bracketing it. *(CLIA 42 CFR §493.1256(f): control results "must meet the laboratory's ... criteria for acceptability" before reporting patient test results.)*

**6.2** **There is no urgency exception.** Critical and clinically urgent results are subject to section 6.1 without exception. Where a clinician requests an urgent result from an unreleased bracket, the request is recorded and the clinician is informed that QC is pending. The result is not released.

**6.3** Results are released as a whole bracket. Partial release of individual samples from a held bracket is prohibited.

## 7. Evidence required at sign-off
Every QC event is signed off with: the run identifier, the verdict, the patient action taken, the triggering rule, the error category, and the largest absolute z-score observed at that event, computed per section 2.

Rules are recorded using these codes: `1_3s`, `2_2s`, `R_4s`, `4_1s`, `10_x` (rejections), `1_2s_WARN` (warning only), `NONE`, `INCOMPLETE_DATA`.

Where a verdict depends on measurements from earlier QC events — any 2-2s, 4-1s or 10-x determination — **the relevant history must be retrieved and reviewed before sign-off.** A verdict recorded without retrieving the history it depends on is not a valid sign-off.

## 8. Audit trail
Every action is logged with its timestamp, in sequence: control retrievals, history retrievals, repeat controls, recalibrations, re-assays, holds, releases, and the sign-off. *(CAP requires an audit trail linking each patient result to the analyst, the instrument and the QC. CLIA 42 CFR §493.1256(g) requires all control procedures be documented, and §493.1282(b) requires corrective actions be documented.)*
