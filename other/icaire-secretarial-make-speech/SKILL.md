---
name: icaire-secretarial-make-speech
description: Draft ICAIRE keynote, opening, closing, or panel-discussion speech content from supplied material. Use when the user asks for speech remarks or panel content.
---

# ICAIRE Secretarial Make Speech

Turn supplied ICAIRE material into keynote remarks, formal openings, closing
remarks, or panel-discussion content with clear audience, duration, tone, and
approval boundaries.

## Contract

- Confirm occasion, audience, speaker, language, duration, tone, and delivery
  format before drafting.
- Use supplied material and relevant ICAIRE brain context for grounding.
- Preserve official positioning and avoid creating new policy commitments,
  partnership claims, or institutional promises.
- Support full speech, short remarks, panel talking points, moderator notes, or
  Q&A preparation.
- Treat speech content as review-ready draft material unless the user explicitly
  confirms it is final.
- For government-machine workflows, prepare copy that the user can transfer
  manually.

## Workflow

1. Define the speech job.
   - Identify occasion, speaker, audience, language, target duration, and
     desired outcome.
   - Ask for missing source material when the event or official position is not
     clear.
2. Gather source context.
   - Read supplied notes, decks, reports, meeting pages, prior language, and
     relevant ICAIRE context.
   - Separate confirmed claims from proposed framing and placeholders.
3. Draft the speech.
   - Choose the right format: full remarks, short intervention, panel opening,
     panel answers, or Q&A prep.
   - Build a clear structure: opening, context, message, evidence, invitation
     or ask, and close.
   - Match formality to the setting.
4. Review.
   - Check for unsupported claims, sensitive wording, overcommitment, and
     external-approval needs.
   - Offer concise alternatives when tone or length may need adjustment.

## Output

Default to this structure:

- `Speech Brief`: occasion, audience, speaker, language, and duration.
- `Draft Remarks`: full speech or requested speech format.
- `Panel / Q&A Points`: if relevant.
- `Tone Notes`: formality, emphasis, and adaptation choices.
- `Approval Flags`: claims, names, or commitments needing review.
- `Source Basis`: source files or brain pages used.

## Guardrails

- Do not invent policy positions, approvals, launch dates, metrics, or partner
  commitments.
- Do not use confidential brain context in external remarks unless the user has
  approved it for that audience.
- Do not write final government or public remarks without marking review needs.
- Do not ignore requested duration; shorten or expand to match the speaking
  slot.
- Do not make the speech sound like a generic corporate template when ICAIRE
  context is available.
