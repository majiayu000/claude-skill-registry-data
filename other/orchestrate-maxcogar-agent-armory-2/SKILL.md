---
name: orchestrate
description: Run the AgentBoard workspace pipeline across a board's cards — planning → review → implementation → audit waves with parallel subagents per card, server-driven verdict routing, and checkpoint pauses. Use ONLY when the user explicitly wants to run or continue the pipeline on a board that already has cards — e.g. "/orchestrate", "run the pipeline", "orchestrate the board". Do NOT trigger on general discussion of orchestration, or when no cards exist yet (create them via architecture or sweep first).
---

# Workspace Orchestration

Orchestrate parallel subagents through workspace board columns: planning → review → implementation → audit → finished.

**Source of truth and invocation.** This skill is the authoritative reference for the orchestrate workflow — wave logic, prompt templates, checkpoint policy, retry policy, build verification, and per-wave failure handling all live here. Run it directly as `/orchestrate` (optionally `/orchestrate --auto`). Before the first wave, load the `agentboard`, `codegraph`, and `rag` tool schemas via `ToolSearch` and call `agentboard_health_check`. The one flag is `--auto` — skip checkpoints where the board's blocking toggle is OFF (blocking ON always pauses; see Checkpoint Logic below).

## Prerequisites

- AgentBoard cloud reachable (call `agentboard_health_check` — AgentBoard is cloud-hosted, this is a reachability/auth check, not a local-process check)
- A workspace board with cards in `backlog` (created via `/architecture`, which itself depends on a spec from `/foundation`)
- An approved architecture document at `docs/arch/architecture-<spec-basename>.md` whose Card Slices section corresponds to the cards on this board. Note: the architecture pipeline has a correction loop, so the document a card's slice came from may have been revised since the cards were created — if cards predate the current architecture document, re-create them from the current Card Slices section before running this skill.
- MCP tools loaded: `agentboard`, `codegraph`, `codebase-rag`

## Pipeline Overview

```
Wave 1: Planning    → parallel agents build plans per card     → cards advance to review
Wave 2: Review      → parallel agents validate plans           → cards advance to implementation (or back to planning)
Wave 3: Implementation → parallel agents write code            → build/lint check → cards advance to audit
Wave 4: Audit       → parallel read-only agents verify         → cards advance to finished (or back to implementation)
```

Waves 2 and 4 each open with a **board-level cross-card consistency barrier** (see that section below) that holds all cards at once before the per-card agents run — catching inconsistencies *between* cards that the per-card waves cannot see.

Transitions are **server-enforced and verdict-driven** — agents and the orchestrator never move a card themselves. Both rejection loops route on the submitted artifact's `## Verdict:` heading:

```
backlog → planning → review → implementation → audit → finished
              ▲          │            ▲            │
              │  review  │ FAIL       │  audit     │ FAIL
              └──────────┘            └────────────┘
   review_note FAIL → planning     audit_report FAIL → implementation
```

## Cross-Card Consistency Barrier (Waves 2 and 4)

The per-card waves each see one card at a time. Nothing in them holds the whole board at once, so a class of failure is invisible to them: the cards drift out of consistency *with each other* even when each card is individually correct against its own plan and the architecture. The architecture's design-time review paired the *slices*, but plans and then code can each drift from the slices in locally-valid ways that are only globally inconsistent — orphaned or signature-skewed contracts between a producer card and a consumer card, incompatible edits to a shared allowed-touch file, realized dependency cycles, contracts the cards collectively dropped.

Two board-level cross-examiners close that gap. Each runs **once, as the opening action of its wave, before the per-card agents are spawned**:

| Wave | Cross-examiner | Cards held | Fails inconsistent cards by | Server routes them to |
|------|----------------|------------|-----------------------------|-----------------------|
| 2 (Review) | `cross-card-plan-reviewer` | every `plan` in `review` | submitting a `review_note` FAIL | `planning` |
| 4 (Audit) | `cross-card-implementation-auditor` | every `implementation_note` + diff in `audit` | submitting an `audit_report` FAIL | `implementation` |

**They fail cards themselves, then report.** Each cross-examiner runs first, holds the whole column at once, and for each card it finds cross-card-inconsistent it **submits the wave's FAIL verdict artifact on that card** (`review_note` / `audit_report` with `## Verdict: FAIL`). The server routes that card on the verdict exactly as it routes any failure — `review`→`planning`, `audit`→`implementation`. The cross-examiner does not move cards directly (no `update_workspace_card`); routing stays verdict-driven and server-enforced. Because the inconsistent cards leave the column before the per-card agents are spawned, **the per-card agents simply never run on them this round** — they run only on the cards the cross-examiner cleared. The cross-examiner then returns a summary message to you (the orchestrator).

Mechanically, per wave:

1. **Spawn the cross-examiner first** (background, single instance), passing: Wave 2 → `board_id`, `agent_id`, `arch_path`, and the `review`-column card IDs from Collect Cards; Wave 4 → `board_id`, `agent_id`, `repo_root`, `arch_path`, and the `audit`-column card IDs. Wait for it to return.
2. **Read its return summary.** It carries `## Cross-Card Consistency: PASS | INCONSISTENT` and lists the cards it **failed** (already routed back by the server via the FAIL it submitted), the cards it **escalated** (architecture change required — see step 4), and the cards it **cleared**. It has already submitted the FAIL verdicts before returning — you do not route those cards yourself.
3. **Spawn the per-card wave on the cleared cards only.** Re-query the wave's input column (`review` for Wave 2, `audit` for Wave 4) — the failed cards have already moved out — and spawn the per-card agents (Wave 2 → `review-agent` per card; Wave 4 → the two-phase audit per card) on the cards that remain. These are exactly the cards the cross-examiner cleared; they are evaluated on their own per-card merits.
4. **Architecture-change escalations.** A finding whose resolution is an architecture change (the contract surface itself is wrong, not either card's realization of it) is **not** failed by the cross-examiner — re-planning or re-implementing the card cannot fix it. The cross-examiner lists it under "Cards escalated" instead. Surface each escalation to the user — the same handoff the `/architecture` correction loop uses for its spec route — naming the contract and cards affected. Do not spin the card through its wave to the retry cap.

Retry accounting: a cross-card-triggered FAIL counts against the existing per-card retry cap (2) — a card the cross-examiner keeps failing on re-entry exhausts the cap like any repeated failure. Report the cross-examiner's verdict (failed / escalated / cleared counts) in your wave-status and checkpoint output so the human sees board-level consistency alongside per-card readiness.

## Checkpoint Logic

Read the board's `auto_transitions` to determine pausing:

| Board Setting | Default Behavior | With `--auto` Flag |
|---|---|---|
| `review_blocking: true` | PAUSE after Wave 1 | PAUSE (blocking always wins) |
| `review_blocking: false` | PAUSE after Wave 1 | Auto-proceed |
| `audit_blocking: true` | PAUSE after Wave 3 | PAUSE (blocking always wins) |
| `audit_blocking: false` | PAUSE after Wave 3 | Auto-proceed |

**Default is always pause.** The `--auto` flag only skips pauses when blocking is OFF.

## Running a Wave

For each wave, follow this pattern:

### 1. Collect Cards

Query cards by status matching the wave's input column:
- Wave 1 (Planning): cards in `backlog`
- Wave 2 (Review): cards in `review`
- Wave 3 (Implementation): cards in `implementation`
- Wave 4 (Audit): cards in `audit`

Use `mcp__agentboard__agentboard_list_workspace_cards` filtered by status. Always pass `limit=100` to prevent silent truncation on large boards — if the result count equals your limit, paginate with `offset` to retrieve the rest.

### 2. Spawn Parallel Subagents

**Waves 2 and 4 first run the Cross-Card Consistency Barrier** (see that section above): spawn the board-level cross-examiner, wait for it to fail the inconsistent cards (it submits the FAIL verdicts itself, routing them out of the column) and return its summary, then re-query the column and spawn the per-card agents below only on the cards that remain (the cleared ones). Waves 1 and 3 have no barrier — spawn the per-card agents directly.

Launch one Agent per card using `run_in_background: true`. Set `subagent_type` to the agent name for the wave. The agents carry their own system prompts, tool allowlists, and model assignments — the prompt only needs to pass the per-card variables.

| Wave | Phase | `subagent_type` |
|------|-------|-----------------|
| 1 — Planning | A (haiku) | `planning-research-agent` |
| 1 — Planning | B (opus) | `plan-compose-agent` |
| 2 — Review | — | `review-agent` |
| 3 — Implementation | — | `implementation-agent` |
| 4 — Audit | A (haiku) | `audit-research-agent` |
| 4 — Audit | B (opus) | `audit-compose-agent` |

**Phase A prompt (Waves 1 and 4):**

The research agents (`planning-research-agent`, `audit-research-agent`) fetch their own card data via `agentboard_get_card`; do not pass `card_title` in the prompt — those agents do not declare it as a declared input.

```
card_id: 7f3c...
board_id: a91e...
agent_id: claude-opus-4-6
arch_slice: <paste the card's section from `## Card Slices` in the arch doc — full slice with all eight §6.3 fields: Description / Allowed-touch list / Forbidden-touch list / Produces / Consumes / Verification scope / Depends on / Source decisions>   ← Wave 1 only
repo_root: /absolute/path/to/repo                                                                                                                                                            ← Wave 4 only
```

After Phase A completes for each card, capture the artifact ID returned by the research agent's `agentboard_submit_workspace_artifact` call — Phase B needs it as `facts_bundle_artifact_id` (Wave 1) or `audit_facts_bundle_artifact_id` (Wave 4).

**Phase B prompt (Waves 1 and 4):**

Before spawning Phase B agents, capture the Phase A artifact ID from each card:
- Call `agentboard_list_workspace_artifacts` for the card (or use the artifact ID the Phase A submission returned, if you captured it directly).
- Identify the artifact whose `artifact_type` is `FACTS_BUNDLE_V1` (Wave 1) or `AUDIT_FACTS_BUNDLE_V1` (Wave 4) and capture its artifact ID.

Pass the artifact ID to the compose agent — the compose agent fetches the bundle itself via `agentboard_get_workspace_artifact`. Never embed bundle JSON in the prompt; the orchestrator does not parse the bundle, and Phase B compose agents declare the artifact ID as a required input. For Wave 1, also pass the `arch_slice` so the compose agent does not need to re-extract it:

```
card_id: 7f3c...
board_id: a91e...
agent_id: claude-opus-4-6
card_title: Add pagination to workspace cards endpoint                    ← Phase B compose agents declare card_title as a declared input
arch_slice: <the same per-card slice passed to Phase A — full slice with all eight §6.3 fields: Description / Allowed-touch list / Forbidden-touch list / Produces / Consumes / Verification scope / Depends on / Source decisions>   ← Wave 1 only
facts_bundle_artifact_id: <uuid of the FACTS_BUNDLE_V1 artifact>          ← Wave 1 (use audit_facts_bundle_artifact_id on Wave 4)
```

If a Phase A artifact is missing for a card, skip Phase B for that card and report the failure — do not spawn a compose agent without a bundle artifact ID.

**Waves 2 and 3 prompt:**

```
card_id: 7f3c...
board_id: a91e...
agent_id: claude-opus-4-6
card_title: Add pagination to workspace cards endpoint
arch_path: /repo/docs/arch/2026-05-08-<topic>.md    ← review-agent only — full architecture doc, not just the slice
```

### 3. Wait for All Agents

All background agents must complete before proceeding. Report results:

```
## Wave [N] Complete: [Wave Name]
- Cards processed: [X]/[total]
- Passed: [N]
- Failed: [N] (list card titles)
- Time elapsed: [duration]
```

### 4. Handle Failures

**Review rejections (Wave 2):**
- The reviewer submits a `review_note` with `## Verdict: FAIL`; the **server auto-routes** the card back to `planning`. The orchestrator does NOT call `agentboard_update_workspace_card` to move the card — that path is deprecated.
- A `review_note` lacking the `## Verdict: PASS|FAIL` marker is rejected with HTTP 422 (`REVIEW_NOTE_MISSING_VERDICT`); the reviewer reads the `instructions_for_agents` field and resubmits with the marker (the app is not broken).
- Re-run Wave 1 for rejected cards only (max 2 retries per card)
- After 2 failures: report to user, do not retry

**Build/lint failure (after Wave 3):**
- Stop pipeline — do NOT proceed to Wave 4
- Report which files changed and likely culprit
- Wait for user intervention

**Audit failure (Wave 4):**
- The audit agent submits the `audit_report` with `## Verdict: FAIL` and does NOT move the card — the server routes on the verdict. A **FAIL routes the card to `implementation` unconditionally**, regardless of the `audit_blocking` setting. The orchestrator does NOT call `agentboard_update_workspace_card`; that path is deprecated.
- An `audit_report` lacking a valid `## Verdict:` heading (a level-2 heading with value `PASS` / `PASS WITH NOTES` / `FAIL` inline) is rejected with HTTP 422 (`AUDIT_REPORT_MISSING_VERDICT`); the audit agent reads `instructions_for_agents` and resubmits with the marker (the app is not broken).
- On a FAIL, re-run Wave 3 (Implementation) for the rejected card against the findings in the audit report. The audit report body carries the full rework context.
- A `## Verdict: PASS` or `PASS WITH NOTES` advances the card to `finished` only when `audit_blocking` is OFF; when ON, the card holds in `audit` for a human checkpoint — report the verdict to the user, who accepts (finish) or reworks (back to `implementation`).

### 5. Checkpoint (if applicable)

If this wave requires a pause (per checkpoint logic above):

```
## Checkpoint: [Wave Name] Complete

[Results table]

Proceed to [next wave]? (waiting for confirmation)
```

Wait for user confirmation before starting the next wave.

## Build Verification

After Wave 3 (Implementation), before Wave 4 (Audit), verify the project builds and lints. Build/lint commands are project-specific — do not hardcode `npm`, `cargo`, `pytest`, etc. into this skill. The `implementation-agent` runs build and lint as part of executing the plan and reports the result in its submitted `implementation_note` artifact; the orchestrator reads that artifact's build/lint status field instead of running build commands itself.

If the implementation-agent's submitted artifact reports a build or lint failure, stop the pipeline (do not advance to Wave 4) and report which files changed and the failing command output. Wait for user intervention.

When the build/lint command for the project is not obvious from `implementation-agent`'s context (e.g., a polyglot repo, an unfamiliar project shape), the orchestrator may inspect the repo root for build-system markers (`package.json` scripts, `pyproject.toml`/`setup.py`, `Cargo.toml`, `go.mod`, `Makefile`, `.claude-plugin/`) and pass a hint to `implementation-agent`; this is an inspection step, not a hardcoded command.

## Retry Policy

| Scenario | Action | Max Retries |
|---|---|---|
| Review rejects a plan (`review_note` FAIL) | Server routes card to `planning`; re-plan with feedback | 2 per card |
| Cross-card plan inconsistency (Wave 2 barrier) | `cross-card-plan-reviewer` submits a `review_note` FAIL on the card; server routes it to `planning` | 2 per card (shared with review) |
| Build fails | Stop, report to user | 0 (user intervenes) |
| Audit fails (`audit_report` FAIL) | Server routes card to `implementation`; re-run Wave 3 against the audit findings | 2 per card |
| Cross-card implementation skew (Wave 4 barrier) | `cross-card-implementation-auditor` submits an `audit_report` FAIL on the card; server routes it to `implementation` | 2 per card (shared with audit) |
| Cross-card finding needs an architecture change | Stop re-running the card; surface the contract/cards to the user | 0 (user intervenes) |
| Agent crashes/times out | Report, card unchanged | 1 |

## Status Reporting

Between waves (and at checkpoints), show:

```
## Orchestration Status — Board: [name]

| Column | Count |
|--------|-------|
| backlog | 0 |
| planning | 0 |
| review | 2 |
| implementation | 0 |
| audit | 3 |
| finished | 5 |

Progress: 5/10 cards finished (50%)
```

## Agents

All wave workers are dedicated agents defined in `agents/` at the plugin root:

The model column below shows each agent's `model:` frontmatter value verbatim. Workspace-pipeline agents use short aliases (`opus`, `sonnet`, `haiku`) to track ongoing model capability improvements; the hooks validate submitted artifact shape at runtime, so a model change that breaks output format is caught immediately. Architecture-pipeline agents pin specific versions for separate reasons that live in their own profile docs.

| Agent | Model | Role |
|-------|-------|------|
| `planning-research-agent` | `claude-haiku-4-5-20251001` | Wave 1 Phase A — codegraph/RAG discovery, emits `FACTS_BUNDLE_V1` |
| `plan-compose-agent` | `opus` | Wave 1 Phase B — fetches bundle by ID, writes plan artifact with full Expert Standard rigor |
| `cross-card-plan-reviewer` | `opus` | Wave 2 opening barrier — board-level; holds every plan in `review` at once, submits a `review_note` FAIL on each cross-card-inconsistent card (server routes it to `planning`), returns a summary to the orchestrator |
| `review-agent` | `opus` | Wave 2 — validates each cleared plan against constraints |
| `implementation-agent` | `sonnet` | Wave 3 — executes plans, writes code, runs build/lint |
| `cross-card-implementation-auditor` | `opus` | Wave 4 opening barrier — board-level; holds every implementation in `audit` at once, submits an `audit_report` FAIL on each card with realized-code interface skew (server routes it to `implementation`), returns a summary to the orchestrator |
| `audit-research-agent` | `claude-haiku-4-5-20251001` | Wave 4 Phase A — git diff + blast radius, emits `AUDIT_FACTS_BUNDLE_V1` |
| `audit-compose-agent` | `opus` | Wave 4 Phase B — fetches bundle by ID, writes audit report with a `## Verdict:` heading, then stops; the server routes on the verdict |

### Two-Phase Pipeline (Waves 1 and 4)

**Wave 1:**
1. Spawn `planning-research-agent` per card in parallel — runs RAG discovery then codegraph structural analysis, emits `FACTS_BUNDLE_V1` artifact
2. Wait for ALL Phase A agents to complete
3. Spawn `plan-compose-agent` per card in parallel — reads the bundle, writes the `plan` artifact (no discovery calls)

**Wave 4:**
0. **Barrier first:** spawn `cross-card-implementation-auditor` (board-level, single instance), wait, and read its return summary — see the Cross-Card Consistency Barrier section. It has already submitted `audit_report` FAILs on the cross-card-inconsistent cards, routing them to `implementation`; the cards remaining in `audit` are the ones it cleared. Steps 1–3 run on those remaining cards only.
1. Spawn `audit-research-agent` per (remaining) card in parallel — gathers git diff, blast radius, cross-references the plan artifact, emits `AUDIT_FACTS_BUNDLE_V1`
2. Wait for ALL Phase A agents to complete
3. Spawn `audit-compose-agent` per card in parallel — reads the bundle, writes the `audit_report` artifact with a mandatory `## Verdict:` heading; the server routes on the verdict (FAIL → `implementation` unconditionally; PASS / PASS WITH NOTES → `finished` when `audit_blocking` is OFF, else holds in `audit` for a human checkpoint).
