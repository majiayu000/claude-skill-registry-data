---
name: ls-framework-compliance
description: "Pre-task workflow, certainty assessment, context load, document status, testing, Git checkpoints, document maintenance. Use for framework modifications, PRDs, or any task that must follow checklist and checkpoints."
metadata:
  version: "1.2"
---

# Framework Compliance

Use this skill when a task affects LocalSetup framework behavior, shipped skills, installer/runtime rules, repo documentation, PRDs, or any workflow where rule compliance and traceability matter.

## Pre-Task Flow

Before changing files:

1. Identify the task type: documentation, skill, framework code, installer, tests, git operation, PRD/queue work, or release workflow.
2. Load the active repo context from the repository instructions and the relevant documents under `ls/docs/`.
3. Run or request the context check when framework state is uncertain:

```bash
./ls/tools/verify_context
```

4. Check core constraints before acting: repo/data separation, user-owned worktree edits, secret/private state exclusion, platform compatibility, and required tests.
5. Assess certainty. If the active docs do not answer a core-rule question, pause for clarification before making a risky change.

## Current Sources Of Truth

Use active active sources only:

- Owning skills and workflow packages for operational behavior. Public docs carry `owner_skill` or `owner_package` frontmatter so agents know what to load.
- `ls/docs/AGENTIC_DESIGN_INDEX.md` for agent-facing design and workflow doc navigation.
- `ls/docs/WORKFLOW_REGISTRY.md` for named workflows and their triggers.
- `ls/docs/DOCUMENT_LIFECYCLE_MANAGEMENT.md` for document status meanings and ownership metadata.
- `ls/docs/SKILLS_AND_RULES.md` and `ls/docs/AGENT_SKILLS_COMPLIANCE.md` as public references for skill format and loading rules; `ls-skill-creator` and `ls-task-skill-matcher` own execution behavior.
- `ls/docs/REPO_AND_DATA_SEPARATION.md` as the public reference for framework source versus repo-local data boundaries; this skill owns the operational guardrail.
- `ls/docs/QUICKSTART.md` for supported verification commands.
- `ls/config/platforms.yaml` and `ls/docs/PLATFORM_REGISTRY.md` for supported platform paths.
- `ls/config/pack.yaml` for pack membership and `extensions.skill_taxonomy`; generated catalogs must not invent their own classification.

Do not reference removed removed draft helper files or indexes. In particular, do not call missing rule-enforcer or document-maintenance shell helpers, and do not rely on non-existent YAML document/rule indexes.

## Document Status Check

Before relying on a framework document:

1. Open the actual Markdown file under `ls/docs/`.
2. Read its YAML frontmatter.
3. Treat `status: ACTIVE` as current guidance.
4. Treat `status: PROPOSAL`, `DRAFT`, `DEPRECATED`, or `ARCHIVED` as non-authoritative unless the user explicitly asks you to work from it.
5. For active public framework docs, read `owner_skill` or `owner_package` and load that owner for operational rules before changing behavior.
6. If `status:` or ownership is missing, treat the document as uncertain and cross-check against an active index or ask before relying on it for core behavior.
7. When adding or materially changing a framework doc, include `status:`, `version:`, and the appropriate owner field.

The status meanings are defined in [DOCUMENT_LIFECYCLE_MANAGEMENT.md](../../docs/DOCUMENT_LIFECYCLE_MANAGEMENT.md).

## Implementation Guardrails

- Preserve unrelated work. If the worktree is dirty, identify your owned files and do not revert edits made by others.
- Keep framework source in `ls/`; do not put generated private state, local secrets, or machine-specific agent data into tracked files.
- For skill changes, keep `SKILL.md` Agent Skills compatible with `name` and `description` frontmatter, and keep auxiliary files scoped to the skill directory.
- Prefer the repo's active Python and shell tooling over ad hoc helpers.
- Use relative links for repo docs and verify they still resolve.
- For PRD or workflow queue work, update status/outcome fields only in the relevant active queue or PRD files.

## Verification

Choose checks based on the surface changed:

```bash
./ls/tools/verify_context
./ls/tools/verify_rules
uv run --locked python ls/tools/localsetup.py --source-root . validate-catalog
uv run --locked python ls/tools/localsetup.py --source-root . scan-migration
uv run --locked python ls/tools/localsetup.py --source-root . audit-global-first
uv run --locked ./ls/tests/automated_test.sh
workers="$(uv run --locked python ls/tools/localsetup.py --source-root . test-workers)"
uv run --locked pytest -n "$workers" ls/tests -q
git diff --check
```

- Run `verify_context` when validating that the framework context is present.
- Run `verify_rules` after framework or rule-related changes.
- Run `validate-catalog` after skill, catalog, platform, or registry changes.
- Run `validate-package-surface` after package materialization, deployed docs, resolver-token, workflow, or path-contract changes.
- Run `scan-migration` when migration, installer, adapter, generated-artifact, or source-boundary behavior may be affected.
- Run `audit-global-first` when global-first layout, lockfile, target-state, PowerShell removal, or source/target docs claims may be affected.
- Run focused tests and compliance checks for the code you changed before broad suites. Use the full pytest suite only as final consolidation for broad/shared runtime behavior, release/publish work, dependency changes, or explicit user requests. Resolve the permitted worker count with `localsetup test-workers`; [COMMAND_REFERENCE.md](../../docs/COMMAND_REFERENCE.md) owns its formula and aggregate-budget rule.

Unless a repository explicitly defines a stricter policy, every unit-test runner - regardless of language or framework - uses one aggregate concurrency budget of `max(1, floor(available CPU cores / 3))`. Round down before applying the minimum of one worker; concurrent test processes share the applicable aggregate cap. `localsetup test-workers` is the framework default proposal, not permission to exceed stricter active machine, client, or repository limits. Keep LocalSetup's portable `floor(cores/3)` default; do not hard-code a host-specific shared formula into the package.

For a serial illustrative pytest run, use `uv run --locked pytest -n 1 ls/tests -q`; use `localsetup test-workers` to query an appropriately bounded parallel run.

## Git And Handoff

- Shared, global, client, and repository authorization plus no-write boundaries govern execution. A workflow checkpoint does not grant commit authority.
- Create commits only when authorized by the active user instruction or standing authorization.
- Use Conventional Commit style for normal commits.

- Never stage broad unrelated work from a dirty worktree.
- In the final handoff, report changed files, checks run and results, and any residual risk or skipped checks.

## Proportional validation and evidence reuse

Run inexpensive checks and focused tests while editing. One successful full
suite for the final candidate is sufficient; authoritative CI may provide it.
Do not run another local suite or repeat a successful suite for the same tested
inputs just because a task moves from PR to main or publication. Record the
commit, environment, command/workflow, and result; invalidate evidence only when
relevant inputs change. Bound long jobs, preserve successful jobs when retrying
an understood failure, and stop automatic retries on an unexplained failure.
Complete source changes and the release record before generating final docs.

LocalSetup's hosted implementation uses eight isolated Python shards with an
all-shards success gate and exact-commit Actions evidence. The publishing workflow
checks that evidence before building instead of running the full suite again.
See [repository maintenance](../../docs/REPO_MAINTENANCE.md#validation-reuse).
