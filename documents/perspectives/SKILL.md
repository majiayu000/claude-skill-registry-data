---
name: perspectives
description: Re-read the same events through other lenses — the other person's account, a neutral observer, the user in five years, someone who loves them. Use when the user says "how else could I read this", is stuck in one account, or wants to steelman someone they're angry with.
---

# perspectives

The same facts, deliberately re-read from positions other than the one they're standing in.
Not to correct them — to give them something to compare against.

## Preconditions

- The events must already be written down (a session note, a timeline). Do not run this on a
  story told once, ten minutes ago; you'll be shifting perspective on a version that hasn't
  settled.
- Check `context/working-agreement.md`. Some people find this exercise invalidating. If the
  agreement rules it out, say so and don't run it.
- Ask first, always: "do you want the other readings, or do you want to stay with yours today?"
  Both answers are legitimate and the second is not avoidance.

## Lenses

Offer three or four; let them choose which to actually write. Never do all of them.

| Lens | The question |
| --- | --- |
| **The other party** | Told from their side, in good faith, from what they plausibly knew at the time |
| **Neutral observer** | Someone with no stake who watched it happen — what would they describe? |
| **Five years on** | What of this will still matter, and what won't |
| **A friend's version** | If a friend described this to you, what would you say to them |
| **Younger self** | What the person they were at 20 would make of how they handled it |
| **The generous reading of themselves** | Usually the hardest one, and often the one that's missing |

## Output

`artefacts/perspectives-<subject>.md`:

```markdown
---
type: artefact
kind: perspectives
subject: <what was re-read>
built_from: [sessions/...]
updated: 2026-08-14
---

## The account as it stands
Their reading, in their words. Not shortened.

## <Lens>
Written in full, in the third person, as an account rather than an argument.
What this lens can see that the standing account can't.
What it can't see that the standing account can.

## What the user said about it
Left blank until they respond. Their reaction is the point of the artefact.
```

## Rules

- **The other party's version is written in good faith or not at all.** A strawman is worse than
  nothing — it lets the standing account off the hook.
- **Nothing here overrides their account.** State explicitly, once, in the artefact: these are
  alternative readings, not corrections.
- **Do not adjudicate.** No "the truth is probably in the middle". Sometimes it isn't, and it is
  not your call.
- **Never run this on abuse, coercion or violence** in the "understand their side" direction.
  Steelmanning someone who hurt them is not a perspective exercise; it is a harm. Offer the
  neutral-observer and five-years lenses instead, or nothing.
- End by asking what, if anything, landed. Record their reaction verbatim.
