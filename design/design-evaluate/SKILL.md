---
name: design-evaluate
description: Use when assessing an identified interface candidate against agreed criteria, comparing revisions, or handing off missing design evidence.
---

# Design evaluation

Read the brief, versioned rubric, exact candidate and access instructions. Use
`docs/templates/design-evaluation.md` and `docs/templates/design-selection.md`.
An evaluator forms observations; generator claims/self-ratings are not evidence.
Record independent-session, human or self-review truthfully. If independent
review is unavailable, provide a fresh-session/human handoff and its missing access.

In the ai-dlc source repository, these templates/examples live under
`agents/templates/` and `agents/examples/`. In older projects without copied
assets, use the record contract below directly; do not require adoption.

Produce `docs/design/<work-id>/iterations/<candidate-id>/evaluation.md` with:

- Candidate ID/revision or digest, rubric version, work/RQ links, reviewer/session,
  actual tools/model/harness, review mode and limitations.
- Tested states/viewports/fixtures, expected versus observed, evidence links plus
  digest or immutable reference. Distinguish actual observation, supplied capture
  and synthetic example; never invent a tool run, transcript or human label.
- Each behavior result as pass/fail/unverified; each rating against its declared
  anchors or unverified. A screenshot can support limited visual judgment but
  cannot establish persistence, keyboard behavior or another interaction.
- Findings with criterion/candidate identity, severity, reproducible state/action,
  expected/observed evidence and specific correction/retest or prerequisite.
- Verdict, stop/continue reason, remaining authorized budget and next action.

A required failure or insufficient required rating means needs-work regardless
of aesthetics. Missing required evidence without a known failure means unverified.
Acceptance needs every required behavior pass, required rated thresholds met and
required evidence present. Keep optional ratings separate; missing evidence is
neither zero nor a pass. Compare brand-constrained work against its brief, not
against an invented demand for novelty or a new component system.

Use `decision.md` to retain candidates, matching reports and the effective rubric.
An earlier revision can win; cost and recency do not establish quality. Material
rubric changes create a new version and require reevaluation of every candidate
compared under it. Preserve old results under their old version, not as new proof.

Stop at contract satisfaction, exhausted budget, declared plateau or a material
unresolved decision. Stopping does not mean acceptance or authorize more rounds.
If no candidate qualifies, retain needs-work/unverified, residual findings and a
bounded follow-up. Human risk decisions cannot relabel evidence or bypass existing
specification/review/CI/finish gates. Do not delete authored candidates or reports.

The original library-room examples are synthetic. Follow
`docs/examples/design-evaluation/calibration.md` only for a separately scoped,
explicitly budgeted calibration exercise; absent human review and quality gains
remain unmeasured. This skill requires no new service, model or paid experiment.

For a running frontend with Playwright/browser setup in an adopted repository
(has `ai-dlc.toml`) with `ai-dlc` on PATH, use `ai-dlc design capture
--url URL --viewport WIDTHxHEIGHT --state NAME=SELECTOR` and cite its manifest
and PNG files for observed states and viewports. A named selector waits for
visible content; capture does not perform clicks or verify interaction journeys.
Missing capture remains unverified, and a skipped frontend-smoke check is not
application evidence. Keep manual interaction checks separate in the evaluation.
