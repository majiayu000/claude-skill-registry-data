---
description: Develop brand voice, tone, messaging pillars, and verbal identity
---

# Verbal Identity

Develop the verbal identity for "$ARGUMENTS". Create the voice, tone, messaging framework, and language guidelines that bring the brand personality to life in words.

## Prerequisites

Read `.metapowers/branding/$ARGUMENTS/01-discover.md` and `.metapowers/branding/$ARGUMENTS/02-strategy.md`. If `02-strategy.md` does not exist, tell the user:

> Phase 2 (Strategy) has not been completed for "$ARGUMENTS". Run `/branding:strategy $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/branding/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context files:**
   - Read `.metapowers/branding/$ARGUMENTS/01-discover.md` for audience insights
   - Read `.metapowers/branding/$ARGUMENTS/02-strategy.md` for personality, values, and positioning

2. **Define brand voice:**
   - Voice is consistent — it's WHO the brand is
   - Describe the voice using the personality traits from Strategy
   - Provide "We are / We are not" examples
   - Example: "We are confident but not arrogant. We are friendly but not casual."

3. **Define tone variations:**
   - Tone adapts to context — it's HOW the brand speaks in different situations
   - Define tone for: marketing, support, social media, formal communications, error messages
   - For each context: tone description + example copy

4. **Create messaging pillars:**
   - 3-5 key messages the brand consistently communicates
   - For each pillar: headline, supporting statement, proof point

5. **Develop tagline/endline options:**
   - Generate 3-5 tagline candidates
   - Evaluate each against the positioning and personality
   - Recommend the strongest option

6. **Language guidelines:**
   - Preferred vocabulary and phrases
   - Words and phrases to avoid
   - Grammar and style preferences (e.g., Oxford comma, contractions, capitalization)

7. **Write the artifact** to `.metapowers/branding/$ARGUMENTS/03-verbal.md`

## Output

The verbal identity written to `.metapowers/branding/$ARGUMENTS/03-verbal.md`. Present a summary to the user highlighting:
- Voice description in one sentence
- Top tagline recommendation
- Messaging pillars overview
