---
name: personal-ai-data-governance
description: Use when designing, implementing, or reviewing personal AI data governance, seven-layer personal memory systems, four-layer MVP rollouts, local-first Markdown knowledge vaults, personal document conversion, privacy controls, backup and sync boundaries, Agent retrieval, or safe dependency setup across macOS, Linux, Windows, or WSL.
---

# Personal AI Data Governance

## Overview

Build a private, traceable, and reversible personal AI memory system from local files, authorized exports, and reviewed Markdown. Keep raw evidence, indexes, durable knowledge, situations, procedures, current state, and usage controls distinct.

Use the seven-layer model as the target architecture. Start with the four-layer MVP when a smaller rollout is safer and easier to verify.

Use this Skill only for one human owner and one private workspace. Exclude enterprise, family or household shared-vault, multi-owner, and shared-governance workflows. Treat minimized third-party data as content governed by the owner, never as another owner or a shared workspace.

## Core Principles

- Preserve originals and provenance; never replace evidence with an AI summary.
- Keep processing local-first and disclose every device, removable-media, sync, backup, and cloud boundary.
- Use `memory.md` as a routing index, not as a copy of source documents.
- Separate reviewed facts, lived situations, reusable procedures, current state, and usage controls.
- Prefer existing tools, operating-system capabilities, standard libraries, and zero-dependency paths.
- Require explicit authorization before creating, moving, converting, uploading, or deleting personal data.
- Require the human owner to review and explicitly approve each individual record before promoting it into durable L2 or `vault` storage.
- Never store passwords, API tokens, cookies, recovery codes, seed phrases, private keys, or complete authentication credentials in `memory.md` or the knowledge vault.
- Keep health, finance, and legal decisions human-only; organize information and evidence without making the decision.
- Minimize third-party personal data and retain only what the approved purpose requires.

## Seven-Layer Personal Memory Model

Map each artifact to one primary L0-L6 layer and link related layers instead of duplicating content:

| Layer | Define and store |
| --- | --- |
| L0 evidence | Preserve originals, authorized exports, scans, messages, and photos with source, date, version, or hash. |
| L1 index | Route questions through `memory.md`, keywords, prompt patterns, summaries, and paths without copying sensitive evidence. |
| L2 semantic | Store only facts, preferences, rules, and long-term knowledge that the human owner reviewed and approved individually, with evidence links and review status. |
| L3 situational | Record projects, decisions, learning, travel, life events, and retrospectives with time and context. |
| L4 procedural | Maintain Skills, SOPs, checklists, templates, and repeatable maintenance procedures. |
| L5 state | Track active projects, tasks, habits, risks, and unresolved items without treating them as durable facts. |
| L6 meta-memory | Record sensitivity, trust, version, expiry, device or cloud location, and sharing boundaries. |

Retrieve in this order: `L6 -> L1 -> L0 -> L2 -> L3 -> L4 -> L5`.

Check L6 first to decide whether data may be used and trusted. Use L1 to route, verify against L0, interpret reviewed L2 knowledge and relevant L3 context, select an L4 procedure, then reconcile the result with current L5 state. Report sources, versions, dates, and uncertainty.

## Workflow

1. Select one personal scenario and define its purpose, scope, success criteria, and prohibited actions.
2. Inventory only sources the user names or explicitly authorizes; do not scan a device, account, mailbox, photo library, or cloud drive automatically.
3. Classify sensitivity, third-party content, trust, expiry, location, sharing, and retention in L6 before processing.
4. Preserve or map originals into L0 and record source, date, version, and hash when practical.
5. Put conversions, drafts, progress, and errors in a separate work area; never overwrite L0.
6. Use sampling only to validate the pipeline; never use sample approval to authorize promotion of any unreviewed record.
7. Require the human owner to review and explicitly approve each individual record before promoting it into durable L2 or `vault` storage.
8. After the required review, promote approved knowledge to L2, situations to L3, procedures to L4, and current items to L5.
9. Update L1 with concise routes to evidence, knowledge, situations, procedures, and state.
10. Verify retrieval, provenance, permissions, backup recovery, and rollback before expanding scope.

Before processing a long task, assign a batch ID and create a reversible change log. Record every artifact that the batch creates or modifies. Rollback may remove or reverse only this batch's recorded `work/` outputs and changes; never alter `raw`, originals, or unrelated files. Before deleting any batch output during rollback or cleanup, show the owner the recorded list and obtain explicit approval.

### Required User-Facing Rollback Plan

Whenever proposing or executing a long task, the user-facing response MUST include a clearly labeled `Rollback Plan` section, or its exact localized equivalent, before execution starts. The user-facing rollback section must state the batch ID and change-log record. It must identify exactly which current-batch `work/` outputs may be reversed. It must state that `raw`, originals, and unrelated files remain protected. It must state that deleting any batch output requires displaying the recorded list and obtaining the owner's explicit approval.

For long tasks, report total items, processed items, successes, failures, skips, and skip reasons. Maintain an authorized error log. Apply a timeout to each item; record a timeout as a failure or skip and continue with later items instead of waiting indefinitely.

Minimize and redact progress and error logs; exclude secrets, extracted content, unrelated filenames, and full paths.

## Personal Data Domains

Enable only the domains needed for the approved pilot:

- Identity and administration: index identity documents, applications, contracts, policies, and life administration as highly sensitive by default.
- Work and projects: organize project files, meetings, deliverables, decisions, and retrospectives.
- Learning: organize courses, reading notes, research, questions, and reviewed knowledge cards.
- Finance: organize bills, invoices, budgets, and asset records without trading or making financial decisions.
- Health and life: organize reports, exercise, diet, care, and life records without replacing professional judgment.
- Communication and social: handle authorized email, chat, and contact exports while minimizing third-party data.
- Photos and media: preserve originals and add time, place, and manually confirmed identity metadata only when authorized.
- Devices, accounts, and backups: track inventories and recovery procedures without storing authentication secrets.

## Target Workspace

Use this full seven-layer target when its complexity is justified:

```text
personal-ai-memory/
  raw/          # L0 evidence
  index/        # L1 indexes, including memory.md
  vault/        # L2 reviewed durable knowledge
  cases/        # L3 situations and retrospectives
  skills/       # L4 procedures
  state/        # L5 active state
  governance/   # L6 trust, sensitivity, expiry, location, and sharing
```

Treat the tree as a reference architecture. Create or change it only after the user approves the exact paths and operations.

## Cross-Platform Environment Preflight

1. Identify macOS, Linux, native Windows, or WSL, plus architecture and the active shell.
2. Check for an existing capability before proposing software.
3. Prefer operating-system tools, Python standard-library features, and zero-dependency alternatives.
4. Run `scripts/bootstrap-posix.sh` on macOS, Linux, or WSL only to locate Python 3.10 or newer and render the next safe step.
5. Run `scripts/bootstrap-windows.ps1` on native Windows only to locate Python 3.10 or newer and render the next safe step.
6. Run `scripts/preflight.py check` only to detect the platform, command or module, and available installation method.
7. Treat WSL as a Linux boundary; never modify the Windows host, Windows PATH, registry, services, or execution policy silently.

Keep every preflight and bootstrap operation read-only. Never let these scripts download, install, execute a proposed installation command, change PATH, alter a registry or execution policy, or start a service.

Treat `python3`, `python`, and, on Windows, `py` as candidates only. Run the fixed read-only `--version` check, skip launchers older than Python 3.10 or launchers whose version check fails, and return only the first compatible launcher's actual path. Use that exact returned launcher for `scripts/preflight.py`; never guess or substitute another candidate. Reject displayed values containing Unicode Control, Format, Line Separator, or Paragraph Separator characters before echoing them.

Interpret exit codes consistently:

- `0`: the requested capability exists.
- `2`: required request data is missing or invalid.
- `20`: installation approval is required.
- `21`: the platform is unsupported or cannot be identified.
- `22`: the installation method or package manager cannot be identified.

## Mandatory Installation Gate

Before any download or installation, disclose exactly:

1. Current platform.
2. One named software dependency. Include package identity and source or publisher.
3. Purpose for the current task.
4. Project, user, or system installation scope.
5. Package manager or installation method. Include a pinned or reviewed version and a checksum or signature when available.
6. Every command that would run.
7. Any administrator, `sudo`, UAC, or other elevation requirement.
8. Network, disk, PATH, service, registry, execution-policy, and environment impacts.
9. A no-install alternative, or an explicit statement that none is available.

Before an installation proposal is approval-ready, disclose and review every ordered download, read-only dependency preview or resolution, installation, pre-install source-integrity verification, and post-install verification command or confirmed reliable non-command procedure. Do not output `INSTALL_APPROVAL_REQUIRED` when any required verification command, step, or confirmed reliable non-command procedure is unknown. Never invent a current version, command, checksum, signature, dependency list, or verification procedure to complete a proposal.

Verify source integrity before installation; post-install checks do not replace pre-install source verification. A package-manager command that may install undisclosed transitive dependencies is not approval-ready. Use a safe read-only dependency preview and disclose every package that would be installed, use a reviewed lockfile or bill of materials (BOM) that lists them, or use a verified no-dependencies mechanism. If none is available, fail closed and use the no-install alternative.

Disclose every package that will be installed; never claim that transitive dependencies will be handled later when the disclosed command could install them now. Keep one named direct dependency per proposal, and list every transitive package that its disclosed command would install within that same proposal. Treat read-only detection and dependency preview as non-installing steps; disclose any network access or other impact they have.

Provide structured proposal values for the software source or publisher, reviewed version, dependency-resolution mechanism, complete reviewed dependency inventory, ordered download steps, dependency-preview steps, pre-install integrity steps, installation commands, and post-install verification steps. Use `reviewed-read-only-preview`, `reviewed-lockfile-bom`, or `verified-no-dependencies` as the explicit resolution mechanism. Every package that the installation command may install must appear in the reviewed inventory; the no-dependencies mechanism still lists the named package. The scripts validate proposal structure only; the owner must verify the truth and evidence before approval.

For example, invoke the generic gate only with reviewed synthetic values shaped like this:

```sh
"$python_launcher" scripts/preflight.py check \
  --probe-type command --probe-value synthetic-converter \
  --software "Synthetic Converter" \
  --software-source-publisher "Reviewed local repository / Example Publisher" \
  --purpose "Convert the approved pilot files" \
  --scope "project environment" \
  --install-method "reviewed offline package" \
  --reviewed-version "1.0.0" \
  --dependency-resolution-mechanism reviewed-lockfile-bom \
  --dependency-inventory "synthetic-converter==1.0.0" \
  --download-step "retrieve the reviewed local artifact" \
  --dependency-preview-step "review the approved BOM" \
  --pre-install-integrity-step "verify the recorded artifact checksum" \
  --install-command "examplepkg install ./synthetic-converter-1.0.0.pkg" \
  --post-install-verification-step "examplepkg verify synthetic-converter==1.0.0" \
  --admin "no" \
  --impact "project files only; no service or PATH changes" \
  --alternative "use plain-text extraction"
```

Then output `INSTALL_APPROVAL_REQUIRED` and stop. Do not download, install, or run any disclosed command in the same step.

Handle one direct dependency at a time. Treat every approval as specific to the named software, commands, scope, platform, and privilege level. Never reuse an earlier approval for a newly discovered dependency, changed command, expanded scope, or privilege change.

Fail closed when approval is absent, ambiguous, refused, stale, or unavailable in a non-interactive run. Stop the chain after an installation or verification failure. Forbid unreviewed remote pipe installers such as `curl | sh`, `curl | bash`, or remote PowerShell expressions.

## Four-Layer Personal MVP

Use this as a rollout subset of the seven-layer target, not as a replacement for the full model:

```text
personal-pilot/
  raw/                 # MVP component 1; primary L0 evidence
  work/                # MVP component 1 staging; supports L0 processing
  memory.md            # MVP component 2; primary L1 routing
  vault/               # MVP component 3; primary L2 knowledge
  skills/              # MVP component 4; primary L4 procedures
  governance-lite.md   # Supporting L6 controls
  state-lite.md        # Supporting L5 state
```

- MVP component 1 - Evidence and staging (`raw/`, `work/`): map primarily to L0. Treat `work/` as temporary staging that supports L0 processing, not as durable L0 evidence.
- MVP component 2 - Routing index (`memory.md`): map primarily to L1.
- MVP component 3 - Reviewed durable knowledge (`vault/`): map primarily to L2.
- MVP component 4 - Repeatable procedures (`skills/`): map primarily to L4.

`governance-lite.md` supports L6 and `state-lite.md` supports L5; neither creates another MVP component. Defer L3 `cases/` and richer `index/` structures until the pilot proves the need.

Keep `raw` immutable, isolate `work`, route with `memory.md`, promote only individually reviewed and owner-approved knowledge to `vault`, and implement at least one repeatable procedure in `skills`.

## Approved Markdown Template

Use a personal record such as:

```markdown
---
id: personal-note-001
title: Example reviewed note
domain: learning
memory_layer: L2
source: raw/learning/example-source.pdf
source_date: 2026-07-01
version_or_hash: sha256:example-only
owner: self
reviewer: self
sensitivity: private
trust: reviewed
expiry: 2027-07-01
device_location: primary-mac
cloud_location: none
share_boundary: private-to-owner
status: active
tags: [example, reviewed]
---

# Summary

Record only the reviewed conclusion needed for retrieval.

## Evidence

- Link to the exact page, section, message, photo, or source version.

## Limits

- Record uncertainty, missing context, and prohibited uses.

## Related Memory

- Index: `memory.md`
- Situation: `cases/example-case.md`
- Procedure: `skills/example-review.md`
- State: `state-lite.md`
```

Replace example values with non-secret metadata. Keep sensitive evidence in its protected source location and store only the minimum routing data needed.

## Concrete memory.md Example

Use a concise personal index entry such as:

```markdown
# Personal Memory Index

## Renew a personal insurance policy

- keywords: renewal, policy, annual admin
- prompt_patterns: What evidence and steps are needed for the next renewal?
- owner: self
- reviewer: self
- sensitivity: restricted
- trust: reviewed-against-current-policy
- expiry: 2027-06-30
- device_location: encrypted-local-vault
- cloud_location: none
- share_boundary: private-to-owner
- evidence: `raw/identity-admin/policy-current.pdf`
- knowledge: `vault/identity-admin/policy-renewal-facts.md`
- procedure: `skills/review-policy-renewal.md`
- state: `state-lite.md#policy-renewal`
```

Keep the entry as a route. Do not copy identity numbers, account numbers, health details, credentials, or full document text into it.

## Backup And Sync Boundaries

Treat sync and backup as different controls: sync propagates current state and deletions, while backup preserves independent recovery history.

Document which paths sync, which paths back up, who controls each account, whether encryption applies, how long versions remain, and where an independent recovery copy exists. Test restoration from backup before relying on it. Do not describe a synced folder as a backup unless independent versioned recovery has been verified.

Perform a restore test only after explicit owner approval. Restore into a separate destination; never overwrite originals or the live workspace. Validate restored file counts and hashes before accepting the restore. Clean up restore-test output only after owner review and explicit approval.

## Risk Controls

- Never store passwords, API tokens, cookies, recovery codes, seed phrases, private keys, or complete authentication credentials in `memory.md` or the knowledge vault.
- Keep health, finance, and legal decisions human-only; require the owner or a qualified professional to make high-risk decisions.
- Minimize third-party names, messages, contact details, faces, and identifiers; retain only what the authorized purpose requires.
- Preserve raw evidence and require explicit authorization before any file creation, conversion, move, deletion, cleanup, or cloud upload.
- Never scan an entire device, account, mailbox, photo library, removable drive, or cloud service automatically.
- Treat an expired record as not current. Revalidate it or quarantine it; never delete it automatically solely because its expiry date passed.
- Minimize and redact progress and error logs; exclude secrets, extracted content, unrelated filenames, and full paths.
- Label OCR, extraction, transcription, and summaries with tool, time, confidence, and review status.
- Stop long-term memory promotion for suspected secrets; report only the risk category and a remediation path.
- Keep a reversible change log and verify counts, links, hashes, permissions, and recovery after each batch.

## Acceptance Checklist

- [ ] Map every artifact to one primary L0-L6 layer and preserve `L6 -> L1 -> L0 -> L2 -> L3 -> L4 -> L5` retrieval.
- [ ] Keep the full target and the four-layer rollout subset clearly distinct.
- [ ] Require owner review and explicit approval for each individual L2 or `vault` promotion; use sampling only to validate the pipeline.
- [ ] Verify originals, provenance, review status, links, versions, and rollback.
- [ ] Verify the personal owner, reviewer, sensitivity, trust, expiry, device, cloud, and sharing fields.
- [ ] Exclude credentials, unnecessary third-party data, and unsupported high-risk decisions.
- [ ] Keep preflight and bootstrap scripts read-only across macOS, Linux, Windows, and WSL.
- [ ] Apply all nine installation disclosures, including package provenance and version verification, output the marker, and stop before each dependency.
- [ ] Distinguish sync from independent backup and run any restore test in a separate destination with owner approval, hash and count validation, and reviewed cleanup.
- [ ] Revalidate or quarantine expired records without automatic deletion.
- [ ] Report long-task totals, processed, successes, failures, skips, reasons, error-log location, and timeout behavior.
- [ ] Confirm that no automatic scanning, deletion, cloud upload, or unapproved installation occurred.

## Recommended Pilot

Choose one low-risk, high-value domain such as a small learning project. Limit the pilot to a named source set, preserve originals, convert into `work`, and review a representative sample only to validate the pipeline. Review and explicitly approve each proposed durable note individually before promotion. Add one `memory.md` route and one Skill, record lightweight governance and state, and test retrieval plus backup recovery under the restore safeguards before expanding.

## References

Read `references/personal-ai-data-governance-guide.zh-CN.md` for the Chinese implementation manual, personal privacy classifications, backup and sync boundaries, cross-platform software selection, and installation examples.

Read that guide when implementing the MVP, selecting platform-specific software, classifying sensitive personal data, planning sync or backup, or preparing a concrete installation disclosure. Keep this Skill as the controlling behavior contract.
