---
name: simplification-audit
description: "Use when the user explicitly asks for an audit of the codebase or to refactor a part of the codebase. Coordinates a bounded, read-only pass over every subsystem in scope and returns ranked simplification recommendations for data structures, state representation, control flow, algorithms, and ownership, without changing a single file."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- **Audit-only and read-only.** Never edit, create, or delete a file. Never run the test suite, a fixer, a static analyser, or a build. Never implement a recommendation. Never stage, commit, push, or open a pull request. Read-only inspection commands (`git log`, `git grep`, `rg`, `find`, `cat`, `sed -n`) are allowed. The repository is byte-identical when the audit ends.
- **Runs only on an explicit user request** — see *Use when*. Never start as a side effect of another skill or agent.
- **Publishes nothing.** No tracker comment, no issue, no PR. An audit produces proposals, and `@rules/compound-engineering/tracker.md` *File deferred points as follow-up tracker issues* → *The filing bar* files no refactoring proposal of any kind. The report stays in this run's output; the user decides what becomes an issue.
- Apply `@rules/refactoring/general.md` — it owns what refactoring is (behaviour-preserving structural change), when not to refactor ("just to make the code look nice", "without a business reason"), and the no-big-bang-rewrite rule. Every recommendation must be implementable incrementally.
- Apply `@rules/writing/general.md` — one idea per sentence, active voice, one term per concept, no marketing register. A finding states a fact, never an adjective.
- Apply `@rules/php/core-standards.md` **only once it is established that the audited project is a PHP project (PHP stack in `composer.json`) and the recommendation touches PHP code** — skip it for a non-PHP subsystem.
- Apply `@rules/laravel/architecture.md` **when the project is a Laravel project using `pekral/arch-app-services` and the recommendation moves logic between layers** — that rule owns where business logic lives, so the ownership dimension of this audit never invents a competing taxonomy.
- **Never force an abstraction.** Boring local code that is already clear stays. Style consistency, hypothetical extensibility, line-count reduction, and moving existing branching behind a new type are not recommendations.

---

## Scope
Coordinate a bounded, read-only audit that finds materially useful simplifications in the audited scope's **data structures, state representation, control flow, algorithms, and ownership**, then rank them.

The signals a worker looks for in those five dimensions live once, in the brief it is handed — `references/worker-brief.md`. This file does not restate them.

**What this skill deliberately leaves to another skill.** It never implements: an accepted recommendation is implemented later, in a separate and separately requested run, by `@skills/class-refactoring/SKILL.md` (class-level structure) or `@skills/refactor-entry-point-to-action/SKILL.md` (entry-point orchestration extraction). A suspected defect is not a simplification — route it to `@skills/analyze-problem/SKILL.md`. A pull-request diff review is `@skills/code-review/SKILL.md`, which is tied to a PR and never triggered by a bare audit request.

---

## Use when
- The user explicitly asks for an audit of the codebase ("audit this codebase", "prověř celý projekt", "find simplifications across the repo").
- The user explicitly decides to refactor a part of the codebase and wants the cleanest available option before any code changes.

**Never runs when:** no such explicit request was made. This skill is never a side effect of another workflow — not `@skills/resolve-issue/SKILL.md`, not `@skills/code-review/SKILL.md` or any other review skill, not `@skills/process-code-review/SKILL.md`, and not an agent pipeline step. Another skill or agent may invoke it only when that caller is itself carrying out an explicit user audit or refactoring request, and it names that request when it does.

**Scope of the audit.** An audit request covers the whole repository. A refactoring request covers the part the user named, and the inventory boundary in step 1 is then that part plus the interfaces it exposes to the rest of the tree. Never widen the boundary beyond what was asked.

---

## Execution

You are the coordinator. Continue until every subsystem in scope has been reviewed and the final audit is validated.

### 1. Establish the coverage contract

Inspect the repository and inventory every identifiable subsystem in scope. Each row carries:
- a stable ID and a descriptive name;
- an exact ownership boundary;
- its key implementation files;
- its relevant public interfaces, major call sites, and tests;
- a status: `queued`, `in review`, `recommend`, or `skip`.

Include frontend, backend, shared infrastructure, platform bridges, generated-contract ownership, and test / tooling infrastructure wherever they are materially relevant to the audited scope.

Hold the whole audit in **one canonical report** — the shape lives in `templates/audit-report.md`. It carries the subsystem inventory, the confirmed opportunities, the explicit skip decisions, the cross-cutting patterns, the duplicates and superseded findings, the final priorities and dependencies, and the audit log.

This inventory **is** the coverage contract. A broad catch-all row does not prove coverage of what it claims to cover: split it until every row has a boundary a worker can hold in one pass.

Record the pre-audit `git status --short` output in the report's `## Scope` block before any subsystem review starts. That line is the baseline the read-only guarantee in *Done when* is checked against.

### 2. Run bounded subsystem reviews

- Give every worker exactly one subsystem, with an **exact, non-overlapping** ownership boundary.
- Use fresh, read-only workers where the host provides them. Where it does not, run the same bounded passes sequentially in this context, one subsystem at a time, reading only that subsystem's files per pass.
- Keep concurrency bounded to the number of lanes you can actively coordinate.
- Use one consolidated wait mechanism. Do not interrupt a productive worker merely because it is slow. Close a completed worker once its result is harvested.
- Hand every worker the quoted brief block in `references/worker-brief.md` verbatim, with its subsystem row substituted in. That block is the whole of what a worker receives, and it carries the worker's read-only limit itself. The same file also holds the eight fields every recommendation must carry.
- A worker returns **at most two** opportunities, or `skip` when nothing clearly meets the threshold. Set the row's status from what it returned.

### 3. Validate and synthesize

- **Verify every finding yourself against the current repository before accepting it.** Re-open the cited `file:line` and its surrounding context. A finding you cannot confirm in the real, current bytes does not enter the report.
- Reject, narrow, or demote a recommendation that is vague, duplicates another finding, misunderstands intentional semantics, or merely relocates complexity instead of removing it.
- Record every `skip` as **completed coverage**, not as a gap.
- Deduplicate overlapping findings and assign each accepted recommendation to exactly one authoritative subsystem.
- Keep opening bounded review batches until every inventory row is complete.

### 4. Audit the audit

Before finishing, run fresh independent passes for:
- repository coverage and missing subsystem boundaries;
- duplication and ownership overlap;
- materiality and over-abstraction;
- schema completeness (every finding carries all eight fields);
- dependency-aware priority ranking.

When the coverage pass finds a real omission, add an **explicit new subsystem row** and audit it. Never hide an omission by broadening a boundary that is already marked complete.

Then rank the accepted recommendations by concrete impact, confidence, implementation effort, blast radius, and prerequisites, and name the best first implementation slices.

---

## Output

One markdown report in the shape of `templates/audit-report.md`, returned in this run. It contains:
- the subsystem inventory with a final status on every row;
- every accepted recommendation with its eight fields;
- the explicit skip decisions and their reasons;
- the cross-cutting patterns, and the duplicates and superseded findings that were removed;
- the ranked priorities with their dependencies, and the best first implementation slices;
- the audit log.

Write the report in the language the user made the request in. Code identifiers, file paths, and status words stay verbatim.

---

## Done when
- Every identifiable subsystem in scope has been reviewed.
- Every subsystem row carries a recommendation or an explicit skip.
- Every finding carries complete evidence, scope, risk, and validation fields.
- Duplicates and weak abstractions have been removed.
- Priorities and dependencies are internally consistent.
- The repository is unchanged — `git status --short` matches the pre-audit baseline recorded in the report's `## Scope` block.

---

## References
- `references/worker-brief.md` — the verbatim brief handed to each subsystem worker, and the eight required recommendation fields.
- `templates/audit-report.md` — the canonical report shape.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
