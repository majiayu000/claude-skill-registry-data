---
name: first-pr
description: 'Composite skill — land a safe first PR in an unfamiliar repo without rediscovery loops or guessing at conventions. Chains onboard-new-repo (architecture + scripts + CI scan) → context-pack (relevant files + standards + ADRs for the scoped change) → scope-and-execute (narrow the task) → test-driven-development (write failing test first) → pr-to-release (open the PR). Use the first time you contribute to a repo OR when an unfamiliar contributor needs a guided first change.'
user-invocable: true
auto-invoke: '"first PR in <repo>", "I just cloned X", "what''s a safe first change", new-repo detection on first non-trivial work'
metadata:
  owner: global-agents
  tier: contextual
  canonical_source: ~/.claude/skills/first-pr
---

# First PR

The "I just landed in this repo, how do I ship something safely" composite.
Forces onboarding + scoping + TDD + release-branch flow in one chain so the
first PR matches the repo's conventions instead of fighting them.

## Auto-invocation triggers

- User says "first PR", "I just cloned X", "starter contribution", "good first issue"
- Repo has never appeared in `~/.claude/handoffs/` AND user is asking for any change
- User explicitly invokes `/first-pr`

## Workflow

### Phase 1 — Onboard (always)
Invoke `onboard-new-repo`. Required outputs:
- Architecture summary (1 paragraph)
- Build / test / lint commands
- CI provider + required checks
- Conventional commit prefix (detected from history)
- Whether `release` branch exists (drives later phase)
- Whether a CHANGELOG.md exists and follows Keep a Changelog
- Code-review tools installed (CodeRabbit / Greptile / SonarCloud / Sentry)

Save outputs to `~/.claude/handoffs/<repo>/onboarding.md` so this phase never
needs to repeat for the same repo.

### Phase 2 — Pick a safe scope (always)
If the user has not specified a change, suggest one from:
- A typo / doc fix flagged by spell/lint
- A test that documents existing behavior (no behavior change)
- A `// TODO:` with low surface area
- An issue labeled `good first issue` or `help wanted`

Refuse to scope a first PR as: refactor, dependency bump, architectural change,
or anything spanning >3 files. Surface to user: "First PRs should be ≤3 files
and have an obvious blast radius. Want to pick something smaller?"

### Phase 3 — Context pack (always, before any edit)
Invoke `context-pack` scoped to the target files + their callers + any rules
in `.claude/standards/`, `CLAUDE.md`, or `docs/adr/` that govern the area.

Token budget cap: 6k tokens. If retrieval exceeds the cap, narrow scope further
before continuing.

### Phase 4 — Scope and execute
Invoke `scope-and-execute` with the change framed as a one-line goal:
"Change <file>:<symbol> to <new behavior> so that <consumer> no longer <issue>."

If the goal cannot fit in one line: scope is too big — return to Phase 2.

### Phase 5 — Test-driven (mandatory for first PRs)
Invoke `test-driven-development`:
1. Write a failing test that asserts the desired behavior
2. Run the test, confirm it fails for the right reason
3. Implement the smallest change that makes the test pass
4. Re-run the full test file (not just the new test) to catch unintended breakage

Refuse to skip this phase for a first PR. Even doc-only changes get a smoke
check that the rendered output still parses.

### Phase 6 — Pre-flight checks (always)
Run the repo's own commands as discovered in Phase 1:
- Lint (`npm run lint` / `pnpm lint` / `ruff` / detected equivalent)
- Type check (`tsc --noEmit` / `mypy` / equivalent)
- Test (just the affected suite, not the full matrix)
- Build, if cheap (<60s)

If ANY check fails: fix before opening the PR. Never open a red PR for a first
contribution.

### Phase 7 — Open the PR
Detect base-branch model:
- If `release` branch exists → invoke `/pr-to-release` (handles full chain
  including CodeRabbit waits and CHANGELOG entry)
- If direct-to-main repo → invoke `/merge-confidently`

Title and body follow the conventions detected in Phase 1. Body must include:
- Why this change (link issue if it exists)
- What was tested (the new test added, plus any manual verification)
- A line acknowledging "first contribution to this repo" so reviewers know to
  apply a lighter touch for unfamiliarity but a heavier touch for convention
  mismatch

### Phase 8 — Capture the onboarding (always)
Invoke `knowledge-loop` to save a durable memory:
- Repo name
- Architecture summary from Phase 1
- Build/test/lint commands
- Conventions encountered (commit prefix, merge method, base branch)
- Surprises ("the test runner is `bun test`, not `vitest`")

This way subsequent sessions in this repo skip Phase 1.

## Stop / escalation conditions

- Phase 1 can't determine build/test commands → surface to user; do not guess
- Phase 2 user insists on a wide-scope first PR → ask twice, then refuse
- Phase 5 can't write a failing test (repo has no test infrastructure) →
  surface; recommend that the test infra get scaffolded as the actual first PR
- Phase 6 lint/type/build fails on `main` itself (not just the change) →
  surface; first PR should not be in a repo where main is broken
- No CHANGELOG.md and the project clearly versions itself → surface; ask
  whether to add one as a separate first PR before code changes

## Reconciliation

```
FIRST PR — <repo>
  Onboarding:      saved to handoffs/<repo>/onboarding.md
  Scope:           <one-line goal>
  Files touched:   <N> (≤3 enforced)
  Tests:           1 new test added; suite passes
  Checks:          lint ✓ | typecheck ✓ | test ✓ | build ✓
  PR:              #<n> opened against <release|main>
  Captured:        knowledge note: <repo> conventions
```

## Outputs / Evidence

- Onboarding summary path
- Scope statement
- PR number + base branch + CI status
- Knowledge note slug

## What this composite is NOT

- Not for routine work in repos you already know → `/pr-to-release`
- Not a refactor or architectural change → `/refactor-pipeline`
- Not an emergency fix → `/hotfix`
- Not for adding a new feature end-to-end → `/feature-from-zero`

## Pairs with

- `/onboard-new-repo` — used internally; standalone if no PR is intended
- `/pr-to-release` — Phase 7 delegates to it when release branch exists
- `/knowledge-loop` — Phase 8 ensures the onboarding cost is paid once
