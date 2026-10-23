---
name: spin-off-side-task
description: Hand a side task found in the current thread to a new agent in its own Herdr worktree, with a brief that gives it the thread's context. Use when the user asks to spin off or hand off a fix, or to make a separate PR for something this thread found, while this session keeps its own task.
---

# Spin off a side task

A **side task** is work this thread found but does not own: a slow CI job spotted while reviewing a PR, a bug next
to the one being fixed. It gets its own branch, worktree and agent, so this session's branch and focus stay
untouched. The new agent starts with nothing but the brief and the repo, so the brief is the whole hand-off.

Run every command from this session's pane. Check `test "${HERDR_ENV:-}" = 1` first; if it fails, tell the user
this session is not inside Herdr and stop.

## 1. Write the brief

Write it to a temporary file. The new agent must be able to act on it without asking what it means:

- **Task**: what to change and what the result should be, in one or two sentences.
- **Evidence**: what this thread found, copied in full: log lines, numbers, file paths, PR and issue numbers,
  commands that reproduce it. Mark guesses as guesses and say what would confirm them.
- **Decisions**: every choice the user already made in the thread, and options they turned down with the reason,
  so the new agent does not reopen them.
- **Scope**: where the side task ends, and which parts stay with this session.
- **Finish**: what the user asked for. Default to "commit locally with small atomic conventional commits; do not
  push or open a pull request". Allow a push or PR only when the user asked for one, as in "make a new PR".
- **Source**: a pointer back to this thread, so the new agent can read more when the brief leaves a question open:

  ```text
  This side task comes from Herdr pane <HERDR_PANE_ID>. Read it for more context with:

      herdr pane read '<HERDR_PANE_ID>' --lines 400 --source recent-unwrapped
  ```

Done when a reader with only the brief and the repo could start the work.

## 2. Pick the target

The side task usually lives in this repo. When it belongs in another one, such as "add this to my skills repo",
find that repo's local checkout: `herdr workspace list` and the `cwd` of its panes show the checkouts open in Herdr.
If no checkout exists, ask the user where it is, and leave cloning to them.

Pick a short kebab-case branch name for the side task. The base is `origin/main`. Use `HEAD` only when the side task
is in this repo and needs commits that exist only on this branch, and say so in the brief.

## 3. Launch in the background

Creating the worktree and starting the agent takes about a minute and needs nothing from the thread, so hand it to a
background subagent with the Agent tool. Give it this prompt, filled in:

```text
Follow <this skill's base directory>/launch.md with:
- brief: <brief file>
- repo: <checkout path>
- branch: <branch>
- base: <origin/main or HEAD>
- caller pane: <HERDR_PANE_ID>
```

Tell the user in one line that the side task is launching, then go back to this session's own task.

## 4. Report

When the subagent reports back, relay the branch, workspace ID and agent name in one or two lines. If it stopped on
a question, such as a `--trust-repository` prompt or a blocked agent, show the user the question and leave the
answer to them. The side task belongs to the new agent now, so leave its files and branch alone.
