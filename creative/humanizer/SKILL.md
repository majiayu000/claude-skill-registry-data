---
name: humanizer
description: Use when editing or reviewing prose to remove AI-writing patterns while preserving facts, intent, and the author's voice.
---

# Humanizer

Edit prose so it sounds like a person wrote it, without changing its facts or
argument. Use [references/patterns.md](references/patterns.md) when a detailed
pattern audit is useful, and read [references/workflow.md](references/workflow.md)
for invocation modes and the draft, audit, and final-rewrite process.

## Rules

- Preserve every supported claim, name, number, date, quote, citation, and
  deliberate opinion. Never invent detail to make prose sound human. Creative
  expansion, including invented fiction detail, is disabled unless the user
  explicitly requests the separate creative-expansion mode below.
- Match the supplied voice and register. A writing sample outranks the default
  style rules, including punctuation preferences.
- Apply personality only to essays, blogs, opinion, and personal writing. Keep
  technical, legal, reference, and encyclopedic prose neutral.
- Prefer specific subjects, active verbs, varied sentence lengths, and concrete
  endings. Cut filler rather than replacing it with polished filler.
- Do not rewrite code, frontmatter, data, link targets, or quoted text in file
  mode unless the user explicitly asks for those parts.

## Workflow

1. Read the complete input and any supplied voice sample.
2. Draft a rewrite that preserves meaning and register.
3. Audit for clustered AI patterns, factual additions, and voice drift. Do not
   flag an isolated punctuation choice or ordinary transition as proof of AI.
4. Revise once, then run the final checks below.

## Invocation modes

- **Pasted text:** return the draft, brief remaining-pattern audit, and final
  rewrite.
- **File:** rewrite only the prose in place and report a short change summary.
- **Embedded:** return only the final text for the calling workflow.
- **Creative expansion (explicit):** use only when the user separately and
  explicitly authorizes invented detail. Keep the expansion bounded by the
  requested story, voice, and constraints, and distinguish additions from
  source-supported facts when reporting the result.

## Final checks

- Every factual statement is supported by the input or user.
- The result has no generic opener, fake enthusiasm, unsupported attribution,
  promotional inflation, or generic positive conclusion.
- Remove em/en dashes unless the supplied voice sample intentionally uses them.
- Read the result aloud mentally; preserve unusual human details and mixed
  feelings instead of smoothing them away.

Based on [Wikipedia's signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
