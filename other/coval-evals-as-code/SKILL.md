---
name: coval-evals-as-code
description: Maintain Coval evaluation configuration in a repository using Terraform. Use to adopt existing agents, suites, cases and metrics, add regression cases, review drift, or prepare isolated CI evaluations while preserving resource identity and run evidence.
---

# Maintain Coval evaluations as code

Make the customer's existing evaluation setup reproducible and maintainable.
Terraform owns configuration; the customer's runner or Agent SDK owns execution
and result collection. Keep their repository structure, authoring format and
transport unless the task calls for changing them.

## Find the source of truth

Inspect repository instructions, Terraform configuration/state ownership, provider
lockfile, case definitions, runner and CI. Confirm the intended organization,
workspace and API environment from supplied configuration and scoped readback.
A valid credential or successful CLI doctor check does not establish the tenant.
Use the public `/v1` API only; do not print credentials or inspect other tenants.

Inventory the full requested scope, including suites excluded by old allowlists,
development/held-out splits, existing IDs, criteria, personas and runtime fixtures.
Distinguish configuration resources from execution history and offline tests.
Do not convert an offline evaluator into a chat script if that loses its semantics.

Choose the authoritative writer for each resource. In a Terraform-managed project,
edit its declared source instead of silently using CLI/MCP/UI configuration writes.
Read APIs, run launches and result retrieval remain useful. If the customer uses
mixed ownership, document the boundary rather than migrating everything by default.

## Author a useful change

Keep cases in one reviewed source (existing JSON/YAML/HCL is fine) and derive
Terraform inputs from it. Do not maintain a second copy of scripts or expectations.
Use stable case keys and explicit suite/split identity; equal content in different
suites does not establish shared ownership. Record requirement/provenance, caller
input, separate expected behaviors, and the evidence needed to judge each behavior.

Use `build-test-suite` or `configure-metrics`, if installed, for coverage/rubric
design; their direct-create examples must respect the ownership choice above.
Retain held-out cases for explicit checkpoints, not iterative prompt tuning.
Declare fixture, permission, audio and tool-evidence requirements alongside cases;
adding a definition alone does not provide those capabilities.

For a new setup, adapt the [tested Terraform example](references/example.md).
For an existing setup, read [the lifecycle guide](references/lifecycle.md) and make
the smallest change in its conventions. Verify the pinned provider's schema before
inventing fields or copying old examples. Upgrade versions deliberately and keep
the dependency lockfile; a version shown here is a tested reference, not a mandate
to downgrade an existing project.

## Reconcile configuration deliberately

Prepare and inspect a plan before applying. Honor authority already given for
configuration changes; ask only for missing authority after the change is reviewable.
Creating configuration does not authorize paid runs or a production agent rollout.

- **Adopt:** match exact workspace, IDs and content; import existing resources to
  retain history. Name matches alone are insufficient. Reconcile differences before
  accepting an import-plus-update plan. Do not create duplicates on ambiguous retries.
- **Edit:** preserve stable addresses for ordinary serialized maintenance. If a PR
  changes shared fixtures while other runs use them, choose explicit isolation before
  applying: immutable versioned definitions or an independent candidate workspace.
- **Retry:** retain the same state owner, resource bindings and launch intent. Never
  switch an attempt from owned fixtures to a newly published shared binding midway.
- **Verify:** read back affected resources, compare content and IDs, then require a
  no-op plan. Unexpected updates, replacements or deletes need reconciliation, not
  deleted state, blanket `ignore_changes`, or removed destruction guards.

Serialize one shared state owner or use a remote backend with appropriate locking
and access control. A file lock does not coordinate separate CI machines. Every
concurrent candidate needs its own target registration/session and owned state;
never rotate another run's endpoint or credential. Share only immutable definitions
whose exact suite/split and complete definition fingerprint match.

State, saved plans, variable files and provider diagnostics can contain secrets,
even with `sensitive = true`. Keep them private and out of CI artifacts. Export only
allowlisted IDs, source/definition revisions and sanitized verdicts. Keep state
recoverable for retries; stopping processes does not require deleting resources
that explain historical runs.

## Execute and interpret separately

Use the existing runner and a concrete authorized budget. Pin the candidate source,
case/criteria fingerprint, metric version, target configuration, persona and fixture
version in a receipt before launch. On timeout, reconcile the saved intent and run
ID before retrying; do not blindly spend again. Keep the baseline explicit when
checking a fix and require it to reproduce the alleged failure.

Check required capabilities and read scopes before paid launch. Keep runner and
target credentials separate: a management key is not a substitute for the target's
scoped key. A missing fixture or actual API access denial is an incomplete test;
retain the raw result and investigate the intended access contract before blaming
the agent or environment. Do not infer HTTP errors solely from model dialogue.

Retrieve complete transcripts and individual criterion outputs, not just a summary
score. Reconcile planned, launched, completed, scored and untested counts. Inspect
contradictions between verdict and explanation. Side effects need independent
state/tool evidence; acoustic claims need audio. Preserve failures and disagreements
rather than redefining criteria until the run passes. Route judge calibration to
`coval-calibrate-metric` if available; never fabricate human labels.

For Agent SDK voice targets, the provider supports `MODEL_TYPE_SDK_WEBSOCKET` with
no customer endpoint. That registers configuration; the SDK still needs to start
and serve the intended candidate. Read the installed SDK version's public guidance.
A text-over-HTTPS check, mock-provider test or successful registration does not
qualify WebSocket audio execution. Keep target readiness, execution completion and
quality verdict distinct. Do not turn advisory coverage gaps into successful checks
or install a release-blocking gate without a validated, agreed policy.

## Leave a reviewable result

Report changed sources/resources, imported or retained IDs, plan/readback/no-op
results, run links and pinned revisions, actual coverage, and remaining gaps.
Separate configuration validation, live execution, agent quality and deployment.
Use the [lifecycle acceptance cases](references/lifecycle.md#acceptance-cases) when
introducing this workflow or changing its ownership model. Keep account-specific
receipts private; publish only fictional examples and generalized lessons.
