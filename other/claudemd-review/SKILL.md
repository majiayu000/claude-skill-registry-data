---
name: claudemd-review
description: >
  Use right after being corrected on something a CLAUDE.md file should
  already have told you, when explicitly asked to review CLAUDE.md, or
  periodically after a session with a lot of back-and-forth — reviews THIS
  conversation for friction and proposes a bounded CLAUDE.md edit. A
  lightweight, single-session complement to skill-tuning-loop (which mines
  many sessions and validates a proposal against held-out cases before
  surfacing it — reach for that instead when the ask is "make this
  systematic," not "check right now"). Own version of the dx plugin's
  `/dx:review-claudemd`.
---

# CLAUDE.md Review

A quick self-check, not a pipeline: read back over this conversation, find
places where the human corrected something a project rule should have
already covered, and propose a small, bounded edit. Nothing here gets
applied without the human reviewing it first.

## Process

1. **Scan this conversation** for corrections, "no, actually", or repeated
   clarifications — the same signal `skill-tuning-loop`'s Mine stage looks
   for in past sessions, except you already have the transcript in context.
2. **For each one, classify it:**
   - **Already covered, ignored anyway** — the relevant CLAUDE.md already
     says this; the fix is emphasis or clarity, not new content.
   - **Genuinely missing** — no existing rule addresses it; a new line would
     have prevented the correction.
   - **One-off** — specific to this task, not a durable project convention.
     Don't propose an edit for this; CLAUDE.md is for what generalizes.
3. **Propose a MINIMAL diff** for the "genuinely missing" and "ignored
   anyway" cases only. Match the file's existing voice and structure — don't
   restructure sections that aren't implicated. State the rule concretely
   (name the specific convention), not "follow best practices."
4. **Present the diff, don't apply it.** Show the human the proposed
   addition and why (quote the correction that motivated it). They edit the
   file, not you — CLAUDE.md is read on every session for every task in the
   project; a bad edit here is a bad edit everywhere.

## When to reach for skill-tuning-loop instead

This skill only ever sees one conversation, so it can mistake a one-off
correction for a durable pattern. If the same friction keeps showing up
across sessions and you want a validated, evidence-gated proposal rather
than a quick check, that's what `skill-tuning-loop` is for.
