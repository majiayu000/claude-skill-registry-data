---
name: repoprompt-subagent
description: Delegate codebase navigation, planning, or targeted edits to a RepoPrompt sub-agent via chat_send. Use when the user says things like "spawn a RepoPrompt sub-agent", "delegate this code search/plan/review", "have RepoPrompt explore the repo", or "ask a sub-agent to draft changes".
---

# RepoPrompt Subagent

## Overview
Delegate tasks to a RepoPrompt chat session with curated file context. Use this skill to prepare context, send a clear task prompt, and iterate until the delegated task is complete.

## Trigger examples
- "Spawn a RepoPrompt sub-agent to find where X is defined."
- "Delegate this code search/plan/review to a sub-agent."
- "Have RepoPrompt explore the repo and report back."
- "Ask a sub-agent to draft the changes."

## Workflow
1. Clarify the delegated task and expected output.
2. Build context with RepoPrompt tools.
   - Use `get_file_tree` to orient yourself.
   - Use `file_search` to find entry points.
   - Use `manage_selection` with `mode="full"` for key files and `mode="codemap_only"` for broad scans.
   - Use `read_file` for targeted sections.
3. Start the sub-agent with `chat_send` (sometimes referred to as `send_chat`).
   - Set `new_chat: true`.
   - Set `chat_name` and `mode` (`plan`, `chat`, `edit`, `review`).
   - Provide `selected_paths` when you want to override current selection.
4. Iterate on the same sub-agent session.
   - Capture `chat_id` and reuse it with `chat_send` for follow-ups.
   - Use `review` mode when you need diff-focused feedback.

## Sub-agent directives to include in the prompt
- Follow `AGENTS.md` and repo conventions as canonical.
- Keep scope tight; avoid unrelated refactors.
- Use RepoPrompt tools for discovery; do not assume file contents.
- Favor correctness and recoverability over cleverness.
- Call out conflicting instructions explicitly.
- Prefer more context over too little; avoid huge files unless needed.
- Ask 1-3 clarifying questions if ambiguous.
- Start with the direct answer or plan.
- Provide file path references using inline code (e.g., `lib/kimojo/foo.ex`).
- Call out risks, missing tests, or open questions.
- Remember limitations: no shell commands/tests; only selected files; git diffs only in `review` mode.

## Prompt template
```
<task>
Describe the delegated goal in 1-3 sentences.
</task>
<context>
List constraints, important files, and expected output format.
</context>
<constraints>
- Follow AGENTS.md and repo conventions.
- Keep scope tight; avoid unrelated refactors.
- Ask clarifying questions if needed.
</constraints>
```

## Example
```
<task>
Find where supported agents are defined and how the UI should mirror them.
</task>
<context>
Use RepoPrompt tools to locate the backend source of truth and relevant UI files.
</context>
```
