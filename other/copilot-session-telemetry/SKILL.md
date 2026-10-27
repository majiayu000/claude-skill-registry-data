---
name: copilot-session-telemetry
description: Audit the real-session efficiency of an agent skill's execution episode in a Copilot session against four goals - minimize LLM token usage, minimize execution time, minimize semantic (model-judgment) steps, and maximize deterministic (script/code-executed) steps - by parsing the session's local events.jsonl telemetry and persisting a dated report for historical analysis and hand-off to waza eval refinement. Use AFTER a skill has finished executing in a session, to audit what a real run actually burned, diagnose token/time/step hotspots, or build an efficiency record in any agentic workflow executed by an AI agent - software delivery, research, operations, content production, or any other skill-driven run. Do NOT use for judging skill output quality or writing/running evals (use the waza-cli skill - that is the benchmark/evaluation instrument), for general session inspection, or when the session has no events.jsonl telemetry.
metadata:
  version: 0.4.0
---

# Copilot Session Telemetry

Audit one skill-execution episode from a Copilot session's local telemetry — what the run
actually burned (tokens, time, scripted vs ad-hoc steps). It measures; it does not judge
skill quality. Goals, metric definitions, and classification rules live in `references/` —
load them only as needed.

> **Terminology**: an **episode** is one execution run of the target skill — a
> time-window *slice* of the session's `events.jsonl` transcript, from the skill's
> invocation to the next external skill invocation (or session end). One session
> can contain many episodes. `--mode session` measures everything in the session
> before this audit's own activation instead.

## Relationship to waza (hand-off)

Vocabulary: **"benchmark" is reserved for waza's authored evals** — this skill produces
**telemetry**. The two are complementary halves of one loop:

1. **Audit** a real run here → find the hotspot (a repeated ad-hoc shell block, a
   discovery-heavy subagent window, a SKILL.md loaded every turn).
2. **Hand off** the evidence to the [`waza-cli`](../waza-cli/SKILL.md) skill: scaffold an
   eval case (`waza new eval <skill>`), assert the corrected behavior with graders
   (`action_sequence`, `tool_constraint`, `text`, …), and gate regressions with `waza gate`.
3. **Re-audit** after the fix and compare the new dated report against the previous one to
   confirm the improvement held in production.

Do not load this skill to judge skill output quality — that is waza's domain.

## Workflow

1. **Identify target skill and session.** Determine the skill name that executed
   (repo-level in `skills/<name>/` or `.github/skills/<name>/`, or user-level/published). Locate the session dir:
   the current session (`$env:COPILOT_HOME` or `~/.copilot` + `session-state/<uuid>`),
   or scan `session-state/*/workspace.yaml` for `repository`/`git_root` matching the
   current repo (most recently modified first). Do NOT use the `sessions` SQLite
   catalog for discovery — it can be days stale.

2. **Pre-flight telemetry check.** Confirm `events.jsonl` exists in the session dir
   and contains a `skill.invoked` **event type** whose `data.name` equals the target
   skill. Filter on the event `type` field exactly — a substring match on
   `skill.invoked` also catches `skill.invoked_ref` events, whose `data.name` is an
   empty string; those are noise, not evidence of a missing skill. If either check
   is missing, stop and report the specific gap — never silently fall back to the
   stale SQLite catalog.

3. **Run the audit.**

   ```powershell
   pwsh -NoProfile -File skills/copilot-session-telemetry/scripts/Invoke-SessionTelemetry.ps1 `
     -SkillName <target-skill> -SessionDir <session-dir>
   ```

   The orchestrator resolves the telemetry location (target skill's `telemetry/` folder
   when repo-level — `skills/<skill>/` or `.github/skills/<skill>/` —, `telemetry/<skill>/` at repo root when user-level; an
   existing legacy `benchmarks/` folder is reused with a warning; override with
   `-OutDir`), runs `scripts/compute_metrics.py`, and writes:
   - `YYYYMMDD-HHMMSS-episodeN-report.md` — dated report with the full metric tables (the
     only persisted artifact; the engine also echoes the full metrics as JSON on stdout)

   Options: `-Episode N` (earlier invocation of the skill), `-Mode episode|session`,
   `-EventsPath` (direct file), `-OutDir`, `-RepoRoot`.

   **Modes**: `-Mode episode` (default) measures one execution run of the skill.
   `-Mode session` measures everything before this audit's own activation —
   the whole-workflow number that survives ambiguous attribution; per-episode
   detail appears as a secondary breakdown table. Session mode writes
   `…-session-report.md` (keep episode and session reports separate — they answer
   different questions and must never cross-compare).

4. **Present results.** Show the four-goal scorecard. When a metric looks off versus the
   previous dated report, name one concrete improvement: raise the deterministic ratio by
   scripting a repeated ad-hoc shell command; cut tokens by trimming context loaded
   per step; cut semantic steps by batching edits.

## Reading the output

- Tokens are primary; cost is informational only (BYOK sessions report 0).
- Active time excludes `ask_user` waits — human idle never penalizes the workflow.
- A high `uncertain` count (usually ad-hoc `powershell` one-liners) is a signal, not
  noise: each one is a candidate for promotion to a repo script, or for a waza eval case
  that locks the fix in (see Relationship above).
- `query_read` steps count as decision points — grep/view spam is visible, not free.
- **Degenerate-episode guard**: an episode with ≤ 2 tool steps (or a < 2 min window
  while the session holds far more work) is flagged in the report's Caveats — a
  skill-load measurement must never be mistaken for the workflow. Use `-Mode session`
  for a whole-workflow number.
- **Skill-chain & subagent attribution**: loads of driver/helper skills named by the
  target's `SKILL.md` (or its `machina:` contract) and skill loads inside subagent
  windows do not terminate the episode — they appear in the report's Boundaries
  table with their own sub-window totals.
- Classification rules and the tool-name alias map: `references/classification.md`.
- Metric formulas and episode attribution (self-exclusion, timestamp windows):
  `references/metrics.md`. Event shapes: `references/event-schema.md`.

## Edge cases

- **Multiple invocations**: default is the most recent episode; use `-Episode N`.
- **Meta/driver skills belong to their owner**: when a driver skill (e.g.
  `machina-driving`) is chain-merged into a declaring orchestrator's episode, its
  cost is already owned by that orchestrator's scorecard (shown as a boundary row).
  Do NOT audit a shared driver as its own episode — it would double-count
  and mix callers (several orchestrators can declare the same driver). Audit a
  driver directly only when the session drove the workflow with no orchestrator
  involved (e.g. a direct human-conductor run).
- **Sub-agent (`task`) work**: included in totals and broken out in `sub_agent_tokens`.
- **Audit self-contamination**: excluded automatically — the episode ends at the
  audit's own activation (hard stop, even across skill chains).
- **No/old telemetry**: pre-flight fails with a named gap; the engine still writes a
  `*-cannot-audit.md` stub (exit code 3) so the failure itself is a durable record.
