---
name: implement-change
description: Use when the user says "implement this", "/implement-change", "translate the spec into code", "the ADR and spec are done, build it", "code this up", or asks Claude to turn a planned change (ADR + Gherkin spec, usually produced by /plan-change) into actual code in the touched paths. Reads the ADR for architectural decisions, the spec for the behavioural contract, the existing code in the touched paths for conventions and seams, then writes the implementation and runs the spec's scenarios as smoke tests. Stops at "spec scenarios pass"; does not run the full audit suite — that's /drive-change's job. Use /plan-change first to produce the ADR + spec, /implement-change to write the code, then /drive-change to audit and polish.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(npx:*), Bash(go:*), Bash(cargo:*), Bash(pytest:*), Bash(vitest:*), Bash(jest:*), Bash(playwright:*), Bash(just:*), Bash(make:*), Read, Edit, Write, Grep, Glob, Skill, Task
---

# implement-change

Translates a planned change — ADR (architecture decisions) + Gherkin spec (behavioural scenarios) — into actual code. Stops when the spec's scenarios pass as smoke tests. Does not run the full audit suite (that's `/drive-change`).

This skill expects a **formal contract** (ADR + spec). If you don't have one yet, run `/plan-change` first. If you're working on a quick change that doesn't warrant formal planning, use `/drive-change` instead.

Primary caller: `/drive-plan` (which sequences `/plan-change` → `/implement-change` → `/review-change`). Also callable directly when you have a spec from elsewhere.

## Phase 0 — Locate ADR + spec

Resolve the contract from any of:
- explicit user-supplied paths (e.g. `/implement-change docs/adr/0042-multi-tenant.md spec/multi-tenant.feature`)
- handoff context from `/plan-change` (look for recent ADR + spec creation in current branch's commit log)
- discovery: search the repo for ADR + spec pairs matching the user's stated intent

**Refuse to proceed without at least the spec.** The ADR is strongly preferred (provides "why" + design constraints) but the spec is mandatory (provides "what" + acceptance criteria).

If no spec is found, recommend `/plan-change` and stop.

## Phase 1 — Read the contract

Read the ADR (if present) and the spec. Extract:

- **Architectural decisions** — what's being chosen, what's being rejected, what constraints are load-bearing
- **Scenarios** — each `Scenario:` or `Scenario Outline:` block in the spec, parsed into `Given/When/Then` triples
- **Edge cases** — every scenario tagged `@edge` or named with edge-y language
- **Out-of-scope notes** — anything the ADR explicitly says is *not* being done in this change

Write a `## Contract` block in working state:

```
## Contract
- ADR: <path> (<one-sentence summary>)
- Spec: <path> (<N> scenarios)
- Architectural decisions:
  - <bullet 1>
  - <bullet 2>
- Scenarios:
  1. <Given/When/Then>
  2. ...
- Out of scope:
  - <bullet>
```

## Phase 2 — Map the touched surface

Identify the files and symbols the implementation will touch. Prefer symbol-level queries when an LSP is available — see [`references/language-tooling.md`](../../references/language-tooling.md):

- `tslsp outline` (or language equivalent) on each likely-touched file to see what's there without reading the body
- `tslsp find_symbol` to locate any symbols the spec references by name
- `tslsp references` to see who calls into the symbols you'll change — those are the seams to respect

Fall back to `Read` + `Grep` where LSP isn't available.

Write a `## Surface` block:

```
## Surface
- New files: <list>
- Modified files: <list>
- Symbols introduced: <list>
- Symbols modified (with caller counts from LSP): <list>
- Symbols removed: <list>
```

## Phase 3 — Plan the diff

Propose the file-by-file plan: new files (with one-line purpose each), modified files (with what changes), tests to add or update.

Confirm with the user before writing. Show:

- The plan
- An estimated commit log (one commit per scenario or one per architectural seam)
- Any architectural decisions you're interpreting that might be ambiguous

Ask: "Plan looks right? Proceed to write the code?"

Do not proceed without confirmation. The user may want to iterate the plan or push back on a specific architectural read.

## Phase 4 — Write the implementation

Apply edits via `Edit` and `Write`. Commit logically:

- One commit per scenario (preferred for self-contained features)
- One commit per architectural seam (preferred for refactors / cross-cutting changes)
- Match commit message style with `git log -5` to follow the repo's conventions

For large multi-domain implementations (Phase 3 plan touches more than the small-mode threshold — >30 files or >3 top-level dirs), use the agent pipeline:

1. Invoke `agents/orchestrate-slice.md` via `Task` to partition the implementation work by domain.
2. For each slice, write the implementation directly (or dispatch a `fix-applier` agent in "implement mode" — same agent file, the `## Input` block carries the implementation intent and the spec scenarios for that slice).
3. Single-thread anything that touches cross-slice contracts (the slicer's `contracts_in`/`contracts_out` lists).

## Phase 5 — Run scenarios as smoke tests

For each scenario in the spec, derive an executable check:

- If the project has a Gherkin runner (cucumber, behave, godog, pytest-bdd), run the spec file directly: `npx cucumber-js <spec>`, `behave <spec>`, etc.
- If not, translate each scenario into a unit/integration test and run it via the project's test runner: `npm test`, `pytest`, `go test ./...`, `cargo test`.
- For scenarios that aren't easily testable (UI flow, manual smoke), surface them as `## Manual scenarios to verify` and skip the auto-run.

Iterate until all auto-runnable scenarios pass or you've isolated a blocker. If a blocker is real, surface it to the user — don't paper over with a skipped test.

## Phase 6 — Handoff

Print:

```
Ready for `/drive-change` (or `/review-change` for read-only audit).

Touched files: <count>
Commits since start: <count>
Scenarios passing: <pass>/<total>
Manual scenarios to verify: <count>
```

Do **not** auto-invoke `/drive-change`. The user (or `/drive-plan` if that's the caller) decides the next step.

## Operating rules

- **Spec is mandatory; ADR is strongly preferred.** Refuse Phase 0 without at least a spec.
- **Confirm Phase 3 before writing.** The plan-the-diff phase exists to catch architectural misreads cheaply.
- **One commit per scenario or per seam.** Don't squash unrelated work; don't split a single behavioural change across multiple commits.
- **Scenarios drive the loop, not the LLM.** Stop when scenarios pass. Don't run the full audit — that's `/drive-change`'s job.
- **Never auto-handoff.** Phase 6 ends with a recommendation, not a `Skill` invocation of `/drive-change`.

## Composing with other skills

- Called by: `/drive-plan` (Phase 2). Also callable directly.
- Calls: `agents/orchestrate-slice.md` and `agents/fix-applier.md` via `Task` (for large multi-domain implementations only).
- Sibling: `/plan-change` (precedes), `/drive-change` (the no-spec implementation path), `/review-change` (audit-only).
