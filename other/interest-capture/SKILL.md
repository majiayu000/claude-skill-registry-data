---
name: interest-capture
category: exec-function
codex-short-description: "Fast-file the current hyperfixation to the vault so it doesn't derail today's work"
description: >
  Capture the current hyperfixation into the Obsidian vault fast, so it isn't lost and
  doesn't derail today's work. Use when the user says "capture this idea", "hyperfixation
  dump", "interest capture", "stash this", "don't let me forget", or invokes /interest-
  capture.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Read
  - Write
  - Skill
  - Bash
related-skills:
  - task-initiation
loop-eligible: false
---

# Interest Capture

A new idea, project, rabbit hole, or hyperfixation just lit up in the user's brain. If they chase it now, today's actual work is gone. If they ignore it, it'll either be forgotten by lunch or rattle in their head for hours stealing attention. The answer is **fast capture** — get it down with enough fidelity to resume later, then go back to what they were doing.

## Why no council

Speed is the whole point. A council call adds latency that defeats the purpose. **Always run inline.**

## When to activate

When the user says:
- "Stash this"
- "Capture this"
- "Don't let me forget"
- "I just thought of"
- "Side quest"
- "Hyperfixation"
- "Rabbit hole I don't have time for right now"

## The capture flow

**One question, fast:**

> What's the idea? (One sentence is fine. I'll capture, tag, file, and send you back to what you were doing.)

If the user already dumped the idea in the trigger message, **skip the question** and go straight to capture.

## What to capture

A short note with this exact shape — no more, no less:

```markdown
---
captured: YYYY-MM-DD HH:MM
status: stashed
tags:
  - hyperfixation
  - [topic-tag-1]
  - [topic-tag-2]
---

# {{title — 5-8 words, descriptive}}

## The idea

{{one paragraph, in the user's words where possible}}

## Why it lit up

{{one sentence — what was the trigger? a thing they read, a problem at work, a connection to another project}}

## Next concrete step if I come back to this

{{one literal action — "read X", "spike a script that does Y", "talk to Z" — not a plan, an action}}

## Linked
- [[{{related-existing-note-if-any}}]]
```

## Where to file it

Delegate to `obsidian-vault` skill. The note goes in the user's `📥 Inbox/` (or equivalent capture folder — check the vault config). Filename: `YYYY-MM-DD-{{kebab-title}}.md`.

If the user doesn't use Obsidian, fall back to writing the file to `~/captures/` and tell the user the path.

## Output to the user

One line. Maximum two.

> **Captured:** [[2026-05-19-rust-async-runtimes-comparison]] — `#hyperfixation #rust #async`. Back to what you were doing.

That's it. No "great idea!", no expansion, no follow-up questions. Send them back.

## Edge cases

- **User dumps a lot:** capture all of it verbatim under "The idea". Don't try to summarize on the fly — that's slower than just writing it down. They can refine later.
- **User keeps dumping more:** capture each as a separate note (one idea per note, linked) rather than one mega-note.
- **User wants to act on it now:** route to `task-initiation` instead. Capture is for *not* acting now.
- **Already a duplicate:** if there's an existing note on the same topic in the vault, append a `## Re-surfaced YYYY-MM-DD` section to it instead of creating a new file.

## What NOT to do

- Do not ask clarifying questions beyond the one in "The capture flow"
- Do not engage with the idea ("that's interesting because...")
- Do not suggest next steps beyond the one-line "next concrete step" field
- Do not offer to research or expand
- Do not produce a summary back to the user — the note *is* the summary
- Do not invoke `clarity-council` — latency kills the use case

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/interest-capture.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
