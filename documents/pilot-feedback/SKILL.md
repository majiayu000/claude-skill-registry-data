---
name: pilot-feedback
description: Capture and compound pilot-user feedback (good + negative) into a ledger; ingest a pilot's git branch for passive signal; report polarity+tag patterns for improvement routing.
triggers:
  - pilot feedback
  - user feedback
  - ingest rene
  - ingest dad branch
  - compounding feedback
---

# pilot-feedback

The compounding loop that turns real pilot-user usage (René today, Marcel next) into structured
improvement signal. **Both good and negative feedback are captured** — negative feedback is the
high-value ΔU/surprise signal (it points at what's broken/wrong/rejected); positive feedback
confirms what to keep + compound.

## When to invoke

- After fetching a pilot's branch (`git fetch`, review their recent commits) → `ingest-git`.
- When the operator says "good"/"bad" about a session/output/feature → `add` explicit.
- Periodically (or before a design pass) → `report` to see where the friction concentrates.

## The mechanism (capability: `pilot-feedback-capture`)

Script: `node _SYSTEM/Scripts/pilot-feedback.mjs <cmd>`
Ledger: `_SYSTEM/state/pilot-feedback.jsonl` (append-only JSONL via `_SYSTEM/lib/jsonl.mjs`).

| command | what it does |
|---|---|
| `add --pilot <name> --polarity good\|bad\|neutral [--source explicit\|commit\|session] [--tag <area>] [--note "..."]` | record one explicit feedback event |
| `ingest-git --pilot <name> --branch <ref> [--since 1d] [--author <name>]` | parse a pilot's branch commits; classify each subject → good/bad + tag; record signal-bearing ones (neutral skipped) |
| `report [--pilot <name>]` | aggregate by polarity + tag, print recent 5 |

### Tags (auto-classified)
`voice` · `file-io` · `safety` · `memory` · `launcher` · `persona` · `tool` · `automation` · `other`

### Polarity heuristic (commit subjects)
- **bad** = the prior state was wrong/rejected: `replac…/reject/broken/wrong/fix/rollback/revert/crash/hang/fail/missing/dead`
- **good** = addition/build/enable: `add/new/improve/ship/feature/enable/wire/scaffold/launch/builds`
- A commit with BOTH (e.g., "Kokoro replaces robotic SAPI") → **bad** (it's a rejection of the prior).

## How it compounds

1. **Capture** — `ingest-git` after every pilot fetch + `add` for in-session explicit feedback.
2. **Report** — before a design/build pass, run `report` to see where friction concentrates (high `bad` count in a tag = priority fix).
3. **Route** — negative feedback in a tag feeds the corresponding roadmap phase (e.g., `voice` bad-count → A0 voice quality; `memory` → A3 NEURO_CORE). Negative feedback = the ΔU/surprise that NEURO_CORE weights heavily (write_strength = |ΔU| × precision).
4. **Synthesize** (periodic, GLM lane) — a higher-level pass over the ledger produces improvement proposals → memory proposals → skill updates. (Future wiring; the deterministic `report` is the v1.)

## Worked example (2026-07-05, René's branch)

Manual review of `origin/rene` surfaced: robotic TTS rejected (bad/voice), PDF/Word/Excel text
extraction added (good→fix, bad/file-io on the prior raw-bytes), folder-scoped safety (good/safety),
local FTS5 second-brain (good/memory), one-word launcher (good/launcher). That manual review is
exactly what `ingest-git` automates:

```bash
node _SYSTEM/Scripts/pilot-feedback.mjs ingest-git --pilot rene --branch origin/rene --since 1d --author "René"
node _SYSTEM/Scripts/pilot-feedback.mjs report --pilot rene
```

## Session Notes
- 2026-07-05: built v1 (add + ingest-git + report + hermetic tests 5/5). Ledger at `_SYSTEM/state/pilot-feedback.jsonl`. Feeds A0–A5 priority via the negative-feedback signal. Next: GLM synthesis pass for cross-session pattern extraction.
