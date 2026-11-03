---
description: "Read eight offline session signals and record the observation through the canonical seed writer."
---

# /pulse

Read eight offline session signals and record the observation through the canonical seed
writer. Use when the user requests `/pulse`, a quick session health check, or a boundary
readout. The underlying stdlib script calls no model, network service or test suite.

## Arguments

- `$ARGUMENTS` — optional `--boundary`, `--topic`, `--source` or `--signals-file` options for
  `session-pulse.py`. Pass `--topic` only for a fleet topic, consistently to reader and writer.
- `--source` names the actual host: `claude`, `codex` or `chroxy`. Leave it unspecified when
  unknown. Never consult Claude's meter for Codex/chroxy; the Claude arm additionally
  requires the real `$CLAUDE_CODE_SESSION_ID`.

## Instructions

1. **Read, do not manufacture measurements.** The script reads the canonical seed and local
   git state. Tests and CI are cached STATE values, never fresh runs. Unknown measurements
   are `n/a`, including open counts and turns when no explicit cached count exists.
2. **Observe into a scratch snapshot.** Run the installed script, adding only appropriate
   arguments above. Show its eight lines verbatim:

   ```bash
   PULSE_SNAPSHOT=$(mktemp "${TMPDIR:-/tmp}/session-pulse.XXXXXX")
   python3 ~/.claude/scripts/session-pulse.py --snapshot-file "$PULSE_SNAPSHOT"
   ```

   Plain invocation is observational. `--snapshot-file` may write a scratch JSON file; it
   refuses seed names, aliases and the handoff directory. It does not write a seed. The
   reader always exits zero, including source, timeout and snapshot-output failures, so
   inspect the eight lines rather than treating the exit code as proof of persistence.
3. **Persist only with the real session identity.** When the host supplies the actual
   session ID, record the snapshot using the writer:

   ```bash
   python3 ~/.claude/scripts/session-seed.py write \
     --refresh-pulse "$PULSE_SNAPSHOT" --session "$ACTUAL_SESSION_ID"
   ```

   `ACTUAL_SESSION_ID` is supplied by the host, never guessed from a worktree, a seed or the
   newest transcript. A real Claude host may omit `--session` and use its harness-provided
   environment ID. If the ID is unavailable, keep this pulse observational and report that
   it was not saved. Pass the reader's same `--topic` when applicable. Do not hand-edit
   the seed, even for a snapshot. The writer preserves the existing date/body/decisions,
   archives an incumbent owned by a different session and runs fresh canonical proof.
   Missing or hollow legacy seeds remain unchanged when refresh refuses. Report REFUSE or
   snapshot-save failure honestly; never claim the baseline was stored without `seed:`.
4. **Act on the readout.** A WARN never stops authorized work. Invoke `/decide` for an actual
   pending choice, respecting owner-reserved authority. Run `/visual-brief` when a pulse
   delta crosses a WARN threshold or at package close. End the surrounding response with
   the fleet four-slot `**Status:**` block and one-task `**Next:**` sentence.

## Cached signals contract

`--signals-file` accepts only an explicitly supplied JSON object with `source` matching
`--source` and a full UTC `observed_at`. Optional `open_items`, `turns` and `compactions` are
nonnegative integers, never booleans. `context_pct` is a finite number from 0 to 100.
`estimate` and `actual` are finite nonnegative numbers supplied together with their common
nonempty `unit`. Keep their source and timestamp in the cached input; missing data stays
unknown. Do not estimate usage or context from spend, elapsed time or another host.

The eight lines cover scope; seed age and dispatch; HEAD/branch/tree/ahead/behind; commits
since seed/open items/turns; cached tests and CI; decisions count/age/default; usage/context/
compactions; and delta/WARN. Claude usage may come only from `usage-pace.py --oneline`.
All subprocesses share a 0.8-second deadline; unavailable sources degrade to `n/a`.

The readable Claude usage line remains the helper's bounded raw `--oneline` output.
Material comparison uses only supported printed measurements at that formatter's
precision: direct `sd`, `fh` and fable percentages; total or explicitly labelled subtotal
spend; fable spend; and derived capacity percentage/cap. Sample timestamps and ages,
reset countdowns, rates, burn, headroom and projected landings are excluded. Missing or
unrecognized measurements remain unknown. This small presentation signature reuses the
single bounded `--oneline` call; it neither recalculates accounting nor makes another
source call for a separate JSON report.

A missing previous snapshot says `no baseline`; unchanged material state says
`no material change since TIME`. Changed material fields are named. Decision recurrence
counts advance only when snapshots are persisted. Raw ages and recurrence counters do not
manufacture material changes, but stable threshold booleans make a newly crossed WARN
visible in delta and remain unchanged while the threshold remains crossed. WARN thresholds
are a repeated decision text across at least two recorded pulses,
more than three open items, a seed older than 24 hours, at least two compactions, a dirty
working tree at a boundary, or stated estimate drift above 25 percent. Legacy pending
DECISION prose warns with known age and unknown count until structured metadata is supplied.

## Seed metadata contract

The full writer accepts `--decisions-file` containing a JSON list of
`{"text":"Approve the proposed plan","opened_at":"2026-10-28T13:00:00Z","default":"Hold the proposed plan pending an answer"}`
objects; default omission is an empty list. Carry every unresolved choice and its original
`opened_at`. This default is a recommended plan, never reserved execution authority.
`--pulse-file` carries a snapshot in a full seed write. `--refresh-pulse` updates snapshot and
session metadata only, preserving date and body. Both flow through the same validation,
archive and proof path. `decisions` and `last_pulse` are single-line JSON flow values within
YAML frontmatter; conventional block-style YAML is outside this stdlib contract.
