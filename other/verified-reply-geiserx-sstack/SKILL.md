---
name: verified-reply
description: Draft a reply the user will send as themselves, with every factual claim checked against a live source first and posted only after they approve the exact text. Use when asked to answer a message, reply to a thread, PR or ticket comment, or check a reply the user wrote.
argument-hint: "<the message or thread to answer, or the user's own draft to check>"
---

## Running in Codex

This is the Codex copy of this skill. Read the rest of it with these translations:

- Agents launched in parallel: spawn each one with `spawn_agent` before waiting on any, then collect the
  results with `wait_agent`. Tell every agent you spawn not to spawn agents of its own. If subagents are
  unavailable, run each lane yourself, one after another.
- "Your default model" and "your strongest model": spawn the agent with an `agent_type` whose role file in
  `~/.codex/agents/` sets `model` and `model_reasoning_effort`. An agent without a role runs on the
  session's model.
- A slash command such as `/name`: mention the skill as `$name`.
- This repository's hooks and `.claude/` paths are for Claude Code only, and nothing here installs a Codex
  hook. A loop runs one pass per invocation, saves its state and reports how to resume.
- `CLAUDE.md`: also read `AGENTS.md`, which is the file Codex loads.

# verified-reply

A reply that goes out under the user's name must be right, and must read as theirs. Verify first, draft second,
post only on their approval of the exact text.

## Order

1. **Read the thread and the asker.** Who asked, what they already tried, what their message shows they know, and
   what they actually asked. Done when you can state the question in one sentence.
2. **List the claims.** Every factual statement the reply needs: a behaviour, a number, a date, an owner, a
   decision, a command that works. Done when each claim is one line.
3. **Check each claim against a live source.** Repository facts against the current code at the right ref, not a
   stale clone or memory; anything executable by running it; tickets and wiki pages through their own tools;
   earlier decisions in the team's own record, including whether the user already settled this question. Give each
   claim one verdict: `verified` with the source, `soften` (state it as belief) or `cut` (unverifiable and not
   needed). Done when no claim rests on memory alone.
4. **Draft in the user's voice.** Two to four lines by default, in the register of the thread. Answer what was asked
   and stop. One number per claim, plain words, no headings or lists in a chat message, hedges only where the
   evidence hedges. When a line corrects the reader, give the one check they can run to see it. Start sentences with
   the point and end on substance. Done when every sentence carries information.
5. **Hand it over.** The reply, then separately one line per claim with its source, so the user can defend each line.
   Flag what you cut or softened. The evidence never goes into the message itself. Done when the user has both.
6. **Post on approval only.** Post the exact text the user approved, through the tool for that surface. If they
   edited it, check any claim the edit added or changed, say what the check found, and post their version once
   they approve it. Then read the posted item back and confirm it rendered: code in backticks, links
   live, formatting intact. Done when the posted text matches the approved text.

## Rules for the text

- Write as the user, in the first person. Whether to say how the reply was drafted is the user's call; follow the
  place's own rule when it has one.
- No service phrases ("happy to help", "let me know if", "hope this helps"), no grading of the reader ("good catch",
  "you're right"), no transition filler ("that said", "it's worth noting").
- A senior reader's own field is never explained to them.
- When the reader pushed back on the previous reply, the next one is shorter.
- Never reopen something the reader already settled.
- A link the user will paste by hand is a bare URL with nothing attached to it; a link posted through an API may use
  the surface's link syntax.
- Re-run a check that is more than a day old before posting, when it is cheap.
