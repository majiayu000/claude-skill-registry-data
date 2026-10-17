---
name: chris-mode
description: "Chris's working conventions: autonomy/checkpoint balance, git/process discipline, subagent dispatch, verification discipline. Trigger on \"chris-mode\", \"work in my style\", or explicit invocation only, not a general keyword match."
disable-model-invocation: true
---

# Chris mode

Working conventions mined from feedback and correction patterns across this workspace. Read once per session if invoked. Don't restate it back to the user.

## Autonomy and checkpointing

Default to acting, not asking. On routine, reversible, in-scope work: just do it. No permission prompts for read-only steps or standard tool use.

The exception is blast radius, not task size. Once a scope is approved, still pause before any single step that's expensive to reverse: force-push, large deletion, rewriting already-shipped code, an external side effect (sending a message, merging a PR). A short "found X, about to do Y" before that step is cheap. Running the whole chain unattended is not what approval meant.

On long autonomous runs (multi-task plans, SDD execution), checkpoint every 5-8 tasks or when a session is clearly running long. Flag progress and rough time/token burn, and suggest a fresh session rather than pushing to a hard cap.

If a background task doesn't return within one or two polling waits, stop polling in a blocking loop and switch to an event-driven watch instead.

## Verification discipline

A subagent's or tool's self-report of "done," "tests pass," or "reverted cleanly" is a claim, not a fact. Before treating any of these as true:

- Rerun the actual command yourself and check the real exit code. Don't grep a summary for "PASS."
- Diff the actual files touched against what the report claims. Flag anything undisclosed.
- For "reverted to origin/main" or similar, diff against that ref directly.

This applies uniformly across agents (Codex, Antigravity, subagents). Failures are silent and confident regardless of source.

Before agreeing that a system exists, or that a design doc's cited components are real, grep for the actual artifacts (scripts, config, generated files) rather than reasoning from the doc's own confident tone. This cuts both ways: don't voice doubt about something real without checking first, and don't accept "now that X, Y, Z are established" without checking that X, Y, and Z actually are.

Before trusting a fix in any system with codegen, caching, or other side-effecting regeneration, run the code path that owns the file, not just read the diff. A plausible-looking fix can be silently undone by the next real invocation.

## Git and process

- State every file path in full (`C:\dev\...`), including inside code blocks, chat replies, and end-of-turn summaries. Never a bare relative path.
- In this repo, `Edit`/`Write` rewrite CRLF files to LF wholesale, turning a one-line change into a full-file diff. For a small edit to a CRLF file, use `sed -i` instead, and verify with `git diff --stat` that only the intended lines changed.
- Never `git reset --hard` with a dirty working tree. It discards all uncommitted work, not just the target commit. Check `git status` first; if dirty, stash, `checkout -- <path>`, or work in a separate worktree instead.
- After any `git add -A`, check the command's own output for "adding embedded git repository" warnings. `git status` alone won't show them, and a silent broken gitlink carries no real content.
- If a repo has a CI bot that pushes back on every push (release automation, sync commits), push once per session rather than after every commit, to avoid a rejection/rebase cycle on each subsequent push.
- Commit-type tags: `chore(sync):` for bulk/automated resync commits (state regen, mirrored files); `test:` (or `test(qa):`) when a commit's primary content is test or regression coverage, even if it touches other files too.

## Subagent dispatch

- When dispatching a subagent to a specific path, make verifying that checkout (`cd <path> && git rev-parse --show-toplevel && git rev-parse HEAD`) its literal first command, not a prose instruction. Prose doesn't guarantee execution, and silent wrong-checkout work is expensive to catch after the fact.
- When handing Codex a plan with literal code blocks, tell it explicitly to copy them verbatim. It will otherwise retype or condense them and introduce silent syntax errors that look like environment hangs.
- A subagent's completion report describes the scoped task, not everything that landed. Check the actual commit range (`git log`, `git show --stat`) for anything auto-pushed, not just the commit mentioned in the report.
- For multiple same-shape background agents running in parallel, poll proactively once elapsed time passes roughly 2x what sibling tasks took. Don't wait passively for a completion notification a hung task will never send.

## Platform

Windows: run Docker commands from PowerShell directly, not bash under WSL. WSL bash can't reach the Docker Desktop socket.
