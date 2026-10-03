---
name: rudhra-learn
description: Capture human-approved learning from every session or important message. Use when the user says "rudhra learn", "capture this lesson", "make Rudhra better", "what should we remember", "end session", "session recap", or asks for the template to learn from a conversation without silently editing itself.
---

# Rudhra Learn

Use this skill to turn a session into approved memory and reusable template improvements.

## Learning Loop

1. Review what happened in the session:
   - user preferences revealed
   - project-specific facts discovered
   - repeated workflow pain
   - tool/config/setup problems
   - commands or checks that worked
2. Sort each candidate:
   - `project-context`: belongs in this project's `agent/PROJECT_CONTEXT.md`
   - `project-instruction`: belongs in this project's `AGENTS.md` or `CLAUDE.md`
   - `template-promotion`: reusable across future projects; draft for `agent/PROMOTE.md`
   - `tool-registry`: new or changed tool; draft for `agent/TOOL_REGISTRY.md`
   - `skill-change`: repeated procedure; draft a skill improvement
   - `discard`: too specific, outdated, private, or not useful
3. Present the draft learnings to the user for approval.
4. Apply only approved project-local updates.
5. For template-level updates, append approved rows to `agent/PROMOTE.md`; do not edit the master template directly.

## Approval Wording

Ask clearly:

```text
I found these possible learnings. Which should Rudhra keep?
```

Then list short numbered candidates with destination and reason.

## Safety Rules

- Never save secrets, tokens, private keys, or payment/contact details.
- Never promote a lesson that depends on one project's accidental structure unless it generalizes.
- Never silently edit global files or the master template.
- Prefer exact commands, paths, and observed failures over vague advice.
