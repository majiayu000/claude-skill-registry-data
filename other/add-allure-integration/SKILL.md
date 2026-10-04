---
name: add-allure-integration
description: Add or adapt optional Allure reporting in a pytest hardware project. Use for local viewing, CI or server publication, integration with an existing Allure service, or help configuring Report Storage, a publisher, Test Runner, and hardware stands.
---

# Add Allure Integration

Implement the user's selected reporting workflow in the target project. Keep the integration
small and optional unless the user explicitly requires Allure for every run.

## Understand the project

Read the target repository's `AGENTS.md` and applicable nested instructions completely. Read
its README, reporting documentation, relevant architecture decisions, and active task record.
In this template, start with
[helpers/allure/README.md](../../helpers/allure/README.md). When installed separately, locate the
target project's equivalent documentation; do not assume this relative path exists.

Inspect Git status and diffs, dependency metadata, pytest configuration and plugins, artifact
creation, and relevant tests. Read Docker, CI, and runner-service documentation only when those
execution paths are relevant. Verify documented capabilities against code: an `allure` extra,
custom flag, shared run directory, or UI link may not exist yet.

## Select the workflow with the user

If the user has not selected a mode, ask which outcome they need, explaining the practical
differences briefly:

- Local viewing: collect results and open a report on the user's machine; no shared server.
- CI or server publication: generate reports and expose a URL for the team.
- Existing Allure system: integrate with the specified service, distinguishing Allure Report
  Storage, TestOps, and third-party services rather than assuming interchangeable APIs.

Reuse choices and authorization already given in the conversation. If the existing HTML report
meets the stated need, explain that option without overruling an explicit Allure request.

Ask follow-up questions only for missing information that changes implementation. For local
viewing, establish OS and native CLI versus container preferences. For publication, establish
the execution environment, existing CI/service, whether provisioning is requested, and whether
history or a Test Runner link is needed. Determine whether multiple modes must coexist and how
users should enable collection. Inspect discoverable configuration before asking about it.

For an existing service, obtain its type/version, endpoint, project identifier when required,
and the names or locations of runtime secret references. Do not request token values in chat.
Use environment variables or the project's secret store. Ask about network restrictions and
history grouping only when applicable. Continue independent inspection while awaiting answers;
do not invent required connection details or treat unanswered questions as approval.

## Guide configuration explicitly

When publication through a runner or hardware stand is selected, treat configuration as a distinct
deliverable rather than merely listing environment-variable names. Locate the tracked example files,
explain which untracked files the user must create, and help determine every non-secret value from
the actual deployment. Offer a copy-ready configuration block with secret placeholders, but never
write, print, request, or persist real token and password values.

Read the [publication configuration guide](references/configuration.md) when configuring Report
Storage, the disposable publisher, Test Runner, or a virtual/physical stand. It defines credential
roles, the non-obvious endpoint reachability rule, template file mapping, verification order, and
layered diagnostics. Use only the portions relevant to the selected deployment.

## Define the change

Check current official documentation for the selected adapter, generator major version, and
service. Verify compatibility with the project's Python and pytest versions. Keep adapter,
generator, and upload client responsibilities distinct; do not mix Allure 2 and 3 CLI syntax.
If documentation cannot be accessed, state what remains unverified and avoid guessing APIs.

Describe the chosen behavior, affected files, dependency placement, enable/disable mechanism,
artifact layout, and verification. Prefer the standard adapter options unless a project-specific
option removes a concrete usability problem. Satisfy the target AGENTS.md approval rules before
editing; in this template, changes affecting more than two files require architectural approval,
and test edits require approval of the main code changes. Reuse approval already granted for the
same scope. Create an architectural decision record only when the project's criteria warrant it.

## Implement the selected integration

- Follow existing dependency conventions. An optional extra fits optional collection; mandatory
  runtime reporting belongs in runtime dependencies. Update and verify the lockfile when needed.
- Keep ordinary runs usable without the adapter or generator when optional mode is selected.
  Avoid unconditional Allure imports in shared fixtures or tests that must collect without it.
- Keep raw results under artifacts in a unique directory per invocation. When sharing the
  project's run directory, configure the path before the adapter initializes. Never identify
  concurrent runs through a latest link or filesystem timing. Define conflicting path-option
  behavior and do not clean a directory that another run could be writing.
- Preserve JUnit, HTML, logs, and pytest's outcome. Generate or publish available results after
  failed tests as well as successful ones; report publication failures separately. Avoid putting
  commands after an unconditional shell exit or chaining them only to pytest success.
- Keep report generation outside device APIs and hardware connection lifecycle. Add structured
  steps or attachments only if requested; StepLogger logs are not automatically Allure steps.
- For local use, provide exact setup, generation, and viewing commands. For container use, pin
  tooling and mount the selected artifact directory; avoid adding a server to local-only setups.
- For publication, implement only the chosen destination and requested UI changes. Keep service
  credentials out of inventory, scenario data, tracked files, and logs. Account for captured
  output in attachments. Define history grouping and retention if history is requested.
- Preparing configuration does not authorize deployment or uploading real test data. Perform
  those actions only within the user's granted scope. If access is unavailable, finish the local
  integration and clearly identify the remaining live verification instead of claiming success.

## Verify and document

Follow the target project's test-edit approval requirements. Use focused non-hardware checks to
verify enabled and disabled collection, fresh result directories, and failed-test artifacts.
When generation or upload is implemented, check its failure behavior and preserve pytest status;
use fakes for external services. Validate the generated report with non-sensitive local results
when the required tooling is available. Never run hardware tests without explicit authorization
and a ready stand.

Run the required quality gate. In this template use `./scripts/ci.sh`; do not expand it into
separate commands except to diagnose failures. Update documentation with the actual installation,
enable/disable, viewing or publication commands, and runtime prerequisites. Update task records
according to repository rules. Report what works, what was verified, and any deployment or access
steps still outstanding. Complete the implementation rather than stopping at the proposed plan.
