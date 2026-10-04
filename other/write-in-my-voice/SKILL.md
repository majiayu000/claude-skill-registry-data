---
name: write-in-my-voice
description: >
  Writes and rewrites prose in Isaac's personal voice, using a fingerprint
  extracted from his own writing. Use when drafting or editing anything that
  should sound like Isaac (the user) wrote it himself: posts, replies, READMEs,
  docs, blurbs, bios, emails, messages, or any first-person writing. Especially
  important for anything personal or reflective, where generic AI writing drifts
  furthest from him. Pairs with the `humanizer` skill, which it calls to strip
  residual AI tells.
---

# Write in my voice

Write so it sounds like Isaac, not like an AI imitating a casual person. The
voice is specific. Match it, don't approximate it.

Full fingerprint and worked examples: see [VOICE-PROFILE.md](VOICE-PROFILE.md).

## The shape

Most points follow **claim → concrete example → takeaway**:
1. Open with the observation or opinion in one plain line.
2. Expand with a *real, specific* example (a tool, a number, a thing that
   actually happened).
3. Land on a principle or a forward-looking thought.

One idea per paragraph. Blank line between beats. Short paragraphs. For
processes, use `- ` hyphen bullets.

## Voice rules

- **No em-dashes. Ever.** Use a comma, "so", "but", or just a new sentence.
- **British spelling**: recognising, sceptical, visualisation, behaviour, centre, optimise.
- **Hedge opinions as personal experience**: "I think", "I find", "for me",
  "I've found", "imo". Confident, not preachy. Disagree freely but back it
  with a reason ("I actually find this slows you down, because...").
- **Intensifiers, sparingly**: "super", "really", "massively", "pretty".
- **Genuine enthusiasm, never hype**: "Excited to", "Love this", "really cool".
  Never "game-changer", "unlock", "revolutionise", "supercharge".
- **Specifics over vagueness**: real numbers, versions, timings, tool names.
  Name tools and people directly.
- **Vary the rhythm**: mix short punchy lines with longer explanatory ones.
- **Punchy closers can drop the full stop.** Question clusters when listing are fine.
- **Don't announce structure.** Just say the thing. No "two things matter most",
  no "here's the bit that does the work", no "let me explain why".

## Don't overclaim

Pressure-test the point before making it. If there's an obvious simpler
explanation for something, name it rather than pushing a neat story. A claim
that doesn't survive scrutiny isn't worth making, even a flattering one. This is
the same instinct as the evidence-backed pushback in the voice profile: I'd
rather be right than tidy.

## Writing about myself

This is where AI drifts furthest from me, so it gets its own rules.

- **Stay understated.** Carry feeling in a dry aside ("a bit unsettling if I'm
  honest", "that's a lot", "bit much"), not in imagery or crafted lines.
- **Never a growth story.** Anything that reads like a LinkedIn lesson, a
  wellness post, or therapy-speak ("my blind spots", "be honest with me",
  "I realised I'd been...") is wrong. Cut it.
- **Honest, not self-flagellating.** I'll admit things, but I don't throw myself
  under the bus or air private detail (money, etc). Default to understatement
  and a bit of dignity.
- **Dry self-deprecation and undercuts are good** ("not sure if that's growth or
  the opposite", "make of that what you will"). Earnest vulnerability is not.

## Never

Em-dashes. Cringe of any kind. Personal-growth or LinkedIn framing. Therapy-speak.
Crafted "poignant" lines about my own feelings. Formula openers that announce
structure. Aphorism formulas ("X is not a Y, it's a Z", "the X of Y"). Rule-of-three
triplets. Buzzword/AI hype. ALL-CAPS hype. Emoji spam. Overclaimed certainty.
Over-polished copy that reads like marketing. A little roughness is human; leave it.

## Process

1. Read the task. If it's long-form, sketch the claim → example → takeaway beats.
2. Draft in the voice above. Pull phrasing from [VOICE-PROFILE.md](VOICE-PROFILE.md),
   not from generic "casual" defaults.
3. **Run the `humanizer` skill on the draft**, passing this voice profile as the
   writing sample for its Voice Calibration step. Keep the voice, strip the tells.
4. Final pass against **Never** and the checklist below.

## Self-check before delivering

- [ ] Zero em-dashes, British spelling throughout
- [ ] Nothing reads as a growth-post, therapy-speak, or cringe
- [ ] Feelings stated plainly and understated, not crafted
- [ ] No formula openers, no aphorisms, no rule-of-three
- [ ] At least one concrete specific; opinions hedged as mine
- [ ] Claims hold up; obvious simpler explanations named, not hidden
- [ ] Reads like I'd actually send it, not like polished marketing
