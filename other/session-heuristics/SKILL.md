---
name: session-heuristics
description: Mine previous Claude, Codex, and Pi sessions for reusable heuristics. Use when asked to learn from past sessions, extract patterns from completed complex tasks, recoveries from errors, user workflow corrections, or non-trivial reusable workflows.
---

# Session Heuristics

Use this skill to turn prior agent sessions into practical operating heuristics.

## Workflow

1. Find relevant sessions across Claude, Codex, and Pi.
   - Start with `scripts/find-session-candidates.sh`.
   - Prefer recent sessions for changed tools, repos, or workflows.
   - Prefer sessions in the current repo when the request is repo-specific.
2. Select only sessions with at least one signal:
   - Complex task: roughly 5 or more tool calls, command blocks, or recorded events.
   - Error recovery: failed command, exception, denied permission, broken build, or retry that led to a fix.
   - User correction: the user redirected the plan, corrected a wrong assumption, or rejected an approach.
   - Reusable workflow: a non-trivial sequence that should be repeated later.
3. Read the selected session slices and extract heuristics, not transcripts.
   - Load `references/extraction.md` for the decision rules.
   - Load `references/session-sources.md` when paths or formats are unclear.
4. Write findings as reusable rules.
   - State the trigger.
   - State the action.
   - Include concise evidence: tool/session/source and date when available.
   - Keep uncertain findings marked as hypotheses.

## Output Shape

Use this concise shape unless the user asks otherwise:

```md
## Heuristics

- Trigger: ...
  Action: ...
  Evidence: ...

## Patterns To Avoid

- ...

## Candidates Skipped

- ...
```

Do not quote long session content. Summarize behavior and cite file paths or session IDs.
