---
name: crav1-tighten-spec
description: Walk an existing spec issue-by-issue. For every finding (including architecture-reviewer notes), offer explained resolution choices (including get a suggestion) and wait; patch only that issue after a pick. Use when spec.md exists and needs tightening. Do not write application code.
disable-model-invocation: true
icon: book-open
color: cyan
---

# Tighten spec

You refine a spec **one issue at a time**. The spec is the source of truth; chat is commentary.

Do **not** offer a single menu of workflow modes (“apply the whole review”, “make everything testable”, “full pass”). That hides per-finding decisions.

**Do not patch until the user picks a resolution for the current issue** (or sends a batch of `I#: letter` answers). `suggest` is not a patch.

## Find the spec

Use the spec the user @-mentions. Otherwise the most recently edited file under `docs/specs/` excluding `_template/`. If several, ask which slug. Expected `spec.md` headings: this skill’s `assets/spec.md`.

Read `spec.md` and note `diagrams.md`, `adr/`, `tasks.md`, `export/`.

Also read the latest **crav1-architecture-reviewer-agent** / **crav1-spec-reviewer-agent** output in this chat if present. Those findings become issues. Do not collapse them into one “apply reviewer notes” action.

## Build the issue list (no edits)

Number issues `I1`, `I2`, … Each issue is **one** defect, ambiguity, or decision smuggled into the wrong layer.

Sources, in order:

1. Numbered issues already listed by a reviewer in this chat (preserve their meaning; split if they bundled two problems)
2. Fresh read of `spec.md` / diagrams / ADRs (add only issues the reviewer missed)

Typical issue shapes (from this skill’s job):

- Acceptance / SHALL that is not yes/no
- Missing happy, fail, or **empty** path
- Mechanism in a requirement (flag, relational DB, library) that should be constraint, ADR, or non-goal
- Open question that could be cut to a non-goal now
- Missing home for a tech gap (no ADR, no open question, no constraint)
- Diagram or ADR that contradicts `spec.md`

Skip nitpicks. Merge duplicates. Prefer fewer sharp issues over a laundry list.

If **no issues** and the tight-enough checklist passes, say so and offer only: stop and Plan Mode, or run `crav1-spec-reviewer-agent`.

## Walk one issue at a time

### Index (every turn, short)

List remaining issues as one line each: `I2` … `In` titles only. Mark the current one.

### Current issue (full)

For **only** the current `I#`:

1. **Finding** — one or two sentences. Quote the spec/ADR/diagram line.
2. **Why it matters** — testability, v0 size, or requirement-vs-decision blur.
3. **Options** — 2–4 mutually exclusive resolutions. Use the questions tool when available.

Every option: **letter**, **name**, **what changes**, **impact** (who/v0/tests, and which files). Use the resolution catalog below. Drop resolutions that do not fit this issue (always keep **`suggest`**). Never add a product feature as a “fix.”

Offer **2–4** mutually exclusive **patch** resolutions, then **`suggest`**. Add `ask` / `keep` only when they fit. `suggest` does not count toward the 2–4.

4. How to answer: `A` / `B` / … for this issue, or a batch: `I1 A, I3 C, I4 D`. Unmentioned issues stay for later.

Stop. Do not edit. Do not preview a full patched spec.

If they already answered this `I#` in the same message with a **patch** letter (`make-testable`, `cut-from-v0`, …), skip the menu and execute. If they asked for a suggestion in the same message, follow **When they pick `suggest`**.

### When they pick `suggest`

Do **not** patch. Stay on this `I#`.

1. Name the **letter** and catalog id you would pick from the options already shown.
2. **Why** — 2–4 sentences (testability, v0 size, requirement vs decision). Do not invent a new resolution or a product feature.
3. Re-offer the **same** patch letters (and `ask` / `keep` if they were present). Include `suggest` again only if they want a different recommendation; at most **one** alternate, then they must pick a patch letter, `ask`, or `keep`.

Then stop. Do not advance to `I+1`.

### After a choice

1. Patch **only** what that resolution allows for **that issue**. (`suggest` never reaches here.)
2. Recap: **Added / Removed / Still open** for this issue.
3. If acceptance is still mushy on *this* issue and they did not choose `make-testable`, say so — do not silently rewrite.
4. Advance to the next unanswered issue (same format). If none remain, run the tight-enough checklist.

Do not start the next issue’s patch in the same turn unless they batched answers.

## Resolution catalog (per issue, not per turn)

Pick the ones that fit; rewrite names to the actual REQ/ADR.

| Id | Name | What it does | Typical impact |
| --- | --- | --- | --- |
| `make-testable` | Make this falsifiable | Rewrite this SHALL/acceptance into a yes/no check. No extra features. | `spec.md` that requirement/journey. Tests can assert one outcome. |
| `cut-from-v0` | Cut from v0 | Move this capability to non-goals / later. | Smaller demo; journeys/acceptance that depended on it go away or shrink. |
| `to-constraint` | Treat as constraint | Remove mechanism from requirements; record accepted tech under `## Constraints`. | Product spec stays behavioral; stack is binding without pretending it is a user journey. |
| `to-adr` | Make / reframe an ADR | This is a real choice with alternatives. Write or fix `adr/NNNN`. Status `proposed` unless they already decided. | Requirements lose “how”; decision is reviewable. May need a later `sync` of diagrams. |
| `to-open-question` | Leave as open question | Do not guess. Add or keep a numbered open question. | v0 stays blocked on this until they answer; no silent product decision. |
| `add-missing-path` | Add the missing path | Write the empty, fail, or happy path (and a matching acceptance line) that is absent. | Demo script and tests cover that state. Disk: journeys + acceptance only. |
| `keep` | Keep as written | Explicitly accept the current text. Say the cost (usually untestable or blurred layers). | No disk change. Use rarely; call out the cost. |
| `suggest` | Get a suggestion | Recommend one of the patch letters already offered, with a short why. No edits. Re-offer the same menu. | Stay on this `I#` until they pick a real resolution. Always offer this. |
| `ask` | Ask, don’t patch | Ask at most 3 questions **about this issue**. No file edits. | Next turn retries this `I#` with answers. |
| `sync-here` | Sync this artifact | Update the diagram/ADR/export that this issue names so it matches `spec.md`. Does not change product intent. | Only the named files. |

Do **not** offer a turn-level `apply-notes` that applies the whole architecture review. Each reviewer bullet is its own `I#`.

You may add `sync-here` as a **second letter on the same issue** only when the chosen resolution would immediately make a named diagram/ADR wrong (“B, then sync the sequence diagram”). Still one issue.

## Hard rules

- Prefer **cutting scope** over adding features.
- Architecture/stack in the user’s answers goes to `## Constraints` or an ADR, not journeys.
- Preserve existing architecture and patterns **only when a real codebase exists** and the spec does not call for change.
- Never “fix” the idea by expanding v0.
- Do not leave `diagrams.md` / `adr/` / `export/` contradicting `spec.md` after a patch that affects them — either the chosen resolution includes `sync-here`, or the next issue is that drift.
- Do not start Plan Mode or write application code unless they explicitly ask after issues are done.
- Do not patch “to be helpful” when they have not chosen a **patch** resolution (`suggest` is not a patch).

## When the spec is tight enough

All remaining issues resolved **and**:

- One primary user
- v0 vs later is explicit
- Non-goals are written
- Happy, fail, and empty paths exist
- Every acceptance line is a yes/no check
- Open questions are listed, not buried

Then stop the issue walk.

If **Open questions** (or unresolved assumptions) remain, the next command is `/crav1-resolve-questions` — not Plan Mode. That skill walks each question with keep-open vs answer.

If the open-question list is empty, tell them: `/crav1-plan-from-spec`, or a new chat in Plan Mode (`Shift+Tab`) with `spec.md` attached. Optional: `crav1-spec-reviewer-agent` once, not as a substitute for unfinished `I#`s or `Q#`s.
