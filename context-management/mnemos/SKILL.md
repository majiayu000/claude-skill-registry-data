---
name: mnemos
description: Task-scoped memory lifecycle — typed MnemoGraph prevents lossy context compaction by treating facts/decisions/code-refs/handoffs as distinct node types with per-type eviction policies
when-to-use: "When you need durable working memory across compactions — checkpoint decisions, preserve task handoffs, or audit what was remembered"
user-invocable: false
effort: high
---

# Mnemos — Task-Scoped Memory Lifecycle

## What It Does

Mnemos prevents lossy context compaction from destroying the structured knowledge you need most. It treats your working memory as a **typed graph** (MnemoGraph) where different types of knowledge have different eviction policies:

- **GoalNodes** and **ConstraintNodes** are NEVER evicted — they survive all compaction
- **ResultNodes** are compressed (summary kept) before eviction
- **ContextNodes** are evictable when their activation weight drops
- **CheckpointNodes** persist to disk for session resume

## Fatigue Model

Mnemos monitors 4 dimensions of "agent fatigue" — all passively observed from hook data, no manual input needed:

| Dimension | Weight | Signal Source | What It Measures |
|-----------|--------|--------------|-----------------|
| Token utilization | 0.40 | Statusline JSON | How full the context window is |
| Scope scatter | 0.25 | PreToolUse file paths | How many directories the agent is bouncing between |
| Re-read ratio | 0.20 | PreToolUse Read calls | How often the agent re-reads files it already read (context loss) |
| Error density | 0.15 | PostToolUse outcomes | What fraction of tool calls are failing (agent struggling) |

Fatigue states and actions:

| State | Score | Action |
|-------|-------|--------|
| FLOW | 0.0–0.4 | Normal operation |
| COMPRESS | 0.4–0.6 | Micro-consolidation runs (compress 3 ResultNodes, evict 1 cold ContextNode) |
| PRE-SLEEP | 0.6–0.75 | Checkpoint written, consolidation runs |
| REM | 0.75–0.9 | Emergency checkpoint, consider wrapping up |
| EMERGENCY | 0.9+ | Checkpoint written, hand off immediately |

## How To Use

### Automatic (hooks handle everything):
1. **Statusline** writes `fatigue.json` on every API call
2. **PreToolUse** hook reads fatigue before every edit, auto-checkpoints at 0.60+
3. **PreCompact** hook writes emergency checkpoint, compaction marker, a `compaction_fired` log line, and tells summarizer what to preserve
4. **SessionStart** (no matcher, so it fires on `startup`, `resume`, *and* `compact`) runs `mnemos-session-start.sh`, which loads the last checkpoint — this is the primary restore on all three sources
5. **PreToolUse fallback** (no matcher) detects the compaction marker on the first tool call and re-injects if SessionStart didn't fire
6. **Stop** hook writes final checkpoint for next session

### Post-Compaction Recovery (Three-Layer Defense):
When Claude Code compacts the context (~83% full), Mnemos uses three layers:
- **Layer 1 (PreCompact)**: Outputs strong preservation instructions with inline checkpoint content for the summarizer. Writes `.mnemos/just-compacted` marker and appends `compaction_fired` to `.mnemos/compaction-log.jsonl`.
- **Layer 2 (SessionStart, unmatched)**: **Primary re-injection.** `mnemos-session-start.sh` fires on every SessionStart source — including `compact` — and prints the checkpoint before the agent acts. It does *not* gate on source and does *not* consume the marker.
- **Layer 3 (PreToolUse fallback)**: `mnemos-post-compact-inject.sh` fires on the first tool call, consumes the marker, injects, and appends `restore_injected` (or `restore_missed_stale` if >5min elapsed). Safety net for the case where Layer 2's output was dropped, and the only layer that fires if the post-compaction turn is pure text with no tool call.

**Two known wrinkles, both benign:**
- Layer 2 doesn't consume the marker, so Layer 3 also fires on the next tool call. The checkpoint gets injected twice. Redundant, not harmful.
- There is no `mnemos-compact-recovery.sh` and no SessionStart `"compact"` matcher. Earlier docs described both; neither ever existed. Layer 2's role is played by the unmatched `mnemos-session-start.sh`. Coverage is intact — only the naming was wrong. (Corrected 2026-07-09.)

The result: after compaction, you'll see a restore block — `MNEMOS SESSION RESUME` (Layer 2) and/or `CONTEXT RESTORED AFTER COMPACTION` (Layer 3) — with your goal, constraints, what you were working on, and progress. Resume from there.

**What's actually been observed (2026-07-11, first-ever compaction, hand-run `/compact`):** Layer 2
delivered — goal, constraints, and a fresh checkpoint landed in post-compaction context, and the
summarizer honored the PreCompact preservation block. Layer 3 logged `restore_injected` and consumed
the marker, but its injected text was never *seen* reaching the model: the plumbing is confirmed, the
injection is not. Treat Layer 2 as the load-bearing one.

**RESOLVED, and it was never flaky (2026-07-24).** The reason Layer 3's injection "was never seen
reaching the model" is now known: `mnemos-post-compact-inject.sh` is a **PreToolUse** hook and it
emitted the restore block as **bare stdout**, which Claude Code routes to the debug log — NOT into
context (verified against `code.claude.com/docs/en/hooks`; only SessionStart/UserPromptSubmit add
bare stdout to context). Layer 2 delivered *because* it is a SessionStart hook. The asymmetry was
the channel, not the plumbing. Layer 3 now emits `hookSpecificOutput.additionalContext` and reaches
the model. **This retroactively taints the trial's Layer-3 evidence** — every prior "not seen"
observation was through a dropped channel (same shape as F-001: empty ≠ unused). P3's compaction
verdict must be re-formed with Layer 3 actually landing. Guarded by doccheck
`pretooluse-hooks-reach-the-model`; see `docs/observatory.md` → "PreToolUse hooks' bare stdout
never reached the model". The same bug silenced `mnemos-pre-edit.sh` (the fatigue/intent injection
below) for the whole trial — also fixed.

**Update (2026-07-16, supersedes the 07-15 reading below):** both gaps re-checked.
- **Fatigue is LIVE, not degraded.** `fatigue.json` carries real token metrics (`source: statusline`);
  `mnemos fatigue` computes all four dims — token-util 0.27 (wt 0.40), composite 0.11 FLOW. The 07-15
  all-`None` reading was **transient** (statusline JSON not received that session), not a real defect.
- **Compaction DOES fire here — without a `trigger`.** The 07-12 `trigger: unknown` event was a *non-manual*
  PreCompact firing (a `restore_injected` followed 23 s later), so the "harness never opens this door"
  read below was too strong. The harness fires PreCompact via its own summarization path, which sends no
  Claude Code `{trigger}` — hence `unknown`. An `auto` (context-full) event has still never been seen, and
  a ~200k overfill produced none, so P3 can't complete here. **DECISION: judge the compaction-recovery half
  on a real Claude Code CLI session; the fatigue half is judged here (it works).** PreCompact now logs a
  key-only `payload_probe` on `unknown` events to learn what the harness sends. **ANSWERED 2026-07-26:
  `{"len": 2, "keys": []}` — the harness sends an EMPTY payload (`{}`), no `trigger`, no `session_id`,
  nothing.** So `unknown` cannot be re-instrumented away; there is nothing to read. P3's ≥3 bar is
  **unreachable here, proven not assumed**, and P3 is snoozed 90d on that evidence with an *event*
  revisit trigger (a `payload_probe` showing any keys, or a real Claude Code CLI session). See
  `docs/observatory.md` → "Mnemos compaction vehicle".

**Original 07-15 reading (kept for the trail, now corrected above):** a session deliberately overfilled to
~200k tokens produced **zero** `compaction_fired` events, and `fatigue.json` read all-`None` (fatigue
*degraded*, token-util blind). Both were session-local artifacts, not standing defects.

### Is the compaction-recovery layer actually working?
`.mnemos/compaction-log.jsonl` is the durable record — the marker is deleted on
consumption and leaves no trace, and `checkpoints` has no trigger column, so this
file is the *only* evidence that compaction ever fired. Tally it with:

```bash
python3 -c "
import json,collections
c=collections.Counter((json.loads(l)['event'], json.loads(l).get('trigger','-')) for l in open('.mnemos/compaction-log.jsonl'))
print(dict(c))"
```

`compaction_fired` with no matching `restore_injected` means the recovery layer
is failing. Zero lines means compaction has never fired — which is *not* evidence
the layer is useless, only that it is untested.

**`trigger` is load-bearing, not decoration.** `auto` = context filled up: the real
event this layer exists for. `manual` = a hand-run `/compact`, i.e. a **test** of the
layer. A test is never evidence about the thing it tests. Without this split, three
deliberate test compactions would trip a verdict on data we manufactured. Compact by
hand as often as you like; it cannot contaminate the trial.

**BUT THE TRIAL WAS WATCHING THE WRONG EVENT (ADR-0015, 2026-07-26).** `tessera-watch`
P3 is no longer a compaction counter — it is `p3_restore_integrity`. The restore path
is **not compaction-specific**: `mnemos-session-start.sh` gates on nothing but the
checkpoint file existing, so it runs identically on `startup`, `resume`, and `compact`.

```
checkpoints 541 · sessions ingested 121 · compaction_fired ~3
```

**The mechanism did not run 3 times. It ran ~121.** Compaction is one *trigger* among
several — session end, crash, `/clear`, restart — for a mechanism whose job is recovery
across **any** context discontinuity. The old predicate counted ~2% of invocations and
reported the mechanism untested for 37 days. Not academic: the goal-blob defect fixed
that day (checkpoint joined every never-evict GoalNode → 11,119 chars → overflowed the
SessionStart output limit → the harness delivered a 2KB preview) was degrading **all
~121 restores**, and compaction found it by accident.

So when reading this file's compaction sections: they describe **one trigger**, not the
mechanism. Three questions now, with different evidence and venues —
**T1** deliverability (guarded by P3, mechanical, green today);
**T2** sufficiency, *does the agent resume without re-deriving* — **the real question. Its
instrument SHIPPED 2026-07-26** (`scripts/restore/`, `docs/contracts/restore-receipt.md`);
this line said UNBUILT until 2026-08-19, which was false for three weeks in the one copy
loaded into EVERY session. **No verdict is available yet, and the reason is now DATA, not a
missing instrument** — `tessera-watch` P16 owns that bar and reads 7/10 receipts across 2/3
downstream projects today. Do not adjudicate before P16 fires; tessera's own receipts do not
count toward it;
**T3** compaction frequency (blocked by the empty PreCompact payload, demoted to
informational). And note `restore_injected` is **a log line the hook writes about
itself** — the log shows four, the model received nothing on all four. Volume of
self-reports is not evidence.

### Manual CLI:
```bash
mnemos init                    # Initialize .mnemos/
mnemos status                  # Show node counts + fatigue
mnemos fatigue                 # Detailed fatigue breakdown
mnemos checkpoint --force      # Write checkpoint now
mnemos resume                  # Output checkpoint for context
mnemos consolidate             # Run micro-consolidation
mnemos nodes --type goal       # List active GoalNodes
mnemos add goal "Build auth"   # Add a GoalNode
mnemos bridge-icpg             # Import iCPG ReasonNodes
mnemos ingest-claude --all     # Ingest Claude Code transcripts (see below)
mnemos haze --recent 10        # Show per-session haziness scores
```

## Claude Transcript Ingestion & Haziness

Mnemos can ingest Claude Code session transcripts (the per-session JSONL under
`~/.claude/projects/`) and score each session's **haziness** — a measure of how
much the agent struggled. The `Stop` hook does this automatically on session
exit; it is also available manually.

**What's stored:** only structural fields (roles, tool names, file paths, error
flags, timestamps) plus a **redacted, 200-char preview** of each turn. Full
content is never persisted, and secrets (API keys, tokens, PEM blocks, JWTs,
credentials) are redacted before anything touches disk.

**Haziness** is a weighted score over five dimensions, each in `[0,1]`:

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| correction_density | 0.30 | User corrections per eligible user turn |
| redo_ratio | 0.25 | Edits re-touched after an error |
| first_try_error_rate | 0.20 | Edits followed by errors within 3 turns |
| orphan_tool_use_rate | 0.15 | Tool calls with no matching result |
| backtrack_norm | 0.10 | `git revert`/`reset --hard`/`restore` calls |

**A `≥` prefix and a `?` on the band mean the score is a FLOOR, not a measurement** (added
2026-07-26). `CorrectionDetector` runs on a 180s wall clock; past it every remaining turn
returns False, so those turns are **unmeasured and recorded as non-corrections**. 13 real
sessions detect at 2.94% against a 17.1% baseline on sessions where it finished. Since
`correction_density` carries the largest weight (0.30) and every unmeasured turn can only push
it *down*, the true haze is **≥** what is shown. **Never band-calibrate on a flagged session** —
this is P3's `unknown` lesson in another organ: a verdict must not rest on what the instrument
could not read. (`regex-only:*` is NOT flagged: a weaker detector over a *complete* pass is a
recall problem, not an incomplete measurement.)

The composite maps to a band: `clear` < 0.05 ≤ `cloudy` < 0.12 ≤ `hazy` < 0.20 ≤ `lost` —
re-anchored to the dogfood distribution's ~p50/p90/max on 2026-07-20 (P10 adjudication; the
original 0.25/0.50/0.75 labeled every session ever ingested 'clear'). Density caveat: measured
reads within ~±50% of true at current detector precision/recall (~0.4/~0.5, silver-label eval
`scripts/mnemos/eval_correction.py`) — treat as ordinal, not absolute.

**Correction detection + typing (spec 13).** `correction_density` counts user turns that push back on
the agent — caught by a keyword regex plus a recall-first local-qwen classifier over the turns the regex
misses (fails open to the regex; `qwen3:8b` + `think=false`, override via `MNEMOS_CORRECTION_MODEL`).
Each detected correction is then **typed** — `misunderstood / defied / overreached / wrong` — stored in
`claude_turns.correction_type`. **Typing is a diagnostic view, NOT a sixth dimension**: it never changes
the composite. See it with `mnemos haze --session <id> --explain` (a `CORRECTION TYPES` rollup + per-turn
`CORRECT:<type>` markers). `mnemos ingest-claude --reclassify --session <id>` re-runs both on history.

```bash
mnemos ingest-claude --all              # ingest every transcript + score
mnemos ingest-claude --session <id>     # one session by id
mnemos ingest-claude --transcript <f>   # a specific JSONL file
mnemos haze --recent 10                 # table of recent sessions
mnemos haze --session <id>              # per-dimension breakdown (+ --explain)
mnemos divergence --session <id>        # per-correction ASK→DID→CORRECTED triplets
mnemos divergence --recent 10           # flat by-type divergence rollup
```

**Action-divergence (spec 13 Phase 3).** Each detected correction is linked to the *action* it drew:
the nearest preceding human prompt (the ASK), the assistant work since it (files/tools, whether it
errored — the DID), and the correction with its Phase-2 type (CORRECTED). Pure structural derivation
over `claude_turns` — no new schema. `mnemos divergence --session <id>` shows the triplets;
`--recent N` a flat by-type rollup; `haze --session --explain` embeds a DIVERGENCE section. **View-only
— it does NOT feed the haziness composite** (P10 fired and was adjudicated 2026-07-20: weight
stays 0.30; any future detector change must re-run `eval_correction.py` and re-open bands/weight
on its numbers).
`--session` needs the FULL session uuid (same as `haze --session`).

Ingestion is idempotent (resumes via `last_line_offset`). **Opt out per project**
with `touch .mnemos/claude-log.disabled`.

**Every ingest leaves a trace** (added 2026-07-20, spec 16): `claude_sessions.classifier_status`
records how correction detection actually ran — `ran` / `regex-only:<reason>` /
`disabled-mid:consecutive-nulls` / `budget-exhausted`. `tessera-watch` **P11** diffs recent
transcripts on disk against ingested sessions (a crashed ingest writes nothing, so only that diff
can see it) and flags 3 consecutive regex-only ingests. This exists because the Stop-hook ingest
was silently dead 07-17→07-20 (console-script import bug, F-001's cousin) and nothing noticed.

## Agent Instructions

When working on a task:

1. **Create a GoalNode** at the start: `mnemos add goal "what you're trying to achieve" --task-id session-1`
2. **Add ConstraintNodes** for invariants: `mnemos add constraint "API backward compatibility" --scope src/api/`
3. **Check fatigue** before long operations: `mnemos fatigue`
4. **Checkpoint at sub-goal boundaries**: `mnemos checkpoint`
5. **On session resume**: the SessionStart hook automatically loads your checkpoint

## iCPG Integration

Mnemos bridges with iCPG (Intent-Augmented Code Property Graph):
- `mnemos bridge-icpg` imports active ReasonNodes as GoalNodes
- Postconditions/invariants become ConstraintNodes
- Checkpoint includes iCPG state (active intent, unresolved drift)

## Storage

Everything lives in `.mnemos/` (gitignored):
- `mnemo.db` — SQLite MnemoGraph
- `fatigue.json` — Live token metrics (updated per API call by statusline)
- `signals.jsonl` — Behavioral signal log (appended by PreToolUse + PostToolUse hooks)
- `checkpoint-latest.json` — Most recent checkpoint
- `checkpoints/` — Archived checkpoints
