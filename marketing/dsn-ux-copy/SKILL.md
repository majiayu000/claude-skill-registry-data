---
name: dsn-ux-copy
version: 1.0.0
description: Write and review interface microcopy - errors, empty states, buttons, labels, and CTAs - that is clear, concise, human, and consistent with the product's voice.
author: matrixx0070
tags: [design, ux-writing, microcopy, content, cta, error-messages]
capabilities: []
---

# UX Copy

## When to use
Use this when a screen needs its words — button labels, error messages, empty states, tooltips, confirmations, CTAs — or when existing copy is confusing, robotic, or blames the user. Works for drafting from scratch or reviewing what exists.

**Not for:** long-form marketing or docs, naming a product/brand, or visual layout decisions (use dsn-design-critique) — this is interface strings, not prose.

## Method
1. **Locate the moment.** Name where the user is, what they just did, what they need next, and how they likely feel. Copy serves that moment, not the system's internals.
2. **Lead with the user's goal.** Say what to do or what happened in plain language. Cut hedges, jargon, filler; front-load the important word.
3. **Errors: cause + fix, never blame.** Explain what went wrong and how to resolve it. Ban "invalid input" and "an error occurred". *Decision:* if the user can fix it, tell them how; if only the system can, apologize and say what happens next.
4. **Empty states earn their space.** Explain what belongs here and give one clear next action — never a blank void.
5. **CTAs describe the outcome.** Prefer "Send invite" over "Submit"; the verb matches what happens.
6. **Voice and consistency.** Match the product's tone; one term per concept everywhere; uniform tense, capitalization, punctuation.
7. **Check length** against real layouts and edge cases.

## Example
Payment fails. Reject: "An error occurred (code 402)." Rewrite: "Your card was declined. Check the number and expiry, or try another card." CTA "Submit" → "Pay $49". Empty invoices list → "No invoices yet. They'll appear here once you bill a client." + button "Create invoice".

## Pitfalls
- Blaming the user ("You entered invalid data") instead of naming the fix.
- Vague CTAs like "Submit" / "OK" that hide the outcome.
- Two words for one concept (folder/directory, delete/remove) — inconsistency erodes trust.
- Writing to the tooltip's width in isolation, then overflowing on the real, narrower mobile layout.

## Output format
```
# UX Copy: <surface>
**Context:** where / what just happened / what's next
**Copy:** element — recommended text (+ character count if constrained)
**Errors:** condition — message (cause + fix)
**Rationale:** why this wording, voice notes
**Rejected alternatives:** option — why not
```
Every string is testable against clarity, brevity, and voice; flag anything that needs product truth to confirm.
