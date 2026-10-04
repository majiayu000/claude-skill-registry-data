---
name: therapist-brief
description: Produce a short handover to take to an appointment — a therapist, GP, psychiatrist or intake assessment. Chronology, what the person wants from the hour, and the questions they mean to ask. Use when the user mentions an upcoming appointment or says "help me get ready for Thursday".
---

# therapist-brief

The bridge. This workspace's premise is that an AI is a poor substitute for a professional and a
very good preparation for one. This is the skill that cashes that in.

An appointment is fifty minutes, of which twenty are usually spent reconstructing events. A
person who walks in with two pages of chronology and three written questions gets a materially
better hour. That is the whole idea.

## Ask first

1. **Who is it for?** A first appointment, an established therapist, a GP, a psychiatric intake,
   an assessment. This changes everything about the document.
2. **How long is the appointment**, and is it the first?
3. **What do they want out of that hour?** One sentence.
4. **Will they hand it over or just read from it?** Handed-over documents get names removed and
   a tighter register; personal notes can stay rough.

## Output

`for-therapist/YYMMDD-<who>.md`. **Two pages maximum.** A clinician will not read six.

```markdown
# Notes for <appointment>, <date>

## What I want from this session
One or two sentences, in the person's own words. Top of the page because it is
the most useful thing on it.

## In brief
Three to five sentences: what the issue is and how long it has been going on.

## Chronology
Six to twelve dated lines, from artefacts/timeline.md. Only what this clinician
needs. Mark what's documented vs recalled.

## What I've noticed
Two or three patterns from threads/, in plain language, stated as observations
rather than conclusions: "the argument is nearly always on a Sunday" not
"I have a conflict-avoidance pattern".

## What's already been tried
Including what helped, what didn't, and what was abandoned and why.

## Current supports and treatment
Who else is involved, any medication (names and doses only if the person wants
it here), other services.

## Questions I want to ask
Numbered, three to five, written to be read out loud.

## Things I find hard to say out loud
Optional and often the most valuable section — what they would struggle to raise
in the room. Include only if they choose to.
```

## Procedure

1. Read `context/issue.md`, `context/goals.md`, `threads/`, the most recent review, and
   `artefacts/timeline.md` (run `timeline` first if it doesn't exist).
2. Draft to the structure above. Plain language throughout.
3. Show it. Ask specifically: *is there anything in here you don't want to bring?* Cut without
   argument.
4. Offer a PDF or a printable version — many people would rather hand over paper than a phone.

## Rules

- **No clinical language, no diagnostic terms, no severity ratings, no screening scores.** You
  are not doing an assessment and a document that looks like one is worse than useless: it
  primes the clinician with framing that didn't come from a clinician. Describe; don't classify.
- **Say what's documented and what's remembered.** Clinicians care about the difference.
- **Their voice, not yours.** The clinician is meeting them, not reading a report about them.
- **Two pages.** Cut the interesting material before the necessary material.
- **Nothing goes in that they haven't seen.** No inference sneaks in at the last stage.
- If there is no professional involved yet and they want help finding one, that's a legitimate
  ask — say plainly what you can and can't do (you don't know local waiting lists or who is
  taking patients) and point at what they'd need to check.
