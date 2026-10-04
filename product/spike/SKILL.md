---
name: spike
description: >-
  Run an exploratory, non-production experiment to decide whether an idea deserves a
  project. Reproduce current behaviour as a validated baseline, design a falsifiable
  experiment, measure gain and regression, produce inspectable evidence, and record
  a directional verdict plus a /sy:plan-ready brief when warranted.
argument-hint: "[problem, success bar, and data anchors]"
disable-model-invocation: true
effort: max
---

Answer: **is this idea worth a proper project?** Produce a reproducible exploratory artifact and directional verdict, not production code.

$ARGUMENTS

Before anything else, run the tracker preflight (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/preflight.md`); a failure stops here with its single `## Action needed` block, before any baseline work starts.

Create/load the spike Task via the `tracker` skill: discover candidate hackday Epics in the configured project (owned by the `tracker` skill), let the user choose the parent via `AskUserQuestion` (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`), create the Task, set it `in-progress`, and self-assign. Keep tracker command mechanics in the `tracker` skill (`/sy:tracker`), not here.

## Routing

- small cohesive evidence ⇒ read directly;
- broad archaeology ⇒ `sy:sweep`;
- one load-bearing production/data path ⇒ `sy:trace`, at most the resolved `limits.max_depth_agents` cap in flight — resolve per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`.

Returned briefs are leads. Verify decisive spans and own the experimental conclusions. Seed every agent prompt with known anchors — paths, symbols, data locations — and name ground already covered.

## 1. Establish the baseline

Locate the real production behaviour and enough representative data to reproduce it offline. Treat production as a **baseline/reference implementation**, not an oracle: the experiment may exist because production is wrong.

Validate baseline fidelity against known examples before comparing alternatives. Record any irreducible mismatch.

## 2. Validate reproduction

A failed reproduction is not yet a negative result. First verify:

- premise;
- data selection;
- baseline fidelity;
- ordering/configuration assumptions;
- sampling bias.

If the problem still does not reproduce, report that plainly. Do not manufacture a positive result.

## 3. Design the experiment

Define:

- falsifiable success bar;
- comparison baseline;
- primary metric(s);
- regression metric(s) in the opposite direction;
- representative and adversarial slices;
- controls for leakage/confounding where relevant.

Surface to the user via `AskUserQuestion` only when a load-bearing choice changes the experiment or verdict interpretation.

## 4. Measure gain and regression

Measure both directions: improvement and what gets worse. Use representative shapes and report uncertainty/sampling limits. Prefer direct metrics over proxy storytelling.

Every material empirical or spatial claim must be directly inspectable through a figure, table, or compact numeric evidence. Do not force a chart where a table or scalar is clearer.

## 5. Stress-test sampling

Probe boundary cases, failure clusters, and slices where the proposed approach should plausibly lose. Look specifically for evidence against the preferred hypothesis.

## 6. Produce the artifact

Create one standalone, reproducible artifact folder with:

- README/run instructions;
- data anchors or retrieval instructions;
- baseline reproduction;
- alternative implementation;
- metrics in both directions;
- figures/tables/numeric evidence;
- limitations and unresolved questions;
- exact environment/commands needed to rerun.

Repository-specific plotting/style defaults belong to repository standards, not this generic skill.

## 7. Record the verdict

Before posting it, pressure-test the directional conclusion with `sy:debate` — unconditionally, not only when the result looks contested: even a clear-looking gain/regression measurement can hide a confound, a sampling bias, or a stronger alternative explanation that only an adversary surfaces. See `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/debate.md`.

Post a tracker verdict comment. Its `human` part is the call being made:

- TL;DR verdict;
- strongest failure cases;
- recommendation: stop, iterate another spike, or start `/sy:plan`.

Its `agent_detail` part is what a later session reruns or cites from:

- headline gain and regression numbers;
- baseline-fidelity confidence;
- artifact path/link.

If the idea clears the bar, write a `/sy:plan` brief that states the opportunity, evidence, success bar, constraints, failure modes, and the next unanswered project-level questions. Link it from the verdict.

Set the spike Task's status to `done` via the `tracker` skill only after the verdict is durable. End with the Task key/link, artifact path, verdict, and `/sy:plan <brief>` kickoff when applicable.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
