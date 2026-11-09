---
name: four-failures-check
description: Checks a video opening for the four ways hooks fail (delay, confusion, irrelevance, disinterest) and points at the exact words or shot that cause each one. Use on any hook draft, script opening or filmed first 3 seconds.
---

# Four Failures Check

A hook that loses people almost always does one of four things. Check all four, in order, and point at the exact words or frame. Never give a verdict without a quote.

## The four failures

| Failure | What it looks like | The test | The fix |
|---|---|---|---|
| **Delay** | The topic arrives late. Greetings, names, "welcome back", "so", "before we get into it", a slow walk in | Count the words (or seconds) before a stranger knows what the video is about | Cut to the first word that carries the subject. Move the payoff frame to second zero |
| **Confusion** | More than one possible meaning, insider words, a pronoun with nothing behind it, a clever line that needs a second listen | Read it as a complete outsider, not as the expert who wrote it. Could a tired stranger say back what the video is about after one listen? | One meaning. Plain active verbs. Name the thing. Enough words to be clear, not as few as possible |
| **Irrelevance** | It's about the creator, not the viewer. "My journey", "a bit about me", a logo, a title card with the brand | Would the viewer think "this is for me" in the first sentence? | Put the viewer's problem, want or belief first. The creator's story can come later as proof |
| **Disinterest** | Clear and relevant but obvious. Nothing to wonder about. "Gardening tips!!", "Here's how our product works" | Is there a gap between what the viewer believes now and what this video shows? | Add contrast: what they expect versus what's true, the old way versus this way, the fail versus the fix |

Two things that are not failures:
- **A vague spoken opening is fine if the picture or text carries the hook.** Check the three channels together (spoken, visual, text) before failing delay or confusion.
- **A hook can take two or three short lines.** Line one sets the subject, line two adds the contrast. Don't cram both into five words if it makes it unclear.

## How to run it

1. Write out the current opening exactly: spoken words, on-screen text, first shot. If you only have one of them, say which are missing.
2. For each failure: PASS or FAIL, the exact words or frame, one line on why.
3. Topic clear at: the word or second when a stranger would know what this is about.
4. The single biggest failure, which the rest of the work fixes first.

## Output (when called on its own)

```
Opening: "[exact words]" | Text: "[text]" | Shot: [shot]
Delay: FAIL. "[words]" Topic is clear only at [word / second].
Confusion: PASS / FAIL. "[words]" [why]
Irrelevance: FAIL. "[words]" is about you, not them.
Disinterest: FAIL. No contrast: viewer already expects [x].
Fix first: [one failure], because [reason].
```

Then give one rewrite that fixes the biggest failure without causing another.

See [references/failure-examples.md](references/failure-examples.md) for before and after pairs.
