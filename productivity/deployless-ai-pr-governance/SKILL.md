---
name: deployless-ai-pr-governance
description: AI PR intake and multi-agent governance for deployless repositories. Use when a repo has high-volume bot or agent PRs, parallel agent work, noisy low-context PRs, merge-queue pressure, CI exhaustion, duplicate fixes, ownership confusion, or review bottlenecks that threaten a single-mainline delivery model.
metadata:
  priority: 7
  pathPatterns:
    - ".github/pull_request_template.md"
    - ".github/workflows/**"
    - "CODEOWNERS"
    - "CONTRIBUTING.md"
    - "docs/**"
    - "AGENTS.md"
  promptSignals:
    phrases:
      - "ai pr"
      - "ai pull requests"
      - "agent pr"
      - "multi-agent"
      - "merge queue pressure"
      - "review bottleneck"
    allOf:
      - [agent, pull]
      - [ai, review]
    anyOf:
      - "low-context PR"
      - "CI exhaustion"
      - "duplicate fixes"
      - "ready for agent"
      - "agent workflow"
    noneOf: []
    minScore: 5
---

# AI PR Intake and Multi-Agent Governance

## Purpose

Keep a deployless mainline healthy when AI agents can generate pull requests faster than humans can review them.

The target model is:

- every AI PR has clear intent, owner, scope, tests, and rollback notes
- only small, reviewable, production-deployable changes enter the mainline queue
- multiple agents do not fight over the same files, migrations, flags, or release paths
- CI capacity is protected from speculative or duplicate work
- humans review decisions and risk, not piles of unexplained diffs
- the primary coordinator turns critique, design, implementation, and review outputs into explicit merge decisions

## Preconditions

Run these first when possible:

1. `deployless-audit`
2. `deployless-mainline`
3. `deployless-release-controls`
4. `deployless-production-path`
5. `deployless-operational-safety`

If the repo is already drowning in AI PRs, apply this skill immediately as an intake stopgap, then backfill the earlier deployless plan.

## Inputs to inspect

- Current open PR count, draft PR count, and PR authors
- Bot, agent, automation, and dependency-update accounts
- PR templates, issue templates, labels, milestones, projects, and merge queue
- CODEOWNERS or equivalent ownership rules
- Branch protection, required checks, and required reviews
- CI cost, queue time, cancellation behavior, and flaky checks
- Repeatedly touched files, merge-conflict hotspots, migrations, and generated files
- Existing agent instructions, task trackers, handoff docs, and branch naming conventions
- Planning artifacts, domain glossary, ADRs, acceptance criteria, test seams, review reports, and issue readiness labels

## Intake states

Create or adapt labels for these states:

```text
ai/generated
ai/needs-intent
ai/needs-owner
ai/needs-scope
ai/needs-tests
ai/conflict-risk
ai/ci-expensive
ai/ready-for-human-review
ai/parked
ai/rejected
```

Use the repo's existing label style if it differs.

## Triage rules

Every AI PR must answer:

- What user or operator problem does this solve?
- What issue, ticket, incident, or decision authorized it?
- What files and behaviors are intentionally in scope?
- What tests or checks prove the change?
- What could go wrong after deployment?
- How can the change be disabled, rolled back, or followed up?

If those answers are missing, mark the PR `ai/needs-intent` or `ai/needs-scope` and keep it out of the merge queue.

Reject or close AI PRs that:

- duplicate an active PR or accepted plan
- are mostly churn, formatting, renames, or broad refactors without a named need
- modify generated files without updating the source
- change production deployment, secrets, migrations, auth, billing, or security-sensitive paths without an explicit owner
- bundle unrelated fixes that cannot be reviewed independently
- pass CI but lack a coherent reason to exist

## Low-context PR handling

Treat low-context AI PRs as untrusted until they provide evidence. A PR that only says "improves the code" or "fixes issues" is not ready for review.

Require a short PR body with:

```markdown
## Intent

## Scope

## Validation

## Risk and rollback
```

For vague PRs, ask the agent to rewrite the PR body and split the diff before requesting human review.

## Multi-agent work contract

Use these rules when several agents work in the same repository:

- One owner per task, PR, or issue.
- One primary coordinator owns scope, sequencing, review classification, and merge readiness.
- One active agent per risky file area unless an explicit coordinator owns the integration.
- Agents claim scope in the issue, task, or coordination doc before editing.
- Agents use short-lived branches and delete them after merge or rejection.
- Agents do not force-push, rebase, or rewrite another agent's branch without explicit handoff.
- Agents rebase or update from `main` before moving a PR to review-ready.
- Agents leave a handoff note when pausing work.

Recommended branch names:

```text
agent/<tool-or-agent>/<ticket-or-area>-<short-slug>
bot/<provider>/<ticket-or-area>-<short-slug>
human/<name>/<ticket-or-area>-<short-slug>
```

## Coordinator-led execution loop

Use this loop for non-trivial AI-authored work.

### 0. Orient

Read repository instructions, contribution docs, domain glossary, relevant ADRs, and the source issue, plan, or PRD. If issue-tracker or label docs exist, follow them.

### 1. Shape

Challenge the scope before coding:

- resolve unclear terms into the repo's domain language
- identify hidden dependencies and hard-to-reverse decisions
- ask one blocking question at a time when human judgment is required
- create an ADR only for real trade-offs that will surprise future maintainers
- keep the PR in draft or `ai/needs-intent` until scope is coherent

### 2. Publish ready slices

Break broad work into vertical tracer-bullet slices:

- each slice should be independently buildable and reviewable
- each slice should have acceptance criteria and a test seam
- dependency order should be explicit
- only slices with enough context for unattended agent work should be marked ready

### 3. Design important interfaces twice

For meaningful module, API, flag, migration, or agent-workflow boundaries, ask independent design agents for multiple distinct designs. Compare them on:

- caller simplicity
- ease of correct use
- hidden implementation complexity
- compatibility with existing patterns
- testability through public behavior

Choose deliberately and record the decision when it affects future work.

### 4. Build with vertical test-first loops

For non-trivial implementation:

- write one behavior test through the highest useful public seam
- make it fail for the right reason
- write the minimum code to pass
- repeat for the next behavior
- refactor only after the current slice is green
- run focused checks regularly and broader checks before final review

Avoid writing all tests first or all implementation first. That usually creates brittle tests and speculative code.

### 5. Review with independent agents

Before merge readiness, run independent review on two axes:

- Standards: whether the diff follows the repo's documented conventions.
- Spec: whether the diff satisfies the source issue, PRD, or plan without scope creep.

Keep those reports separate so one does not mask the other.

### 6. Classify findings

The primary coordinator classifies every critique or review finding:

```text
accepted
rejected
deferred
needs-human-decision
```

Accepted findings become code, docs, labels, tests, or follow-up issues. Rejected findings get a brief reason. Deferred findings get an owner or explicit risk note. Human-decision findings block merge readiness.

## PR size and shape

Prefer PRs that are:

- under 400 changed lines when practical
- limited to one behavior, bug, flag, migration phase, or cleanup
- reviewable without understanding unrelated rewrites
- covered by focused tests or an explicit test-gap note
- deployable immediately after merge

Exceptions are allowed for generated lockfiles, vendored updates, mechanical migrations, or broad formatting changes, but they must be labeled and reviewed as mechanical.

## Queue policy

Use a visible queue with WIP limits:

- Cap active AI PRs per repository or ownership area.
- Keep speculative AI PRs in draft until intent and tests are clear.
- Prioritize incident fixes, production blockers, security fixes, and already-reviewed small PRs.
- Batch dependency updates only when the repo already has reliable tests.
- Park stale AI PRs that conflict repeatedly with `main`.
- Close rejected PRs promptly so they do not drain review attention.

Suggested limits:

```text
max active AI PRs per owner area: 3-5
max review-ready AI PRs per human reviewer: 2-3
max parallel migration PRs touching the same data model: 1
max speculative refactor PRs in merge queue: 0
```

Adjust limits to team size and CI capacity.

## CI protection

Protect CI from PR floods:

- Run cheap checks before expensive checks.
- Cancel superseded runs on the same branch.
- Require intent/scope labels before expensive end-to-end, load, mobile, or integration jobs.
- Use path-aware checks in monorepos.
- Split flaky-check triage from product review.
- Do not let one bot account starve human fixes or incident PRs.

When a PR is `ai/ci-expensive`, require a reviewer or owner to approve full CI.

## Review gates

Before an AI PR enters merge queue, require:

- clear intent and linked issue or decision
- one accountable owner
- small enough diff or documented exception
- completed scope challenge for unclear or broad work
- acceptance criteria and test seam for agent-ready work
- passing required checks
- tests for changed behavior or a documented test gap
- final standards/spec review findings classified by the coordinator
- no unowned migration, auth, billing, secret, deployment, or security change
- release control for unfinished or risky behavior
- rollback or follow-up plan when production behavior changes

For high-risk paths, require CODEOWNER review even if CI passes.

## Docs to create

Create or update:

```text
docs/ai-pr-intake.md
docs/multi-agent-work.md
docs/agent-execution-loop.md
docs/deployless-mainline-plan.md
```

Use existing contribution or operations docs if the repo already has them.

## Minimum templates

### `docs/ai-pr-intake.md`

```markdown
# AI PR intake

## Intake labels

## Triage rules

## Review-ready requirements

## Queue limits

## CI policy

## Close or park rules
```

### `docs/multi-agent-work.md`

```markdown
# Multi-agent work

## Claiming work

## Branch naming

## Handoff notes

## Conflict ownership

## High-risk paths
```

### `docs/agent-execution-loop.md`

```markdown
# Agent execution loop

## Orient

## Scope challenge

## Ready slices

## Interface design alternatives

## Test-first implementation

## Final review axes

## Finding classification
```

## Output

Create or update:

- PR template with intent, scope, validation, risk, and rollback sections
- labels or label documentation for AI PR intake
- CODEOWNERS or ownership docs for sensitive paths
- branch protection or merge queue documentation
- CI concurrency and path-filtering settings where safe
- `docs/ai-pr-intake.md`
- `docs/multi-agent-work.md`
- `docs/agent-execution-loop.md`
- `docs/deployless-mainline-plan.md`, appending AI PR governance status

## Acceptance criteria

This skill is complete when:

- AI-generated PRs have a documented intake path
- low-context PRs are kept out of review-ready and merge-queue states
- multi-agent branch and handoff rules are documented
- non-trivial agent work has a documented orient, shape, slice, design, test-first, and review loop
- ownership exists for high-risk paths
- CI has a plan for flood control or the blocker is documented
- stale, duplicate, speculative, and unreviewable AI PRs can be parked or closed quickly
- deployless mainline rules still apply to every AI PR

## Anti-goals

- Do not auto-merge AI PRs just because CI passes.
- Do not create a separate long-lived AI integration branch.
- Do not let agents bypass CODEOWNERS, security review, or compliance gates.
- Do not use labels as a substitute for reading risky diffs.
- Do not preserve stale AI PRs merely because an agent spent time generating them.
- Do not delegate merge judgment to a critique, design, implementation, or review agent.
