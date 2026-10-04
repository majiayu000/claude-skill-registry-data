---
name: high-assurance-verification
description: Run the heavier pre-apply verification harness for a SENSITIVE change, one that is gate-blind on correctness (a fit or semantic property no existence gate can check), delicate at scale (a wide reshape or bulk mapping where a hand-edit is itself a defect risk), and costly to get wrong (a cited or downstream-relied-on artefact). Use before applying such a change, when the maintainer directs absolute-integrity rechecking, or when resuming a sensitive item left open in the register. It composes research fan-out, a mechanical signal pass over the negatives, independent adversarial verifiers from two or more model families (false-negative and false-positive lenses, blind to each other and to the research), a programmatic invariant floor, and a deterministic scripted apply plus re-parse, so apply-correctness does not rest on the orchestrator's in-context precision. It catches the plausible-but-wrong value that survives every existence gate because the gate confirms the value is well-formed, not that it is right.
derives_from: ../../governance/high-assurance-verification.md
---

# High-Assurance Verification (the sensitive-change harness)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Persistent register: the high-assurance register in the consuming project's working state, one row per sensitive item (the item, which trigger conditions make it sensitive, the stages run and their outcomes, the status). Open rows (`pending` / `in-progress` / `deferred`) are surfaced at session resume by the `/orch` command alongside the other standing registers, so an item survives a session boundary.
- Motivating case: adding a control-framework column to the compliance matrix, where each cell carries a control code whose fit no existence gate can check.
- Cadenced companion on matrix changes: the `/matrix-fit` semantic-fit audit (this harness at apply time, the cadence as the closing check).

An adopting project maps each bullet to its own register location, resume-surfacing mechanism, and companion cadences; the procedure below refers to them generically.

## Overview

Most changes are adequately protected by the routine layers: the research-assistant discipline (workers research, the orchestrator re-reads and authors), the mechanical gates, and the per-change and periodic sweeps. A small subset is not. When a change carries a correctness property no gate can check, is large or delicate enough that a hand-edit is itself a defect risk, and would be costly to get wrong because the artefact is cited or relied on downstream, the routine layers leave a real gap: a wrong value passes every gate, reads as plausible, and ships.

This skill is the executable form of the [`high-assurance-verification`](../../governance/high-assurance-verification.md) governance rule. The rule states the discipline (when and why); this skill states the procedure (how). It is a heavier tier above the routine [`ai-assistant-workflow-disciplines`](../../governance/ai-assistant-workflow-disciplines.md) research-assistant flow, not a replacement for it: it does not relax the routine apply-time verification, it adds independent adversarial verification and a deterministic apply on top. It is the proactive counterpart to the reactive [`trust-recovery-escalation`](../../governance/trust-recovery-escalation.md) suite: trust-recovery re-examines a window of work after process integrity has lapsed; this harness keeps a high-stakes change from becoming that failure in the first place.

The failure mode it prevents is observed directly: the fast first-pass research, uneven in depth, infers a "not applicable" or a value from a title or adjacent metadata without opening the source; a plausible-but-wrong value then survives every existence check because the check confirms the value is well-formed, not that it is the right value for its context. The harness produces the assurance rather than asserting it: independent adversarial stages hunt the misses and the over-assignments, and a deterministic apply plus re-parse makes the applied artefact correct independent of a long hand-edit.

The harness is not for every change. Invoking it everywhere is its own failure: it is expensive, and indiscriminate use erodes the signal that an item is genuinely high-stakes. The trigger (the three conditions in step 1) is a gate, not a default-on.

## When to Use

- **Before applying a sensitive change**, one that meets all three trigger conditions (gate-blind correctness, delicate scale, high escaped-error cost). The canonical shape: a bulk mapping of control codes whose fit no existence gate can check (the parent library's motivating case is named in the project wiring above).
- **When the maintainer directs absolute-integrity rechecking** of a change, regardless of the three conditions (maintainer discretion overrides the default trigger).
- **When resuming a sensitive item left open** in the persistent register named in the project wiring, with status `pending` or `in-progress`, surfaced at session resume.
- **NOT for routine changes.** When only one or two of the three conditions hold, the routine layers (research-assistant discipline, the gates, the per-change and project-wide sweeps) are the right tool and this harness is over-engineering.

## Process

### 1. Confirm the trigger and open the register row

Confirm the change meets all three trigger conditions: (1) **gate-blind correctness** (a wrong value is a correctness defect no mechanical gate catches, typically a fit or semantic property); (2) **delicate scale** (a wide reshape, a bulk mapping, a many-cell edit where a transposition or off-by-one is easy and not gate-caught); (3) **high escaped-error cost** (the artefact is citable, cross-linked, or relied on downstream). If only one or two hold, stop and use the routine layers. When uncertain, prefer the harness (a false escalation costs tokens; a false de-escalation ships a defect) and record the judgement so the threshold stays calibrated. The maintainer may direct the harness regardless of the conditions. Open a row in the persistent register named in the project wiring recording the item, which of the three conditions make it sensitive, and status `in-progress`, so the item survives a session boundary. Apply **guard-first sequencing**: if a mechanical gate for the value class will exist, land the gate before the data so the data is validated as it lands.

### 2. Research fan-out

Dispatch parallel research workers to produce the candidate values, per the research-assistant discipline. Workers produce research, not final prose; the orchestrator remains the author and re-reads every claim against the live source. Record which workers ran and what they produced in the register row.

### 3. Mechanical signal pass over the negatives

Run a deterministic search (a `grep`, a script) over the candidate set to surface what the research may have under-examined. The highest-value target is the **negatives**: the items a worker marked "no fit" / "N/A" / "no change". A negative reached by inference from a title or adjacent metadata, rather than by opening the source, is the dominant first-pass miss. Route every negative that carries a signal of the target attribute to a verifier read (the **open-on-negative-with-signal** discipline): a negative verdict on a candidate bearing a signal of the target attribute must be grounded in opening the source, not inferred.

### 4. Independent adversarial verification

Dispatch separate verifier workers, **blind to each other and to the research workers' reasoning**, each briefed to **refute, not to confirm**. Use two complementary lenses: a **false-negative** verifier that re-reads everything marked negative ("N/A" / "no change") and hunts the ones that should have been positive (the misses); and a **false-positive** verifier that judges every assigned value against ground truth (the source title, the canonical definition) and hunts the ones that are over-assigned or mis-fit. The verifiers are independent because a verifier that sees the research worker's rationale inherits its blind spots. Each verdict quotes the ground-truth source. When more than one failure mode is plausible, give each verifier a distinct lens rather than running identical ones; diversity of lens catches what redundancy cannot. The verifiers ARE drawn from DIFFERENT model families (two or more, for example one Claude-family, one GPT/Codex-family, and a Gemini-family where available), never multiple instances of one family: different families have systematically different blind spots, so a cross-family panel is stronger independence than same-family redundancy, and each additional independent family widens the coverage. Assign the distinct lenses across different families (the false-negative lens to one, the false-positive lens to another); a third available family adds a further independent verifier. Where a single refute-brief fits the change, run it to EACH available family and reconcile the verdicts; run to as many independent families as have tokens, the graduated floor on token or tooling unavailability keeping the cross-family minimum of two wherever two are available. A stage-4 finding loops back: a miss is corrected and re-verified before the apply, not patched in afterward.

### 5. Programmatic invariant floor

For any property a deterministic check can verify (an identifier is in the canonical set, a count matches, a flag is set), run that check and require it to pass. This is the existence-gate floor under the semantic verification above it; it does not replace steps 4 or 6. Where a project gate validates the value class, run it here as the floor.

### 6. Deterministic scripted apply, then re-parse

Do **not** hand-edit the sensitive artefact. Drive the apply with a dry-run-validated, idempotent-guarded script keyed on an explicit map (source location to verified value), then **re-parse the rendered artefact** and confirm every applied value matches the verified map. This is the step that makes apply-correctness independent of the orchestrator's in-context precision: a wide reshape applied by hand depends on the orchestrator not transposing a single cell across a long edit; the same reshape applied by a re-parsed script does not. The script and its dry-run output are part of the record. The script running is not evidence the rendered artefact is correct; the re-parse is.

### 7. Close the register row and surface

Record the harness outcomes in the register row (the workers, the verifier findings, the invariant checks, the apply script and its re-parse result) and set the status to `verified`. Surface the findings (the verifier misses and over-assignments, the invariant results, the re-parse result) in chat. A `verified` row is retained for the audit trail; do not silently drop a `pending` or `in-progress` row. If the item cannot complete this session (a closing re-check or a license-gated dependency remains), leave the row `pending` / `in-progress` (or `deferred` with the blocker named) so the next session resume re-surfaces it.

## Red Flags

- Skipping the harness on a sensitive item because the routine layers "probably caught it". The three conditions define when the routine layers are insufficient; "probably" is the inference the harness exists to replace with verification.
- A verifier that returns "all correct" without having tried to refute. Briefed to confirm, a verifier finds confirmation; the adversarial brief (hunt the misses, hunt the over-assignments) is what surfaces the defects.
- Letting a verifier see the research worker's rationale. Independence is the point; a verifier that inherits the research reasoning rubber-stamps its blind spots.
- Inferring a negative from a title. A "no fit" / "N/A" verdict on a candidate carrying a signal of the target attribute, reached without opening the source, is the dominant first-pass miss.
- Hand-editing the sensitive artefact. "I will just edit it carefully" is the failure mode the deterministic-apply-plus-re-parse step prevents.
- Declaring the apply correct from the script running, without the re-parse.
- Losing a pending item across a session boundary by not recording it in the register.
- Invoking the harness indiscriminately on changes that do not meet the three conditions, which erodes the signal that an item is genuinely sensitive.

## Verification

The harness is complete when:

- All three trigger conditions were confirmed (or the maintainer directed the harness), and a register row was opened.
- The research fan-out ran and the negatives were signal-passed (open-on-negative-with-signal applied).
- Independent adversarial verifiers, one per available model family (two or more; the graduated floor of two applies only on token or tooling unavailability), from DIFFERENT families (false-negative and false-positive lenses, blind), ran, each quoting ground truth; every miss they found was corrected and re-verified before the apply.
- The programmatic invariant floor passed.
- The apply was scripted (not hand-edited) and the rendered artefact was re-parsed against the verified map with zero mismatches.
- The register row records the stages and outcomes and is set to `verified` (or left `pending` / `in-progress` / `deferred` with the blocker named), and the findings were surfaced.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The existence gate passed, so the value is right." | The gate confirms the value is well-formed and in-catalogue, not that it is the right value for its context. Fit is gate-blind by construction. |
| "One verifier is enough." | One verifier briefed to confirm rubber-stamps. Two or more independent verifiers with complementary lenses (refute-the-negatives, refute-the-positives), one per available family, catch orthogonal failure modes. |
| "I read the negatives carefully; a verifier pass is redundant." | The dominant first-pass miss is a negative inferred from a title without opening the source. An independent re-read of the negatives is exactly what catches it. |
| "I will apply the edit carefully by hand." | A wide hand-edit makes correctness depend on not slipping across a long edit. A scripted apply plus re-parse removes that dependency. |
| "The apply script ran, so the artefact is correct." | The script running is not evidence the rendered artefact matches the verified map. The re-parse is. |
| "It is one cell; the harness is overkill." | If it meets the three conditions (gate-blind, delicate, costly), the routine layers are insufficient. If it does not, do not invoke the harness. The trigger decides, not the cell count. |

## See Also

- [`governance/high-assurance-verification.md`](../../governance/high-assurance-verification.md): the parent rule (when and why; the three trigger conditions; the five-stage harness; the persistent register).
- [`governance/trust-recovery-escalation.md`](../../governance/trust-recovery-escalation.md): the reactive counterpart (re-examination after a lapse); this skill is proactive.
- [`governance/ai-assistant-workflow-disciplines.md`](../../governance/ai-assistant-workflow-disciplines.md): the routine research-assistant flow this harness sits above.
- [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md): the apply and verification boundaries (the re-parse and quote-the-source requirements are this rule applied).
- [`matrix-fit`](../matrix-fit/SKILL.md): the cadenced semantic-fit audit; a sensitive matrix change often pairs the harness (apply) with `/matrix-fit` (the cadenced closing check).
- The persistent register named in the project wiring above, surfaced at session resume.
