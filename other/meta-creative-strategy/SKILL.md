---
name: meta-creative-strategy
description: |
  Full creative strategy pass for Meta Ads. Identifies winners + losers across the account, extracts the pattern behind each winner (hook, format, angle, audience pairing), produces a test plan + scaling plan + fatigue check, and outputs a concrete 12-creative production spec (6 static + 6 video) with hook lines, angles, and CTA recommendations. Read-only — no ads built. Use when a brief asks "what should we test next" or before a creative production sprint.
---

# Meta Creative Strategy (Read-Only)

For the ad account the user names, produce a complete creative strategy pass. Default lookback: 30 days. **Read-only — no ads built or modified.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Section 1 — Winners + losers

- Top 10 ads by ROAS with sufficient spend (≥ $500 / 14d or 100+ purchases)
- Bottom 10 ads by ROAS with sufficient spend
- For each: spend, ROAS, CPA, hook rate (3s view %), hold rate (15s view %), thumbstop rate

## Section 2 — Pattern extraction

For the winners, identify common patterns across these dimensions:
- **Hook style** — pain point / curiosity / social proof / pattern interrupt / UGC opener
- **Format** — talking-head / product demo / lifestyle / before-after / split-screen
- **Angle** — value / urgency / aspiration / fear / convenience
- **Audience pairing** — what audience type does each winner pair best with

Output a short table: `Pattern | # of winners using it | Avg ROAS`.

## Section 3 — Fatigue check on winners

Flag any winner that's showing fatigue signals (frequency > 4, CTR declining > 25% from week 1, CPA creeping up > 25%). These are "still winning but on borrowed time" — first priority to remix.

## Section 4 — Test plan

3–5 hypotheses to test next. Each:
- Hypothesis (one sentence)
- What to vary vs control
- Success metric + threshold
- Budget allocation suggestion

## Section 5 — Scaling plan

For each healthy winner with strong ROAS:
- Suggest budget headroom (% increase)
- Audience expansion suggestion (broader lookalike, geo expansion, etc.)
- Risk flag (fatigue ceiling, audience saturation)

## Section 6 — 12-creative production spec

Concrete spec for 6 static + 6 video creatives. For each:
- Format + dimensions (1:1 / 4:5 / 9:16)
- Hook line (the first 1–3 words on screen)
- Angle + audience pairing
- Reference to which winner pattern it remixes

End with: `_Strategy doc — no ads built. Hand this to your creative team or use the `launch-campaigns` skill to build any of the 12 specs._`
