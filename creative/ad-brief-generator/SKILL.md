---
name: ad-brief-generator
description: Turn ranked creative directions (from winning-pattern-synthesis, or any selected evidence-backed angle/hook) into shoot-ready UGC/creator briefs — hook line, shot list, VO/copy direction, and CTA. Use whenever the user asks for a creator brief, script, shot list, or says a direction is ready to hand off for production. This is the final production-facing output of the winning-ads pack.
---

# Ad Brief Generator

Converts a validated creative direction into a brief a creator or editor can shoot from directly — no further interpretation needed on their end.

## When to use this skill

- "Turn this into a brief"
- "Write the script/shot list for [direction]"
- The final step after `winning-pattern-synthesis` has ranked directions, or directly off a single hook from `creative-psychology-hooks`

## Inputs needed

- The direction: angle, hook, mechanism (from synthesis or psychology skill output)
- Format: UGC talking-head, B-roll+VO, static image, carousel
- Any brand-specific constraints: tone, banned claims/words, required disclaimers, existing creator relationships
- Length target (15s, 30s, static, etc.) if the platform/placement is known

If the format template the user wants isn't established in this conversation, ask once before generating — don't guess a template structure only to redo it.

## Brief Structure

### Header
- Direction name / angle
- Source: cross-source overlap / competitor-backed test gap / own-only market whitespace / cold psychology hook (carry this through from synthesis — production should know the confidence level)
- Format + target length

### Hook (0–3s)
- Exact line or visual direction, not a vague description
- Delivery note (tone, pacing, on-camera vs voiceover, text overlay if any)

### Body
- Beat-by-beat shot list for video (what's shown, what's said, timing)
- For static/carousel: panel-by-panel breakdown
- Explicitly carry forward what `own-creative-diagnosis` flagged as strong in the analysis window (e.g. "keep hook, change pacing after 3s" scenarios) if this brief is a variation of an existing strong performer rather than a fresh concept

### CTA
- Exact line
- Visual treatment (on-screen text, verbal, both)
- Any urgency/scarcity element if the diagnosis called for stronger CTA

### Copy (for the ad unit itself, separate from video VO)
- Primary text
- Headline
- Any compliance/disclaimer requirements

## Variation Set

Don't generate a single brief in isolation — generate the brief plus 2-3 named variation directions per the standard test order:
1. Copy variation (same angle, different words)
2. Angle variation (different selling point, same format)
3. Hook variation (same body, different opener) — pull alternates straight from `creative-psychology-hooks` output if available

## Output Format

```
### Creative Brief: [Direction Name]

Source: [cross-source overlap / competitor-backed test gap / own-only market whitespace / cold ideation]
Format: [UGC / B-roll+VO / static / carousel] · Length: [target]

HOOK (0-3s)
[Line + delivery direction]

BODY
[Beat/shot list or panel breakdown]

CTA
[Line + treatment]

COPY
Primary text: ...
Headline: ...

VARIATIONS TO TEST ALONGSIDE
1. [Copy variant]
2. [Angle variant]
3. [Hook variant]
```

## Guardrails

- Never fabricate a specific claim, stat, or testimonial in the copy — placeholder clearly (`[insert verified stat]`) rather than inventing one.
- Flag anything that reads close to a competitor's specific creative execution (not just angle/pattern) rather than an original take built from the pattern.
- Keep briefs specific enough to shoot from — "make it relatable" is not a brief; "open on hands struggling to open packaging, cut to product in 2s" is.
