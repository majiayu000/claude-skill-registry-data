---
name: tech-debt
description: "Track, categorize, and prioritize technical debt across the codebase. Scans for debt indicators, maintains a debt register, and recommends repayment scheduling."
argument-hint: "[scan|add|prioritize|report]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

## User Guide

- When to use: Track, categorize, and prioritize technical debt across the codebase. Scans for debt indicators, maintains a debt register, and recommends repayment scheduling.
- Inputs: Command arguments: `/tech-debt [scan|add|prioritize|report]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before scanning technical debt:
- `design/cdd/game-concept.md` -> **[Game]** categorize debt by gameplay risk, engine integration, content pipeline, performance/frame-time, input/platform constraints, and playtest impact.
- `design/cdd/product-concept.md` -> **[Product]** categorize debt by API/CLI/UI contracts, data migrations, auth/permissions, observability, deployment, dependency risk, testing gaps, and user workflow impact.
- If unclear, keep categories domain-neutral and flag missing concept context.

Game debt categories remain available. Product debt categories are added beside them.
## Phase 1: Parse Subcommand

Determine the mode from the argument:

- `scan` — Scan the codebase for tech debt indicators
- `add` — Add a new tech debt entry manually
- `prioritize` — Re-prioritize the existing debt register
- `report` — Generate a summary report of current debt status

If no subcommand is provided, output usage and stop. Verdict: **FAIL** — missing required subcommand.

---

## Phase 2A: Scan Mode

Search the codebase for debt indicators:

- `TODO` comments (count and categorize)
- `FIXME` comments (these are bugs disguised as debt)
- `HACK` comments (workarounds that need proper solutions)
- `@deprecated` markers
- Duplicated code blocks (similar patterns in multiple files)
- Files over 500 lines (potential god objects)
- Functions over 50 lines (potential complexity)

Categorize each finding:

- **Architecture Debt**: Wrong abstractions, missing patterns, coupling issues
- **Code Quality Debt**: Duplication, complexity, naming, missing types
- **Test Debt**: Missing tests, flaky tests, untested edge cases
- **Documentation Debt**: Missing docs, outdated docs, undocumented APIs
- **Dependency Debt**: Outdated packages, deprecated APIs, version conflicts
- **Performance Debt**: Known slow paths, unoptimized queries, memory issues

Product-specific scan additions:
- API contract drift: undocumented endpoints, unstable error codes, schema/example mismatch, missing idempotency or pagination notes
- CLI debt: unclear flags, stdout/stderr mixing, missing non-interactive mode, missing `--json` or `--no-color` where required
- Web/UI workflow debt: inaccessible focus paths, missing empty/error/loading states, forms without recoverable validation
- Data/migration debt: irreversible migrations, missing dry-run, no rejected-row export, unclear rollback, stale seeds
- Auth/permission debt: overly broad roles, missing tenant checks, unclear ownership boundaries
- Observability/deployment debt: missing logs/metrics/traces, weak health checks, no rollback plan, brittle build/package scripts
- Product docs debt: README/help/API examples do not match implementation, stale screenshots, missing adoption/troubleshooting path

Present the findings to the user.

Ask: "May I write these findings to `docs/tech-debt-register.md`?"

If yes, update the register (append new entries, do not overwrite existing ones). Verdict: **COMPLETE** — scan findings written to register.

If no, stop here. Verdict: **BLOCKED** — user declined write.

---

## Phase 2B: Add Mode

Prompt for: description, category, affected files, estimated fix effort, impact if left unfixed.

For Product entries, also capture:
- Affected surface: API / CLI / web / library / data / migration / docs / deployment
- User Promise or JTBD affected
- Contract risk: breaking / non-breaking / internal only
- Evidence needed to close: contract test, CLI transcript, e2e test, migration dry-run, docs update, validation note

Present the new entry to the user.

Ask: "May I append this entry to `docs/tech-debt-register.md`?"

If yes, append the entry. Verdict: **COMPLETE** — entry added to register.

If no, stop here. Verdict: **BLOCKED** — user declined write.

---

## Phase 2C: Prioritize Mode

Read the debt register at `docs/tech-debt-register.md`.

Score each item by: `(impact_if_unfixed × frequency_of_encounter) / fix_effort`

For Product debt, raise priority when the debt affects:
- Public API/CLI contracts or SDK examples
- Auth, permissions, secrets, tenant data, migrations, or rollback
- User onboarding, core workflow completion, or adoption confidence
- Build/release/deployment reliability
- Test evidence required by `/gate-check` or `/release-checklist`

Re-sort the register by priority score and recommend which items to include in the next sprint.

Present the re-prioritized register to the user.

Ask: "May I write the re-prioritized register back to `docs/tech-debt-register.md`?"

If yes, write the updated file. Verdict: **COMPLETE** — register re-prioritized and saved.

If no, stop here. Verdict: **BLOCKED** — user declined write.

---

## Phase 2D: Report Mode

Read the debt register. Generate summary statistics:

- Total items by category
- Total estimated fix effort
- Items added vs resolved since last report
- Trending direction (growing / stable / shrinking)
- Product distribution by surface: API, CLI, web, data/migration, docs, deployment, dependency, security
- Public contract debt count and user-workflow/adoption blocker count

Flag any items that have been in the register for more than 3 sprints.

Output the report to the user. This mode is read-only — no files are written. Verdict: **COMPLETE** — debt report generated.

---

## Phase 3: Next Steps

- Run `/sprint-plan` to schedule high-priority debt items into the next sprint.
- Run `/tech-debt report` at the start of each sprint to track debt trends over time.

### Debt Register Format

```markdown
## Technical Debt Register
Last updated: [Date]
Total items: [N] | Estimated total effort: [T-shirt sizes summed]

| ID | Category | Description | Files | Effort | Impact | Priority | Added | Sprint |
|----|----------|-------------|-------|--------|--------|----------|-------|--------|
| TD-001 | [Cat] | [Description] | [files] | [S/M/L/XL] | [Low/Med/High/Critical] | [Score] | [Date] | [Sprint to fix or "Backlog"] |

## Product Debt Fields (if product)

| ID | Surface | User Promise / JTBD Impact | Contract Risk | Evidence Needed | Owner |
|----|---------|----------------------------|---------------|-----------------|-------|
| TD-P001 | [API/CLI/web/data/docs/deploy] | [Impact] | [Breaking/non-breaking/internal] | [contract/e2e/migration/docs/validation] | [owner] |
```

### Rules
- Tech debt is not inherently bad — it is a tool. The register tracks conscious decisions.
- Every debt entry must explain WHY it was accepted (deadline, prototype, missing info)
- "Scan" should run at least once per sprint to catch new debt
- Items older than 3 sprints without action should either be fixed or consciously accepted with a documented reason
- Product debt that affects public contracts, migrations, auth, secrets, rollback,
  or core workflow adoption should be reviewed before release even if effort is high
