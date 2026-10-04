---
name: sk-planning
description: Draft a self-contained executable technical plan with atomic testable TODOs. Required context is inlined. Use for planning rules, validation, splits, or any CreatePlan-style output.
---

# Planning

## When to use

- User asks for planning rules or wants a plan validated.
- Draft or tighten a technical plan before work starts.
- Decide whether one plan is enough or the work should split.

## Slug and flow folder

1. If the user provided a slug, use `.agents/flows/sk-<slug>/`.
2. If the user gave no clear context, look for a stuck flow: one where `1 - ALTERNATIVES.md` exists and `2 - PLANNING*.md` is missing. If one, suggest continuing it. If several, list them and ask. If none, derive a short kebab-case slug from the goal and confirm.
3. Create `.agents/flows/sk-<slug>/` if needed.
4. Create or update `RUNBOOK.md` with row `2` as `in-progress`.
5. Write a single-PR plan to `2 - PLANNING.md`. For multi-PR work, write the masterplan to root `2 - PLANNING.md` and each self-contained sub-plan to `pr-<stable-slug>/2 - PLANNING.md`; initialize the root and per-PR runbooks described below.

## Core requirements

- **Self-contained**: an implementer can execute using only this document plus a normal repo checkout. No pointer-only references to Confluence, Jira, Figma, sibling plans, or chat history.
- **Durable**: the active plan always has the exact name `2 - PLANNING.md` in its flow or PR directory, so later phases never guess from a glob.
- **Inlined context**: API/data shapes, field mappings, env vars, flags, acceptance thresholds, before→after snippets, cross-PR contracts, and verification commands. Links are only optional attribution after the facts are inlined.
- **Executable**: every step can be done without guessing missing context.
- **Atomic TODOs**: each `Implementation Plan (TODOs)` item is one focused, testable action.
- **Files near top**: a `Files` section right after `Goal` lists every path expected to change (one per line, repo-relative, no descriptions).
- **No cross-plan or cross-repo references** unless required and fully inlined.
- **Verified paths**: every file path and line number is re-checked against the repo before finalizing.

## Clarification gates

- Before planning: drive ambiguity under ~10%. List unknowns as assumptions with acceptance impact.
- Before acting: under ~5%. Use concrete assumptions instead of percentages when uncertain.

## Pre-finalization pass

Note meaningful chances for refactors, performance, or security — even if deferred, capture them in Risks or a short follow-up list.

## Self-audit before review

- `Context` snippets are current code, not desired state.
- Every file path and line number was verified.
- Test changes name the runner and expected call count.
- Implementation order does not create a broken intermediate state.
- `Implementation Plan (TODOs)` depth stays at 2 or less.

## Plan shape

- **one repo, one PR** → use `templates/plan.md`.
- **multi-repo or multi-PR** → use `templates/masterplan.md` at the initiative root plus one `templates/plan.md` in each PR directory. Sub-plans repeat every fact they need from the masterplan.

## Complexity split

Use a masterplan + sub-plans (one per PR) if any of these hold:

- More than one repo or more than one PR.
- Implementation TODO count > 30 (count only checkboxes under `Implementation Plan (TODOs)`).
- Depth > 3 (nested levels under that same section).
- High-risk items > 5 (distinct risk lines/bullets).

The `Complexity Check` fields `Cross-deps` and total counts inform `Proceed` or `Split`; they do not force a split by themselves (multi-repo / multi-PR always does).

## Template enforcement

- Include every `##` section from `templates/plan.md` in file order: Goal, Files, Context, Scope, Risks, Dependencies, Priority, Logging / Observability, Branch setup, Implementation Plan (TODOs), Delivery, Docs, Testing, Verification, Acceptance, Fallback Plan, References, Complexity Check (omit only if the user narrows scope).
- Fill `Complexity Check` with real counts and an explicit `Proceed` or `Split`.
- Keep `Implementation Plan (TODOs)` depth at 2 or less; flatten nested bullets that are details, not independent TODOs.
- Aim for ~95% TODO coverage of in-scope work.
- Use consistent Markdown.

## Testing discipline

- Run related tests after each implementation TODO; fix failures before moving on.
- Name the runner/producer and confirm expected call counts for test changes.
- Order TODOs so test and dependency changes land before code that would break or hang them.

## Plan review loop (mandatory)

After the plan matches the template and the pre-finalization pass is done, review every emitted document until the latest pass has zero `valid` findings.

1. **Review** — dispatch a new `readonly` `generalPurpose` Task subagent and run the `sk-review-plan` skill on the full plan text (paste the plan; do not point at files).
2. **Triage** — label each finding `valid`, `false_positive`, or `unvalidated` with a one-line reason.
3. **Fix** — resolve every `valid` finding before the next review. Prefer minimal edits.
4. **Repeat** — dispatch a new subagent on the updated plan. Continue until the latest pass is clean.

**Exit rule:** hand off when the latest pass is `Lean & valid. Ship.` or has zero `valid` findings after triage (all `false_positive` or all `unvalidated`).

## Delivery notes

- Omit `Branch setup` and `Delivery` for draft-only or design-only plans.
- Defer commit/push to operator/repo policy.
- If the repo uses an interactive workflow, present the plan in small chunks first; the final artifact can still match the full template once agreed.
- Size each implementation TODO for one focused agent dispatch; split or run multiple cycles if larger.

## Scope boundary

Planning covers what to build, how to sequence it, delivery shape, and plan review. Code review of the implementation is not part of this skill.

## Plan file output

### Single PR

- Plan: `.agents/flows/sk-<slug>/2 - PLANNING.md`
- Keep the normal root `RUNBOOK.md`; set rows `2` and `2r` to `done` with a one-line summary.

### Multiple PRs

- Masterplan: `.agents/flows/sk-<slug>/2 - PLANNING.md`
- Sub-plan: `.agents/flows/sk-<slug>/pr-<stable-slug>/2 - PLANNING.md`
- Replace the root runbook with the `sk-flow` skill's `templates/MULTI-PR-RUNBOOK.md`. Fill ordered PR rows, repository, dependencies, directory, state, branch/base/HEAD placeholders, and `Active PR`.
- Create each PR directory from the normal `sk-flow` runbook template. Mark rows `0`, `1`, and `1r` `skipped` with `initiative root`; mark rows `2` and `2r` `done` and link the local `2 - PLANNING.md`.
- Derive stable slugs from PR purpose. Never use only an ordinal and never rename a slug after it enters the root runbook.
- Set the first dependency-free PR to `in-progress` and `Active PR`; leave other PRs `pending`. If none is unblocked, use `Active PR: none` and mark the initiative `blocked`.
- Do not also emit suffixed `2 - PLANNING-*.md` files. The root and each PR directory have one unambiguous `2 - PLANNING.md`.

Do not commit or push unless requested.

## Next step

Once the user approves the plan, hand off to `sk-implement`.

## Bundled templates

- `templates/plan.md`
- `templates/masterplan.md`

If the repo keeps copies under `.cursor/templates/`, update those in the same change.
