---
name: handoff
description: Start a fresh session without losing the thread - summarize the current conversation into a file so another session (or agent) can continue the work with little context. Use when the chat got long, a topic closed, or the person says "handoff", "let's move to a new session" or "save the state so I can continue later".
argument-hint: "What the next session will be used for"
disable-model-invocation: true
author: sant1jmnz
tags:
  - productivity
  - context
  - sessions
---

Write a handoff document so a fresh agent can continue without rereading the conversation.

1. **Where to save it:** `tracking/handoffs/YYYY-MM-DD_<topic>.md` inside the user's tracking folder (if it doesn't exist, ask for the path once and create it). If there's no tracking folder, use `./handoffs/` in the current project.
2. **Content (short, no filler):**
   - Goal and current state in 3–5 lines.
   - Decisions made and why.
   - What's left to do, in order.
   - Key files and paths (reference them, don't copy their content).
   - Skills the next agent should use and the area/project to read from tracking.
   - Risks or things that couldn't be verified.
3. **Don't duplicate** what already lives in other files (tracking, plans, commits, diffs): link it by path.
4. **Redact sensitive data:** no keys, passwords or personal data.
5. If the user passed arguments, tailor the document to what the next session will do.
6. When done, give them the exact line to paste in the new session: `Read <path> and continue`.
