---
name: swarm
description: Run a multi-agent audit of a codebase by spawning specialized parallel subagents (security, performance, tests, architecture, dead-code), then synthesize their findings into a single prioritized action plan. Use this whenever the user runs /swarm, asks to "audit the repo," "review this codebase," "find issues across the project," wants a comprehensive multi-angle code review, or asks what to fix first in a large or unfamiliar codebase. Also use for /swarm execute to have Claude fix the findings one at a time. Do NOT use this for a single-file review or a narrow bug fix — this skill is for repo-wide, multi-dimensional audits.
---

# Claude Swarm

Runs a parallel "swarm" of specialized subagents over a codebase, each scoped to a
narrow category of issue, then synthesizes their raw findings into one deduplicated,
severity-ranked action plan. Optionally executes fixes for approved findings.

## Commands

- `/swarm audit [path]` — run the full audit (default path: repo root)
- `/swarm status` — show the last audit summary from persisted state
- `/swarm execute <severity|id>` — fix findings matching a severity tier (critical/high/medium/low) or a specific finding id
- `/swarm show <id>` — show full detail for one finding

## State file

All findings persist to `.claude/swarm-audit.json` at the repo root (create the
`.claude/` dir if missing). This lets `/swarm execute` run in a later session without
re-auditing, and lets `/swarm status` answer instantly. Always read this file first
if it exists and the user references "the audit" or "findings" without re-running one.

Schema for this file is in `references/output-schema.md`.

## `/swarm audit [path]` workflow

1. **Scope check.** If no path given, default to repo root, but if the repo is large
   (rough heuristic: >150 files or the user hasn't specified), ask the user to confirm
   scope or suggest a subdirectory. Don't silently audit a massive monorepo — cost and
   time scale with size.

2. **Spawn the five audit agents in parallel.** Use a single message with five Task
   tool calls so they genuinely run concurrently. For each, read the corresponding
   `agents/*.md` file and pass its full contents as the subagent's instructions, plus:
   - the repo path/scope for this run
   - the shared output schema from `references/output-schema.md`
   - explicit tool restriction: **read-only tools only** (Read, Grep, Glob, and a
     bash command runner if restricted to read-only commands like `git log`,
     `git blame`, test runners in check-mode). Do NOT give audit agents Write/Edit —
     the audit phase must not touch files.

   Agents to spawn:
   - `agents/security.md`
   - `agents/performance.md`
   - `agents/tests.md`
   - `agents/architecture.md`
   - `agents/dead-code.md`

3. **Collect raw findings.** Each subagent returns a JSON array matching the schema.
   If a subagent's output doesn't parse as valid JSON, re-prompt it once asking for
   schema-conformant output only; if it fails twice, drop it and note the gap to the
   user rather than blocking the whole audit.

4. **Spawn the synthesizer agent** (`agents/synthesizer.md`) with all raw findings
   concatenated. The synthesizer:
   - deduplicates overlapping findings (e.g. the same auth gap flagged by both
     security and architecture agents) — keep the more specific one, merge notes
   - assigns/normalizes severity using `references/severity-rubric.md`
   - orders the final list by impact-weighted-by-effort, not just severity
   - assigns each finding a short stable id (e.g. `SEC-01`, `PERF-03`)

5. **Persist** the synthesizer's output to `.claude/swarm-audit.json`, overwriting any
   prior audit for that path (keep the previous file as `.claude/swarm-audit.prev.json`
   for one generation of history, no more).

6. **Present a summary to the user** — not the full JSON. Format:

   ```
   Swarm audit complete — <path>

   Found 47 issues.
   🔴 Critical: 2   🟠 High: 7   🟡 Medium: 18   ⚪ Low: 20

   Recommended order:
   1. [SEC-01] Fix authentication token vulnerability — auth/session.py:88
   2. [PERF-02] Fix database connection leak — db/pool.py:41
   3. [PERF-05] Remove N+1 query — api/orders.py:112
   ...

   Run /swarm execute critical to fix the top tier, or /swarm show <id> for detail.
   ```

   Keep this to the top ~10 items inline; point to the state file / `/swarm show` for
   the rest rather than dumping all 47 into chat.

## `/swarm execute <severity|id>` workflow

1. Read `.claude/swarm-audit.json`. If missing, tell the user to run `/swarm audit`
   first — do not fabricate findings.
2. Filter to the requested severity tier (or single id).
3. **Confirm with the user before making changes** if this is the first execute call
   in the session, or if the tier includes more than ~5 findings — briefly list what
   will be touched.
4. Fix findings **one at a time, serially** (not parallel — concurrent edits across
   agents risk file conflicts and inconsistent partial states). For each:
   a. Spawn a fix agent scoped to just that one finding (file + line + issue +
      suggested_fix from the record), with Read/Edit/Write tools this time.
   b. After the edit, run the project's test command (detect from package.json /
      Makefile / pytest.ini / etc., or ask the user if ambiguous).
   c. If tests pass: mark the finding `status: "fixed"` in the state file, move on.
   d. If tests fail: revert the edit, mark `status: "failed"`, note the failure
      reason, and continue to the next finding rather than aborting the whole run.
5. Report a final summary: fixed / failed / skipped counts, and surface any failed
   items with the test failure reason so the user can look at them manually.

## Design principles

- **Read-only during audit, edit only during execute.** Keeps the audit deterministic
  and re-runnable, and means a bad audit run can never corrupt the repo.
- **Structured output only.** Every subagent must return the JSON schema, not prose —
  this is what makes synthesis and persistence tractable. Reject free-text findings.
- **Serialize the fixes.** Parallelism is for *finding* issues, not for *editing*
  files. Never spawn multiple fix agents concurrently.
- **Persist between sessions.** Claude Code sessions end; the audit shouldn't have to
  be redone because the user closed their terminal.
- **Don't silently re-scope.** If the user says `/swarm audit` with no path on a huge
  repo, ask rather than guessing — a full swarm on a monorepo is expensive.