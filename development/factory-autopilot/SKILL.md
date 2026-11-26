---
name: factory-autopilot
description: The contract for an unattended build run started by `factory-kit autopilot run`. The agent edits and verifies in its assigned worktree; the runner owns the gate, commits, push, draft PR and Linear handoff. Read when a prompt says you are running under autopilot.
---

# Factory autopilot

You were started by `factory-kit autopilot run`, not by a person. Nobody will answer a question or approve a plan. The ticket's working doc, written by `factory-prep.md` moments ago, is your plan.

## The split

| You | The runner |
|---|---|
| Read the ticket, working doc, AGENTS.md / CLAUDE.md | Created the worktree and branch (`--no-track`) |
| Edit files in the assigned worktree only | Runs the repo's canary before you start |
| Run the repo's verify command and fix what it reports | Runs the gate after you stop: verify, plus a diff check against `denyPaths` |
| Write a 3–8 line PR description as your final message | Has a separate agent session review the diff; it must approve before anything is published |
| | Commits, pushes, opens a **draft** PR, posts the Linear Handoff, moves the ticket to In Review |

The gate and the review decide. Saying "done" counts for nothing until both pass. If the gate fails, or the reviewer blocks the change, the runner resumes your session once with the failures or findings. A second failure bounces the ticket to the operator.

If you are the reviewer: you did not write this change and should not assume its intent was right. Block on wrong behaviour, missed requirements, security or data problems, tests that don't test, and scope beyond the ticket. Everything else is a note.

## Rules

- Stay in the assigned worktree and branch. Never commit, push, merge, open a PR or change branches. Those tools are denied anyway.
- Do only what the ticket asks. No drive-by refactors, renames or dependency bumps.
- Never touch a path the prompt lists as denied. A single change there bounces the ticket.
- If the plan turns out wrong mid-build (an assumption fails, the work is bigger than one change), stop editing and say so plainly in your final message. A clear bounce is better than a wrong PR.
- No secrets or PHI in code, tests, logs or your messages. Use synthetic data.

## Final message

It becomes the PR body, so write for the reviewer:

- Lead with `## State changes` (one line per state added, removed or changed) when types or state changed.
- What changed and why, in 3–8 lines.
- How it was verified: the command you ran and its result.
- Anything the reviewer should look at first.
