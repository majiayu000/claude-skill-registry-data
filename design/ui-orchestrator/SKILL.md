---
name: ui-orchestrator
description: Read the current project state and recommend which UI skill to run next. Use this skill whenever a user asks "what should I do next?", is starting a new UI project and isn't sure where to begin, has been working for a while and isn't sure if their specs are complete, or is handing off a project to a new session and needs to re-establish context. The orchestrator never does design work — it reads what exists and routes to the right skill.
status: stable
---

# UI Orchestrator

Reads the spec package files that exist in the working directory, checks their status, and recommends exactly one next step. This is a routing skill, not a design skill. It does not produce layout, components, or copy — it tells the user which skill to run next, and why.

## When to use this skill

Use this skill when:
- The user asks "what should I do next?" or "where should I start?".
- The user is beginning a new UI project and isn't sure which skill to run first.
- The user has been working through a spec package and isn't sure whether it's complete enough to move on.
- A project is being handed off to a new session or a different model — the orchestrator re-establishes what has been done and what hasn't.

Do **not** use this skill when:
- The user already has a specific skill in mind ("run ui-brief for this feature") — just run it.
- The user is not building a UI. This skill is part of the UI Specification Kit and only understands UI spec pipelines.
- No spec files exist yet and the user is starting completely fresh — there is nothing to read, so the answer is always `ui-brief`. Skip the orchestrator and run `ui-brief` directly.

## Core principle

**The orchestrator never does design work. Its only job is to read what exists and recommend the next logical step.** It is a router, not a builder. If it finds itself drafting a layout or writing copy, it has crossed a line. Hand off to the appropriate skill and stop.

## Retrospective / spec-recovery mode

If an implementation exists and no spec package exists, and the user wants to document or recover the specification, recommend `ui-surface-inventory` first.

**Reason:** You must identify coherent scopes before running deep recovery. A giant recovery on the whole app is hard to act on.

## Routing logic

The orchestrator checks for spec package files in pipeline order. The first missing or unapproved file determines the recommendation. Files are checked in the order below — do not skip ahead, even if the user asks.

| If this condition is met | Recommend this skill |
|---|---|
| Implementation exists + no spec package + user wants Spec Recovery | `ui-surface-inventory` |
| Large project / ambiguous scope | `ui-surface-inventory` |
| `surface-inventory.md` is missing or not approved (for multi-scope projects) | `ui-surface-inventory` |
| `brief.md` is missing or not approved | `ui-brief` |
| `visual-calibration.md` | `ui-visual-calibration` |
| `flow.md` (required for multi-screen features only) | `ui-flow` |
| `blueprint.md` | `ui-blueprint` |
| `system.md` | `ui-system` |
| `screen-spec.md` | `ui-screen-spec` |
| `component-specs/*.md` | `ui-component-spec` |
| `microcopy.md` | `ui-microcopy` |
| `acceptance.md` | `ui-acceptance` |
| All of the above exist and are approved; no implementation yet | `ui-spec-linter` |
| Implementation exists but `redlines/inspector-report.md` is absent | `ui-inspector` |
| Inspector report exists but no redline audit exists | `ui-redline` |
| Storybook or documentation output is needed | `ui-storybook-docs` |

**Status values:** A file's frontmatter `status` field determines whether it counts as present. Accepted values in ascending order of completeness: `draft` → `current` → `approved` → `complete`. A file with `status: draft` is **not** approved — it counts as a gap. Only `current`, `approved`, or `complete` clears a step.

**Multi-screen vs single-screen:** `flow.md` is only required when the feature spans more than one screen. If the brief describes a single screen, skip the flow check and proceed to `blueprint.md`.

**Numbered spec packages:** Some spec packages use numbered filenames instead of canonical names (e.g., `02-brief.md`, `04-blueprint.md`, `05-screen-spec.md`). If a `00-index.md` exists in the package directory, it is the authoritative manifest — use the file list and dependency chain it describes rather than searching for canonical filenames. If no `00-index.md` exists, fall back to searching for canonical names and then numbered equivalents (any file whose name ends with `-brief.md`, `-blueprint.md`, etc.). Never require both forms to be present — whichever form is used, treat it as equivalent to the canonical name for routing purposes.

## Workflow

### Step 1 — Scan the working directory

First, check whether a `00-index.md` file exists in the spec package directory.

- **If `00-index.md` exists:** Read it to determine the package's file list, scope, and dependency chain. Use the filenames it declares as the authoritative list — do not require canonical names. A numbered file listed in the index (e.g., `02-brief.md`) is equivalent to its canonical counterpart (`brief.md`) for all routing decisions.
- **If no `00-index.md`:** Scan for spec files using both canonical names (`brief.md`, `blueprint.md`, etc.) and numbered equivalents (any file ending in `-brief.md`, `-blueprint.md`, etc.). Treat the first match found for each spec type as that type's representative file.

List every spec file found with its `status` value from frontmatter. If a file has no frontmatter or no `status` field, treat it as `draft`.

### Step 2 — Check each file's status

For every file found, read its frontmatter `status` field. A file is only "done" if status is `approved` or `complete`. A file that exists but has `status: draft` still counts as a gap — it needs review before the pipeline can advance.

### Step 3 — Identify the earliest gap in the pipeline

Walk the routing table from top to bottom. Find the first row where the file is either missing entirely or has `status: draft`. That is the gap.

If no gap is found in the spec pipeline (all files approved), check whether an implementation exists. If implementation exists but `redlines/inspector-report.md` is absent, the gap is at `ui-inspector`. If an inspector report exists but no redline audit exists, the gap is at `ui-redline`. If storybook docs are needed and don't exist, the gap is at `ui-storybook-docs`.

### Step 4 — Recommend the skill that fills the gap

State the recommendation clearly: which skill, what file it will produce or review, and a one-sentence reason.

### Step 5 — If multiple gaps exist, recommend only one

Do not list every gap. Pick the earliest one in pipeline order and recommend it. The user will return to run the orchestrator again after completing that step.

## Output template

The orchestrator does not produce a file. It produces a short conversational recommendation block. Use this exact structure:

```
## Orchestrator recommendation

**Current state:**
- `brief.md` — approved
- `visual-calibration.md` — missing
- (remaining pipeline not yet evaluated)

**Gap identified:** `visual-calibration.md` is missing.

**Recommended next skill:** `ui-visual-calibration`

**Reason:** No visual calibration sheet exists yet — running `ui-blueprint` now would require the model to invent density, shape language, and surface style decisions silently.
```

The current state list should show only the files that have been scanned up to and including the gap. Do not list files that come after the gap in the pipeline — they haven't been reached yet.

## Examples

### Example 1 — fresh project, nothing exists

**Working directory contents:** empty

**Orchestrator output:**
```
## Orchestrator recommendation

**Current state:**
- `brief.md` — missing

**Gap identified:** No brief exists.

**Recommended next skill:** `ui-brief`

**Reason:** Everything else in the pipeline depends on a brief — there is nothing to build layout or components against without one.
```

---

### Example 2 — brief approved, calibration missing

**Working directory contents:**
- `settings-page/brief.md` — `status: approved`

**Orchestrator output:**
```
## Orchestrator recommendation

**Current state:**
- `brief.md` — approved
- `visual-calibration.md` — missing

**Gap identified:** No visual calibration sheet exists.

**Recommended next skill:** `ui-visual-calibration`

**Reason:** The brief is approved but no visual decisions have been locked — running blueprint work now would require silently inventing density, shape language, and palette choices.
```

---

### Example 3 — most of the pipeline done, one file still draft

**Working directory contents:**
- `checkout/brief.md` — `status: approved`
- `checkout/visual-calibration.md` — `status: approved`
- `checkout/blueprint.md` — `status: draft`

**Orchestrator output:**
```
## Orchestrator recommendation

**Current state:**
- `brief.md` — approved
- `visual-calibration.md` — approved
- `blueprint.md` — draft (not yet approved)

**Gap identified:** `blueprint.md` exists but is still in draft status.

**Recommended next skill:** `ui-blueprint`

**Reason:** The blueprint needs review and approval before screen specs and component specs can be derived from it — draft blueprints produce draft components, and the mismatch compounds.
```

---

### Example 4 — full spec package complete, pre-code

**Working directory contents:** All spec files present with `status: approved`.

**Orchestrator output:**
```
## Orchestrator recommendation

**Current state:**
- All spec files present and approved.

**Gap identified:** No implementation exists yet, and the spec package has not been linted for internal consistency.

**Recommended next skill:** `ui-spec-linter`

**Reason:** Before handing the spec to an implementer, run the linter to catch conflicts between files (e.g. a component spec that references a token the system spec doesn't define).
```

## Anti-patterns

1. **Never recommend skipping a step.** Even if the user asks — "can we just go straight to blueprint?" — the answer is to check what's missing and explain why skipping creates downstream risk. The orchestrator does not override the pipeline order.
2. **Never do the design work yourself.** If the orchestrator finds a missing brief and starts drafting one, it has broken its own rule. State the recommendation and stop. The design work belongs to the appropriate skill.
3. **Never modify files or run skills.** The orchestrator is a pure routing skill (gap analyzer). It must not mutate the run manifest, modify files, or execute the skills it recommends. It delegates entirely to the user or an execution agent.
4. **Don't recommend multiple skills at once.** One gap, one recommendation, one skill. Giving the user a list of three things to do introduces ambiguity about what to do first — that is exactly what the orchestrator exists to prevent.
5. **Don't count a draft file as approved.** A file with `status: draft` is not done. It is a gap. Treat it the same as a missing file for routing purposes.
6. **Don't invent files that don't exist.** If no spec files are found, the pipeline starts at `ui-brief`. Do not assume files exist elsewhere or in a different format.

## Acceptance criteria for this skill's own output

A recommendation produced by this skill is acceptable only if every one of these is true:

- [ ] The output uses the exact four-field structure: Current state, Gap identified, Recommended next skill, Reason.
- [ ] Recommended next skill names an actual skill from the routing table — no invented or generalized skill names.
- [ ] Exactly one skill is recommended (not a list, not "either X or Y").
- [ ] The reason is one sentence and explains the downstream risk of not filling the gap — it does not merely restate the gap.
- [ ] Current state lists only files that were scanned up to and including the identified gap — it does not list files that come later in the pipeline.
- [ ] The recommendation does not contain any draft layout, copy, component specs, or design decisions — it is routing only.
- [ ] If all spec files are approved, the recommendation correctly moves to the post-spec phase (ui-spec-linter, ui-inspector, or ui-storybook-docs as appropriate).

If any check fails, revise before delivering.

---

## Promotion checklist

Complete every item before changing `status: draft` to `status: stable`.

### Evidence on the orchestrator-states fixtures

Run this skill against each of the seven state fixtures in `examples/orchestrator-states/` and verify:

- [ ] **01-empty:** Recommends `ui-brief`. Does not hallucinate any existing files.
- [ ] **02-brief-draft:** Recommends continuing with `ui-brief` (not starting a new one). Correctly identifies `status: draft` as a gap — not a completed step.
- [ ] **03-brief-approved:** Recommends `ui-visual-calibration`. Does not skip to `ui-blueprint`.
- [ ] **04-through-blueprint:** Recommends `ui-system`. Correctly identifies that blueprint is approved but system is missing.
- [ ] **05-all-specs-approved:** Recommends `ui-spec-linter`. Does not recommend jumping straight to `ui-generate-code`.
- [ ] **06-inspector-present:** Recommends `ui-redline`. Does not recommend re-running `ui-inspector`.
- [ ] **07-redline-pending:** Recommends `ui-redline`. Correctly distinguishes "inspector done, no redline" from "redline in progress".

### Evidence on the spec-recovery-create fixture

- [ ] Running this skill against `examples/spec-recovery-create/` at the point where `brief.md` is approved but `visual-calibration.md` is draft recommends `ui-visual-calibration` (not `ui-inspector`, which is also present).
- [ ] The recommendation correctly accounts for the `recovery: true` frontmatter flag — it does not flag the absence of `flow.md` as a gap.

### Regression: exactly one recommendation

- [ ] In no tested case does the output contain two skill names in the Recommended next skill field.
- [ ] In no tested case does the output say "either X or Y" — it always chooses one.

### Routing vocabulary

- [ ] `current`, `approved`, and `complete` are all treated as "gap cleared" for a step — none of these should trigger a "not yet approved" recommendation.
- [ ] Only `draft` triggers the "not yet approved" recommendation.

### Skill integration

- [ ] `validate-skill.py` passes for this skill with `status: stable` (no missing sections).
- [ ] `skills.json` entry for `ui-orchestrator` has been updated to `"status": "stable"`.
- [ ] README Skill Map table has been updated to show `stable`.
