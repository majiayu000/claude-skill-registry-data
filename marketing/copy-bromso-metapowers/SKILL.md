---
description: Review content through the lens of a brand strategist
---

# Copy Coaching

Review "$ARGUMENTS" through the lens of a brand and content strategist. Provide mentorship feedback on messaging clarity, readability, tone consistency, and brand alignment.

## Prerequisites

None — this is a utility skill that can run anytime.

## Process

1. **Read the target:**
   - Read the content specified in "$ARGUMENTS" (copy, marketing text, UI strings, documentation)

2. **Check for brand guidelines:**
   - Look for `.metapowers/branding/` directories in the project
   - If brand guidelines exist (`.metapowers/branding/<brand>/05-guidelines.md`), read them
   - If verbal identity exists (`.metapowers/branding/<brand>/03-verbal.md`), read it
   - Use these as the benchmark for tone and voice evaluation

3. **Read reference material:**
   - Read `plugins/coaching/shared/feedback-format.md` for output structure

4. **Evaluate the copy:**
   - **Readability:** Assess Flesch-Kincaid level. Is it appropriate for the audience?
   - **Clarity:** Is the message immediately understandable? Any ambiguity?
   - **Tone consistency:** Does the voice match throughout? Does it match brand guidelines (if available)?
   - **Scannability:** Are headings, lists, and bold text used effectively?
   - **Call-to-action:** Are CTAs clear, compelling, and action-oriented?
   - **Headline strength:** Do headlines grab attention and convey value?
   - **Jargon:** Is technical language appropriate for the audience?
   - **Conciseness:** Can anything be cut without losing meaning?

5. **Write the coaching report** to `.metapowers/coaching/$ARGUMENTS/copy-review.md` following the feedback format.

## Output

The copy coaching report written to `.metapowers/coaching/$ARGUMENTS/copy-review.md`. Present the score and top 3 suggestions to the user.
