---
name: ask-questions-if-underspecified
description: Clarify underspecified requirements before implementation. Use only when the user explicitly invokes this skill.
---

# Ask Questions If Underspecified

Resolve decisions that could send the work down different paths before implementing.

## Workflow

1. **Inspect the request and nearby evidence.** Read relevant project files, configuration, and conventions to answer what you can through low-risk discovery. Check:
   - Objective: what changes and what stays the same.
   - Done: acceptance criteria, examples, and edge cases.
   - Scope: included and excluded files, components, or users.
   - Constraints: compatibility, performance, style, dependencies, and time.
   - Environment: language and runtime versions, OS, and build or test runner.
   - Safety: migration, rollout, rollback, and reversibility.

   A request needs clarification when any of these leaves multiple plausible paths. Finish when each uncertainty is resolved by evidence or identified as a question that could change the work. If none remain, go to step 4.

2. **Ask the blocking questions.** Ask 1–5 questions per pass, starting with decisions that eliminate whole branches. Batch independent decisions. Keep optional details behind a reasonable default. Frame a question as multiple choice or yes/no when that settles it; use open-ended prose when the answer shapes the next question. For discrete choices, use the harness's native structured-question tool when available: Claude Code `AskUserQuestion`, Codex `request_user_input`, Cursor `AskQuestion`, or the Pi `question` extension. Put the recommended choice first. When the tool is unavailable, use the [plain-prose question format](#plain-prose-question-format) for discrete choices. Finish when the highest-impact blocking decisions for this pass are asked and the available evidence answers none of them.

3. **Wait for the decisions.** While blocking answers are pending, limit work to clearly labeled, low-risk discovery that does not commit to a direction. Keep dependent commands, edits, and detailed plans pending. If the user asks you to proceed without answers, state assumptions for every remaining blocking decision in a short numbered list and ask them to confirm or correct it; proceed after that confirmation. Finish when each asked blocking decision is answered or its stated assumption is confirmed. If blocking decisions remain unasked, or an answer reveals another, return to step 2.

4. **Resume the work.** Once no blocking decisions remain, restate the agreed requirements, key constraints, and success condition in 1–3 sentences, then implement.

## Plain-prose question format

Use this format for discrete choices when a structured-question tool is unavailable:

- Number short questions and letter the choices so the user can reply `1b 2a`.
- Mark a recommended or default choice clearly. In a Markdown list, bold it; in a code block, place a bold **Recommended** line immediately above the block and tag the default inside it.
- Offer `defaults` as a fast-path reply when all recommended choices can be accepted together. Offer “Not sure — use default” when helpful.
- Separate blocking from optional questions when that reduces friction. Restate the selected choices in plain language after the reply.

Example:

**Recommended:** choose the current project defaults for both questions.

```text
1) Scope?
a) Minimal change (default)
b) Refactor while touching the area
c) Not sure — use default
2) Compatibility target?
a) Current project defaults (default)
b) Also support older versions: <specify>
c) Not sure — use default

Reply with: defaults (or 1a 2a)
```
