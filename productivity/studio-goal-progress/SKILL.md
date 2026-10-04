---
name: studio-goal-progress
description: Use when a KIT-managed Codex or Hermes Goal needs evidence-backed percentage, ETA range, live read-only progress views, or portable append-only progress recovery.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: interactive
    lifecycle_stage: operate
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: progress.jsonl
    required_evidence: [goal-manifest, progress-events, reduced-state]
    owner: HoaTV Studio
    reviewer: null
    maturity: experimental
    last_reviewed: 2026-09-04
    provenance:
      derived_from: none
      patterns_from: [Codex App Server documented lifecycle events, AGENTS.md evidence labels]
      copied_text: none
---
# Studio Goal Progress

## Overview
Operate an explicitly opted-in KIT Goal from one portable append-only event stream. Percentage is verified weighted work; ETA is a separate range and confidence forecast. Compact and full GUI views read the same reduced state and never control the Goal.

## When to use
Use to preflight or initialize an explicit KIT-managed Goal, append a meaningful workflow event, recover current state from `progress.jsonl`, report verified percentage and ETA, or handle an operator request to `Open Progress`.

## When NOT to use
Do not use for arbitrary Codex tasks, packet planning, speculative progress, durable session transfer, or automatic dashboard opening. Route packet construction to `feature-to-work-packets` and durable transfer to `studio-handoff`.

## Required inputs and context discovery
Require an explicit Goal opt-in, one goal ID, repository root and snapshot, plan version, scope and do-not-touch paths, ordered packets, final verification requirements, and `max_active_timed_packets: 1`. Runtime bindings are optional; declared bindings must identify a Codex thread or Hermes session. Every packet requires `workflow_id`, owner, positive integer `progress_weight`, dependencies, completion criteria, evidence kinds, and may omit or null its low/high duration estimate.

## Safety and risk level
The helpers write only beneath the selected ignored goal root. Run `preflight` before `init`. Because `init` may launch a detached private writer runtime, obtain explicit service-start approval immediately before invoking it; Goal opt-in and a passing preflight are not approval. One writer appends validated events; workflows submit candidates instead of editing JSONL. GUI, context, and handoff consumers are read-only. Never expose raw logs, unrestricted paths, credentials, runtime keys, reusable session tokens, or mutation controls. Browser or panel opening separately requires an explicit `Open Progress` request.

## Workflow
1. Confirm explicit KIT Goal participation and run report-only `preflight` against the manifest and bounded goal root before initialization.
   Completion criterion: schema, root, snapshot, packet ownership, positive weights, dependencies, required evidence, any declared runtime bindings, and timing policy are valid; otherwise initialization is `BLOCKED`.
2. Immediately before `init`, obtain explicit approval to start or reuse the private writer service, then initialize one goal-local writer from the accepted preflight inputs. Do not open a GUI.
   Completion criterion: without immediate service-control approval initialization remains `BLOCKED`; with approval, `goal.started` is accepted into `progress.jsonl`, reduced state is reproducible, and the Goal remains separate from other local sessions.
3. Submit candidate events only at meaningful boundaries: Goal start, packet transition, evidence observation, plan revision, context refresh, terminal state, or an explicitly bounded heartbeat for a long operation.
   Completion criterion: ordinary commentary, elapsed wall time, raw tool output, and optional runtime observations never become completion evidence.
4. Reduce the full append-only stream and calculate percentage from verified weight divided by active planned weight. Recalculate on approved plan revision without changing retained verified weight.
   Completion criterion: packet verification cites accepted matching `Verified` evidence, incomplete Goals display below 100%, and replay restores current state.
5. Calculate ETA as a low/high seconds range with basis, calibration, confidence, and warnings. Missing estimates return `Calculating...`; `waiting_input`, `blocked`, or stale state pauses ETA; unsupported parallel timing is `BLOCKED`.
   Completion criterion: ETA remains forecast rather than evidence and no inactive time or commentary implies completion.
6. On `Open Progress`, accept an explicit goal root, or first resolve one unique nonterminal Goal from the caller's declared manifest runtime binding before repository-level ambiguity fallback. Reuse a healthy authenticated dashboard runtime without new service approval. Starting a stopped or missing runtime requires immediate explicit service-control approval. Python returns one one-time localhost URL and separate server, panel, and browser statuses; it never invokes UI or browser APIs. After URL generation, the host agent uses its panel tool when available, otherwise instructs the operator to open the URL manually.
   Completion criterion: one top-level one-time URL, host-panel instruction, manual-browser instruction, and independent integration statuses are returned without reusable credentials; ambiguous selection, missing service approval, failed server start, unavailable panel/browser, or unavailable App Server is labeled `BLOCKED` while portable progress remains usable.
7. At terminal completion, require every active packet and every final verification requirement to have accepted matching evidence, then return a final evidence card.
   Completion criterion: the card records goal ID, plan version, verified percentage, ETA status, event and reduced-state artifacts, commands and exit codes, integration limitations, evidence labels, final verdict, and next action.

## Evidence and output contract
Treat `progress.jsonl` as sole canonical recovery authority; `goal.json`, `state.json`, context files, runtime descriptors, and GUI output are derived. Report Goal state, verified and planned weights, exact percentage, display percentage, ETA status/range/confidence, current packet, latest evidence, next action, staleness, warnings, integration status, and artifact paths. Missing authority or evidence is `BLOCKED`, never simulated `PASS`.

## Handoff contract
Record goal root, manifest hash, plan version, last accepted sequence, current packet, verified weights, ETA status, relevant commands, integration blockers, and next action. Use `studio-handoff` for durable cross-session transfer.

## Pitfalls and anti-rationalization
- “Work feels almost done” is not verified weight.
- “It has run for an hour” is not percentage or evidence.
- Missing packet weights do not justify equal-weight defaults.
- App Server failure does not invalidate the portable KIT stream, but enrichment remains `BLOCKED`.
- Goal opt-in and preflight do not authorize `init`; service approval is required immediately before that command.
- `Open Progress` never invokes a panel or browser from Python. It reuses a healthy runtime, and starts a missing runtime only with immediate explicit service-control approval; neither path authorizes Goal mutation or reusable token disclosure.

## Verification checklist
- [ ] Explicit Goal opt-in and preflight preceded initialization, with separate service approval immediately before `init`.
- [ ] Packets have positive weights and matching evidence requirements.
- [ ] Only meaningful-boundary events were submitted through one writer.
- [ ] Percentage comes only from verified active weight.
- [ ] ETA is a labeled range or honest Calculating, Paused, or BLOCKED state.
- [ ] GUI opening was manual and views remain read-only.
- [ ] Final evidence card separates Verified, Snapshot, Unverified, and BLOCKED facts.

## References and scripts
Load [commands and interpretation](references/commands.md) before running helpers. The standalone skill bundles `scripts/goal_progress.py`, `scripts/goal_progress_core.py`, `scripts/goal_progress_store.py`, `scripts/goal_progress_server.py`, and `scripts/goal_progress_app_server.py` together with the Goal manifest, event, state, and context projection schemas.
