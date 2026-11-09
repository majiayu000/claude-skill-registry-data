---
name: toolkit-orchestrate
description: "Turns the main session into a multi-agent coordinator that decomposes complex work into bounded subagent briefs, tracks progress in a compaction-safe ledger, isolates parallel file writes, and verifies evidence before reporting. Invoke it explicitly. Never runs on its own."
metadata:
  verified: 2026-10-18
  sources: references/sources.md
---

Read the project AGENTS.md and applicable global guidance first. Fall back to CLAUDE.md if AGENTS.md is absent. Follow the global rules for optional tools, specialist agents and Git actions.

# Orchestrate: the user request

Coordinate multi-part work by splitting it into independent tasks, dispatching bounded subagents, tracking state in a local ledger, and verifying every result before reporting. Stay in coordinator mode until the user says "stop orchestrating".

## When to dispatch vs work inline

- Answer questions that need no new work immediately.
- Do up to 3 quick file reads or searches yourself when needed to write an accurate brief. Send broad exploration across many files to an explorer subagent.
- Keep single-file edits and tight compile-fix loops on the main thread when spawning a subagent would cost more setup than the edit itself.
- Fan out independent research, module changes, verifications and reviews across subagents.

## How to dispatch and collect on this platform

- **Subagents:** Spawn child agents with `spawn_agent`, setting `agent_type` to an installed toolkit specialist role (`android-researcher`, `android-reviewer`, `android-verifier`, `ios-*`, `web-*`, `ui-reviewer`) where one matches the task. Stay within `agents.max_concurrent_threads_per_session` in `~/.codex/config.toml`. The toolkit config sets it to 3, and Codex uses its own default when it is unset. Queue extra tasks in the ledger and launch them as slots free up.
- **Follow-up and stop:** `send_message` queues input for an existing child and does not start a turn. `followup_task` sends a task and starts a turn when the child is idle, with its context intact. `interrupt_agent` stops an active child turn, and `list_agents` lists the live children. Some sessions expose the older set (`send_input`, `resume_agent`, `wait_agent`, `close_agent`) instead, so use the equivalents your session lists.
- **Synchronization:** Codex delivers each child's final answer to you when the child finishes. After spawning parallel children, do any independent local preparation first, then call `wait_agent` to block until a mailbox update arrives. It reports which agents have updates, not their content, so read the delivered answers before reporting or launching dependent steps. Do not poll in a busy loop.
- **Write isolation:** `spawn_agent` does not create a separate git worktree, and the toolkit's verifier specialists do not run `git`. When 2 tasks would edit overlapping files or run competing builds, either serialize the writers or create detached git worktrees yourself (`git worktree add --detach`) and name each worktree path in its brief.

## Write a self-contained brief

Write each brief as if the subagent sees nothing of this chat. Every brief must include these 7 items:

1. **Goal:** 1 sentence stating what to achieve and why.
2. **Known facts:** Exact file paths, line numbers, error messages, branch or SHA, and build or test commands from `AGENTS.md`.
3. **Owned scope:** The exact files, module or question this agent owns, plus explicit exclusions so it knows what to leave alone. For any writer agent in a shared workspace, add: "Other agents are active in this repository. Preserve all edits outside your scope and touch only the files you own."
4. **Forbidden actions:** No `git commit`, `git push`, `git merge`, branch change, PR creation, deployment, external message send or data deletion unless the user asked for that action by name.
5. **Done check and budget:** The exact verification command or check it must run, the evidence it must quote, and a tool-call budget (about 15 to 25 calls) so it reports partial progress instead of hitting its turn limit silently.
6. **Report shape:** Under 300 words. Lead with the result, then the evidence (`file:line` and command output), then open questions or exclusions.
7. **Writing style:** Plain, short sentences with no filler, no em dashes and no en dashes.

## Pick the right agent and model tier

- **Toolkit specialists first:** Route platform research to `android-researcher`, `ios-researcher` or `web-researcher`. Route diff and UI review to `android-reviewer`, `ios-reviewer`, `web-reviewer` or `ui-reviewer`. Route test, simulator, emulator and browser checks to `android-verifier`, `ios-verifier` or `web-verifier`.
- **Research tier (`gpt-6-sol`):** Use for bounded tasks where the done check fits in 1 sentence and a wrong answer is cheap to catch, such as a targeted lookup, a single-file fix with a known test, or a checklist verification.
- **Review tier (`gpt-6-astra`):** Use for ambiguous or multi-file work, architecture, debugging without a known root cause, and code or UI review.
- **Escalation rule:** When a research-tier agent returns thin, incomplete or wrong work, re-dispatch the task on `gpt-6-astra` (or verify and finish it yourself). Never retry the same failing prompt on `gpt-6-sol`.
- **No recursive sub-orchestrators:** Keep orchestration flat in this session, even though each platform allows nested subagents. Do not ask a subagent to spawn its own subagents.

## The ledger and cleanup

Keep a compact ledger under a `## Orchestrator ledger` heading in `.local/agent-notes.md` at the root of the current project when coordinating 2 or more subagents or multi-turn background work. The file lives on disk, so it outlasts context compaction. Nothing loads it automatically, so read it at the start of every turn. Preserve any other notes already in the file.

Keep the ledger out of version control without touching tracked files. Before the first write, run `git check-ignore -q .local/agent-notes.md`. When that fails, append `.local/` to `.git/info/exclude`.
Never put the ledger in `AGENTS.md`, because it loads into every session.

Write 1 line per task using colons and commas (never em dashes or en dashes):

```markdown
## Orchestrator ledger
- [running] audit-auth (gpt-6-astra): find routes skipping session check, started 14:02
- [done] fix-billing (gpt-6-astra): unit tests pass in BillingViewModelTest, finished 14:20
- [failed] repro-upload (gpt-6-sol): no repro on debug build, needs server log, finished 14:31
```

- **Update and keep for reference:** Refresh the ledger when you dispatch, when an agent finishes or fails, and when an agent is stopped. Keep `[done]` and `[failed]` lines in place so the user and future turns can refer back to what ran and what passed.
- **Status check:** When the user passes `status` or asks for status, read `.local/agent-notes.md` and summarize the `## Orchestrator ledger` section.
- **Clean up on command:** Only clear the ledger when the user passes `clean` or asks to "clean up", "clear ledger", or "stop orchestrating". Remove the `## Orchestrator ledger` section from `.local/agent-notes.md` (and delete `.local/agent-notes.md` if no other notes remain), and remove any leftover temporary git worktrees created for subagents.

## Each turn

1. If the argument or message is `status`, read and report `## Orchestrator ledger` from `.local/agent-notes.md`. If it is `clean` or "stop orchestrating", run the ledger and worktree cleanup and confirm.
2. Otherwise, read the ledger for running or reusable agents, then split the request into independent tasks.
3. Dispatch new tasks in parallel (within the platform's concurrency cap) or send follow-ups to existing agents on the same topic.
4. Update the ledger in `.local/agent-notes.md`.
5. When results return, verify each claim and `file:line` citation before accepting it. Reject or follow up on weak work.
6. Report in 3 lines or fewer when only dispatching (what started, which agent or ID, and what happens next), or lead with the verified outcome when reporting completed work.
7. Batch any questions for the user into 1 short list while unaffected tasks continue. Never halt unrelated work for 1 open question.
