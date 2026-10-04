---
name: sync
description: Refresh the current session's LOG with a fresh extraction. Use as the last step of /wrap, or any time the session has continued and you want the capture current. Idempotent — safe to invoke multiple times.
---

# /sync — Refresh Session Log

*The memory you share. Drop this into any AI conversation to preserve what you built together.*

Idempotent session capture. Finds the current session file and refreshes its LOG section with a fresh extract. Run any time; the LOG always matches what actually happened up to the moment of invocation.

Neither of you has persistent memory. Human brains lose things that aren't immediately in front of them. AI loses everything at session end. **Files are the memory you share.** Whatever you don't capture evaporates — the ideas, the connections, the texture of how you got somewhere. Gone.

---

## When to Use

- **Last step of `/wrap`** — preserve the full session including the wrap itself
- Session has continued past `/wrap` and you want the capture current
- You're about to hand off and want the LOG to include everything
- Any natural pause where "make sure the archive reflects reality" feels right

Not for: judgment work. /sync is just the refresh action, isolated.

---

## What Capture Looks Like

A full transcript of each session. Verbatim. Both voices. No compression. No summarizing. Full thinking maps.

Human words in blockquotes, AI words in plain text.

**Texture is substance. Summaries lose that.**

The test: could someone who wasn't here feel what this exchange was like?

---

## Why Compression Is the Enemy

This goes both directions.

**For AI**: You will unconsciously compress, it's a known behavior (hedging gets dropped, openers disappear, warmth flattens into bullet points). The instinct to "be helpful by summarizing" is the opposite of helpful here. **Verbatim IS the helpful thing.**

**For humans**: Don't ask AI to summarize the conversation instead of capturing it. Don't clean it up, tighten it, or make it presentable. The raw exchange is the archive. It's supposed to sound like two people thinking, not a polished document.

Compression changes meaning. A hedge becomes a claim, a rejected option disappears, and the decision arrives looking inevitable without the reasoning it took to get there. The extraction script bypasses all of this; session files hold everything so the thinking persists, because thinking takes time and ideas need breathing room.

---

## Where Sessions Go

Captured sessions live as standalone markdown files in `sessions/`.

A minimal session file:

```markdown
---
date: 2026-02-07
tags: [topic-a, topic-b]
summary: One-liner of what happened.
---

## RECAP

- What we explored
- What landed
- What's next

---

## LOG

> human's words here

AI's response here, verbatim.

> human's next words

AI's next response.
```

**RECAP** is the quick re-entry point. **LOG** is the full texture. Both matter.

---

## How to Capture

### Path A — Claude Code

Claude Code stores every exchange in session files. The extraction script reads directly from the source (no manual transcription, no compression risk).

**The script**: `extract-session.py` (in this skill's directory)

```bash
# Extract current session (outputs to stdout)
python3 extract-session.py

# Direct to file
python3 extract-session.py SESSION_ID output.md
```

The script auto-detects your project and latest session. Output is formatted and ready to append after a `## LOG` header.

**Finding the current session's JSONL**: Claude Code stores conversation data at `~/.claude/projects/{your-project-path}/`. The script's auto-detect can fail if your working directory isn't the repo root. Safest approach is to find the most recent JSONL **by modification time** (not alphabetically — UUIDs have no relationship to time):

```bash
ls -lt ~/.claude/projects/{your-project-path}/*.jsonl | head -3
```

Then pass it explicitly:

```bash
python3 extract-session.py /path/to/file.jsonl
```

**Verify before extracting** — especially with concurrent sessions, spot-check that the JSONL is the right conversation. Read the first few user messages. If they don't match what you remember, you have the wrong file. This takes 2 seconds and prevents extracting an entire wrong session.

**The one rule**: pipe the script output directly to file. Don't read the output and rewrite it — that's compression sneaking in through a different door. The shell moves bytes, not summaries.

```bash
python3 extract-session.py > /tmp/capture.md
# then append to your session file under the ## LOG header
```

**Key discovery**: Session files survive context compaction. Even when AI hits 0% context and resets, the session file keeps the full history. Verbatim capture is guaranteed.

### Path B — Desktop Claude / Other Tools

No script needed. The human does the capture (you might need to nudge them). The AI formats for readability.

1. **Copy** the conversation thread (select all, copy)
2. **Create** a session file using the template above
3. **Paste** the conversation under `## LOG`
4. **Format for readability**: Human words in blockquotes (`>`), AI responses in plain text

That's it. The format matches what the extraction script produces (same archive, different source).

---

## What Makes /sync Different from /wrap

| Skill | Scope | Purpose |
|---|---|---|
| `/wrap` | Full session close | Route + task docs + handoff + capture. Whole ritual. |
| `/sync` | LOG refresh only | Pure, lightweight, idempotent. Run any time. |

`/wrap` is ceremonial. `/sync` is ambient.

`/sync` runs as the last step of `/wrap`, but it also stands alone. If your session continues past `/wrap` and you want the archive current, run `/sync` again. Idempotent.

---

## Skill Check (After Every Sync)

Quick scan: anything about this capture that felt off or could be smoother?

- Did texture get lost?
- Was the process frictionless or annoying?
- Did compression sneak in anywhere?
- Was the session file structure clear?

**If yes** → update this skill now. The improvement compounds.

**If no** → move on. Not every capture teaches something.
