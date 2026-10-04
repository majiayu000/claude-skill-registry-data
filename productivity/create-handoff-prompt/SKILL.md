---
name: create-handoff-prompt
description: Create a self-contained, copy-ready handoff prompt from the current conversation, preserving decisions, rationale, unresolved questions, next steps, work status, and authority boundaries. Do not send messages or manage Codex tasks.
---

# Create Handoff Prompt

Create a prompt the user can paste into another task without requiring access to
this conversation.

This is an explicit-invocation workflow. Invoke it as
`$create-handoff-prompt`, optionally followed by the topic or outcome to
transfer.

Before composing, read `../../references/handoff-composition.md` completely and
apply its shared contract.

## Select The Scope

- Follow an explicit focus supplied with the invocation.
- If that focus is absent from the conversation or lacks enough source context
  for an accurate handoff, ask one concise missing-context question and stop.
- With no focus, use the active topic only when it is unambiguous.
- If multiple topics or referents are plausible, ask one concise scope question
  and stop.
- Exclude unselected topics instead of compressing the whole conversation.

## Stay Within The Conversation

Treat the selected conversation as the default source. This is not a research or
task-management skill.

- Inspect only artifacts explicitly referenced in the conversation, and only
  when needed for accuracy.
- Do not automatically explore repositories, browse the web, run tests, inspect
  tasks, search for a destination, send messages, or navigate between tasks.
- Do not claim the receiving task can see this conversation.
- Do not identify a destination. The user chooses it by pasting the result.

## Compose And Output

Compose a self-contained payload under the shared contract. After the payload is
complete, let `M` be the longest run of consecutive backticks anywhere in it
(`0` when none), and set the outer fence length to `N = max(4, M + 1)`.

Return exactly one outer fenced code block:

1. Start at column 1 with exactly `N` backticks followed immediately by
   `markdown` and nothing else.
2. Put the unchanged payload on the following lines. Preserve every internal
   backtick or tilde fence literally.
3. Close on the line after the payload with exactly `N` backticks and nothing
   else.

Use backticks, never tildes, for the outer fence. Write nothing outside it. Do
not save a file or write to the clipboard.

Before returning, silently verify scope, independent readability, decision and
status distinctions, rationale, authority boundaries, redaction, and the dynamic
outer-fence rule.
