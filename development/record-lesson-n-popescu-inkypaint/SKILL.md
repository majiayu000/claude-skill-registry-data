---
name: record-lesson
description: "Record what ScarletNX work taught, where the next session will look for it. Use after a bug took more than one attempt to find, when the same mistake happened twice, when a debugging technique worked, or when the user corrects how work is done."
---

# Record a lesson

A lesson left in the chat is gone next session. Put it where it will be read.

| Lesson | Where | Form |
| --- | --- | --- |
| How a console component behaves, proven on the game (a service answer, an SDK expectation, a GPU rule) | A comment at the code that depends on it, saying why | One or two lines, naming the SDK function or Switchbrew page |
| A bug pattern a future change could reintroduce | CLAUDE.md, "Lessons that cost a session" | One bullet: the trap and the rule |
| A step of a procedure that was missed | The skill that covers it (`snx-build`, `snx-run`, `snx-crash`, `snx-service`) | An imperative line with the reason |
| Something that must never happen | `.claude/hooks/guard.py` | A rule with the message to show |
| A debugging script that worked | `tools/`, with a docstring and usage, mentioned in docs/DEVELOPMENT.md | The scratchpad is wiped between sessions |
| Reviewer knowledge (a past bug shape in a domain) | The matching `.claude/agents/review/snx-*-reviewer.md`, "Known past-bug shapes" | One bullet |
| Status, plan, the user's choices | docs/ROADMAP.md, and the session memory for things not in the repo | Absolute dates |

Prove it first: a rule from one occurrence is written as what that occurrence needed, not as a general rule, until a
second case confirms it. When an existing lesson turns out wrong, correct it rather than adding a contradicting one.

Commit lessons with the work that found them, or alone with a subject like "Document ...".
