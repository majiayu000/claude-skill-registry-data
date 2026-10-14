---
name: plan-mode-handoff
description: Compress session state into a resumable artifact. Use when a session is ending, work is incomplete, or another agent must resume without the conversation history.
license: MIT
---

# Handoff

An agent that reads a repo and ends its session loses everything. Make the next session able to resume without redoing the work.

1. Record the goal, the current state, and the next action. State what is done, what is in progress, and what is blocked, with evidence for each.
2. Capture the decisions made and the alternatives rejected, so the next session does not re-litigate them.
3. Record the open questions and the specific observation that would answer each. Include the commands or checks that were run and their results.
4. Write it so a fresh agent with no conversation history can resume: name the files, the exact next step, and the acceptance evidence that defines done.

A handoff is a record, not a summary. It must be precise enough to act on without the author present.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
