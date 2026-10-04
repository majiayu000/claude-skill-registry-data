---
name: patpat-learn
description: Convert a recurring failure, correction, or verification gap from the active task into the smallest durable constraint. Use when the same engineering mistake could recur and should be prevented structurally.
---

# Patpat Learn

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [encode lessons](../patpat-loop/principles/encode-lessons.md), [repository truth](../patpat-loop/principles/repository-truth.md), and apply the [learning playbook](../patpat-loop/playbooks/learning.md).

Use evidence from the active task: user corrections, failed verification, repeated retries, review findings, or verifier defects. Separate one-off facts from recurring failure modes. Encode only the latter.

Choose the strongest narrow mechanism that prevents recurrence: type or contract, focused test, lint or validator rule, deterministic script, workflow instruction, then documentation. Prefer enforcement over reminders and update an existing authoritative location before creating a new file. Mine this conversation for recurring working-style or failure rules. Propose edits to existing files only. Present the proposal and wait for approval. Do not auto-apply. There is no new SKILL.md and no *-mode mint on this path. Never create a new SKILL.md. Never mint a personal `*-mode` skill.

Do not mine unrelated conversations or store sensitive task data. Do not modify shared or user-global rules without explicit authority. Verify that the chosen mechanism detects or prevents the original failure, then report what remains unprotected.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
