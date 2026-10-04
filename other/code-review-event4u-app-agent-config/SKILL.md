---
model_tier: high
name: code-review
# Claude Code reserves this /name — model-invocation only, so the bundled /code-review skill stays reachable.
user-invocable: false
description: "Use when the user says \"review this\", \"check my code\", or wants feedback on changes. Reviews for correctness, quality, security, and coding standards."
domain: quality
parallelizable: files
workspaces:
  - engineering
packs:
  - engineering-base
---

# code-review

## When to use

Use this skill when:
- Reviewing a PR (own or someone else's)
- Self-reviewing local changes before creating a PR
- Responding to review feedback on your PR
- The user asks to "review", "check", or "look at" code changes

## Procedure: Review code

### Mindset

- **Be thorough but pragmatic** — catch real bugs, not style nitpicks that tools handle.
- **Understand intent first** — read the PR description, linked ticket, and commit messages before looking at code.
- **Check the full picture** — a change in a service may require changes in tests, migrations, docs.
- **Assume good intent** — suggest improvements, don't criticize.

### Review order

1. **Understand the goal** — what is this change trying to achieve?
2. **Detect the change-type + depth** — route to the right checklist and pick the review depth (below).
3. **Architecture** — does the approach make sense? Right layer? Right pattern?
4. **Correctness** — does it actually work? Edge cases? Error handling?
5. **Quality** — types, naming, readability, SOLID?
6. **Redundancy** — see below; a verdict, not a "this looks duplicated".
7. **Propagation** — did a changed concept reach every occurrence? see below.
8. **Security** — input validation, authorization, injection?
9. **Performance** — N+1 queries, missing indexes, unbounded queries?
10. **Tests** — are new paths covered? Are existing tests still valid?
11. **Conventions** — does it follow project standards?

## The redundancy dimension

`DRY` as a checklist word produced findings nobody could act on: it names a
principle, not a decision, and it has no answer for the case where two copies
should stay. Replace it with a verdict.

Classify the finding against
[`redundancy-taxonomy`](../../../docs/guidelines/redundancy-taxonomy.md) —
implementation, knowledge, or representation — and record one verdict from that
document's list. `keep-duplicated` and `de-abstract` are successful outcomes; a
finding with no recorded verdict stays open. Knowledge, policy, contract and
delivery-authority duplication outrank clone percentage: two copies of a
*decision* diverge into a bug, two copies of a loop usually do not.

**Diff-aware, always.** The finding is duplication this change **introduces**,
or duplication on a surface it touches. Pre-existing duplication is baseline —
it is named once if the reviewer thinks it matters and it never fails an
unrelated change. A review that reds a diff against debt it did not create is a
review nobody will run twice.

For comments, labels, tooltips, placeholders and empty states, run the
Information Delta Test from the same document rather than judging text volume.
A reduction that removes an accessibility name is a defect, not a cleanup.

Naming is the same dimension pointed the other way: a diff that introduces a
second term for a concept the tree already names is the finding, and an existing
split is baseline. The classes and the `canonicalize-term` / `keep-distinct`
verdicts are in the same document.

## The propagation dimension

A change is complete when the **concept** changed everywhere, not when the named
file compiles. Two shapes to check, both of which the file-level review misses:

**A closed set gained or lost a member** (enum, union, literal type, state
machine, role or permission set, schema `enum`, DB check constraint). List the
consumers and their status — every `switch` / `match` / if-chain over the type,
every lookup table keyed by it, every validator, serializer, schema, fixture and
translation key. A `default` branch that silently absorbs the new member is a
missing case, not a handled one. Procedure:
[`downstream-changes-mechanics`](../../../docs/guidelines/agent-infra/downstream-changes-mechanics.md).

**A shared behaviour moved and its siblings did not.** A defect fixed in one
place is presumed to recur until searched: name the exact wrong construct, grep
the tree, and report the count — zero is a real answer and worth stating, because
it distinguishes "this was unique" from "nobody looked".

Diff-aware on the same terms as redundancy: the finding is a concept **this
change** left half-migrated. Pre-existing incompleteness elsewhere is baseline.

When the diff **creates** a class, component, service or hook rather than
changing one, the question is whether it needed to exist: what was searched,
what was found, and why composing or extending the incumbent was rejected. An
answer, not a ceremony — and the thresholds for when repetition actually earns
an abstraction are in
[`component-oriented-and-oop-development`](../../../docs/guidelines/component-oriented-and-oop-development.md).

## Change-type routing — load only the checklist the diff needs

Per-domain checklists live in `checklists/`, loaded **on demand** — a review
carries only the depth the change needs (progressive disclosure; a dependency
bump does not pay for the backend security table). Detect the change-type from
the diff's file paths, then read the matching file:

| Change-type | File-pattern signal (any match) | Checklist |
|---|---|---|
| **dependency** (expedited) | ONLY `composer.json`/`*.lock`, `package.json`/lockfiles, `pyproject.toml`, `go.mod`/`go.sum`, `Cargo.toml`/`*.lock` | [`checklists/dependency.md`](checklists/dependency.md) |
| **migration / database** | `**/migrations/**`, `**/*migration*`, schema files, query-heavy data-access code | [`checklists/database.md`](checklists/database.md) |
| **frontend / UI** | `*.tsx`, `*.jsx`, `*.vue`, `*.blade.php`, `*.css`, `components/**`, `resources/views/**` | [`checklists/frontend.md`](checklists/frontend.md) |
| **infra / IaC / CI** | `*.tf`, `Dockerfile*`, `k8s/**`, `*.yaml` under `.github/workflows/`, Pulumi/Ansible | [`checklists/infra.md`](checklists/infra.md) |
| **test-only** | ONLY `tests/**`, `*.test.*`, `*.spec.*`, `*Test.php` | [`checklists/test-only.md`](checklists/test-only.md) |
| **docs-only** | ONLY `*.md`, `docs/**` | [`checklists/docs.md`](checklists/docs.md) |
| **backend / default** | anything else (server-side logic) | [`checklists/backend.md`](checklists/backend.md) |

A diff spanning several types loads each matching checklist; a mixed diff is
never downgraded to the expedited path (a lockfile bump *plus* code is backend
+ dependency). Every `checklists/*.md` file MUST be reachable from a row above.

Framework-specific conventions defer to the carve-outs: PHP / Laravel →
[`laravel`](../laravel/SKILL.md), [`laravel-validation`](../laravel-validation/SKILL.md),
[`eloquent`](../eloquent/SKILL.md), [`pest-testing`](../pest-testing/SKILL.md),
[`blade-ui`](../blade-ui/SKILL.md), [`php-coder`](../php-coder/SKILL.md);
Symfony → [`symfony-workflow`](../symfony-workflow/SKILL.md); Next.js / TS →
[`nextjs-patterns`](../nextjs-patterns/SKILL.md), [`react-shadcn-ui`](../react-shadcn-ui/SKILL.md).

### Metadata gates — verdict `❓` until satisfied

Some changes are unverifiable from source; when a gate fires the verdict is
`❓`, not approval — ask for the missing evidence:

- **UI diff without a screenshot / visual check** → `❓` (rendered result unverifiable from source).
- **New module / feature without a test plan** → `❓` (behaviour coverage unconfirmable).
- **Optional cross-cutting gate** (per-project): a new state-changing op without a telemetry OR authz touch → `❓`.

### Adaptive review depth

Pick depth from diff size, override upward on risk:

| Diff / surface size | Depth | What it means |
|---|---|---|
| **SMALL** (single file / few lines) | DEEP | Read every line; trace each branch. |
| **MEDIUM** (a feature, several files) | FOCUSED | Deep on changed logic + its callers; skim the rest. |
| **LARGE** (sweeping / many files) | SURGICAL | Deep on the risk-bearing files; explicitly bound the rest as un-deep-reviewed. |

**Risk triggers force HIGH depth regardless of diff size:** auth / crypto,
external calls / SSRF, removal of a validation or authz check, money /
tenant-boundary code. [`blast-radius-analyzer`](../blast-radius-analyzer/SKILL.md)
is one input to sizing; the depth policy + coverage-honesty line are this
skill's addition. Every review ends with a **Coverage & confidence** line
(deep-reviewed vs skimmed/bounded-out files + confidence) — silent partial
coverage reads as full coverage.

## Re-review scoping + parallel-review de-biasing

- **Re-review scoping** — on a follow-up push, scope to the **changed lines
  only**; never flag new issues in untouched code (note pre-existing issues
  separately, never in the blocking set). Same discipline `fix-pr-comments`
  reply rounds apply.
- **Ordering-bias** — when N reviewers/lenses get the **same file set**
  (`parallelizable: files`; council lenses), give each an independently
  shuffled file order (deterministic seed per session, logged for replay) so
  a fixed order does not correlate their blind spots. Single-reviewer → no shuffle.

**MEASURED, and the result is a null — 2026-08-23.** This control is prose and nothing in
the package implements it. That is now true for a recorded reason rather than by
omission: the pre-registered question — does rotating reviewer order change the finding set
on a frozen corpus, by more than 15 % — **cannot be answered from the corpus that exists**.
`agents/evidence/reviews/` holds 123 findings artifacts, and none of them records the file
order it was produced under, so the counterfactual is not recoverable; re-running reviewers
produces fresh judgements in which ordering is confounded with run-to-run variance. Full
null, with its reopening condition: `agents/evidence/review-rotation-prereg-and-null.md`.
A reduced-power crossover was considered and refused — it would risk a false closure on a
control this paragraph still specifies.

## Before creating a PR

1. When `quality.local_auto_run: true`: run the project's quality pipeline (see the stack carve-out for the exact commands — PHP: `quality-tools`) and tests via the project's runner (`make test`, `npm test`, `pytest`, `go test ./...`, or the project's wrapper script). Under the default (`false` / missing): skip both — remote CI on the PR is the gate.
2. Ensure CI passes on the branch (remote CI is authoritative).
3. Self-review the diff: `git diff origin/main..HEAD`.

## Receiving feedback

### The response pattern

Constraint: **understand each comment fully before touching code, verify it against codebase reality, and implement one item at a time (test each).** Restate anything ambiguous in your own words — or ask. Push back with technical reasoning when a suggestion is unsound for *this* codebase rather than complying reflexively.

If **any item is unclear**, STOP — do not implement anything yet. Items may be related;
partial understanding leads to wrong implementation.

### No performative agreement

- **Do NOT** reply with "Great point!", "You're absolutely right!", "Excellent catch!" or similar.
- **Instead:** Just fix it. "Fixed." or "Updated — [brief description of what changed]."
- Actions speak louder than words — the code itself shows you heard the feedback.

### Source-specific handling

**Internal team feedback** (trusted colleagues):
- Implement after understanding — no need for deep skepticism.
- Still ask if scope is unclear.
- Skip to action or technical acknowledgment.

**External / Copilot / bot feedback** (less context):
- Check: Technically correct for THIS codebase?
- Check: Does it break existing functionality?
- Check: Is there a reason for the current implementation?
- Check: Does the reviewer understand the full context?
- **YAGNI check:** If the reviewer suggests "implementing properly", grep the codebase
  for actual usage. If unused → suggest removing (YAGNI).
- If it conflicts with existing architectural decisions → discuss with the team first.

### When to push back

Push back when:
- Suggestion breaks existing functionality.
- Reviewer lacks full context.
- Violates YAGNI (unused feature).
- Technically incorrect for this stack.
- Legacy/compatibility reasons exist.
- Conflicts with architectural decisions.

How: Use technical reasoning, not defensiveness. Reference working tests/code.

### Addressing PR comments systematically

Constraint: **clarify anything unclear before implementing, fix one item at a time (test each), and reply in each review thread** — not as a top-level PR comment. Triage first (blocking → simple → complex) so blockers land first; `gh pr view --comments` lists the threads.

```bash
# Reply to a specific review comment thread
gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/replies \
  -f body="Fixed in latest commit."
```

## Rubric pass (optional, surfacing-only)

After completing a review, run
[`judge-artifact-completeness`](../judge-artifact-completeness/SKILL.md)
with rubric `pr-review-score` to verify evidence-fit, risk/blast-radius
coverage, and migration/rollback completeness. Invoke when the review is
high-risk or the user asks for a completeness check — not by default.

## Output format

Validate, then emit these parts in order:

1. **Reasoned validation first** — group candidates by file + line range,
   disposition each CONFIRMED / adjusted / DROPPED with a one-line reason (not
   vote-counting).
2. **Tier 1 — Mechanical** — enumerated, fix-ready findings by severity blocks, never mixed.
3. **Tier 2 — Alignment** — each flag names the principle/ADR at stake + the concern (from the governance-conflict scan); not fix-ready by construction.
4. **Dropped false positives** — collapsible; each DROPPED candidate + reason. Empty is fine, but the section is mandatory (its presence proves validation ran).
5. **Verdict line** — `YES` / `NOT-SURE` (`❓`, a metadata gate fired or coverage bounded) / `NO`, plus Tier-1 blocker/suggestion counts.
6. **Coverage & confidence line** — deep vs skimmed/bounded-out files + confidence.

Full template, governance-conflict scan (status-aware over `docs/decisions/`,
incl. draft ADRs; guarded `git blame` reviewer hint), and the security-class
deep-verify path → [`checklists/producing-the-review.md`](checklists/producing-the-review.md).

> **Tally-vs-reasoned boundary.** Finding-level review uses reasoned validation
> (each finding stands on its own traced reason); option-level decisions use
> the council **stance tally** ([`ai-council`](../ai-council/SKILL.md)). Never
> cross-apply — no resolving a bug finding by counting votes, no resolving a
> design option by reasoned-validating one take. Mirrored in `ai-council` so
> the boundary is grep-checkable from both sides.

Group related findings; skip what the linter / type-checker already catches.

## Adversarial review

Before creating a PR or presenting code changes, run the **`adversarial-review`** skill.
Focus on the "Code changes / Refactoring" attack questions.

## Auto-trigger keywords

- code review
- PR review
- pull request
- review checklist
- review feedback
- review changes
- check my code

## Gotcha

- Don't rewrite code that works and is tested just because you'd write it differently.
- The model tends to suggest changes that are out of scope — stay focused on the PR's intent.
- "I would prefer X" is not a valid review comment unless X prevents a bug or violates a rule.
- Always check if the PR has tests — missing tests is always worth flagging.

## Do NOT

- Do NOT approve without actually reading the code.
- Do NOT agree with review comments without verifying them against the codebase.
- Do NOT use performative language when responding to feedback ("Great point!", "Excellent catch!").
- Do NOT nitpick style issues the project's formatter / auto-refactor (ECS, Prettier, Ruff, gofmt) handles automatically.
- Do NOT merge without CI passing and quality checks green.
