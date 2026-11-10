---
name: spec-format
description: The three change artifacts for Iron Pipeline and their exact formats — Spec (docs/specs/*.md with decisions, ambiguity log, numbers, ACs, size, budget), Features (features/*.feature, Gherkin only) and Plan (plans/*.md for planned-size work) — plus the scenario→test mapping. Load before writing, reviewing or implementing any change.
---
# Spec, Features, Plan

Three artifacts, three names, never mixed. The words "spec", "features" and "plan" mean only these.

| Artifact | File | Holds | Who owns it |
|---|---|---|---|
| **Spec** | `docs/specs/NNNN-<name>.md` | intent, scope, **Numbers** (with tolerances), **Decisions & Ambiguity Log**, ACs, commands/state, presentation, consistency gate, **Size**, **Budget** | human approves (Gate 1) |
| **Features** | `features/NNNN-<name>.feature` | Gherkin scenarios only; each becomes one test | human approves with the Spec |
| **Plan** | `plans/NNNN-<name>.md` | slices, steps (IMPLEMENT/TEST/REFACTOR/Files/Commit), waves, Build Progress | produced by `/dev-team:plan`, human approves; **planned** size only; slices copy the Features scenarios (same S-IDs and steps, plus `# Still passes if:` comments; Features wins on any difference) |

Templates: `docs/specs/TEMPLATE.md`, `features/TEMPLATE.feature`. Worked example: 0001.

## Rules
- **Spec id** = exactly four digits, allocated as max existing + 1 (`scripts/next-spec-id.sh`; run it when naming work), never reused, no suffixes or letters. A follow-up gets the next number and cites its parent in the Spec header as `**Follows:** NNNN`. `0000` is reserved for process-only branches (no Spec). The definition lives in `scripts/lib/spec-id.sh`; `scripts/check-spec-ids.sh` enforces names, uniqueness and Spec↔Features links.
- **A new package, a new project, a new external file format, or hand-writing a parser/serializer for a standard format (YAML, JSON, CSV, TOML, XML) is always a `human` decision. Never inferable.** The allowlist is `dependencies.allowed`; changing it needs a `human` row in a Spec naming the package and why.
- **On "approved", re-read the Spec and Features files from disk** before acting; the human may have edited them.
- **Every change has a Spec and a Features file**, even a bug fix (a Spec can be ten lines; "no decisions" is a valid log).
- **Numbers live in the Spec, with a tolerance or `exact`.** A value with no tolerance is not approvable. Values then go to `content/`, never into C#.
- **Ambiguity Log:** before writing ACs, list every open question. Try to infer; if one plausible alternative exists that the repo does not rule out, it is `human`, and the human answers it before approval. "Inferable" is not a convenient default. If you can offer a guess, the decision is inferable — write the guess as the rationale. `human` is reserved for decisions where two defensible answers lead to different games.
- **Schema'd content:** when the change's content has a schema in `content/schemas/`, add an AC "the loader enforces every schema rule" with one scenario per rule.
- **Geometry and layout:** a decision that defines geometry or layout (offset parity, neighbor order, coordinates) must have literal coordinate examples in a scenario — an independent oracle, not a restatement of the formula.
- **Size** decides the machinery (CLAUDE.md): `small` → single agent + deterministic gates + `spec-consistency` reviewer (ADR 0006); `planned` → `/dev-team:plan`, `spec-consistency` + the other spec reviewers, review fan-out, playtest. A Spec with more than six scenarios is not small.
- **Budget** (commits, review rounds) is enforced by `scripts/check-budget.sh`. Default for small = number of scenarios + 3 commits; review fixes count and go in their own commit; amend only unpushed commits. Exceeding it means stop, defer, escalate — never keep polishing.
- **Scenario IDs** `S01…` are stable; add at the end, never renumber. Each scenario ⇒ exactly one xUnit test `S<NN>_<ScenarioInPascalCase>` in `<Name>AcceptanceTests`. Invariants are FsCheck property tests listed in the Features trailing comment, not scenarios.
- **Reviewers may not raise the bar above the Spec.** A stricter bar is a `spec-change` finding for the human, never a fix request.
- The Gherkin keyword `Feature:` is syntax; do not use "feature" for a task size (sizes are `small` and `planned`).

## Review checklist (what `spec-*` agents look for)
Pillar named · Size honest (≤ six scenarios if small) · Budget set · every Number has a tolerance and a range · every `human` decision actually answered · every AC has a scenario and vice versa · nothing in Scope-Out referenced · every scenario expressible as a Command · no time or floats · presentation stated for anything player-facing · schema rules each have a scenario · geometry decisions have literal coordinates · consistency gate PASS. The mechanical subset is the `spec-consistency` agent's whole job.
