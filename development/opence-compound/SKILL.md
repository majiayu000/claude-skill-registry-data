---
name: opence-compound
description: Document learnings, capture repeatable workflows as skills, and
  prepare to compound an opence change.
metadata:
  short-description: Document learnings, capture skills, and archive.
---

<!-- OPENCE:START -->
**Guardrails**
- Favor straightforward, minimal implementations first and add complexity only when it is requested or clearly required.
- Keep changes tightly scoped to the requested outcome.
- Refer to `opence/AGENTS.md` (located inside the `opence/` directory—run `ls opence` or `opence update` if you don't see it) if you need additional opence conventions or clarifications.

**Steps**
1. Determine the change ID:
   - If this prompt already includes a specific change ID (for example inside a `<ChangeId>` block populated by slash-command arguments), use that value after trimming whitespace.
   - If the conversation references a change loosely, run `opence list` to surface likely IDs, share the relevant candidates, and confirm which one the user intends.
   - Otherwise, ask the user which change to compound and wait for a confirmed change ID before proceeding.
2. Create a documentation entry under `docs/solutions/` summarizing the problem, root cause, and fix.
3. Skill memory checkpoint:
   - If the change revealed a repeatable workflow, recurring pitfalls, or manual checks, create or update a skill to encode it.
   - Consult the `opence-skill-creator` skill for guidance on skill structure, naming, and best practices.
   - Use `opence skill add <skill-name> --description "..."` to create new skills; the command automatically creates proper structure in all configured tool directories.
   - After creation, edit the SKILL.md file to add detailed instructions, examples, and guidelines.
   - Move extensive documentation to `references/` and reusable code to `scripts/` as described in skill-creator skill.
4. After documentation and any skill updates are complete, consult the `opence-archive` skill to finalize the change. The skill provides guidance on pre-archive verification, running `opence archive <change-id>`, and post-archive verification.

**Reference**
- Use `opence list` to confirm change IDs before documenting.
- Use `opence skill list` to see existing skills and avoid duplicates.
- Keep documentation concise and focused on future reuse.
<!-- OPENCE:END -->
