---
name: forge-snapshot
description: Regenerates FORGE_SNAPSHOT.md from real project sources so no session loses the mission across compaction. Use on /forge snapshot or let PreCompact/SessionStart hooks trigger it.
---

# Forge playbook — Snapshot (context-continuity snapshot system)

**Self-improvement substrate (wp-skill-evals, 2026-07-31):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction (an owner fix, a false assumption caught, a preference stated), append it to
`learnings.md` with a date and real evidence — never invent a lesson that didn't happen.

**Owner request (2026-07-29):** "bij elke 50% context een snapshot.md zodat er geen memory wordt vergeten…
en dan een uitgebreid rapport zodat de agents nog weten wat we maken — dit geldt ook voor globaal." There is
**no context-percentage available to a hook** (a closed Claude Code feature request — the only percentage
lives in the separate statusline channel, `context_window.used_percentage`, which no hook can read). This
system never fabricates or estimates one. Instead it fires on the real, honest signals: a **PreCompact**
hook (the genuine "context is about to be compacted" event), a phase boundary, or an explicit manual call.

## What it does

1. **`forge-bin/forge-snapshot.cjs`** — the generator. `write([--run <id>] [--reason ...])` regenerates
   `.claude/FORGE_SNAPSHOT.md` from real sources: `FORGE_MEMORY.md`'s latest status block, `FORGE_TASK_HISTORY.md`'s
   latest entry, `tasks/WORK_PACKAGES.md`'s latest mission block, `FORGE_DECISIONS.md`'s most recent rows, the
   newest run's `events.jsonl` (done/in-progress buckets, each with a real evidence pointer), `command-center/mission/TODO_GRAPH.md`
   or `WORK_PACKAGES.md`'s WP-ID/Status lines (open items), `git log`/branch/dirty state, `FORGE_VERSION.json`,
   and the newest `forge-runs/*/doctor.json`. Ten fixed sections: Mission · Why · Current state · Key decisions
   · Active constraints · Key file paths · Known gaps/limitations · Next actions · Evidence pointers · Honesty
   footer. `check([--max-age-hours N])` is a read-only staleness probe (for the doctor or a manual check).
2. **`forge-bin/forge-snapshot-marker.cjs`** — the **PreCompact** hook target (matchers `manual`+`auto`).
   Writes `.claude/.forge-snapshot-due.json` and immediately calls `forge-snapshot.cjs`'s `write()` so a real
   skeleton exists even if the session ends before the next step runs. Never blocks compaction (always exits
   0), never prints anything to stdout, never prints a secret.
3. **`forge-bin/forge-snapshot-reinject.cjs`** — the **SessionStart** hook target, matcher `compact`. If the
   due-marker exists, prints a short (<= ~600 tokens) block — Mission + Current state + Next actions + an
   explicit instruction to refresh sections 3-9 — to **stdout**, which Claude Code re-injects directly into
   context (the one official re-injection point this whole system relies on). Then deletes the marker. No
   marker -> prints nothing, exits 0.
4. **`forge-bin/forge-snapshot-settings.cjs`** — the one-time, idempotent `.claude/settings.json` MERGE
   helper used to wire the two hooks above without ever clobbering pre-existing hooks/keys (`apply --target
   <path> --marker-command "<cmd>" --reinject-command "<cmd>" [--backup]`).

## Anti-drift (the core design decision)

- **Section 3 ("Current state") is ALWAYS re-derived fresh from source-of-truth** on every regeneration —
  never patched forward from a previous snapshot. Changing `events.jsonl` or `TODO_GRAPH.md` between two
  `write()` calls changes the output; nothing is ever carried over except what section-1 explicitly
  preserves.
- **Section 1 ("Mission") is the one deliberate exception — preserved VERBATIM** across regenerations. It is
  read from an existing `<!-- MISSION:BEGIN -->...<!-- MISSION:END -->` marker if the current
  `FORGE_SNAPSHOT.md` already has one; else migrated verbatim from a pre-existing hand-written snapshot's own
  first `## ` section (a one-time migration path so a hand-authored stopgap's mission survives the switch to
  this tool); else derived from `FORGE_MEMORY.md`'s latest status heading; else an honest, clearly-marked
  TODO for a human/agent to fill in — never guessed prose.

## Size discipline

Target <= ~2000 tokens of prose (chars/4 heuristic — approximate, not a real tokenizer, and reported honestly
as `approxTokens` rather than presented as exact). Long things are **paths**, never inlined. Every generated
section (2..9 — Mission is exempt) that would exceed its own character budget is cut with an explicit
`"(truncated — see <path>)"` marker rather than growing unbounded.

## Honesty

Every generated claim carries a real evidence pointer (a relative path, optionally with an event type/heading)
or is explicitly marked in the Honesty footer's "unknown/missing" list — never a bare, unattributed assertion.
**No context-window percentage is ever fabricated or estimated anywhere in this system.**

## Wiring (opt-in, already applied 2026-07-29 — see `HOOKS_OPT_IN.md` for the live record)

- **Project-local** `.claude/settings.json`: PreCompact (matchers `manual`+`auto`) -> `forge-snapshot-marker.cjs`;
  SessionStart (matcher `compact`) -> `forge-snapshot-reinject.cjs`.
- **Global** `~/.claude/settings.json`: the same two events, appended alongside the 2 pre-existing global
  hooks (hotspot-lock, secret-scrub) and every other pre-existing entry — proven preserved byte-for-byte by
  `forge-snapshot-settings.test.cjs`'s load-bearing safety suite. The global hook commands point at the
  GLOBAL minimal mirror (`~/.claude/forge-bin/forge-snapshot-{marker,reinject}.cjs`), which resolves the
  target project's root from `CLAUDE_PROJECT_DIR` (or cwd) and dynamically requires **that project's own**
  `.claude/forge-bin/forge-snapshot.cjs` — a project with no Forge install degrades silently (no output, exit
  0).

## When to use

- Automatically: the wired PreCompact/SessionStart(compact) hooks fire on a real compaction.
- Manually: `/forge snapshot` (phase boundary, or whenever the owner wants a fresh, evidenced snapshot without
  waiting for a compaction) -> `node .claude/forge-bin/forge-snapshot.cjs write --reason phase`.
- Suggest `/compact` with a short focus note at a logical boundary (a phase just finished, or before an unrelated task) — around 60% context use — never in the middle of a task.
- `node .claude/forge-bin/forge-snapshot.cjs check --max-age-hours 24` to probe staleness (e.g. from a doctor
  pass or before a long unattended run).

## Skills / commands

`forge-bin/forge-snapshot.cjs` (`write`/`check`), `forge-bin/forge-snapshot-marker.cjs` (PreCompact target),
`forge-bin/forge-snapshot-reinject.cjs` (SessionStart target), `forge-bin/forge-snapshot-settings.cjs`
(settings.json merge helper), `.claude/FORGE_SNAPSHOT.md` (the generated artifact — never hand-edit sections
2-10; edit only the text between the MISSION markers to change the Mission), `.claude/.forge-snapshot-due.json`
(transient marker, deleted on consumption).

## Fan-out & flow

**1 agent, no team.** This is a deterministic, zero-dependency CLI + two small hook targets — not a
multi-agent task. Any Boss doing build/fix work can call `write --reason phase` directly at a natural
checkpoint.

## Ship-readiness (unique)

Never fabricates a context percentage; never blocks compaction/session-start (both hook targets always exit
0); never prints a secret (FORGE_SNAPSHOT.md only ever holds paths/pointers/short evidenced text, never raw
file bodies or credentials); the settings.json merge is proven idempotent and non-destructive by a dedicated
test suite before being applied to the real global config; degrades silently in a project with no Forge
install.
