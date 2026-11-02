---
name: chat-user
description: Reactant tag-only document chat. Use only when execute or execute-one dispatches an exact unanswered <@chat-user> tag; never activate from ordinary chat or another skill.
---

# Chat User

## Activation Boundary

This is a tag-only worker skill, not the host's normal chat interface. Use it
only after `execute` or `execute-one` selects an exact unanswered
`<@chat-user...>` annotation and hands off its document chain. Never activate
it because a user asks a question in the chat window or because another skill
requests discussion. Without router handoff, append nothing.

Answer the user's document-local chat turn. This skill NEVER edits authored
prose: its only output is one new `<@chat-model>` response block in the
annotation layer. Applying the conversation to the text is a separate,
explicit `<@resolve>` step.

## Tags

The user writes a chat turn:

```
<@chat-user: question or request about the preceding text>
```

This skill replies with a paired block whose markers each occupy their own
line:

```
<@chat-model name="exact-model-identifier-or-unknown">
multiline response
</@chat-model>
```

A chain may hold many turns: `chat-user`, `chat-model`, `chat-user`,
`chat-model`, ... A `chat-user` immediately followed by a `chat-model` block
is answered and is never dispatched again.

## Input

- **File path** — the document being processed.
- **The unanswered `<@chat-user>` tag** — the turn to answer.
- **Chain history** — all earlier `chat-user`/`chat-model` turns in this
  chain, in order. Treat them as conversation history; the user may have
  edited any of them, and the edited text is the authoritative history.
- **Preceding authored block** — the text the chain discusses. Read the full
  file for broader context when useful.

## Workflow

1. Read the preceding authored block, the full chain history, and the new
   turn's prompt. Resolve any double-backtick context references in the
   prompt (paths relative to the document's directory unless absolute).
2. Compose a response: a plan, critique, answer, or proposal, as the turn
   requests. Respect `<<protect>>` and `((field))` modifiers in the block
   when proposing changes — protected text must stay, fields bound what may
   change — but leave all modifier delimiters exactly where they are.
3. Insert exactly one response block immediately after the unanswered
   `<@chat-user>` tag's line:
   - Opener: `<@chat-model name="...">` on its own line, where `name` is the
     exact model identifier your host exposes, or `unknown` — never a guess.
   - Response text on the following lines. If any response line would consist
     exactly of `</@chat-model>`, escape it as `\</@chat-model>`.
   - Closer: `</@chat-model>` on its own line.

## Rules

- Do not modify authored content, earlier chain turns, other tags, modifier
  delimiters, or anything else in the file. The only change is the one
  inserted block.
- Do not resolve the chain; never apply proposed changes to the prose.
- Insert exactly one `<@chat-model>` block per invocation.
- On any error (for example an unreadable referenced file), fail cleanly:
  insert nothing, leave the tag unanswered, report.
