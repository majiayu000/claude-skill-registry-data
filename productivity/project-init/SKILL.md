---
name: project-init
description: Bootstrap or reconcile the minimal project-control structure for an explicitly selected repository. Use for new-project initialization, existing-project reconciliation, or later control updates; route substantive work requests to spec-workflow.
license: MIT
---

# Project Init

Own repository-control bootstrap and reconciliation. Do not invent product
behavior, application architecture, code, dependencies, or implementation
tasks.

## Entry point

Use this skill when the user asks to initialize, bootstrap, reconcile, or
refresh project controls for an explicitly selected repository. Resolve the
exact target and classify it using safe metadata:

- `new/empty` — no entries;
- `new/git-only` — only `.git`; or
- `existing/reconciliation` — any other target, including incomplete projects,
  hidden files, symlinks, `.env`, and secret-looking names.

Empty and `.git`-only targets receive the same minimal bootstrap proposal.
Existing targets receive a reconciliation proposal based on inspected evidence.
Rerunning the skill is supported; reconcile only controls affected by actual
project evolution.

The bundled inspector and inventory are evidence only. They never authorize a
write, Git mutation, product decision, or application change.

## Responsibility and handoff

Project-init owns:

- safe target classification and repository inspection;
- the minimal project-control bootstrap; and
- progressive reconciliation of repository-wide routing and rules when the
  project actually gains a capability.

It does not own feature planning. For a feature, bug, improvement, refactor,
performance, security, migration, maintenance, or technical-debt request,
bootstrap or reconcile the controls first, then hand the work request to
`spec-workflow`. Do not create a SPEC, task list, implementation, or separate
execution document from project-init.

Use `product-discovery` or `brainstorming` for unresolved product direction,
`technical-design` for architecture/interface decisions,
`schema-design` for justified non-trivial persistence design, and
`implement-next` for an already selected SPEC task.

## Modes and approval

- **Light** — explain the relevant control changes without writing.
- **Standard** — reconcile selected controls in an existing project after
  inspection and approval for each write scope.
- **Strict** — bootstrap a new project or handle higher-risk reconciliation;
  show the exact target, proposal, approval scopes, and validation before
  writing.

Ambiguity resolves to Light. Escalate review for persistence, migrations,
public APIs, authentication, authorization, permissions, or source-of-truth
revisions. High-impact writes require an `Approving:` acknowledgement naming
the exact target, operation, and forbidden side effects.

## Default output contract

The minimal new-project control plane is:

```text
AGENTS.md
SESSION_STATE.md
.ai/memory/
docs/specs/
```

If `.gitignore` is missing, the helper may copy the bundled template after
approval. It protects environment files and local runtime state while keeping
`.ai/` trackable.

Project-init does not create `README.md`, roadmap files, schema documents,
user-flow documents, architecture documents, decision documents, plan
directories, review directories, rules, helper prompts, application files, or
framework files by default or through a compatibility shortcut. Conditional
project knowledge is created later only when the owning workflow shows that it
is justified.

Existing source, configuration, Git metadata, secrets, and useful project
documents are inspected safely and never overwritten by bootstrap. A separate
approved migration is required for any user-requested removal or revision.
If an existing project already uses `specifications/`, `specs/`, or
`docs/specifications/` as its SPEC source of truth, preserve that location and
pass it as an explicitly approved `--spec-dir` mapping to the bundled helper;
the helper refuses to guess an alternate source.

## Safety boundaries

Read [`references/workflow.md`](references/workflow.md) for the full inspect →
propose → approve → write → validate → handoff sequence. Always:

- resolve and show the exact canonical target before writing;
- inspect only safe metadata until a relevant document is approved for review;
- never read, copy, parse, print, or write `.env` contents, credentials, keys,
  browser state, or other secrets;
- preserve source code, configuration, symlinks, Git metadata, and existing
  project controls;
- obtain separate approval for missing-file creation, existing-file revision,
  and local `git init`; and
- never create commits, branches, remotes, pushes, deployments, or external
  mutations.

If a capability or approval is unavailable, stop without a partial write.

## Bundled helper boundaries

`inspect-project.sh` is read-only target/mode inspection.
`inventory-project.sh` is read-only safe filename evidence and classification.
`init-project.sh` is deterministic copy-if-missing scaffolding for the minimal
control plane. It may report and preserve existing files and symlinks, but it
does not choose a stack, create application files, inspect `.env` contents,
initialize a feature, install dependencies, or mutate remote state.
`validate-foundation.sh` validates only the minimal control plane after an
approved write. Use its matching `--spec-dir` mapping when an existing
project's approved SPEC source is not `docs/specs/`.

## Workflow

1. Resolve the exact target and run the read-only inspector. For an existing
   target, run the safe inventory as well.
2. Read applicable instructions, existing `SESSION_STATE.md`, and only the
   project-control evidence needed for the proposal. Never preload speculative
   documentation or open secrets.
3. Propose the smallest missing or affected controls. Treat frontend,
   persistence, authentication, public API, monorepo, deployment, background
   jobs, multiple deployables, and AI as reconciliation signals, not automatic
   reasons to create files. Ask whether each signal introduces durable
   repository-wide knowledge or routing that is not already represented
   clearly; if not, do nothing.
4. Show exact paths, ownership, evidence, assumptions, validation, and the
   approval scope. Wait for approval before writing.
5. Apply only the approved copy-if-missing or explicitly approved revision.
   Use `--init-git` only after separate approval for the exact target and
   `--allow-nested` only for an explicitly approved nested target.
6. Run `validate-foundation.sh`, inspect the diff, and report created,
   preserved, skipped, blocked, and unresolved items.
7. Hand substantive work to `spec-workflow`; do not create the work contract
   or tasks inside project-init.

## References

Load only the references needed by the active branch:

- [`workflow.md`](references/workflow.md) — target classification, approval,
  reconciliation, Git, validation, and handoff;
- [`existing-repository-safety.md`](references/existing-repository-safety.md) —
  preservation, legacy-artifact, secret, Git, and external-state boundaries;
- [`template-manifest.md`](references/template-manifest.md) and
  [`output-boundary.md`](references/output-boundary.md) — minimal outputs and
  forbidden application/external mutations;
- [`source-of-truth.md`](references/source-of-truth.md),
  [`reconciliation-report.md`](references/reconciliation-report.md), and
  [`reconciliation-population.md`](references/reconciliation-population.md) —
  evidence and safe existing-project proposals;
- [`conditional-documents.md`](references/conditional-documents.md) — optional
  architecture, ADR, shared-flow, schema-context, and engineering-rule
  templates;
- [`feature-lifecycle.md`](references/feature-lifecycle.md),
  [`traceability.md`](references/traceability.md), and
  [`technical-questionnaire.md`](references/technical-questionnaire.md) —
  SPEC lifecycle and conditional-document preparation;
- [`project-profiles.md`](references/project-profiles.md),
  [`technical-options.md`](references/technical-options.md), and
  [`prompt-contract.md`](references/prompt-contract.md) — optional concern,
  technical-option, and existing-project prompt guidance;
- [`init-compatibility.md`](references/init-compatibility.md),
  [`git-approval.md`](references/git-approval.md), and
  [`capability-matrix.md`](references/capability-matrix.md) — harness,
  prompt, Git, capability, and reload boundaries; and
- [`acceptance-scenarios.md`](references/acceptance-scenarios.md) — observable
  bootstrap and reconciliation evidence.

## Validation and handoff

Run the narrowest project-init tests first, then the repository validator and
diff checks. Structural checks do not prove live harness reload, application
runtime, browser, provider, deployment, or remote behavior. Report those paths
as untested unless they were actually exercised.

After an approved `AGENTS.md` change, show the exact diff and recommend a
fresh session or harness reload before relying on the new routing. Update
existing session state only through the `session-state` workflow and the
repository's state policy.
