---
name: session-log-archaeology
description: Dig a user's original text out of their own archives when they ask for it — dated memory notes first, then session logs, then repo snapshots, then workspace logs. Includes the JSONL shape traps that produce silent zero hits, the cross-machine gap that makes a session genuinely absent, and the rule that not finding it must be reported rather than filled with a rewrite. Triggers on "翻出我记忆里的", "之前那个稿子找出来", "上次写的 XX 在哪", "去会话记录里挖". Not for writing a checkpoint (session-checkpoint) and not for maintaining the memory base (personal-secretary-memory).
version: 1.0.0
---

# Session Log Archaeology

He asks for an artifact he believes exists: a script, a version, a number, a decision.
Your job is to find **the original**, not to produce something equivalent.

## Step 1 — Search in this order

1. **Dated memory notes** (the vault / memory-area markdown). Fastest, and usually indexed.
2. **Session logs** (`.jsonl`). This is where anything that was never saved to disk still lives.
3. **Repo snapshots / tarballs** of the private memory repo — may contain files the local mirror
   does not, and may be newer than the local mirror.
4. **Workspace daily logs**, which often record what was produced even when the artifact itself
   was not persisted.

Widen the keyword set before concluding anything. Try the thing's own name, then money figures in
every notation (`五百 / 500 / 两百 / 200`), then the actors, then the product. A single keyword
returning nothing means nothing.

## Step 2 — JSONL shape traps (these cause silent zero hits)

A scan that reads the wrong field returns 0 matches and looks like "not found". Verify the shape
before trusting the result:

```
line = { type: "message", role: "assistant", content: [ { type: "output_text", text: "..." } ], ... }
```

- `content` is a **top-level field**. Reading `obj["message"]["content"]` yields nothing forever.
- Block type is **`output_text`**, not `text`. (User turns use `input_text`.)
- `role` is top-level; some records nest it under `providerData`, some do not.
- Tool results are separate records (`type: "function_call_result"`) — grep the raw line when a
  keyword clearly exists but no message matches.
- Do not filter by message length. A short "背景对上了" line is often the pointer you need.

Sanity-check by grepping the raw file for an ASCII-only token from your keyword set first. If raw
grep hits and your parser does not, the parser is wrong, not the archive.

## Step 3 — The cross-machine gap

Session logs live **per machine**. A conversation that happened on the office machine is simply
absent from the home machine, and the local log will show a clean time gap where it should be.

Before declaring something lost, print the log's hour-by-hour coverage. A missing afternoon
between two evening blocks is the signature of "it happened on the other machine" — not of
"it was never written".

> Real case: a script was said to have been delivered at 15:44. The home machine's log covered that
> date from 20:37 onward with a clean gap before it. The 15:44 session was on the office machine.
> Reporting "not on this machine, and here is the gap" is the correct answer.

## Step 4 — Report, do not substitute

🔴 **Never fill the hole with a rewrite.** Drafting a fresh version in his voice when he asked for
the original is the worst failure in this workflow: he now holds a document he cannot attribute,
and the retrieval he asked for has not happened.

Report instead:
- what was searched (each source, one line)
- the best evidence that it existed (e.g. a memory note saying "delivered two drafts at 15:44")
- why it is not retrievable here (never persisted / different machine / session rotated out)
- the options: paste it in, dictate it, or explicitly authorise a rewrite labelled as such

## Step 5 — Cite the source when you do find it

Every recovered artifact ships with file, line number, and timestamp. He will want to check it, and
an unsourced quote from a chat log is not verifiable.

Also say which version it is — archives hold several, and "the original" is often the one he
revised by hand afterwards.

## Self-check

- □ Searched memory → session logs → repo snapshot → workspace logs, in that order
- □ Keyword set widened at least twice
- □ Parser validated against a raw grep hit
- □ Hour coverage printed before declaring a gap
- □ Found: source cited with file + line + timestamp
- □ Not found: reported honestly, no substitute draft shipped

## Red lines

- 🔴 **No rewriting to fill a gap.** Stated once, it is the whole point of this skill.
- 🔴 **No publishing private chat content.** Recovered logs stay local; quote the minimum needed.
- 🔴 **No claiming a clean search when the parser was broken.** Validate the tool before the
  conclusion.
