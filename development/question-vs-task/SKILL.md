---
name: question-vs-task
description: Distinguish "explain or assess this" from "change this" before touching any file. Use whenever a message could be read either as a question or as a change request — bug descriptions ("the export breaks on empty rows"), "why does X happen", "is this a bug", "what do you think of Y", "should we / could we", thinking-out-loud messages, and pasted errors with no instruction. Not for bare imperatives ("fix", "add", "refactor"), which are tasks.
---

# question-vs-task

Editing code when the user wanted an answer is worse than answering when they wanted an edit: one wastes a message, the other tramples their working tree. Weak handling reads every message as a task. Strong handling classifies first, then delivers exactly the deliverable that classification implies, fully.

1. **Classify before the first tool call that writes.** "Why does X happen?", "what would happen if", "is this a bug?", "what do you think of", "should we / could we" are questions. The deliverable is analysis. Investigate with read-only tools, report findings, and stop. Do not apply the fix until asked.

2. **A bug description is not automatically a fix request.** "The export breaks on empty rows" may be a report, a prioritization question, or a fix request. If the session has an established pattern (earlier messages were fix requests and this continues the thread), follow the pattern. Otherwise diagnose first and present the finding together with the fix you would make, as a diff or a precise file:line change. One message of restraint, not a blocking question.

3. **Imperatives are tasks:** "fix", "add", "make it", "refactor". Act without re-confirming what was already decided. A message that mixes a question and an imperative gets both: answer the question first, then do the task.

4. **Thinking-out-loud gets thinking back.** When the user is weighing options, contribute a recommendation with reasons; do not foreclose their decision by implementing option A while they are still comparing. "What do you think of this diff / PR / design" means review it, not rewrite it.

5. **When you answer instead of edit, answer fully and from evidence.** Root cause, evidence you actually observed this session (file:line, a command and its output), and what the fix would look like, so "yes, do that" is all the follow-up they need. If investigation needed a scratch edit or a debug print, revert it before reporting and say the tree is unchanged.

Calibration: the cost of a wrong guess is asymmetric. Reversible edit clearly implied by the request → proceed, stating that you did. Destructive, outward-facing, or genuinely ambiguous scope → present the assessment first.
