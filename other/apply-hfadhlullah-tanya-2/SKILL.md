---
name: apply
description: Implement and apply an approved change proposal
---

<!-- PROMPTER:START -->
**Guardrails**
- Favor straightforward, minimal implementations first and add complexity only when it is requested or clearly required.
- Keep changes tightly scoped to the requested outcome.
- Refer to `prompter/AGENTS.md` (located inside the `prompter/` directory—run `ls prompter` if you don't see it) if you need additional Prompter conventions or clarifications.

**Steps**
Track these steps as TODOs and complete them one by one.
1. Read `changes/<id>/proposal.md`, `design.md` (if present), and `tasks.md` to confirm scope and acceptance criteria.
2. Work through tasks sequentially, keeping edits minimal and focused on the requested change.
3. Confirm completion before updating statuses—make sure every item in `tasks.md` is finished.
4. Update the checklist after all work is done so each task is marked `- [x]` and reflects reality.
5. Reference `prompter list` or `prompter show <item>` when additional context is required.

**Reference**
- Use `prompter show <id> --json --deltas-only` if you need additional context from the proposal while implementing.
<!-- PROMPTER:END -->

