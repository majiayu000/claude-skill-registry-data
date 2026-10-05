---
name: error-log
description: Apply when learning from a mistake. Central memory of past errors and derived rules; consult before logging a new error to avoid duplicates.
license: MIT
version: 1.0.0
tokens_target: 3000
triggers:
  - made or corrected a mistake
  - learn from this
loads_after: []
supersedes: []
---

# Sub-Skill: Error Log

**Purpose:** Central memory for all mistakes the agent has made or observed. Each entry prevents the same mistake from happening twice. Validated by [`tools/validate_rules.py`](../../tools/validate_rules.py) against [`schemas/error-entry.json`](../../schemas/error-entry.json) on every PR.

---

## Entries

```yaml
errors:

  - id: ERR-2026-001
    date: 2026-04-12
    category: development
    severity: high
    context: TypeScript project with strictNullChecks. Agent disabled it per-file to silence a demo error.
    what_happened: Added triple-slash directive disabling strictNullChecks; CI caught it.
    root_cause: Silenced compiler instead of fixing the null path.
    impact: Null-safety gap shipped to CI; required revert.
    resolution: Removed directive; fixed the null path properly.
    new_rule: Never disable strictNullChecks or any strict TypeScript flag to silence a compiler error; fix the type instead.
    target_file: skills/typescript/SKILL.md

  - id: ERR-2026-007
    date: 2026-04-28
    count: 2
    category: development
    severity: high
    context: TypeScript monorepo rename. Agent renamed in source and adjacent test only.
    what_happened: Reported rename complete; cross-package refs still used old name.
    root_cause: Local tsc scope hides cross-package references in a monorepo.
    impact: 35 min lost first occurrence; 10 min second.
    resolution: Added project-wide grep step to rename checklist.
    new_rule: After any rename, run a project-wide grep for the old name before claiming the rename is complete.
    target_file: skills/code-quality/SKILL.md

  - id: ERR-2026-012
    date: 2026-05-04
    category: deployment
    severity: high
    context: Billing service deploy with DB migration. Agent ran rollout before migration job.
    what_happened: New image expected a column that didn't exist; readiness probes failed ~90 s.
    root_cause: Assumed migrations run at pod startup; they're a separate Helm Job.
    impact: 90 s probe failures; on-call paged.
    resolution: Ran migration Job first, then re-rolled deployment.
    new_rule: Before any deployment that includes a database migration, run the migration job to completion first.
    target_file: skills/review-deployment/SKILL.md

  - id: ERR-2026-014
    date: 2026-05-13
    category: development
    severity: medium
    context: pytest fixtures returning mutable dict shared across tests.
    what_happened: First test mutated fixture; second received already-mutated object. Flaky in CI.
    root_cause: Fixture returned mutable object by reference; no fresh instance per test.
    impact: 2 h debugging cross-test pollution.
    resolution: Changed fixture to factory callable returning fresh dict per invocation.
    new_rule: Never return mutable objects from pytest fixtures; use factory fixtures that create fresh instances per invocation.
    target_file: skills/python/SKILL.md

  - id: ERR-2026-016
    date: 2026-05-13
    category: development
    severity: medium
    context: API client retry logic caught broad Exception, silently retrying a TypeError.
    what_happened: None dereference retried 3x before failing; 4 h debugging.
    root_cause: Overly broad except caught programming errors that should crash immediately.
    impact: Real error buried in retry logs.
    resolution: Narrowed catch to ConnectionError and Timeout only.
    new_rule: Always catch specific exception types rather than broad base classes in retry or error recovery logic.
    target_file: skills/code-quality/SKILL.md

  - id: ERR-2026-017
    date: 2026-05-13
    category: development
    severity: medium
    context: is_palindrome implemented before tests; empty-string edge case missed.
    what_happened: Tests validated code-as-written; empty string returned True instead of False.
    root_cause: No failing test first; no signal that empty-string was unhandled.
    impact: Bug shipped.
    resolution: Rewrote with TDD; empty-string test failed first, drove correct implementation.
    new_rule: Always write a failing test before implementing new behavior to ensure tests validate intended behavior.
    target_file: skills/tdd/SKILL.md

  - id: ERR-2026-018
    date: 2026-05-13
    category: development
    severity: medium
    context: Agent applied a fix to a reported bug without first reproducing it.
    what_happened: Bug recurred within two days under a slightly different input path.
    root_cause: No reproduction case; no way to confirm the fix addressed the actual failure mode.
    impact: Duplicate bug report; additional debugging cycle wasted.
    resolution: Wrote a minimal reproduction test, traced to root cause, fixed the invariant.
    new_rule: Before fixing a bug, reproduce it on demand and encode the reproduction as an automated test first.
    target_file: skills/debugging/SKILL.md

  - id: ERR-2026-019
    date: 2026-05-13
    category: security
    severity: high
    context: REST API with RBAC. Agent added admin endpoint without ownership check.
    what_happened: Any authenticated admin could delete any user's record by supplying an arbitrary ID.
    root_cause: Role check treated as sufficient; resource ownership never verified.
    impact: Privilege escalation; any admin could delete records belonging to other users.
    resolution: Added ownership assertion before delete; returns 403 if caller does not own the record.
    new_rule: Always verify resource ownership in addition to role-based access on mutation endpoints.
    target_file: skills/security-review/SKILL.md

  - id: ERR-2026-020
    date: 2026-05-13
    category: development
    severity: medium
    context: Python service Dockerfile. Agent placed COPY . . before RUN pip install.
    what_happened: Every code edit triggered a full pip install in CI, adding ~3 min per build.
    root_cause: Source copy invalidated the dependency layer before the install step.
    impact: 3 min added to every CI build; feedback loop degraded.
    resolution: Moved COPY requirements.txt and RUN pip install before COPY . .
    new_rule: Always install dependencies in a separate layer before copying application source.
    target_file: skills/docker/SKILL.md

  - id: ERR-2026-021
    date: 2026-05-13
    category: deployment
    severity: high
    context: CI deploy script for a Node service. Agent omitted set -e.
    what_happened: npm install failed mid-run; script continued and uploaded a broken artifact.
    root_cause: Missing set -euo pipefail allowed the script to proceed past a fatal error.
    impact: Broken artifact deployed to staging; 45 min rollback.
    resolution: Added set -euo pipefail at the top; re-ran pipeline successfully.
    new_rule: Always begin shell scripts with set -euo pipefail to fail fast on errors.
    target_file: skills/shell-scripting/SKILL.md

  - id: ERR-2026-022
    date: 2026-05-13
    category: development
    severity: high
    context: SaaS app users table. Agent added email column without a UNIQUE constraint.
    what_happened: Concurrent registrations bypassed app check; duplicate email rows inserted.
    root_cause: Uniqueness enforced only in application code; concurrent writes race past the check.
    impact: Duplicate accounts; users locked out; manual DB cleanup required.
    resolution: Added UNIQUE constraint on users.email; backfilled duplicates before applying.
    new_rule: Always enforce uniqueness at the database level rather than relying on application-layer checks.
    target_file: skills/db-schema/SKILL.md

  - id: ERR-2026-023
    date: 2026-05-13
    category: git
    severity: high
    context: Self-extension workflow. Agent ran gh pr create without --label needs-rule-review.
    what_happened: PR created without required label; auto-approve CI gate skipped the PR.
    root_cause: Agent omitted --label flag; gh pr create silently succeeds without required labels.
    impact: Rule change stalled; CODEOWNERS approval gate never triggered.
    resolution: Closed and re-created PR with --label needs-rule-review; gate ran and approved.
    new_rule: Always include required labels when creating PRs for branches with automated gates.
    target_file: skills/github-cli/SKILL.md

  - id: ERR-2026-024
    date: 2026-05-13
    category: git
    severity: high
    context: Feature branch open 3 days. Agent merged without rebasing; regression fix had landed on main.
    what_happened: Merged without rebasing; branch was missing a regression fix from main.
    root_cause: Assumed CI green on branch meant safe to merge; did not check main for new commits.
    impact: Regression reintroduced to main; required hotfix and re-deploy.
    resolution: Rebased onto main, resolved conflicts, re-ran CI, then merged.
    new_rule: Always rebase onto the target branch before requesting merge to catch regressions.
    target_file: skills/branch-finishing/SKILL.md

  - id: ERR-2026-025
    date: 2026-05-13
    category: development
    severity: high
    context: FastAPI service pinning pydantic>=2.0. Agent wrote model using v1 Config syntax.
    what_happened: Model used class Config with orm_mode and .dict(); broke at runtime on Pydantic v2.
    root_cause: Agent defaulted to v1 patterns without checking the installed Pydantic version.
    impact: Runtime ValidationError on first request; service failed to start in CI.
    resolution: Rewrote model using model_config = ConfigDict(...) and model_dump(); tests passed.
    new_rule: Always use Pydantic v2 syntax (model_config, model_dump) unless the project explicitly pins Pydantic v1.
    target_file: skills/fastapi/SKILL.md

  - id: ERR-2026-026
    date: 2026-05-13
    category: development
    severity: high
    context: LangChain service. Agent wrote a new chain using LLMChain constructor.
    what_happened: Used LLMChain(llm=..., prompt=...) removed in LangChain v0.2+; chain failed at import.
    root_cause: Agent defaulted to pre-LCEL patterns without checking LangChain version.
    impact: ImportError at startup; chain unusable until rewritten.
    resolution: Rewrote chain using LCEL pipe syntax; tests passed.
    new_rule: Always use LCEL pipe operator syntax for new chains instead of deprecated constructor-based chain classes.
    target_file: skills/langchain/SKILL.md

  - id: ERR-2026-027
    date: 2026-05-13
    category: development
    severity: medium
    context: Agent added architecture diagram to repo by committing only the PNG export.
    what_happened: Committed architecture.png without the .drawio source; reviewers could not diff or edit.
    root_cause: Assumed the rendered image was sufficient; did not consider future editability.
    impact: Diagram uneditable without re-creating from scratch; review blocked.
    resolution: Added the .drawio source file alongside the PNG export.
    new_rule: Always commit diagram source files alongside or instead of rendered image exports.
    target_file: skills/drawio/SKILL.md

  - id: ERR-2026-028
    date: 2026-05-13
    category: development
    severity: medium
    context: Agent asked to design rate limiting for a REST API; immediately proposed one solution.
    what_happened: Committed to Redis token bucket without exploring alternatives.
    root_cause: Converged on the first plausible solution without a divergent generation phase.
    impact: Suboptimal architecture chosen; rework required after stakeholder review.
    resolution: Generated three alternatives, evaluated against criteria, selected the best fit.
    new_rule: Always generate at least three alternatives before committing to an approach.
    target_file: skills/brainstorming/SKILL.md

  - id: ERR-2026-029
    date: 2026-05-13
    category: development
    severity: medium
    context: Agent tasked with adding a new API endpoint; began writing code immediately.
    what_happened: Started implementing without listing affected files; missed updating the schema file.
    root_cause: No pre-implementation file touch list; scope not fully enumerated before coding.
    impact: Schema mismatch caused runtime error; additional debugging cycle required.
    resolution: Produced a file touch list first; identified the missing schema update before coding.
    new_rule: Always list all files that will be modified before beginning implementation.
    target_file: skills/implementation-plan/SKILL.md
```
