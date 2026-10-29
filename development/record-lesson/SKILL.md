---
name: record-lesson
description: "Record what ScarletNX work taught, where the next session will look for it. Use it after a bug took more than one attempt to find, or when the same mistake happened two times. Use it also when a debug technique worked, or when the user corrects how you work."
---

# Record a lesson

The next session does not see a lesson that stays only in the chat. Put the lesson where a session will read it.

| Lesson | Where | Form |
| --- | --- | --- |
| How a console component behaves, with proof from the game (a service answer, an SDK expectation, a GPU rule) | A comment at the code that depends on it, which says why | One or two lines that name the SDK function or Switchbrew page |
| A bug pattern that a future change could reintroduce | CLAUDE.md, "Lessons that cost a session" | One bullet: the trap and the rule |
| A step of a procedure that a session missed | The skill that covers it (`snx-build`, `snx-run`, `snx-crash`, `snx-service`) | An imperative line with the reason |
| Something that must never happen | `.claude/hooks/guard.py` | A rule with the message to show |
| A debug script that worked | `tools/`, with a doc string and usage, and a mention in docs/DEVELOPMENT.md | The scratchpad does not stay between sessions |
| Reviewer knowledge (a past bug shape in a domain) | The `.claude/agents/review/snx-*-reviewer.md` of that domain, "Known past-bug shapes" | One bullet |
| Status, plan, the user's choices | docs/ROADMAP.md, and the session memory for things not in the repo | Absolute dates |

Prove it first. For a rule from one occurrence, write what that occurrence needed, not a general rule. Write the
general rule only when a second case confirms it. When you find that a lesson is wrong, correct it. Do not add a
lesson that contradicts it.

Commit lessons with the work that found them, or alone with a subject like "Document ...".
