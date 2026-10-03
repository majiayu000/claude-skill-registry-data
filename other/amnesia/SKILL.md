---
name: amnesia
description: Use when the user returns to a session and needs to be reoriented, including requests such as "amnesia", "what did I miss", "recap the session", "where were we", "catch me up", "what happened while I was away", or "what was I doing". Reports when the session started, the last user message verbatim, what happened since it, and any earlier changes still worth knowing.
disable-model-invocation: true
---

# Amnesia

## Overview

Reorient the user after they stepped away. Report what the session is, where it left
off, and what changed while they were gone.

Answer from the conversation already in context. Do not re-run builds, re-read files,
or start new work to produce this recap.

## Output

Report these four sections, in order.

### Session started

When this session began. Use timestamps available in the conversation context. If no
timestamp is available, say so plainly instead of guessing — an approximation stated
as fact is worse than "unknown".

### Last user message

When the user last wrote, and the verbatim text of that message — the one before this
request, not this request itself. Quote it; do not paraphrase. If it was long, quote
the first few lines and mark it as truncated.

### Since then

What happened after that message: files created or modified, commands run and their
outcome, conclusions reached, questions asked and still unanswered. Include failures
and abandoned attempts — those are the part a returning user is most likely to have
missed.

### Also worth knowing

Significant changes from earlier in the session that are still relevant: decisions
made, approaches reversed, work left unfinished, anything agreed to but not yet done.
Skip this section entirely if the session holds nothing beyond what the previous
section already covered.

## Rules

- Be brief. This is a status readout, not a transcript.
- Never invent timestamps, file names, or outcomes. Unknown is an acceptable answer.
- Distinguish what was done from what was only proposed.
- If the session has no prior user message, say that this is the first turn and stop.
