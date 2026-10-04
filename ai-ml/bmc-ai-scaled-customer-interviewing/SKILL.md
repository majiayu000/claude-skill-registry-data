---
name: bmc-ai-scaled-customer-interviewing
description: "Uses AI-moderated interviews to run customer discovery conversations at a scale no human team could match — hundreds of short interviews in parallel — then treats the aggregate as a filter: mines it for the most interesting outliers and patterns, and follows up on those personally."
---

# BMC AI-Scaled Customer Interviewing

## Purpose

Direct customer interviews are the strongest evidence a hypothesis can
get, but a human team can only run so many before time runs out. This
skill uses AI-moderated interviews to remove that ceiling — running
many short conversations in parallel — and treats the resulting mass of
transcripts as a filter, not a final answer: mine it for the most
interesting outliers, contradictions, or recurring patterns, then call
those specific people back personally. Use this as a first, wide pass
before or alongside the personal follow-up interviews
`bmc-proxy-expert-validation` and direct customer research already
call for.

## Anchored in research

Grounded in a well-documented, mainstream 2026 practice, independent of
any single named source: roughly 40% of B2B SaaS product teams now
report AI-moderated interviews monthly, up from under 10% in 2024;
early-stage founders in 2026 run a median of 47 completed interviews
per discovery round, up from 8–12 in 2022, enabled specifically by AI
moderation removing the scheduling and synchronous-time cost; a typical
AI-moderated conversation runs under $5 in compute. Multiple named
platforms exist for this specifically (Perspective AI and others), and
the underlying mechanism — a software moderator running many sessions
in parallel, asking unscripted follow-ups, and synthesizing themes
across every transcript — means research throughput is no longer capped
by researcher headcount.

## Method

1. **Design the interview for AI moderation, not just transcription.**
   The value here isn't automating note-taking on human-run calls —
   it's a software moderator that asks unscripted follow-up questions
   live, based on what the respondent actually says, the same way a
   skilled human interviewer would probe an interesting answer. Confirm
   the chosen tool actually does this, not just records and summarizes.
2. **Recruit at volume, using low-friction channels** — a newsletter
   invite, an embedded flow on a signup or thank-you page, an outbound
   message offering a short (5-10 minute) conversation. The low
   per-conversation cost only pays off if recruitment volume is
   genuinely high; a handful of AI-moderated interviews doesn't unlock
   the advantage this method offers.
3. **Run interviews in parallel, at a volume a human team couldn't
   match** — tens to hundreds of conversations depending on the
   audience's size and reachability, not a handful.
4. **Treat the aggregate as a filter, not a conclusion.** Don't try to
   read every transcript individually — instead, synthesize across all
   of them for: the most frequently recurring theme, the sharpest
   contradiction between what different respondents say, and the most
   surprising individual outlier that doesn't fit the pattern.
5. **Personally follow up on what the filter surfaces**, not on a
   random sample. Call back the specific respondents behind the most
   interesting outliers or the clearest pattern-breakers — these
   personal, human-led follow-ups are where the deepest insight
   actually comes from; the AI-moderated pass exists to find WHO is
   worth that follow-up, not to replace it.
6. **Check for AI-moderation-specific bias before trusting the
   aggregate.** Respondents may behave differently with a software
   moderator than a human one — more candid on sensitive topics, less
   candid on ones where they'd normally read social cues from an
   interviewer. Note this explicitly as a limitation of the aggregate
   data, not just of the individual transcripts.
7. **Compare this method's role to the pack's other validation
   sources**, so it isn't used as a like-for-like substitute:
   `bmc-proxy-expert-validation` gets pattern-rich signal from adjacent
   professionals, not target customers directly; `bmc-experiment-method-selection`
   decides whether to build something or use a proxy test at all. This
   skill's distinct contribution is volume — direct customer
   conversations at a scale personal outreach alone can't reach.

## What this skill does NOT do

- Doesn't replace personal follow-up interviews — it's explicitly
  designed to identify WHO to follow up with personally, not to
  substitute for that follow-up.
- Doesn't guarantee representative sampling just because the volume is
  high — recruitment channel bias (who sees the invite, who's willing
  to talk to a bot) still applies and should be checked, not assumed
  away by volume alone.
- Doesn't work well for topics that genuinely need human trust or
  rapport to surface honest answers (deeply sensitive, high-stakes, or
  relationship-dependent topics) — use judgment about which questions
  suit AI moderation and which don't.

## Refinement notes

- Which AI-interview tool or approach has actually produced the
  cleanest signal in your own practice?
- What's a real case where the aggregate filter surfaced an outlier
  worth a personal follow-up that a small human-only interview batch
  would have missed entirely?
- How do you personally handle the AI-moderation bias risk (Step 6) —
  have you seen a clear case of respondents behaving differently with a
  bot vs. a human interviewer?

## Continue from here

- Use alongside: `bmc-proxy-expert-validation/SKILL.md` — a different,
  complementary customer-understanding source (adjacent professionals,
  not target customers directly).
- Use alongside: `bmc-experiment-method-selection/SKILL.md` — decides
  whether to build or use a proxy test; this skill is one form of cheap,
  fast direct-customer testing within that decision.
- This pack's shared guardrails: `../../CLAUDE.md`

## References

- `../../references/bmc-source-material-notes.md` — source material background
- `../../../../ai-strategy-and-governance/references/ai-native-reshuffle-heuristics-research.md` —
  selection and grounding notes for this skill and its siblings
- `../../CLAUDE.md` — this pack's shared guardrails
