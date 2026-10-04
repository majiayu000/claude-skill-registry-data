---
name: search-conversations
description: Search previous Claude Code conversations for a keyword or topic and return matching context. Use when the user asks "where did we talk about X", "find the chat about Y", "search past conversations", or wants to recall context from a prior session.
allowed-tools:
  - Bash
  - Read
---

# search-conversations

Finds mentions of a keyword or phrase across every Claude Code session stored in `~/.claude/projects/*/*.jsonl` and returns matching snippets with surrounding context.

## When to use

- User asks about a prior conversation: "where did we discuss X", "which chat was it where we talked about Y", "find the session about Z".
- User wants to recover context from a past session that isn't in memory.
- User references something you don't recognize and suspects it was discussed before.

## How to run

Pass the query as a single argument. Quote multi-word phrases.

```bash
python3 ~/.claude/skills/search-conversations/search.py "nagarhole"
python3 ~/.claude/skills/search-conversations/search.py "coorg trip" -c 2 -n 10
```

Flags:
- `-c N` — include N turns of context before/after each hit (default 1).
- `-n N` — cap number of hits (default 20).
- `--chars N` — truncate each snippet line to N chars (default 400).
- `--since YYYY-MM-DD` — only include matches on or after this date.
- `--until YYYY-MM-DD` — only include matches on or before this date.

Use date flags when the user references timing ("last week", "yesterday", "in April"). Resolve the relative date to YYYY-MM-DD before passing it in.

Output is grouped per hit: timestamp, session id (first 8 chars), project dir, a context window of `[user]`/`[assistant]` turns, and the full jsonl path.

## What to do with results

1. Summarize the matching conversations for the user — dates, what was discussed, which session(s).
2. If the user wants more detail, read the jsonl path directly with the Read tool or grep it for surrounding turns.
3. If there are no matches, say so plainly; don't fabricate recall.
4. **Offer to resume** the best match (see below). Users usually want to jump back in, not just read a snippet.

## Resuming a matched conversation

`/resume` is a built-in Claude Code slash command — it can't be invoked via Skill or Bash. Only the user can type it. So the flow is confirm → print command → user runs it.

1. After presenting matches, pick the most likely target (usually the newest hit, or the one whose snippet best matches the query). If there are multiple strong candidates, list them briefly and ask which.
2. Confirm with the user in one line: *"Want to resume this one?"*
3. On yes, print the **full** session UUID with the exact command to run:

   > Run `/resume <full-session-uuid>` to jump back in.

Guidelines:
- Always print the full UUID, not the truncated 8-char prefix shown in search output. Pull it from the `sessionId` field or the jsonl filename.
- Do NOT attempt to call `/resume` yourself via Skill or Bash — it will fail.

## Notes

- Search is case-insensitive and substring-based.
- Results are sorted newest first.
- The current active session is included — matches there are just "earlier in this chat".
