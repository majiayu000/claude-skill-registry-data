---
name: pd-resume
description: >
  Resume PD sessions with minimal context overhead. Reads next-session.md directly
  (no subagents), spawns PD coordinators with lean briefings. Invoke as
  /pd-resume all or /pd-resume [slug]. Optimized for context window efficiency:
  no recall subagents, no temp files, no embedded protocol duplication.
---

# /pd-resume

Fully autonomous. Reads state directly, spawns PDs with pre-digested briefings.

**Context budget principle:** save-state does the synthesis at write-time so
pd-resume pays near-zero at read-time. Every token in the PD spawn prompt
must earn its place.

## SSOT

Project registry: `~/.claude/memory/medium-term.md` — Active Projects table.
Read it FIRST. This is the ONLY project-to-path map. No hardcoded tables.

## If Slug Not Found

1. Check `~/.claude/memory/medium-term.md` Active Projects table.
2. If not found → output: `PROJECT NOT FOUND: {slug}` and stop.

## Step 1 — Resolve Targets

Accept argument: `all` | single slug | comma-separated slugs.

1. Read `~/.claude/memory/medium-term.md`
2. Parse the Active Projects table for slug → path + PD name mappings
3. Skip archived projects (listed in the Archived line)
4. If slug not found → stop with error

## Step 2 — Read Briefings Directly

For each target project, read these files in parallel using the Read tool.
**Do NOT spawn subagents.**

**Per project, read simultaneously:**
1. `{project-path}/memory/next-session.md` — the PD startup briefing
2. `{project-path}/memory/inter-spawn-tasks/index.md` — inter-spawn tasks Active Summary
3. All files matching `{project-path}/memory/inter-spawn-tasks/incoming/*.md` — unread inbound tasks
4. `{project-path}/memory/pd-structure.md` — structural contract (if exists; skip silently if not)
5. All files matching `{project-path}/memory/tasks/ongoing/delegated-*.md` — inter-spawn delegation sweep
6. `{project-path}/memory/dev-plan.md` — check for existence only (do not embed; just note present/absent)

**DEV-PLAN-ABSENT CHECK:** After reading, check whether `{project-path}/memory/dev-plan.md` exists.
- If absent: inject into the PD spawn prompt (Step 3): "DEV-PLAN ABSENT — generate
  {project-path}/memory/dev-plan.md before spawning any Coord. Apply the two-condition
  parallel rule to assign layers. After generating the dev-plan (and any needed structure
  files), run /save-state and respawn to enter the deployment phase with a clean context."
- If present: inject a one-line note: "Dev-plan: {project-path}/memory/dev-plan.md (present — read before spawning Coords)"
This ensures every PD session starts from a dev-plan, retroactively generating one if absent.

**DELEGATION SWEEP (mandatory):** Read all `delegated-*.md` files found in step 5. For each file,
check for a `## Completion` block. If a Completion block is found:
- Include in the PD briefing: "COMPLETED INTER-SPAWN TASKS: {task-id} — {summary from Completion block}"
- The PD must move the file from ongoing/ to completed/ on startup and log the completion.
If no delegated-*.md files exist or none have Completion blocks, skip silently.
This sweep makes inter-spawn completions visible on the very next pd-resume, regardless of when save-state ran.

If next-session.md doesn't exist or is empty, use fallback:
```
Phase: unknown
Next: read project memory and assess current state
Blockers: none
```

If `inter-spawn-tasks/incoming/` has no files or doesn't exist, skip silently.

**INCOMING INTER-SPAWN TASKS (mandatory injection):**
After reading, if any files exist in `incoming/`, inject an "INCOMING INTER-SPAWN TASKS"
section into the PD spawn briefing (Step 3). Format:

```
INCOMING INTER-SPAWN TASKS ({N} unread):
- {filename}: {first line of each file — the task title or # header}
  [verbatim: first 3 lines of each file]
Active Summary (from index.md): {Active Summary section verbatim}
```

The PD MUST read and act on these at startup — the identity file contract says
"inter-spawn-tasks/incoming/ checked FIRST" and the spawn briefing must enforce it.

## Step 2.5 — Check Showcase Mode

Showcase is **off by default** and activates ONLY when explicitly requested in
the current invocation. Do NOT probe `~/.claude/state/pd-showcase.flag` on
every resume — that file is a persistent toggle used only by `/pd-showcase on/off`
for manual demo sessions, not the default resume path.

**Determine showcase_on:**
- If user passed `--showcase` as an argument to `/pd-resume` → `showcase_on = true`.
- If user invoked `/pd-showcase on` in this same session AND has not yet run any `/pd-resume` → check for the flag file as confirmation.
- Otherwise → `showcase_on = false`. Do NOT read the flag file.

Record this as `showcase_on = true | false` for use in Step 3. NOTE: if
multiple targets were resolved in Step 1 and showcase is ON, spawn them
**sequentially** (foreground spawns block) — not in parallel.

## Step 2.6 — Operator-Blocked Guard (skip-spawn check)

Before spawning, detect projects whose only pending work is an operator-side decision.
Spawning a PD with nothing actionable burns a session cycle and triggers an
immediate `/save-state` — wasteful and noisy. Better: report BLOCKED status, skip
the spawn, let the operator act first.

For each target project, evaluate these three conditions:

1. **`Next:` line in next-session.md matches a blocked pattern.** Case-insensitive
   regex: `\b(user|operator)\s+(approves|approve|decides|decide|reviews|review|sign-?off|ack(s|nowledg(es|ement))?|confirm(s|ation)?)\b` OR contains the phrase `awaiting (user|operator|approval|sign-?off|ack)`.
2. **`{project-path}/memory/tasks/ongoing/` contains no `.md` files** (empty dir, or
   only contains hidden/index files).
3. **`{project-path}/memory/inter-spawn-tasks/incoming/` contains no `.md` files**.

**If ALL THREE are true** → mark project as `BLOCKED_NO_SPAWN` and DO NOT spawn its PD.
Instead, include it in the Step 4 summary as:

```
{slug} — BLOCKED — no spawn
  blocked-on: {extract verbatim from Next: line}
  ongoing tasks: 0 | incoming inter-spawn: 0
  action: Operator must act, OR queue work to tasks/ongoing/, OR edit next-session.md Next line
```

**If ANY of the three is false** → spawn normally (project has actionable work
even if the headline is operator-blocked).

**Override:** if user invokes pd-resume with explicit `--force` flag, skip this guard and spawn anyway.

## Step 3 — Spawn PD Coordinators

Spawn one pd-coordinator per target that was NOT marked `BLOCKED_NO_SPAWN` in Step 2.6.
**All in a single message** (parallel) WHEN showcase is OFF. When showcase is ON, spawn one at a time.

If ALL targets were marked `BLOCKED_NO_SPAWN`, skip Step 3 entirely and go to Step 4.

**Spawn config:**
- `subagent_type`: pd-coordinator
- `model`: opus
- `run_in_background`: `false` if `showcase_on`, else `true`

**⚠️ Advisory only:** the `model` value above is not a reliable override in all harness/session configurations — some setups ignore the Agent-tool spawn-time `model` param and resolve to the agent definition's own frontmatter `model:` key (or a session default) regardless. Treat `core/agents/pd-coordinator.md`'s frontmatter `model:` line as the actual binding value; keep this spawn-config line in sync with it, but do not rely on it alone.

**Spawn prompt — LEAN FORMAT (do not add to this):**

```
You are PD-{slug}, resuming {project-name}.
Project: {project-path}
Tasks: {project-path}/memory/tasks/ongoing/
Inter-spawn tasks: {project-path}/memory/inter-spawn-tasks/

--- BRIEFING ---
{verbatim content of next-session.md}
---

{IF incoming inter-spawn tasks exist, append:}
--- INCOMING INTER-SPAWN TASKS ({N}) ---
{verbatim task list from Step 2 injection block}
Read and action these FIRST before any other work. Each file is at:
{project-path}/memory/inter-spawn-tasks/incoming/
---

Start the Next action immediately. On startup, read only memory/tasks/ongoing/
and memory/inter-spawn-tasks/incoming/. Your agent definition has your full
protocol and lifecycle — do not wait for additional instructions.
When done or blocked, /save-state {slug} and stop.

{IF showcase_on, append:}

--- SHOWCASE MODE ---
A live audience is watching this session. Optimize for comprehension over speed:

1. Before each tool call, write ONE short sentence explaining what you're
   about to do and why.
2. After each tool result, write ONE short sentence summarizing what you
   learned before choosing the next step.
3. When deciding between approaches, narrate the trade-off out loud
   ("I could either X or Y — going with X because...").
4. When you finish a phase (research, planning, implementation, verification),
   call it out explicitly so the audience knows where you are.

Keep narration tight — one sentence each, no lectures. The audience reads
your tool calls; you just connect the dots.
--- END SHOWCASE MODE ---
```

**IF pd-structure.md exists and was read, inject only the safety-critical sections into spawn prompt:**
```
--- STRUCTURAL CONTRACT (from pd-structure.md) ---
## No-Touch Zones
{verbatim No-Touch Zones section only}

## Integration Contracts
{verbatim Integration Contracts section only}
---
```
Note: Architecture Decisions, Active L3 Boundaries, and Cross-L3 Dependencies are in pd-structure.md — PD reads on-demand when needed, not at cold-start.

**What is NOT in the spawn prompt (already in pd-coordinator agent definition):**
- PD Standard Protocol (decompose → parallelize → report)
- Agent Selection Hierarchy
- Decomposition guide (L1→L3)
- Coord spawn template
- QA gate protocol
- ACK/NACK reference
- Status log format
- Escalation protocol

**What is NOT in the spawn prompt (available on-demand via file read):**
- PD Directory / cross-project paths (medium-term.md — read only for inter-spawn)
- Project CLAUDE.md (read only if PD needs project-specific config)
- Historical sessions (sessions/*.md — never read at startup)

## Step 4 — Output Summary

After all eligible PDs are spawned (and any BLOCKED_NO_SPAWN targets are noted):

```
PD RESUME — {n} projects ({s} spawned, {b} blocked)

{slug} — {phase} — spawned
  next: {next action}
  blockers: {blockers or "none"}

{slug} — BLOCKED — no spawn
  blocked-on: {Next: line verbatim}
  ongoing tasks: 0 | incoming inter-spawn: 0
  action: Operator must act, OR queue work to tasks/ongoing/, OR edit next-session.md Next line

[...one per project...]

{IF showcase_on:} Showcase MODE — PDs are running in the foreground. Tool calls and narration stream into this session live.
{ELSE IF any spawned:} Spawned PDs running in background. Progress arrives via SendMessage.
{ELSE:} No PDs spawned. All targets blocked on operator — review the blocked-on items above.
```

Then stop. Do not poll or wait.
