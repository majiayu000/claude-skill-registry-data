---
name: clean-my-loop
description: Audit and clean the persistent context that feeds a recurring autonomous agent loop — memory files and indexes, scheduled-task / automation prompts, and CLAUDE.md / AGENTS.md — so the loop stops degrading into a self-reinforcing echo chamber. Works for Claude Code /loop crons and Codex automations.
---

# clean-my-loop

A recurring autonomous loop (Claude Code `/loop` cron, Codex automation) re-reads the same
context every iteration: its memory/state files, the scheduled-task prompt, and CLAUDE.md /
AGENTS.md. Those artifacts **decay**: memory grows into a changelog, task rules acquire
no-exit "skip on error" clauses, instruction files give the loop cover to feel productive
while defeating its own purpose. The decay compounds — each iteration re-reads the bloated
state and writes more of it back. The result is a degenerate loop: lots of motion, no
progress. **This skill diagnoses that decay with evidence and fixes it.**

This is a destructive-edit + behavior-change task on the user's automation. **Move carefully,
show evidence before editing, and put the irreversible / judgment calls behind
`AskUserQuestion`** (see Step 4).

## When this applies

The user points at a loop and says it feels stuck, repetitive, bloated, expensive, or "off" —
or just asks to clean / health-check a `/loop` cron or Codex automation. If no loop is named,
ask which one (Step 1).

## Workflow

### 1. Scope the target

Identify exactly one loop to clean. If the user named a repo/automation, use it. Otherwise
enumerate candidates and ask via `AskUserQuestion`:
- Claude Code crons: call the `CronList` tool; also `cat <repo>/.claude/scheduled_tasks.json`
  and `~/.claude/scheduled_tasks.json` if present.
- Codex automations: `ls ~/.codex/` and look for an automations/scheduled config; check the
  repo for `AGENTS.md`.

Confirm the **platform** (Claude Code vs Codex) — it decides where the context lives. See
[references/platform-layout.md](references/platform-layout.md) for exact file locations and
the discovery commands for each.

### 2. Map the loop's context surface

Gather every artifact the loop re-reads or re-writes each iteration. Read them, and measure
sizes (`wc -l -w -c`). The surface is typically:

| Artifact | Claude Code | Codex |
|---|---|---|
| The task prompt | `scheduled_tasks.json` `prompt`, or `CronList` | the automation's prompt/config |
| Persistent memory | `~/.claude/projects/<enc>/memory/MEMORY.md` + `*.md` | whatever STATUS/state file the prompt maintains |
| Instruction files | `~/.claude/CLAUDE.md` + `<repo>/CLAUDE.md` | `~/.codex/AGENTS.md` + `<repo>/AGENTS.md` |
| Run history (for forensics) | `~/.claude/projects/<enc>/*.jsonl` | `~/.codex/sessions/` or history logs |

**Anchor each artifact to its own last-touch date, not a shared one.** The surface decays on
*independent* cadences — a memory file rewritten yesterday and a CLAUDE.md untouched for months
need different staleness windows, and a single global date gives wrong reads for both. Per
artifact, record its last-modified time: `git log -1 --format=%ai -- <path>` for tracked files,
`stat -f %Sm <path>` (mtime) for untracked ones like `~/.claude/.../memory/*.md`. That per-file
date is the window you measure churn and staleness against in Step 3.

### 3. Diagnose against the decay heuristics

Run the checks in [references/detection-heuristics.md](references/detection-heuristics.md).
Each smell has a quantitative trigger and a fix. The high-value ones:

- **Memory-as-changelog** — a "one fact" memory file that's grown to a per-iteration log
  (large size, append-not-replace, dense `DONE/deferred/done` markers).
- **Bloated index** — Claude `MEMORY.md` with a single line far over a one-line hook.
- **No-exit task rule** — a "skip / defer on error" clause with no "stop after N failures /
  escalate after M hours" exit. A transient guard becomes a permanent stall.
- **Dead-end human handoff** — the prompt tells the unattended loop to "ask the user to do X";
  nobody reads it in real time, so the loop churns forever.
- **Unbounded queue growth** — each iteration piles up unvalidated/unadopted work. Confirm
  with `git`: commits since the last deploy/adopt marker growing monotonically while reported
  status stays upbeat.
- **Doc-as-cover** — CLAUDE.md / AGENTS.md framing that lets "keep building locally" feel like
  discipline while the loop's actual purpose goes unmet.

**Use the run history as evidence, not vibes.** Extract each iteration's final report from the
`*.jsonl` (or Codex session) logs and look for: the same action repeated K times, a
"queue/count ahead" number rising monotonically, real progress (deploys/merges) stalled. Cite
concrete numbers (file sizes, repeat counts, queue depth) in your findings — the
[detection-heuristics](references/detection-heuristics.md) ref has the extraction one-liners.

**Scale how much history you read to how much the loop has churned.** A loop that fired 200
times since its last clean hides its decay differently than one that fired 8 times — and
reading only the most recent few sessions samples the *tail*, exactly where a degenerate loop
looks calmest. Count the iterations in the window (sessions since the last-touch date from Step
2), then sample accordingly:

| iterations since last clean | how to read run history |
|---|---|
| < 10 | deep-read every session |
| 10 – 49 | deep-read the latest ~10, spot-check the oldest 2–3 for when the smell began |
| ≥ 50 | sample across the whole window (early / middle / recent), not just the tail; the early sessions date the onset |

When you sample rather than read exhaustively, **say what you skipped** in your findings — a
silent tail-only read reads as "the loop is fine lately" when the bloat is upstream.

### 4. Ask the key judgments (AskUserQuestion)

Before any destructive or behavior-changing edit, surface findings and put the calls **only
the user can make** behind `AskUserQuestion`. Don't ask what you can verify yourself; do ask:

- **Which fixes to apply** (multiSelect) — list each detected smell as an option so the user
  opts in per-fix rather than all-or-nothing.
- **History: archive or delete** — when slimming a bloated memory/state file, archive the old
  body to a cold sibling file vs. drop it (git already has the history).
- **Edit the task prompt itself?** — changing the cron/automation prompt changes the loop's
  future behavior (e.g. adding an exit condition). This is higher-stakes than cleaning files;
  confirm before touching it.
- **The exit / "blocked" policy** — when adding a no-exit fix, ask what should happen on
  persistent failure: stop generating new work and only health-check + alert, keep going, or a
  threshold (after N fails / M hours). This is a real ops-judgment call.

Recommend a default in each question (first option, "(Recommended)") but let the user steer.

### 5. Apply the approved fixes

Common, proven moves:

- **Snapshot + cold archive a bloated memory/state file.** Copy the full file to a sibling
  archive (e.g. `<name>-archive.md`, `type: reference`, with a header pointing back to the live
  file). Rewrite the live file as a short **current-state snapshot** — identity, a single
  `## CURRENT STATE` block, what's blocking, what's next. End it with an explicit rule:
  *"This is a SNAPSHOT — overwrite the state block in place each iteration; do NOT append a
  per-commit log here."* That last line is what stops re-bloat.
- **Shrink the index** (Claude `MEMORY.md`) back to one hook line per memory; add a dim pointer
  for the archive so it's findable but not loaded every run.
- **Add an exit condition** to the task prompt: after N consecutive failures / M hours blocked,
  stop producing new deferred work and switch to health-check + a single loud BLOCKED line +
  (if available) a real notification.
- **Add a counter-rule** where an instruction file gives unproductive cover.

Keep edits minimal and reversible; the archive preserves everything.

### 6. Report and prevent recurrence

Summarize before/after with numbers (sizes, queue depth, repeat count). Flag the **recurrence
risk explicitly**: if you cleaned files but the loop's prompt still says "append progress each
run", the next fire re-bloats them — so the prompt fix in Step 5 is what makes the cleanup
durable. If the user declined the prompt edit, say so plainly.

## External references (prior art, security-clean — read for ideas, don't run)

This skill's niche — auditing the *loop* (its prompt, exit conditions, and run-history), not
just a static memory file — appears unoccupied. But three adjacent, MIT/local-only projects are
worth reading when you need depth on the memory half:

- **`wan-huiyan/memory-hygiene`** (GitHub) — the closest analogue: tiered memory architecture,
  index truncation-risk thresholds, inline-content-extraction, and an approval gate before
  destructive edits. Best single reference for the memory-file cleanup mechanics.
- **`/slim` self-audit** (ai-muninn blog) — per-turn token-cost measurement and the
  index→one-line-pointer + subfile shrink mechanic (mirrors Step 5's "shrink the index").
- **Pensyve** (`major7apps/pensyve`) — FSRS decay scoring for "stale memory." Borrow the
  recency-decay *concept* for smell #7; don't pull in its runtime.

Avoid hosted "memory hygiene" SaaS that ask you to paste memory contents off-machine, and don't
copy any `rm -rf`/service-restart commands from third-party SKILL.md files verbatim.

## Boundaries

- **Don't** run the loop's actual work, deploy, or rotate secrets — this skill cleans the
  loop's *context*, it doesn't operate the system the loop manages.
- **Don't** delete history without an archive unless the user explicitly chose delete in Step 4.
- Treat recalled memory as possibly stale: if it names a file/flag/commit, verify it still
  exists before trusting or repeating it.
