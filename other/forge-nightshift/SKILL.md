---
name: forge-nightshift
description: "Overnight session-limit-resilient builder — work-package queue, auto-resume, morning briefing: run this overnight, keep going while I'm away, resume tomorrow, opt-in only."
---

# Forge playbook — Nightshift (overnight self-resuming builder)

**Do not duplicate existing tools — defer to:** `forge-manifest.cjs` (ARM/RECONCILE per-WP manifest),
`forge-swarm-resume.cjs` (re-dispatch plan for unfinished WPs), `forge-checkpoint.cjs` (idempotency for any
side-effecting WP), `forge-actiongate.cjs` (hard-gates — deploy/push/spend/DNS/etc.), `usage-guard.cjs`
(the real, already-built session/usage-limit watchdog + auto-resume signal), and `forge-briefing.cjs`
(piece J5 — the real, tested morning-briefing generator this skill's output depends on). This file is
doctrine/orchestration only: it explains how those pieces compose into an overnight run, it does not
reimplement any of them.

## What Nightshift actually is (and is not)
Nightshift is **not** a new autonomous scheduler and **not** a background daemon that decides on its own to
start work. It is a documented *pattern* for composing four already-real, already-tested pieces so a large
swarm can survive a session/usage-limit interruption and resume honestly the next time a session runs:
1. **Plan** the work queue up front and ARM it (`forge-manifest.cjs::arm()`) so every work package's exact
   scope (`narrowed_prompt`, `deps`) is persisted BEFORE dispatch — never re-derived from memory later.
2. **Dispatch** normally (Agent-tool subagents, per this project's real-agents-only governance). Each
   WP's real completion/failure is logged as an ordinary event (`wp_completed`/`check_passed` or
   `wp_failed`/`check_failed`) — Nightshift adds no new event-logging mechanism of its own.
3. **Survive the interruption.** If the session ends (session-limit pause, usage-limit pause, or the owner
   simply closes the laptop), nothing is lost: the manifest + `events.jsonl` already on disk are the
   complete record. The NEXT session that runs calls `forge-swarm-resume.cjs::resume({run_id})` to get
   back exactly the unfinished WPs (with their original scoping) — never a fabricated "pick up where I
   think I left off".
4. **Report honestly.** Before (or instead of) resuming, run `forge-briefing.cjs --run <id>` to generate the
   MORNING BRIEFING — a markdown of what **ran**, what's **blocked**, and what **only the owner can decide**
   (retry/reassign/drop a failure, resume/reprioritize/drop an unfinished WP), derived purely from the
   run's own logged manifest + events. This is a real, hermetically-tested tool
   (`forge-bin/forge-briefing.cjs` + `forge-briefing.test.cjs`), not a scaffold.

## Hard rules
- **Hard-gates still interrupt overnight.** Nothing about running unattended changes
  `forge-actiongate.cjs`'s classifier or the owner-approval requirement it enforces. A deploy/push/spend/
  DNS-change/credential-rotate/workflow-activate/outbound-send WP that gets dispatched overnight **still
  stops and waits for `owner_confirmed:true`** — it does not queue itself for "approve all in the morning".
  An overnight run that hits a hard gate logs the block and moves on to other, non-gated WPs; it never
  silently proceeds past one.
- **Scheduling is opt-in only — this skill never self-schedules.** Nothing in this project starts a new
  Claude Code session on its own. Two real, owner-enabled opt-in paths exist (see "Opt-in flow" below);
  neither is active until the owner turns it on.
- **Every resumed WP still owns its own idempotency.** A re-dispatched WP that has a real side effect
  (email, deploy, external write) MUST check `forge-checkpoint.cjs::shouldRun/claim` for its own
  idempotency key before repeating that side effect — `forge-swarm-resume.cjs::resume()` only tells you
  WHICH WPs are unfinished, it does not itself guard against double-running one (see that file's own header).
- **Never fabricate progress.** A WP with no qualifying completion/failure event stays "armed" — exactly
  `forge-manifest.cjs`'s "never fabricate a completed WP" invariant — and is reported as unfinished in the
  morning briefing, never quietly assumed done because "it was probably fine."
- **The briefing is evidence, not narrative.** `forge-briefing.cjs` only ever renders what the run's own
  manifest.json/events.jsonl already say. If a WP's outcome was never logged, the briefing says so; it does
  not infer success from a file that merely looks correct.

## Opt-in flow (dormant until the owner acts)
Nothing below is active by default. Both paths are the owner's explicit choice, and both still end in the
SAME place: a Claude Code session running the plan → dispatch → resume → briefing loop above.
1. **`usage-guard.cjs` watch/auto-resume (already real, already built).** The owner runs
   `node .claude/forge-bin/usage-guard.cjs start` to watch the real Anthropic usage endpoint. When a
   session-limit pause happens, the guard's own documented RESET-RHYTHM auto-resume signals the paused
   session to continue once the limit window resets (see that file's header — this is existing, tested
   behavior, not new for Nightshift). Nightshift's contribution is simply: on that continue signal, the
   resumed session's FIRST action is `forge-swarm-resume.cjs::resume({run_id})`, not "start over."
2. **OS-level scheduler (cron / Windows Task Scheduler), fully owner-configured.** For a literal overnight
   wake-up (not just a usage-limit reset), the owner configures their OWN OS scheduler to start a Claude
   Code session at a chosen time, with a prompt that names the `run_id` to resume (e.g. "resume Forge run
   <id> via forge-swarm-resume, then produce the morning briefing"). Forge does not ship or install this
   scheduler config — it is standard OS tooling the owner sets up outside this project, exactly like any
   other cron job the owner already runs.
Either path ends at the same resume+briefing loop; neither is required for Nightshift's tools to work
manually (an owner can always run `forge-swarm-resume.cjs`/`forge-briefing.cjs` by hand, on demand, with no
scheduler at all — that manual path is the actually-proven one).

## Skills / commands / MCP
`forge-manifest.cjs` (arm/reconcile/status), `forge-swarm-resume.cjs` (resume plan), `forge-checkpoint.cjs`
(per-WP idempotency), `forge-actiongate.cjs` (hard-gate classifier, reused not duplicated), `usage-guard.cjs`
(real session/usage-limit watchdog + auto-resume), `forge-briefing.cjs` (real morning-briefing generator —
`node .claude/forge-bin/forge-briefing.cjs --run <id> [--json]`), `forge-worktrees` skill when overnight
work is parallelized across multiple Bosses.

## Fan-out & flow
No dedicated team of its own — Nightshift is a cross-cutting composition pattern the Lead (Head Chef) applies
around whatever domain team a task already needs (`forge-website`, `forge-fullstack`, etc.).
**Serial, once per session boundary:** plan + ARM manifest → dispatch WPs normally → (session ends) →
next session: `forge-swarm-resume.cjs::resume()` → re-dispatch only the unfinished WPs → `forge-briefing.cjs`
before/after each resume, so the owner always has an up-to-date, real morning briefing rather than only a
next-morning one.

## Ship-readiness (unique)
A real manifest was armed before dispatch (`manifest.json` exists for the run); every WP's real
completion/failure is a logged event, never inferred; `forge-swarm-resume.cjs` output was actually used to
scope the resumed dispatch (not a manually-reconstructed guess); every hard-gate hit during the run is
still logged as a block awaiting `owner_confirmed:true`, never silently bypassed; the morning briefing
(`forge-briefing.cjs --run <id>`) was actually generated and its `ran`/`blocked`/`decisions_needed` reflect
real logged content; any side-effecting resumed WP re-checked its own `forge-checkpoint.cjs` idempotency key
before repeating a real action. State plainly whether an opt-in scheduling path is active or the resume was
run manually — never imply an automatic overnight wake-up happened when the owner simply re-ran the command.
