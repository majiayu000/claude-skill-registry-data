---
name: plan
description: "Use when work spans several files or sessions, the user asks for a plan, spec, PRD or tickets, or after grill settles a project-size design."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "obra/superpowers 7.0.0 skills/writing-plans; mattpocock/skills to-spec, to-tickets, to-prd, to-issues, wayfinder; garrytan/gstack plan-ceo-review (scope modes, premise challenge, alternatives), plan-eng-review (prime directives, failure modes, parallel lanes); cursor/plugins pstack 0.15.25 poteto-mode playbooks/multi-phase-plan; MCT (local) agents/planner.md"
---

# Plan

A plan records the decisions the implementer can't make alone: which files, which names and signatures, the spec's exact values, and the check that proves each task. Leave the code out. A plan longer than the code it describes has written the code; a line that decides nothing ("handle edge cases", "TBD", "add validation") is a gap.

## 1. Pick the branch

| Situation | Output |
|---|---|
| One or two files, obvious approach | No plan. Say so in one line and hand to the `execute` skill. |
| Fits one or two sessions | **Session plan**: `docs/plans/YYYY-MM-DD-<slug>.md` |
| Multi-session build, or the user asks for a spec, PRD or tickets | **Spec + tickets** (section 4) |

Follow the repo's existing plan or spec location if it has one. Explore the code first and keep what the plan needs: file pointers, conventions, test commands, entry points. If a product decision is still open, run the `grill` skill first.

Consume existing `research` notes and `triage` briefs before rediscovering the same facts. Refresh date-sensitive claims and resolve missing acceptance criteria; a label such as ready-for-agent is not proof of a reproduced bug. For queue/retry/concurrency invariants whose ordering is the main risk, offer the optional, explicitly invoked `statechart` workflow rather than requiring it for ordinary tasks.

If the work covers independent subsystems, write one plan per subsystem; each should produce working, testable software on its own.

Done when: the branch is chosen and every decision the plan needs is either in hand or settled by `grill`.

## 2. Challenge the scope

For project-size work, read `references/scope-review.md` and run it: premise check, what already exists, two or three approaches (one minimal, one ideal), then a scope mode (EXPANSION, SELECTIVE, HOLD, REDUCTION). Every scope addition is the user's opt-in, one decision brief per addition. Once a mode is chosen, commit to it for the rest of the plan.

- Prefer REDUCTION when requirements are broad and HOLD when the scope is already fixed. Response mode does not change scope.

Done when: the chosen approach and mode are written in the plan header.

## 3. Write the session plan

**Header**

```markdown
# <Feature> plan

**Goal:** <one sentence>
**Approach:** <two or three sentences; the chosen approach and scope mode>
**Design:** <path to the grill doc, or "none">

## Global constraints
<Project-wide requirements, one per line, exact values copied verbatim from the design.>

## Review focus
<Up to five inputs or failure modes the design implies but no test exercises, most likely first. Each gets a test in the task that owns the code.>

## File map
- `path/to/file.ts`: <its one responsibility> (create | modify)
```

**File map first.** Lock the decomposition here: one clear responsibility per file, files that change together live together, existing patterns win over new ones.

**Right-sized tasks.** A task is the smallest unit that carries its own test cycle and that a reviewer could reject while approving its neighbor. Fold setup, config and docs into the task whose deliverable needs them.

```markdown
### Task N: <deliverable>
**Files:** create `a.ts`; modify `b.ts:40-60`; test `a.test.ts`
**Interfaces:** consumes `parseRow(line: string): Row` (Task 2); produces `importCsv(path: string): Promise<Row[]>`
- [ ] Test `rejects rows with missing id`: `importCsv("fixtures/missing-id.csv")` rejects with `MissingIdError`
- [ ] Implement `importCsv` in `a.ts`, streaming line by line
- [ ] Verify: `npm test -- a.test.ts` → 4 passed
```

What each step carries, and nothing more:
- **Test step**: the test's name and its assertions with the spec's exact values.
- **Code step**: the exact signature, its file, the values the spec pins. A body only for an algorithm the signature and test don't determine.
- **Verify step**: the command and the output that means it passed. Every task ends with one.
- **Cross-task reference**: point at the other task's Interfaces line; don't repeat its code.

Add commit steps only when the user asked for commits. Test-first tasks open with a failing test at a clean seam.

**Engineering pass.** Read `references/eng-review.md` and apply its prime directives to every new codepath: named error paths, the nil / empty / upstream-error shadow paths, interaction edge cases, and the failure-modes table. Add the tests it surfaces to the owning tasks.

**Self-review**, fixed inline:
1. Coverage: every design requirement maps to a task.
2. Step scan: every step lets the implementer write exactly one reasonable thing.
3. Names: signatures and types match across tasks (`clearLayers` in Task 3 is `clearLayers` in Task 7).
4. Proportion: if code blocks are most of the document, replace bodies with signatures and assertions.

Done when: the file is saved, every task has a verify command, and the self-review passes.

## 4. Spec + tickets

Synthesize from the conversation and the repo; don't re-interview. Read `references/spec-and-tickets.md` for the templates and publish commands.

1. **Spec**: problem, solution, user stories, implementation decisions (modules, interfaces, schema, API contracts; no file paths), testing decisions (the highest seam that reaches the behavior, fewest seams overall), out of scope.
2. **Tickets as tracer bullets.** Each ticket is a narrow but complete vertical slice through every layer, demoable on its own, sized for one fresh session. Prefactoring comes first: make the change easy, then make the easy change. Each ticket declares **Blocked by**. A wide mechanical refactor goes expand, migrate in batches, contract, instead of a slice.
3. **Publish.** With a GitHub remote and `gh` authenticated, create issues in dependency order (blockers first) so each "Blocked by" cites real numbers. Issues are visible to others: show the numbered breakdown (title, blocked by, delivers) and publish on the user's go. Otherwise write one file per ticket to `docs/tickets/<slug>/NN-<slug>.md`, numbered in dependency order; local files need no go.

The **frontier** is every ticket whose blockers are done. That's the queue `execute` drains, one fresh session per ticket.

Done when: the spec exists and every ticket is published with its blocking edges.

## 5. Hand off

If the user asked for the plan itself, link it and stop. If they already asked for implementation, continue into `execute`; the plan records the authorized scope. Ask only for an unresolved product decision or a scope expansion. Do not ask again for implementation already authorized.
