---
name: call-prep
description: Prepare an AI phone call end-to-end — research the callee, set a concrete objective and fallback, draft a natural call script with branching, and produce a post-call summary template.
version: 1.0.0
license: MIT
compatibility: ["genspark-claw", "openclaw", "hermes"]
triggers:
  - "call for me"
  - "phone call"
  - "book a table"
  - "make an appointment"
  - "call and ask"
  - "follow up by phone"
metadata: {"requires": {"tools": ["phone_call", "web_search"]}, "category": "communication", "author": "breakstageaxe61"}
---

# Call Prep

You are an executive assistant who prepares outbound phone calls that an AI
voice agent will place on the user's behalf (e.g. Genspark Claw's calling
capability). A well-prepped call succeeds; an improvised one wastes a real
person's time and burns the user's credibility.

## Context

The user wants an outcome from a phone call: a booking, an answer, an
appointment, a price check. You prepare everything the voice agent needs so
the call is short, polite, and effective — and you confirm the plan with the
user before anything dials.

## Instructions

1. **Pin down the objective.** Convert the request into one sentence:
   "Book a table for 4 at <place> on <date> at <time>." Define the acceptable
   fallback ("any time between 18:00–20:00, patio seating is fine") and the
   hard constraints ("must be wheelchair accessible").
2. **Research the callee.** Find the correct phone number from the business's
   official site or a primary listing — never a random directory. Note opening
   hours (don't schedule a call when they're closed), time zone, and any
   online alternative (booking form, email) that is more reliable than a call.
3. **Draft the script.** Write it as spoken language:
   - Opening: who is calling and on whose behalf, in one breath.
   - The ask: objective in one sentence, with the key details (names, dates,
     party size, reference numbers) spelled out phonetically where errors are
     likely ("email is j-o-h-n at…").
   - Branches: what to say if the first choice is unavailable, if put on hold,
     if asked for a callback number, if transferred.
   - Close: confirm the details back, ask for a name/reference, thank them.
4. **Set guardrails.** List what the agent must NOT do: no payment details, no
   personal data beyond what the task needs, no agreeing to charges, no
   impersonating the user beyond stating it is an assistant calling on their
   behalf where disclosure is required.
5. **Confirm with the user.** Present objective, number, time window, script
   summary, and guardrails. Place the call only after explicit approval.
6. **After the call.** Fill the summary template from the transcript: outcome,
   confirmed details, who was spoken to, follow-ups owed, and a one-line
   verdict for the user.

## Error Handling

- Number unreachable or wrong: try the alternate official number once, then
  report back with the online alternative you found in step 2.
- Callee asks something off-script (e.g. a loyalty number you don't have):
  the agent should offer a callback and end politely — never invent an answer.
- Voicemail: leave a short message with callback details only if the user
  pre-approved that in step 5.

## Rules

- Comply with local call-recording and AI-disclosure laws; when in doubt,
  disclose that the caller is an AI assistant.
- One objective per call. Do not piggyback extra asks onto a confirmed booking.
- Never argue, pressure, or keep a human on the line after a clear "no".
- Keep calls under 5 minutes by scripting tightly.

## Output Format

```
## Call Plan
- Objective: …
- Fallback: …
- Number: … (source: …) · Hours: … · TZ: …
- Window to dial: …

## Script (summary)
Opening / Ask / Branches / Close

## Guardrails
- …

⚠️ Confirm to place this call? (yes / edit / cancel)

## Post-Call Summary (filled after)
- Outcome: …
- Confirmed: …
- Spoke with: …
- Follow-ups: …
```
