---
name: sci-experiment-manager
description: Manage experiment evidence for long-running academic research with stable E/F identifiers, frozen protocols, experiment and family cards, low-token indexes, raw-result provenance, synthesis, and safe generated outputs. Use when creating, updating, combining, indexing, retrieving, or closing experiments and diagnostic probes. Defer route-level continue/redirect/stop decisions to sci-research-manager and pure cross-artifact audits to sci-result-auditor.
---

# SCI Experiment Manager

Maintain the chain:

`validation requirement -> experiment/probe -> raw result -> interpretation -> typed handback`

Follow project-local instructions and the lifecycle/evidence rules in `sci-research-manager`.

## Retrieve evidence efficiently

Read the project's equivalents of:

1. `HANDOFF.md` or `PROJECT_HANDOFF.md`.
2. `QUERY_MAP.md`.
3. Experiment index/registry.
4. Relevant cards.
5. Raw files only for exact verification.

Do not globally scan runs, logs, results, or weights when an index can narrow the task.
Do not connect to remote hosts during a local/read-only audit unless the user explicitly requests remote verification; mark remote-only artifacts unavailable instead.

## Execute only within the requested scope

Discussion, known-paper intake, and a targeted literature check do not allocate experiment IDs or start remote work. Reuse an approved protocol and authorization while the action, target, and cost class remain unchanged. For a new method, changed information role, or costly expansion, have `sci-research-manager` integrate the nearest-prior comparison before proposal-specific preparation or execution; do not repeat it for ordinary approved runs.

Use the smallest protocol that can distinguish the live explanations. Prefer existing artifacts or a no-training check when informative; a small controlled training intervention may be justified when those cannot answer the question. Do not broaden a probe into a sweep, lower statistical standards, or promote exploratory evidence automatically.

## Track work on an SSH server

Use SSH to connect to a user-configured server only within existing authorization. Keep host addresses, usernames, credentials, local paths, and provider configuration outside portable skills and public artifacts.

Give a live task exactly one monitoring owner. Use a deterministic transfer/verification script when appropriate, and follow the waiting rules in `sci-research-manager`: retain the job ID or remote PID, command identity, output path, last progress, and completion marker; poll according to progress/ETA with backoff when event completion is unavailable. Do not delegate a second monitor or restart because a download is quiet.

A local SSH or terminal exit does not prove remote completion. Before restart, query the recorded remote identity; if missing, make a bounded lookup by expected user, command signature, and output path. Unresolved identity means potentially active. After authorized cancellation, verify that the remote job/process and its relevant open output handles are gone; retain partial files as incomplete. When another check cannot change a decision until an event/ETA, hand back the live identity and next eligible check instead of spinning indefinitely. Do not assume a particular notification tool or model is available.

## Preserve stable identifiers

- Use the project's established convention.
- Use `E001`, `E002`, ... for formal or standalone experiments when no convention exists.
- Use `F120` for a direction family and `F120-D01` for a diagnostic inside it.
- Never renumber historical records for appearance.
- Keep aliases and archived child IDs in the canonical family card.

## Freeze the protocol before execution

Record:

- question, hypothesis, competing explanation, and validation requirement;
- dataset/version, split, seeds, model/checkpoint, baseline, and controls;
- metric definition and aggregation;
- checkpoint/threshold/method-selection rule;
- config, command/run path, result path, and code commit;
- promotion gate, stop gate, and do-not-do-next.

Flag test-set selection, mixed protocols, missing seeds, or unverifiable paths. Do not promote unsafe evidence into a main claim.

## Use three record levels

### Single experiment card

Record one run, diagnostic, smoke test, or formal evidence item. Use [experiment_card_template.md](templates/experiment_card_template.md) when the project has no template.

### Direction family card

Summarize one research question across several probes: shared hypothesis, validation requirements, child table, synthesis, conflicts/confounds, blocked branches, proposed promotion/stop decision, do-not-repeat list, and raw links. Return the proposed decision to `sci-research-manager` for integration.

### Evidence synthesis

When several records support one conclusion, prefer one active synthesis linking the existing child cards. Do not create parallel plan/status/audit/handoff records for the same fact. Only archive or move cards within an authorized maintenance task; preserve IDs/raw evidence and record old path, new status, reason, and preservation proof.

## Interpret results conservatively

After each result, state separately:

1. `supports`;
2. `does_not_support`;
3. weakened/falsified assumption;
4. confounds and protocol warnings;
5. evidence status;
6. claim strength;
7. optional paper role or manuscript placement;
8. next decision and smallest justified validation.

Never infer metrics from filenames or conversation. Use `not available` or `needs_verification`.

## Maintain indexes with generated outputs

- Use `scripts/generate_experiment_card.py` to create a non-overwriting E/F card.
- Use `scripts/update_experiment_index.py` to generate reviewable Markdown and CSV indexes. Do not overwrite hand-edited indexes automatically.
- Use `scripts/collect_results.py` only when explicit result collection is needed. Review the generated table before treating it as evidence.
- Run scripts with `--help` and prefer explicit `--root`, directory, and output arguments in nonstandard projects.

After a run or interpretation changes, update only the bounded project chain in scope, preferably:

`raw result -> card -> project current-state index/query route`

For new projects, prefer an editable `EXPERIMENTS.tsv`; treat legacy `EXPERIMENT_INDEX.csv/.md` as the established authority or a generated view, never both. Return evidence status, claim-strength recommendation, selection warnings, and any proposed promotion/supersession to `sci-research-manager`. Do not write the shared canonical registry, claim map, or project handoff unless that owner explicitly includes the write in the handoff contract.

Use `sci-result-auditor` before paper promotion or when artifacts disagree.
