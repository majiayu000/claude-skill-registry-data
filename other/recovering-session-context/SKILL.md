---
name: recovering-session-context
description: Reconstruct what happened in prior agent sessions from their transcripts and surface everything raised but never resolved — unanswered questions, work promised and not done, topics dropped, partial completions, and incomplete todos. Use when resuming after an interruption or compaction ("pick up where we left off", "what was I doing"), when auditing recent days for loose ends ("what's outstanding", "what did we drop"), or before declaring a thread finished. Covers locating transcripts per tool, reconstructing turns, the taxonomy of what counts as unresolved, and how to present findings.
license: MIT
metadata:
  last_updated: "2026-07-31"
---

# Recovering Session Context

Agent sessions end badly more often than they end cleanly: interrupted mid-task, compacted, or
simply overloaded until an early question is buried under later context. The transcript still
holds all of it. This skill turns that transcript back into an accurate picture of what is
actually outstanding.

Two modes, same machinery:

| Mode | Scope | Ends with |
| --- | --- | --- |
| **Resume** | The tail of the single most recent session | Continue the work — do not ask permission |
| **Audit** | Every session for this project over a lookback window (default 3 days) | Grouped findings, then an offer to track or act |

They differ only in breadth and output. Locating transcripts, reconstructing turns, and deciding
what counts as unresolved are identical, which is why they live here once rather than in each
command that calls them.

## When to use

- Resuming after an interruption, a crash, a compaction, or a multi-day gap.
- The user asks "what was I doing", "pick up where we left off", "what's still open",
  "what did we drop", "what's outstanding".
- Before declaring a piece of work finished — to catch the "I'll also…" that never happened.
- Auditing whether a plan was actually executed end to end, or only partly.

Not for searching the historical corpus by topic — that is `cc-recall` (discoverability across
tens of thousands of sessions). This skill reads *recent* transcripts in full.

## Quick reference

| Need to… | Read this |
| --- | --- |
| Find this project's transcripts, reconstruct turns, extract incomplete todos | [`references/locating-and-reconstructing.md`](references/locating-and-reconstructing.md) |
| Decide what counts as unresolved; format the brief or the audit | [`references/what-counts-as-unresolved.md`](references/what-counts-as-unresolved.md) |

## Behavioral guidance

**Cast a wide net, then narrow.** The failure mode is reading the transcript for the *task* and
missing everything adjacent to it. Surface candidates generously first; discard afterwards.

**An unanswered question runs in both directions.** Agents reliably notice the user's unanswered
questions and reliably forget their own — a question the agent asked that the user never replied
to is the single most common dropped thread, because the agent moved on and nothing marked it.

**Resume mode continues; it does not ask.** Present the brief and proceed to the next step. "Shall
I continue?" wastes the turn that reconstructing the context just paid for. The one exception is a
genuinely ambiguous final state — then say so in a sentence and ask exactly one focused question.

**Scale the output to what you found.** Three lines for a simple interrupted task. Grouped bullets
only when several threads were genuinely in flight. A long report about a short session is noise.

**Be specific enough to execute.** "Follow up on the auth thing" is not a finding. Name the file,
the decision, the question, and the session it came from — the reader should be able to act
without re-reading the transcript you just read.
