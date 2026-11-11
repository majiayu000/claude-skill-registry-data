---
name: script-polish
description: "Reviews and rewrites a video script (YouTube long-form, a short, or a talking-head reel) so it sounds like one person talking to one friend and holds attention: kills forced analogies and presenter phrases, fixes framing, checks hooks, open loops and re-engagement beats, and suggests titles. Use when someone says fix this script, polish my script, make it sound like me, tighten this before I film, or asks for a hook or title for a video. Returns the rewritten script plus a short change log."
---

# Script Polish

Takes a draft script and returns a version you can read on camera without sounding like a presenter or an AI. Two passes: voice (does it sound like a person) and retention (will people keep watching).

By Johann (@johannships). These rules came from rewriting dozens of my own scripts after viewers told me what felt fake.

## Inputs

- **The script** (pasted, or a file path in Claude Code). Required.
- **Format**: long-form (5 to 20 min), short (25 to 60 s), or reel. Ask if not obvious from length.
- **Optional**: 1 to 3 transcripts of the creator's own past videos. If given, match their words and rhythm over the defaults below.
- **Optional**: the source (repo, article, product page) the script is about. If it is a repo or product, read its README or page before touching the hook.
- **Optional**: a hook the creator wrote and wants kept. Keep it word for word unless they ask for a new one.

If no voice sample is given, use the default voice below and say so in the change log.

## Hooks: three per script, three different types

For any short or reel, read `references/hooks-and-voice.md` first. Return **3 hooks of different types**
(callout, mistake/warning, belief flip, proof, number, story opener, question, curiosity gap, comparison/POV),
each 8 to 16 words and said inside 1.5 to 4 s, so all three get recorded and tested as separate trial reels
(see the `trial-post` and `reel-scorecard` skills). Structure the body as: hook -> why it matters -> the one idea
with a real example -> proof (something the creator did) -> a simple close. Anything not yet verified goes in
[brackets] and is confirmed or cut before filming. Keyword reels get two recorded endings: "comment KEYWORD" for
Instagram and "check the link in my bio" for every other platform.

## Pass 1: voice rules

1. **No forced analogies.** Delete any comparison a real person would not say to a friend ("Ferrari in first gear", "like reading a textbook while having a conversation", anything after "think of it like..."). Say the thing directly. "73KB of context is slow" beats any metaphor.
2. **One person to one person.** Talking to a friend, not presenting to a room.
   - Do: "So skills, right?" / "Here's the move." / "Let it cook."
   - Cut: "Let me tell you about...", "I'm going to walk you through...", "Today we'll be covering...", "Let me recap what we just covered."
3. **Energy from results, not metaphors.** "57% less context. Noticeably faster. That's it." beats "It's like going from a bike to a rocket." Only use numbers the creator actually measured or that the source states. Never invent one.
4. **Expert framing.** The speaker is teaching their process, not discovering it or confessing a mess. "Here's how I keep these tight." not "So we audited every file and found a bunch of bloat."
5. **Sentences.** Short. Fragments are fine. If a sentence has a comma, ask whether it should be two. If you would run out of breath reading it, split it.
6. **No em dashes and no `---` dividers** in the script, description or captions. Periods or line breaks.
7. **Stage directions stay practical**: `[to camera]`, `[beat]`, `[screen: what is shown]`. Never acting notes like "conspiratorial energy". The creator is being themselves, not acting.
8. **"I", not "we"**, unless there really is a team.
9. **No private names.** A client becomes "a PE firm owner", never their real name, unless the creator says it is approved.
10. **What and why, not how it works under the hood**, unless the audience is technical and asked for it.

Line test: for every line ask "would this person say this to a friend over coffee?" If no, rewrite or cut.

## Pass 2: retention (long-form)

- **0:00 to 0:05**: pattern interrupt or bold, true claim. No greeting, no channel intro.
- **Open loop early**: plant a question in the first 30 s that is only answered later.
- **Never close a section clean.** Tease the next section before wrapping the current one.
- **Re-engagement every 2 to 3 min**: a visual change, a new promise, or a shift in energy. Minutes 3 and 6 are the usual drop-off points, so put the strongest transitions there.
- **No section over 2.5 min** without a visual or energy change. Alternate talking head and screen.
- **Front-load value.** Someone who leaves at minute 4 should still have got something.
- `[beat]` only before a real reveal.
- CTA: small asks along the way, final CTA earned at the end, never a cold "like and subscribe" open.

## Pass 2: retention (shorts and reels)

Default shape for a 25 to 45 s talking reel:
1. Two-second tension hook: one contrarian, specific or story-led sentence.
2. One real situation the creator is in or saw.
3. One useful mechanism: what to do differently and why.
4. One hard closing line. Then cut. No "follow for more".

One idea per reel. Write it loose enough to deliver in one take.

For a reel about a new tool, repo or AI release, do not open with a feature summary:
```
[Who] did [specific surprising thing].
Then [the problem or tension it created].
So they built [product].
[One sentence: what it does.]
[Why this changes how the viewer should think.]
[One honest caveat if the source has one.]
[Concrete CTA: a finished guide, checklist or prompt.]
```
- The first two lines must create a question. "X open-sourced a platform" is a dry hook when the origin story is stronger.
- Compress the features around one mechanism. Do not list memory, files, sandboxes, connectors and crons as equal bullets.
- Exaggerate the framing, never the facts. "Challenging" does not become "a nightmare". Stars are not installs. A README's before/after is an illustration, not a benchmark.
- Spoken pace: about 2.6 words per second. 90 to 105 words is roughly 35 to 40 s. Count, do not guess.

## Titles (if asked)

- Under 60 characters. Front-load the hook. Numbers add specificity ("in 20 Minutes" beats "Fast").
- Do not repeat the thumbnail text; the two should complement each other.
- Leave a reason to click. Patterns: "I [did X]. Here's What Happened." / "Stop Using [X]. Do This Instead." / "How I [result] in [timeframe]".
- Give one strong title by default, plus two alternates only if asked.

## Output format

1. The rewritten script, ready to read.
2. A change log of 3 to 8 bullets, each naming the rule applied.
3. Retention notes (long-form only): where the hook, open loop and minute 3 / minute 6 bumps sit.
4. Word count and estimated runtime.

Example change log:
```
- Cut "think of it like a Ferrari in first gear" (rule 1). Replaced with the measured number from your notes.
- "Today I'm going to walk you through" -> "So here's the move." (rule 2)
- Split the 41-word sentence in section 2 into three (rule 5).
- Added a tease of the cost section before the setup section ends (open loop).
- 312 words, about 2 min at 2.6 words/s.
```

## When something is missing

- No source for a claim in the script: keep the claim, flag it in the change log as "unverified, check before filming". Do not delete or strengthen it.
- Creator's hook conflicts with a rule: keep their hook, mention the concern once.
- Asked for a caption instead of a script: give the caption only, no strategy notes.
- A video file was attached: use what is actually said and shown in it, not the topic of the earlier conversation.

## Keep a feedback log

When the creator says "this doesn't sound like me", write the pattern into `feedback.md` next to this file (date, what was wrong, the new rule) and read it before the next run.
