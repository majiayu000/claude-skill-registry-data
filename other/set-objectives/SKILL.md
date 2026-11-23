---
name: set-objectives
description: Choose the dominant outcome and the smallest useful set of observable objectives, each with a target stated as an owner-set or proposed ambition with its reason, a horizon and trade-off rules. Use when strategy starts, when the mandate or stage changes, or when a review shows an objective is inadequate.
---

# set-objectives

Writes [`objectives`](../../../../.group/contracts/objectives.md) under the shared [document rules](../../../../.group/contracts/document-rules.md).

## When and what it decides

The question: **which outcome deserves concentration now, at what ambition and by when, and what yields when outcomes conflict?** Runs from the start (no readout is needed) and again when a strategy-review finds the objective itself is the defect.

## Inputs and authority

- `mandate` and owner material: ends, horizon, binding commitments. An owner-set target or date binds; quote it.
- `venture-definition`: what the venture is and its current focus.
- Current commercial state; `readout` and the previous `strategy-review` when they exist.
- A financial observation (`financial-report`) only when it bears on the particular choice.
- A missing baseline stays `unknown`; choosing a target never supplies one.

## Method

Record sources, exact owner quotes and calculation premises in the relevant table’s basis or source cells. Carry decision status in its status column and the document’s role; prose states choices and ambition directly.

1. **Derive outcomes from ambition.** Read Perspective and ambition and recover the owner's intended reach, adoption, authority or scale. Develop observable outcomes that express it, then the first commercial outcomes that serve it. Apply [objective trade-offs](../../../knowledge/objective-tradeoffs-and-outcome-mechanisms.md) §2 to connect those ends and means.
2. **Separate kinds.** Sort candidates into outcomes, leading indicators and activities (§1). Only outcomes become objectives; leading indicators go to bets as control signals; activities go to the focus-plan.
3. **Choose a connected set.** Keep the ambition beside the first commercial outcomes. Include each outcome that changes a decision; use a guard where pursuit could damage an important result. State which near-term outcome deserves concentration and how it contributes to the wider ambition.
4. **Set targets and baselines.** Baseline holds the current value or starting for a new venture. Basis carries its source, the reason for each target and horizon, and the owner quote when the target is owner-set. Target status carries owner-set, proposed or accepted. Use an observation criterion when a number would add unsupported precision.
5. **Resolve conflicts.** For each real conflict over shared inputs, write a precedence or conditional rule and what is deferred (§4).
6. **Name reconsideration.** State the condition that warrants revising each objective. When revising, show the reason; a missed target is recorded as missed, never hidden by a moved date.

## Evaluate and correct

| Defect | Detect by | Correct by |
| --- | --- | --- |
| Ambition missing from the objective set | Only first sales appear despite a wider owner ambition | Develop the reach, adoption, authority or scale outcome and connect commercial objectives to it |
| Activity as objective | It can be met with the venture no better off | Move it to the focus-plan; state the outcome it serves |
| Target as forecast | Language of expectation ("we will reach") or no rationale | Restate as ambition with its reason and status |
| Invented baseline | Current value lacks a source | Use starting for a new venture or retrieve the current value and cite it in Basis |
| Unattributed owner target | "owner-set" without a quote | Add the passage, or change status to proposed |
| Too many objectives | Objectives that never change a decision | Remove or turn into a guard |

Run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {material}` for structure, statuses and quotes.

## Recovery

- **NeedData:** no end or horizon is stated anywhere. Propose an outcome from the venture-definition with status proposed and ask the owner the single question that fixes the horizon; prioritize-bets may proceed on the proposed objective.
- **Conflict:** mandate horizon and owner brief disagree. Use the mandate, state the discrepancy for the owner.
- **Failure:** check errors; correct at the row and rerun.

## Example

Illustrative fixture: fictional founder material and venture.

Brindlewick's founder wants own-format reporting to become a professional standard and wants paying inspectors using the app on real jobs by the end of March.

```markdown
## Focus
Establish own-format reporting as a useful professional practice, beginning with paid use of the app on real inspection jobs. Commercial adoption supplies working examples that other inspectors can learn from.

## Objectives
| ID | Outcome | Metric or observation | Baseline | Target | Target status | Horizon | Basis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OBJ-1 | Own-format reporting spreads across practices | Inspectors outside the initial users reuse a published report approach and explain its value | starting | Independent reuse of the first practice example | proposed | First adoption cycle | [proposed] observable first step toward wider reach and authority; [owner: "We want own-format reporting to become the standard across independent practices and inspection firms."] |
| OBJ-2 | Inspectors pay for and use the app on real jobs | Paid licence followed by a delivered client report | starting | Paid use on real jobs | owner-set | End of March | [owner: "Our first goal is paying inspectors using the app on real jobs by the end of March."] Paid use develops sustainable delivery for the wider ambition |

## Trade-offs
| Competing outcomes | Rule | Deferred |
| --- | --- | --- |
| OBJ-1, OBJ-2 | Use completed report examples to serve both learning and adoption; preserve report quality when preparing commercial demonstrations | Broad promotion until a useful example is ready |
```

A new venture's baseline is starting. An operating venture replaces it with its sourced current value; the target remains the desired outcome.

## Final readable delivery

After this change's native documents and checks are final, follow the group's Human-readable result delivery: run `python3 {product-root}/.group/tools/result_html.py {state-directory} --open` once for the combined result and return `result.html` with the native files. The product root is this installed strategy group; the state directory is the current documents, with no automatic candidate overlay. Intermediate exports omit `--open`. Keep the complete file and report the exact path if the host cannot open it. This derived view changes no native record, decision, status or delivery contract.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.
