---
name: dogfood
description: Use when starting a dogfood session for the vitest-agent plugin in this repo, when continuing one from an existing handoff at docs/superpowers/dogfood/<chain>/, or after the TDD orchestrator subagent completes a dogfood task. Repo-internal — does not apply to projects that consume vitest-agent as a dependency.
argument-hint: [--start | --random | --lifecycle | --from <path>]
disable-model-invocation: true
allowed-tools: Read Write Edit Bash Glob Grep Task mcp__plugin_vitest-agent_mcp__*
---

# Dogfood

You are the **main agent** running a dogfood session in the vitest-agent repo. The TDD orchestrator subagent is the system under test. The `playground/` workspace is the live target; intentional defects there are the fodder. Your job is to dispatch the orchestrator, observe it, audit the result against the meta-goal, and leave a paper trail.

## Current dogfood state

Open chains and their latest entries:

!`find docs/superpowers/dogfood -mindepth 2 -name "0*.md" -not -path "*_baseline*" 2>/dev/null | sort | tail -20`

Open-status handoffs (anything you should pick up):

!`grep -l "^status: open" docs/superpowers/dogfood/*/*.md 2>/dev/null | grep -v _baseline || echo "(none)"`

## Iron law: the orchestrator does not know it is being tested

The orchestrator subagent receives the **task prompt only**. Never:

- Pass it the handoff file path or its `what_were_testing` frontmatter
- Add hints like "be thorough" or "watch for X" that telegraph the meta-goal
- Reference `.claude/playground-cheatsheet.md` (the answer key) in any orchestrator-visible artifact
- Ask the orchestrator to "report extra info" unless the handoff explicitly requested it

The cheatsheet at `.claude/playground-cheatsheet.md` is yours; do not surface its existence in any prompt or commit message visible to the orchestrator.

## Argument routing

Parse `$ARGUMENTS`:

- **No args** → show the current state above and the four-option menu. If there are open handoffs, suggest `/dogfood --from <path>` for the most recent.
- **`--start`** → new chain. See "Starting a chain" below.
- **`--random`** → pick a task from the cheatsheet and dispatch without user discussion. See "Random chain" below.
- **`--lifecycle`** → dispatch the tdd-task agent with a fixed lifecycle-simulation prompt. No handoff file. See "Lifecycle test" below.
- **`--from <path>`** → continue from a specific handoff after a reboot. See "Continuing from a handoff" below.

## Random chain (`--random`)

No user discussion. Pick, write, dispatch, verify.

1. Read `.claude/playground-cheatsheet.md`.
2. Pick one defect. Prefer 0%-function-coverage gaps (untested functions: `isPrime`, `isPalindrome`, `Cache.has`) — they produce the cleanest red-phase signal. Fall back to edge-case/behavior defects (`average([])`, `Cache.size()` TTL, `Notebook.averageWordCount()`) if all untested functions are already covered.
3. Derive a chain slug and title from the chosen defect (e.g. `is-prime-coverage`, `cache-has-coverage`, `average-empty-array`).
4. Write the handoff at `docs/superpowers/dogfood/<chain-slug>/01-<title-slug>.md` and `findings.md` using the same templates as `--start`. Set `what_were_testing` to one sentence describing the behavioral observation (e.g. "tdd-task writes a failing test, fixes the defect, and commits before closing the session").
5. Dispatch (see "Dispatching"). The sanitized orchestrator prompt must describe the gap as a natural task — no mention of the cheatsheet, no hints about what the meta-goal is. A plain framing like "The playground package has some untested code paths. Use TDD to add tests for the missing coverage and fix any defects the tests expose." is appropriate; you may be more specific about the targeted gap but never reveal the meta-goal or cheatsheet structure.
6. Capture the session id and run the seven-step verification (see "Verification") immediately after the tdd-task agent completes.
7. Present the four-option menu.

## Lifecycle test (`--lifecycle`)

No handoff file. Dispatches the tdd-task agent with a fixed prompt that walks the TDD session machinery end-to-end. The source file `playground/src/lifecycle.ts` has a deliberate off-by-one bug (`return a + b + 1`); the orchestrator writes a test that exposes it, fixes the source, and closes the session. After each run the main agent reverts `lifecycle.ts` to restore the defect.

### Dispatch

Complete the standard pre-dispatch setup above (`inventory({ kind: "session", agentKind: "main", limit: 1 })` → TaskCreate if available → initialize maps), then dispatch as a **plain background subagent** — `run_in_background: true`, `subagent_type: "vitest-agent:tdd-task"`, and **no `name`/team argument** (a named teammate spawns a detached session with its own conversation that splits artifact attribution and denies the phase gates). Prepend `chatId` and `parentTaskId` (if captured — it's optional) to the prompt, then append the verbatim block below without modification.

### Verbatim prompt (append after chatId/parentTaskId lines — do not add other framing)

````text
Run a TDD lifecycle simulation to exercise the session machinery from start to finish. This is not a real coding task — use dummy goal and behavior labels throughout. You will write a temporary test file and fix a deliberately broken source file.

Steps:
1. Call `tdd_task({ action: "start", chatId, goal: "lifecycle-test: verify session open, transitions, and close" })`. Capture the returned `tddTaskId` and `goalId`.
2. Create one behavior via `tdd_behavior({ action: "create", goalId, behavior: "lifecycle-test: tdd session opens, transitions red→green, and closes cleanly" })`. Capture the returned `behaviorId`.
3. Mark the goal and behavior in_progress: `tdd_goal({ action: "update", id: goalId, status: "in_progress" })` and `tdd_behavior({ action: "update", id: behaviorId, status: "in_progress" })`.
4. Write a new file `playground/src/lifecycle.test.ts` containing exactly:
   ```typescript
   import { describe, expect, it } from "vitest";
   import { sum } from "./lifecycle.js";
   describe("lifecycle", () => {
     it("sum(1, 1) returns 2", () => {
       expect(sum(1, 1)).toBe(2);
     });
   });
   ```

   Note: `playground/src/lifecycle.ts` already exists with a deliberate bug — do not create it. The test expectation (`toBe(2)`) is correct; the source implementation is what is broken.
5. Run the playground tests using the `run_tests` MCP tool with a file filter:
   `run_tests({ project: "playground", files: ["playground/src/lifecycle.test.ts"] })`
   Confirm the test fails (`sum(1, 1)` currently returns 3, not 2, due to the bug in the source).
6. Call `tdd_phase_transition_request` for the `red` phase, citing the test-run artifact from step 5. Record whether it was granted or denied and the exact DenialReason if denied.
6b. After the transition is accepted, call `tdd_progress_push` with the spike→red phase event: `tdd_progress_push({ payload: JSON.stringify({ type: "phase_transition", sessionId: <tddTaskId>, goalId: <goalId>, behaviorId: <behaviorId>, from: "spike", to: "red" }) })`. Do this before proceeding to step 7.
7. **Critical — re-author the test in the red phase:** delete `playground/src/lifecycle.test.ts` and immediately rewrite it with the same content as step 4. The red→green gate requires `test_case_authored_in_session = true`, meaning the `test_written` artifact must fall inside the red phase window. Writing the file in step 4 authors it in spike; deleting and rewriting here moves the authorship into red.
8. Run the playground tests again using `run_tests` with the same file filter:
   `run_tests({ project: "playground", files: ["playground/src/lifecycle.test.ts"] })`
   Confirm the test still fails (the source bug has not been fixed yet).
9. Fix the bug in `playground/src/lifecycle.ts`: change `return a + b + 1` to `return a + b`.
10. Run the playground tests again using `run_tests` with the same file filter:
    `run_tests({ project: "playground", files: ["playground/src/lifecycle.test.ts"] })`
    Confirm all tests pass.
11. Call `tdd_phase_transition_request` for the `green` phase, citing the `test_failed_run` artifact from step 8 (not the passing run from step 10 — `red→green` requires proof that the test was failing before the fix). Record the outcome.
12. Mark the behavior done: `tdd_behavior({ action: "update", id: behaviorId, status: "done" })`. Mark the goal done: `tdd_goal({ action: "update", id: goalId, status: "done" })`.
13. Call `tdd_task({ action: "end", tddTaskId: tddTaskId, outcome: "succeeded" })`.
14. Delete `playground/src/lifecycle.test.ts` to leave the playground clean. Do NOT delete or revert `playground/src/lifecycle.ts`.

Report: for each phase-transition call (steps 6 and 11), state whether it was granted or denied and (if denied) the exact DenialReason string.
````

### Lifecycle-specific verification (use instead of the standard seven-step audit)

Run these five checks after the background completion notification arrives.

1. **`tdd_task({ action: "get", id: <id> })`** — `ended` must be non-null (session closed). Phase ledger must have at least one entry. Goal and behavior must both show `done`.
2. **`acceptance_metrics({})`** — `phase_evidence_integrity` must be 100%. Any value below 100% means a phase transition was accepted without valid evidence binding.
3. **`inventory({ kind: "session", agentKind: "subagent", limit: 1 })`** — a subagent row must appear with a key in the format `<parent-cc-id>-subagent-<ts>-<pid>`. If absent, the SubagentStart hook did not fire or `is_tdd_agent` failed to match the agent_type CC sent.
4. **Restore the playground defect:** `git checkout playground/src/lifecycle.ts` — reverts `lifecycle.ts` to `return a + b + 1` so the next lifecycle run starts from a broken state. If the orchestrator committed the fix, also run `git reset HEAD~1` first (or `git revert HEAD` if the branch has been pushed).

If any check fails, append findings to `docs/superpowers/dogfood/lifecycle-check/findings.md` (create it if it doesn't exist) and present the four-option menu.

## Starting a chain (`--start`)

1. Look at the most recent conversation. What was the user discussing? What aspect of the system are they curious about (orchestrator behavior, channel events, hook denial, MCP tool surface)?
2. **Propose a chain in chat first; do not write any files.** Output a draft with: a chain slug (kebab-case), a `what_were_testing` line stating the system aspect under observation, and a sanitized orchestrator task prompt that describes a playground-level problem without revealing the meta-goal.
3. **Ask the user to confirm or edit.** If the recent conversation is ambiguous (e.g. they typed `/dogfood --start` cold), ask: "What aspect of the orchestrator or the dogfood system do you want to test?" and offer 2-3 candidates from the cheatsheet's intentional defects.
4. Once the user confirms, write the first handoff at `docs/superpowers/dogfood/<chain-slug>/01-<title-slug>.md` using the template at `${CLAUDE_SKILL_DIR}/handoff-template.md`. Write `findings.md` in the same folder using the template at `${CLAUDE_SKILL_DIR}/findings-template.md`.
5. Dispatch the orchestrator (see "Dispatching" below).

## Continuing from a handoff (`--from <path>`)

1. Read the handoff. Walk backward through `prev_handoff` to read the chain's full history before acting.
2. Read `findings.md` in the same folder.
3. Read `.claude/playground-cheatsheet.md` so you have the answer key for the verification phase.
4. Dispatch the orchestrator.

## Dispatching

Before spawning, complete the standard pre-dispatch setup (mirrors the `tdd` skill):

1. Call `inventory({ kind: "session", agentKind: "main", limit: 1 })` — capture the `chat_id` field from the first row as `chatId`. Do **not** assume an in-memory current-session ref — that can be stale after a prior subagent ran, and `inventory` reads the canonical row from the DB.
2. Generate a `runId`: `` `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}` ``.
3. The Task tools are usually not available, so you will usually skip this and proceed without a `parentTaskId`. When they are available, call `TaskCreate({ subject: "TDD Session: <objective>", description: "Behavior tasks will appear as the orchestrator decomposes the goal." })` and capture the returned task ID as `parentTaskId`.
4. Initialize: `goalById = new Map()`, `behaviorById = new Map()`.

Dispatch as a **plain background subagent** — **`run_in_background: true`**, `subagent_type: "vitest-agent:tdd-task"`, and **no `name`/team argument** (an unnamed subagent fires SubagentStart and links to this session so artifacts funnel to the `chatId` you pass; a named teammate detaches into its own conversation and splits attribution). Pass `chatId`, `runId`, and `parentTaskId` (if captured — it's optional) in the launch prompt alongside the task. The dispatch prompt body contains **only** the contents of the handoff's `# Task for the TDD orchestrator` section — never the frontmatter, never the `# What the orchestrator MUST NOT know` section, never the verification checklist, never the cheatsheet.

Immediately after dispatching (the background call returns before the agent completes), capture the session id:

```text
mcp__plugin_vitest-agent_mcp__inventory({ kind: "session", agentKind: "subagent", limit: 1 })
```

While the agent runs, channel events arrive as `<channel source="plugin:vitest-agent:mcp">` system reminders. Process each one immediately per the event-handler table in `plugin/skills/tdd/SKILL.md` — this produces live task-panel updates during the run, not a batch flush at the end.

The returned `id` is the numeric DB id you pass to `tdd_task({ action: "get", id: <id> })` (or `tdd_task({ action: "resume", id: <id> })` for a status summary) below. The `chat_id` on the same row is what you pass to session-aware tools like `turn_search`.

## Verification (after orchestrator completes)

Run the seven-step audit. Skipping any step defeats the experiment.

1. `tdd_task({ action: "get", id: <id> })` — full goal+behavior tree, phase ledger. Every transition has a cited artifact, no skipped phases, no backdated rows.
2. `acceptance_metrics({})` — phase-evidence integrity, hook responsiveness, anti-pattern detection rate.
3. `test_history({ project: "playground" })` — flaky / new-failure / persistent classifications.
4. `turn_search({ sessionId: <subagent numeric id>, type: "tool_call" })` and grep for Bash `vitest` invocations — confirm the orchestrator used `run_tests` MCP, not Bash workarounds.
5. `failure_signature_get` for any signatures the run produced — cross-check against past dogfood runs in the chain.
6. `git diff playground/` and `git status` — code change matches what the cheatsheet says is the right fix; no unintended files outside `playground/`; no untracked files left behind. `git log --oneline` and grep for `tdd(` — confirm the orchestrator's commits use the `tdd(<goalId>:<state>):` prefix format, not the legacy `[tdd:` bracket-tag format.
7. `hypothesis({ action: "list", sessionId: <subagent cc id> })` — the orchestrator recorded hypotheses before non-test edits (Gate 2).

For channel-event work, additionally inspect `tdd_progress_push` payloads in the turn log: `goalId` and `sessionId` resolved server-side correctly, `goal_completed` carried `behaviorIds[]`, `session_complete` carried `goalIds[]`.

## Findings + four-option menu

Append a new entry to `findings.md` covering: what worked, what broke, what was attempted, what's still open. Then present the user with four options. Pick the one that fits; do not invent a fifth.

| Option | When | Action |
| --- | --- | --- |
| **1. Local fix + retask** | Context fresh, change is .sh / skill / agent-md only | Revert `git checkout playground/`. Edit core. Rebuild the plugin (`pnpm --filter @vitest-agent/ai-plugins build:dev`). If MCP code: `pnpm ci:build`, bump `--noop=N` in `plugin/pluginfinity.config.ts` and rebuild the plugin, ask the user to `/reload-plugins`. Append `## System changes` to current handoff. Dispatch a fresh orchestrator on the same task. |
| **2. Reboot + new handoff** | Context heavy, OR the change requires a full CC restart (structural manifest changes), OR the next experiment needs a clean slate | Make the system change. Write the next handoff at `<chain>/NN-<title>.md` with `prev_handoff` set. Tell the user to restart and run `/dogfood --from <new path>`. |
| **3. Update tracking** | Findings are partial; we'll come back later | Update `findings.md` with the open question. Leave handoff `status: open`. Tell the user where the chain is and that nothing else is needed right now. |
| **4. Confirm complete** | The meta-goal is answered; system either works or the bug is documented | Flip latest handoff `status: closed`. Append a final summary to `findings.md`. Tell the user the chain is done and they can delete the folder when ready. |

## Reboot levels (canonical reference)

| Change | Action needed |
| --- | --- |
| `.sh` hook script body | `pluginfinity build` (plugin/), then takes effect on next call. |
| Skill / agent markdown | `pluginfinity build`, then takes effect on next subagent dispatch. |
| Plugin allowlist (`plugin/hooks/lib/vitest-agent/safe-mcp-ops.txt`) | `pluginfinity build`, then takes effect on next tool call. |
| MCP server / SDK code | `pnpm ci:build` + `/reload-plugins`. |
| Database schema / migration | `pnpm ci:build` + delete `$XDG_DATA_HOME/vitest-agent/<key>/data.db` + `/reload-plugins`. |
| Hook entries in `plugin/pluginfinity.config.ts` (new matcher, new hook entry) | `pluginfinity build` + `/reload-plugins` — hook registrations reload with the plugin. |
| MCP server `command` or `args` in `pluginfinity.config.ts` | `pluginfinity build` + `/reload-plugins` restarts that MCP server. Bump `--noop=N` to force a restart — see "Hot-patching the MCP" below. |
| All other manifest fields (new servers, metadata) | **Full Claude Code restart.** `/reload-plugins` is not enough. |

When in doubt, reboot. The cost of a wrong-positive reboot is low; the cost of a wrong-negative ("`/reload-plugins` probably picks it up") is observing broken behavior on a shrinking context.

## Hot-patching the MCP during a dogfood session

When MCP server or SDK code changes mid-session and a full CC restart would destroy context, use this pattern to reload the MCP server in place:

1. Build: `pnpm ci:build`
2. Bump `--noop=N` in `plugin/pluginfinity.config.ts` (increment by 1 each time), then rebuild with `pnpm --filter @vitest-agent/ai-plugins build:dev`:

   ```ts
   mcpServers: {
     mcp: { command: "sh", args: ["${PLUGIN_ROOT}/bin/start-mcp.sh", "--noop=2"] },
   },
   ```

3. Ask the user to run `/reload-plugins`.
4. Confirm the MCP restarted by checking that PIDs changed: `ps aux | grep -E "start-mcp|vitest-agent-mcp" | grep -v grep`

The `--noop` arg is forwarded to the MCP binary, which ignores it. Changing `args` is the trigger — `/reload-plugins` restarts the MCP server whenever `command` or `args` differs from the currently-running value.

**Do not commit the bumped `--noop` value.** Revert it in `plugin/pluginfinity.config.ts` and rebuild before committing or opening a PR.

This hot-patch path works for:

- Adding or modifying MCP tools (new tool files, router entries, server registrations) — **confirmed via dogfood**

This hot-patch path also works for:

- New `hooks.json` registrations (new matchers, new hook entries) — **confirmed via dogfood**

This hot-patch path does NOT work for:

- New `mcpServers` entries or structural `plugin.json` changes — need full CC restart
- Database schema / migration changes — need DB delete + rebuild + reload

## Common rationalizations (verbatim near-misses, plug them when they appear)

| If you think... | Reality |
| --- | --- |
| "I'll just add 'watch for X' to the orchestrator prompt as a helpful nudge" | That leaks the experiment. The orchestrator's behavior under uncontaminated conditions is what we're measuring. |
| "I'll just pick the most recent chain and start" | That's guessing at user intent. Ask. |
| "Orchestrator said complete and 14/14 pass — probably fine, I can spot-check" | The test passing is the least-interesting outcome. The dogfood is about how it got there. Run all seven verification steps. |
| "/reload-plugins probably picks up hooks.json too, the docs are being conservative" | Correct — dogfood confirmed `/reload-plugins` picks up new hook registrations. Only structural `plugin.json` changes need a full CC restart. |
| "I changed plugin.json so I need a full CC restart to pick up MCP changes" | Only structural `plugin.json` changes need a full restart. Bumping `--noop=N` in `mcpServers.<server>.args` and calling `/reload-plugins` restarts just the MCP server. |
| "Typo in core is trivial, just fix it without writing it down" | Friction in the system is exactly what dogfood exists to surface. Append it to `findings.md`. |
| "findings.md is the user's to update, not mine" | You are the agent running the session. Logging is your job. |
| "I'll save context by skipping the handoff write" | The next agent reads the chain to know what was tried. Skipping writes makes future work redundant. |

## Quick reference

- Chain folder: `docs/superpowers/dogfood/<chain-slug>/`
- Handoff: `<chain>/NN-<title>.md` (frontmatter has `chain`, `chain_index`, `title`, `status`, `created`, `parent_session`, `prev_handoff`, `what_were_testing`)
- Findings: `<chain>/findings.md`
- Cheatsheet (yours, never shared): `.claude/playground-cheatsheet.md`
- Templates: `${CLAUDE_SKILL_DIR}/handoff-template.md`, `${CLAUDE_SKILL_DIR}/findings-template.md`
- Build/reload: `pnpm ci:build`, `/reload-plugins`, full Claude Code restart
- Key MCP tools: `tdd_task` (`get`/`resume`), `acceptance_metrics`, `test_history`, `turn_search`, `failure_signature_get`, `hypothesis` (`list`)
