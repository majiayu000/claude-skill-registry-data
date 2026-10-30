---
name: stop-slop
description: >
  Detect and eliminate predictable AI writing tells from prose.
  Use when the user asks to "make this sound less like AI", "remove AI tells",
  "make it more human", "this sounds robotic", "clean up the writing",
  "too formal", "sounds generated", or requests a writing/copy review.
  Do NOT use for code — this skill targets prose, copy, and documentation only.
origin: adapted:hardikpandya/stop-slop
license: MIT © Hardik Pandya
version: 1.0.0
compatibility: "Any prose, copy, documentation, README, commit messages, PR descriptions."
---

<!-- Adapted from stop-slop (MIT © Hardik Pandya). Changes: added YAMTAM origin/Anti-Fake-Pass fields, integrated scoring rubric, added Vietnamese-language support notes. -->

## When to Use

- Use when: output reads like a template ("It's worth noting that...", "In conclusion...")
- Use when: user says the copy sounds robotic, AI-generated, or stiff
- Use when: reviewing README, docs, blog posts, commit messages, PR descriptions
- Use when: prose has hedging language ("arguably", "quite", "somewhat", "perhaps")
- Do NOT use for: code comments, technical specs, log output

## The 8 Rules

**Rule 1 — Cut filler phrases**
Remove throat-clearing openers. Start with the point.
```
✗ "It's worth noting that performance improved significantly."
✓ "Performance improved 40%."
```

**Rule 2 — Break formulas**
Avoid binary contrasts and rhetorical setups.
```
✗ "While X is important, Y is equally crucial."
✓ State X. State Y. Let the reader connect them.
```

**Rule 3 — Active voice, human subjects**
```
✗ "The function was refactored to improve readability."
✓ "I refactored the function — now it reads in one pass."
```

**Rule 4 — Be specific, not vague**
```
✗ "This approach offers significant benefits."
✓ "This cuts build time from 4 minutes to 40 seconds."
```

**Rule 5 — Direct address, no narrator distance**
```
✗ "Users may find it helpful to..."
✓ "Run this once to set it up."
```

**Rule 6 — Vary rhythm**
Mix short and long sentences. Kill em-dashes. Kill semicolons used for drama.
One idea per sentence is usually enough.

**Rule 7 — Trust the reader**
State facts. Skip the softening.
```
✗ "This might be one way to consider approaching the problem."
✓ "Do X."
```

**Rule 8 — No pull-quote sentences**
If a sentence reads like it belongs on a LinkedIn post, rewrite it.
```
✗ "Great teams move fast and stay aligned."
✓ [Delete. Say what your team actually does.]
```

## Quick Scan Checklist

Before delivering any prose, scan for:
- [ ] Adverbs ("significantly", "essentially", "importantly", "notably")
- [ ] Passive constructions ("was done", "is considered", "has been implemented")
- [ ] Em-dashes used for drama (—)
- [ ] Vague quantifiers ("many", "various", "several", "numerous")
- [ ] Opening with "I" or "This" followed by a meta-statement about the content
- [ ] Sentences that start with "It is" / "There are" / "This is"

## Scoring Rubric (35/50 = revision needed)

| Dimension | 1 (AI slop) | 10 (human) |
|-----------|-------------|------------|
| Directness | Hedged, passive, vague | Direct, active, specific |
| Rhythm | Uniform sentence length | Varied, natural cadence |
| Trust | Over-explains, softens | States facts, respects reader |
| Authenticity | Template language | Genuine voice |
| Density | Padded, filler words | Every word earns its place |

Score each dimension 1–10. Total < 35 = rewrite.

## Anti-Fake-Pass

```
❌ Removing one adverb and claiming the prose is clean
❌ Rewriting without reading the full piece first
❌ Applying rules mechanically without reading for flow
❌ Fixing one paragraph and ignoring the rest
✅ Score before and after using the 5-dimension rubric
✅ Read aloud — AI slop sounds different spoken
```
