---
name: ci-maintenance"
description: Design, implement, and audit repository CI pipelines and reusable workflow contracts against applicable fleet standards. Use for CI setup, workflow hardening, required-check coverage, or shared pipeline changes. Keep hook-only setup, isolated test diagnosis, and PR monitoring in their existing workflows.
---

# CI maintenance

Build CI around the repository's actual validation and delivery contract. Use its existing platform and tools. GitHub Actions guidance is available below, but a different provider is not a reason to migrate the repository.

For toolchain setup or local/CI drift, use [portable development environments](references/development-environments.md).
Prefer mise for pinned tools, devenv or devcontainers for portable setup, and
NixOS development VMs or system tests when OS behavior matters and the setup
improves reproducibility or onboarding. Share repository commands and version ownership
across environments; preserve working alternatives and verify the actual setup
path selected by CI. When changing environment examples, prefer `.env.spec` with
explicit consumer/validator support and native schema-backed fixtures as described
in that reference. Read [setup and runtime contracts](references/setup-contracts.md)
when changing precedence, bootstrap diagnostics, concurrent services, generated
examples, or secret-provider integration.

## Establish the applicable baseline

Read repository instructions, contributor and release guidance, native task targets, manifests and lockfiles, existing workflows, local/composite actions, and dependency automation. Inspect helper commands before running them. A check may download tools, start containers, access private configuration, or publish artifacts.

Separate four sources of evidence:

| Source | How to use it |
|---|---|
| Repository policy and platform settings | Determine required checks, supported runtimes, authority, and release boundaries. Read settings when available; do not claim them from YAML alone |
| Shared fleet workflows and standards | Inspect the selected revision, inputs, outputs, permissions, secrets contract, and caller compatibility |
| Maintained peer implementations | Find applicable patterns and native commands. Do not treat frequency or a newer-looking workflow as policy |
| Current primary platform/tool documentation | Verify event behavior, action compatibility, runner requirements, and dependency identities before changing them |

Use the established repository/remote inventory, not an assumed `origin` or a hardcoded local directory. Record which source revision was inspected and whether remote freshness is known. When documentation and committed implementations differ, inspect the controlling policy and actual caller before copying either. Ask only about consequential unresolved conflicts.

Prefer an existing shared workflow for genuinely common checks. Keep project-specific builds and release logic in the consumer. Calling a shared lint workflow does not prove its optional security audit is enabled. Inspect the input defaults and pass required policy switches explicitly. Do not copy tool versions or action SHAs from this skill.

## Design the check contract

Treat local commands and CI results as developer and automation interfaces. Verify a contributor can reach the first useful check from the documented setup, and that an unattended caller can invoke it without hidden prompts or diagnostics mixed into structured output. Read [experience and interfaces](../codebase-design/references/experience-and-interfaces.md) when changing command discovery, structured results, or recovery behavior. Measure setup and diagnostic friction when claiming a DX or agent-experience improvement.

For each relevant check, identify its event, tested revision, runner/runtime, command, required status name, permissions, prerequisites, and output. Compare that with the repository's required-check and release expectations.

Reuse existing Make/task/package commands for local and CI validation. Preserve lockfile-based installation, formatter configuration, and supported runtime floors. Document environmental differences, such as machine-specific installation checks that cannot run in hosted CI. Do not weaken a required gate to hide those differences.

When build or test output passes through formatters, `tee`, wrappers, or summary
steps, read [command status and diagnostic output](references/command-evidence.md).
Verify that a failing producer still fails the outer check. Keep build, test,
and application launch outcomes distinguishable.

Select checks by evidence: workflow syntax/security for workflow changes, build/test/type checks for the actual code, container lint for maintained Dockerfiles, secret scanning for the publication boundary, and generated-output or browser checks where those contracts exist. Use the configured security thresholds and suppressions after reviewing their justification. Avoid adding scanners that duplicate an existing service, such as a second code-scanning setup, without checking the current configuration.

For shared browser runners, apply [host capacity and cleanup](references/setup-contracts.md#browser-workload-ownership), including direct entrypoints and the outer task runner. Return status to the existing coordinator instead of launching a separate repair or delivery loop.

Keep commit-time checks bounded through [setup-pre-commit](../setup-pre-commit/SKILL.md). Expensive integration, platform, and browser checks can remain in CI. Shared scripts and global configuration changes must still reach their affected consumers when changed-file selection is used.

For GitHub Actions, read [events, trust, and required checks](references/github-actions.md) before changing triggers, permissions, reusable calls, caches, artifacts, or merge gates. For other providers, verify equivalent behavior in that provider's documentation rather than translating GitHub syntax mechanically.

For build and packaging matrices, prefer broad coverage of current stable/rolling platforms and current supported toolchains. Add legacy runtime lanes only for explicit user or repository compatibility requirements. Preserve existing support promises until deliberately migrated. Use [release-packaging](../release-packaging/SKILL.md) to select targets from language, build tooling, application type, and OS/ABI evidence; keep pipeline events and permissions here. Pin tested tool versions and monitor updates instead of confusing current-version preference with mutable CI inputs.

When commit, PR-title, or release checks are in scope, use [semantic conventions](../git-hygiene/references/semantic-conventions.md). Reuse the repository's parser and release rules. Validate PR titles on creation, title edits, and head updates as supported by the host. Match checks to the merge strategy and verify breaking markers survive squash. Treat titles as untrusted input and pass them as data, never interpolated shell code. A naming check does not require installing release automation or granting publication credentials.

## Implement a compatible change

For an audit-only request, report findings without editing workflows. Implement changes when authorized.

Preserve existing workflow names and required status identities unless their migration is part of the task. Inspect dependencies on those names in settings, badges, automation, and reusable callers. A workflow edit alone cannot update host rulesets.

Prefer full commit SHA pins for all external actions and reusable workflows, including first-party actions, with readable release comments. Prefer SHA-256 digests for CI container images and verify downloaded executable checksums where used. Apply the fleet's immutable-reference policy and verify the source repository, selected release/commit, and action runtime requirements. Local `./` action and workflow references remain tied to the checked-out or calling revision.

Pair immutable pins with Dependabot version-update monitoring for supported dependencies. Check `github-actions` coverage at directory `/` with a recurring schedule, plus the relevant ecosystems for images and tools. Inspect nested actions and script downloads for coverage gaps rather than assuming the workflow entry covers every dependency. Use [triage-dependency-updates](../triage-dependency-updates/SKILL.md#prefer-immutable-pins-with-update-monitoring) for monitoring evidence, unsupported formats, existing updater choices, and actual version candidates. Report configured coverage separately from observed successful update runs. A pin update does not justify unrelated runtime upgrades.

For shared workflow changes, inspect callers at their chosen refs. Treat required inputs, outputs, token permissions, secrets, runner labels, and check names as interfaces. Prefer compatible defaults or stage a documented migration. Validate a representative caller and track remaining consumers through [fleet shared fixes](../audit-repo-fleet/references/shared-fixes.md) when fleet implementation is in scope. Do not update every caller solely because its text matches.

Set bounded job timeouts. Choose concurrency groups that isolate independent branches and workflows. Cancel superseded validation when appropriate, but do not blindly cancel an in-progress release or data-changing job. Scope caches to the relevant runtime and dependency inputs, and keep private configuration out of cached directories and uploaded artifacts.

Editing workflow source is distinct from installing hooks, changing host settings, adding secrets, provisioning runners, dispatching jobs, publishing, or deploying. Carry existing authorization forward and keep any missing external action as a concrete remaining step.

## Verify and report

Run the repository's workflow syntax and security checks, such as its configured actionlint and zizmor entry points. Follow the shared policy for blocking thresholds and offline/online behavior. Linting YAML does not prove expression semantics, caller compatibility, shell behavior, or runner execution.

Run changed helper scripts and native checks in the intended runtime when permitted. For workflow changes, trace normal PR, fork PR, default-branch push, docs-only change, and enabled queue/manual/scheduled paths as applicable. Distinguish source walkthroughs from executed events. Local CI emulators are partial evidence and must not receive production credentials.

When host execution is authorized and available, verify the exact head or synthetic merge revision, selected checks, conclusions, and artifact identity. Report unavailable tools, skipped paths, and permission limits. Do not dispatch a release job to test syntax, mask failure with `continue-on-error`, or call a skipped security job a completed audit.

Use [systematic-debugging](../systematic-debugging/SKILL.md) for a reproducible failure before redesigning its pipeline. Use [sensitive-info-audit](../sensitive-info-audit/SKILL.md) for the bounded publication artifacts and history, keeping credentials and private runner details out of reports. Use [babysit](../babysit/SKILL.md) when the endpoint includes PR or release follow-through. Return to the current coordinator instead of starting a second delivery loop.

Report the applicable baseline, changed checks and interfaces, local/remote evidence, required settings or consumer work, and remaining limitations. During fleet-wide implementation, close confirmed shared matches through the fleet coordinator before declaring fleet completion.
