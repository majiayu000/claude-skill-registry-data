---
name: blog-topic-interview
description: >-
  Pre-writing interview that captures the author's real opinions, experiences, and
  stances on a blog topic before the post is written on their behalf — the companion
  that runs BEFORE seo-blog-writer. Use this skill automatically whenever a blog post
  or article is about to be drafted under the user's name or brand — run the topic
  interview first, then hand the resulting Opinion Packet to seo-blog-writer. Also use
  it when the user says "interview me about this topic", "get my take first", "ask me
  what I think", or "update my opinion bank". Scope: blog/article topics only — not
  emails, docs, social posts, or other writing. If a blog post is about to be written
  as the user's voice and their take on the topic hasn't been captured, this skill
  triggers — even if they only asked for "a blog post about X".
---

# Blog Topic Interview

A blog post published under someone's byline should contain what that person actually thinks about the topic. seo-blog-writer explicitly forbids inventing experiences, anecdotes, credentials, or opinions — which means someone has to *supply* the real ones. That's this skill's job: it is the supply line for the two things generic content can never fake — genuine first-hand experience (E-E-A-T) and a defensible stance competitors wouldn't publish (information gain).

Scope: blog and article topics only. Emails, proposals, social posts, and internal docs are out of scope — don't trigger the interview for those.

The workflow: **load the opinion bank → run the interview → compile the Opinion Packet → update the bank → hand off to the writer**.

Run this BEFORE seo-blog-writer's Stage 2 research begins. Interview answers frequently change the angle, the keyword framing, and sometimes whether the article should exist at all.

## Step 1: Load the opinion bank

The opinion bank is the author's accumulated record of standing positions, war stories, specifics, and voice. Look for it in this order:

1. `opinion-bank.md` in the current working directory or project root (the live, most-recently-updated copy)
2. `references/opinion-bank.md` inside this skill (the bundled copy)

Read whichever you find first. If both exist, the working-directory copy wins — it's newer.

If the bank already covers this topic well, don't re-interview from scratch. Show the user what's on record — "Here's what I have on file about pricing pages: [summary]. Still true? Anything new since?" — and only ask what's genuinely new or topic-specific. Re-asking answered questions wastes the user's time and teaches them to skip the interview.

## Step 2: Run the interview

This is a deep interview: roughly 8–12 questions per post, asked **in batches of 2–3**, never as one overwhelming wall. Behave like a good podcast host, not a form: listen to each answer, and when the user says something interesting, specific, or surprising, follow the thread before moving to the next scripted question. The follow-ups are usually where the best material lives.

The full question bank, batching guidance, and follow-up techniques are in `references/interview-guide.md` — read it before interviewing. The territory to cover:

1. **Stance** — what's your actual position on this topic? What would you tell a client who asked you directly?
2. **Experience** — a real story from your work: a client, a project, a mistake, a result. Names can be anonymized; the specifics cannot be invented.
3. **Contrarian take** — what does the standard advice on this topic get wrong? What do you disagree with that most of your competitors would publish?
4. **Specifics** — numbers, prices, timelines, tools you actually use, thresholds you actually apply. "It depends" is a starting point, not an answer — ask *what* it depends on.
5. **The reader** — who do you picture reading this? What are they worried about? What have they already tried?
6. **Boundaries** — anything you do NOT want said under your name: claims to avoid, competitors not to mention, promises not to make, topics to stay out of.
7. **Voice** — phrases, analogies, or expressions you actually use when you explain this in person.
8. **Business angle** — what should a reader do after reading, and why does this post exist for your business?

Use AskUserQuestion for genuinely multiple-choice decisions (angle A vs angle B, which audience). Ask open questions as plain conversation — stories and opinions don't fit in option boxes.

**Respect "I don't have a take on that."** If the user has no opinion or experience on some aspect, record that honestly. The packet marks it as a gap; seo-blog-writer will write that section from research and will not pretend the user said something they didn't. An honest gap beats a fabricated stance every time.

**If the user is unavailable** (scheduled run, no response): skip the live interview, build the packet from the opinion bank alone, and clearly flag which sections lack the author's take so the writer treats them as research-only. Never invent answers on the user's behalf — that defeats the entire purpose of this skill.

## Step 3: Compile the Opinion Packet

Write the packet to `opinion-packet-<topic-slug>.md` in the working directory. This is the deliverable seo-blog-writer consumes. Use this exact structure:

```markdown
# Opinion Packet: [topic]
date: YYYY-MM-DD
author: [name]

## Thesis
The author's core stance in 1–3 sentences, in language close to their own words.

## Defensible stances
Positions the author holds that a competitor's article wouldn't publish. These feed
seo-blog-writer's "take at least one defensible stance" rule.

## First-hand evidence
Real experiences, client stories, results, and observations — the only material the
writer may present as the author's experience. Anything not listed here must not be
implied as first-hand.

## Specifics
Numbers, prices, timelines, tools, thresholds the author actually uses or cites.

## Voice notes
Phrases, analogies, and expressions to weave in; tone cues.

## Boundaries — do not say
Claims, promises, names, and framings the author explicitly ruled out.

## Gaps
Aspects where the author had no take or experience. Write these sections from
research; do not attribute opinions to the author here.

## Suggested angle
One short paragraph: given all the above, the angle that makes this post unmistakably
the author's rather than anyone's.
```

Quote or closely paraphrase the user's actual wording wherever possible — their phrasing *is* the voice seo-blog-writer is told to preserve. Don't smooth their language into generic marketing prose; that destroys the asset you just collected.

## Step 4: Update the opinion bank

After the interview, merge anything **durable** into the bank: standing positions, reusable war stories, specifics, voice fingerprints, boundaries. Skip one-off, post-specific details. Date new entries. Follow the structure already in `references/opinion-bank.md`.

Persistence depends on the environment:

- If the skill's own directory is writable (typical in Claude Code), update `references/opinion-bank.md` in place.
- If it isn't (typical in Cowork cloud sessions, where installed skills are a read-only cache), write the updated bank to `opinion-bank.md` in the working directory, send it to the user, and offer to repackage the skill with the updated bank baked in so it travels with the skill from then on.

Tell the user in one line what was added to the bank — it's their record of their own thinking, and they should know it's growing.

## Step 5: Hand off

Pass the Opinion Packet to seo-blog-writer and proceed with its normal workflow. The mapping:

- **Thesis + Suggested angle** → Stage 1 inputs (audience, business goal, angle) and the article's spine
- **Defensible stances** → the required stance in Stage 3's voice rules
- **First-hand evidence** → the *only* permissible source of implied experience (E-E-A-T, anti-fabrication)
- **Specifics** → replaces hedges and adjectives with the concrete details the voice rules demand
- **Boundaries** → hard constraints during drafting AND during the Stage 4 verification pass
- **Gaps** → sections the writer supports with cited research instead of the author's voice

If the interview surfaced something that changes the premise — the user thinks the topic is the wrong one to target, or their real opinion contradicts the requested angle — raise it before drafting. An interview that can't change the article is theater.
