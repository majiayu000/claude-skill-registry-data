---
name: session-resume
description: Mid-run failure recovery for disease-market-sizing-orchestration. Inspects .cache/<slug>/ to determine which phase last completed and which phase to run next. Use when orchestration was interrupted and user wants to continue without restarting from phase 1.
license: Cite-or-Block strict (P0 iron law, see ../../CLAUDE.md)
---

# Session Resume (A12 · part 1)

Detects partial state of an interrupted disease-market-sizing-orchestration run by scanning the per-disease cache directory.

## Functions

`detect_partial_state(slug_dir: Path) -> PhaseState` — returns last_completed_phase + next_phase + reason.
`resume_from(slug_dir: Path) -> str` — human-readable resume message.

## Phase progress signals

| Phase complete | Signal in `.cache/<slug>/` |
|---|---|
| 1 (contract) | `contract.json` exists |
| 2 (staging) | `staging.json` exists |
| 3 (recall) | `sources/` non-empty |
| 4 (compose+audit) | both `citations_index.json` and `verification_report.json` exist with `verdict: "ok"` |
| 5 (bundle) | `output/delivery_manifest.json` exists |

## Usage

Always called by `disease-market-sizing-orchestration.run()` at the very start to decide whether to start fresh or continue from a partial run.
