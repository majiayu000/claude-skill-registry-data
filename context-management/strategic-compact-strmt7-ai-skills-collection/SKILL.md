---
name: strategic-compact
description: Checkpoint long, multi-phase work before context pressure or session handoff when losing constraints, evidence, or completed-item coverage would risk incorrect continuation.
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  source-commit: 846ffb75da9a5f4e677d927af1ad4a1951652267
  revision-status: experimental-unbenchmarked
---

# Reliable context checkpoints

Create a small task-local checkpoint when a substantial phase finishes, the
runtime signals context pressure, or another session must resume the work.
Use actual runtime signals when available; tool-call counts and response latency
do not measure remaining context. Do not install global hooks or modify personal
memory merely to make a checkpoint.

## Persist what changes continuation

Record the current objective, accepted corrections, authorization boundaries,
hard constraints, and next actionable step. Preserve exact deadlines and
not-before times with a timezone; elapsed conversation time is not permission.
Distinguish required missing input from optional preferences.

For large collections, maintain a ledger of stable item IDs with explicit states,
such as pending, reviewed, revised, and evaluated. Record the total item universe
and evidence per item. Enumerating or opening a file is not completing its review.
Keep archived records if sources disappear, and invalidate affected conclusions
when their source commit or content hash changes.

Link the files, commits, commands, test logs, and artifacts needed to justify
completed work. Record failed checks, unresolved symptoms, active process IDs,
pending approvals, and meaningful decisions. Prefer pointers to raw evidence over
repeating large tool outputs or preserving every abandoned thought.

Write and verify the checkpoint before requesting compaction or a handoff.
Use the runtime's supported mechanism if one exists; the checkpoint remains useful
without a `/compact` command or a hook script.

## Resume without losing scope

Read the latest user instruction, repository guidance, checkpoint, and affected
worktree state. User corrections take precedence over older checkpoint text.
Verify volatile facts that affect the next action, such as remote heads, active
processes, access, and time gates. Recheck saved evidence if its content or input
signature changed; do not repeat already justified work solely because a new
session began.

Continue from the next eligible incomplete item. Keep deferred work visible until
its actual condition is satisfied. Update the checkpoint after each bounded
batch, and distinguish achieved goals from work that merely stopped.
