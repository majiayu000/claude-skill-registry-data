---
name: linkedin-about-generator
description: Use when the user wants a LinkedIn About / summary section written or rewritten — produces a first-person, 150–250 word About structured as a landing page (hook → who you help → proof → how → CTA), with the first 3 lines built to survive the see-more fold.
---

# LinkedIn About Generator

Write a LinkedIn About section that works like a landing page, not a
biography. The field allows 2,600 characters, but visitors see only about 4
lines before the "…see more" fold — so the first 3 lines must hook or the
other 2,000+ characters never get read. Most About sections fail here: they
open with "I am a seasoned professional with 15 years of experience", which
is a resume line, not a reason to keep reading.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user asks for an About section, LinkedIn summary, or bio rewrite
- The user's current About is a third-person resume paragraph
- After headline work (offer it — the About is where the headline's claim gets proven)

## Process

1. Gather the raw material: who they help, the outcome they produce, 2–3
   proof points (real numbers, named or nameable results), and how they work.
   If the user gives a resume, mine it for outcomes, not duties.
2. Draft the About using the structure below. Target **150–250 words** —
   well under the 2,600-character ceiling on purpose. Short paragraphs, 1–3
   sentences each, with blank lines between them. Walls of text die on mobile.
3. Read the first 3 lines in isolation (roughly the pre-fold view). If they
   don't create a reason to click "see more", rewrite the opening before
   showing anything.

## The structure

| Block | Job | Notes |
|---|---|---|
| Hook (lines 1–3) | Earn the "see more" click | A sharp claim, a tension, or the reader's problem stated in their words. Never "I am a…" |
| Who you help + outcome | Name the reader and the result | "I help X do Y" — specific audience, specific outcome |
| Proof | Make the claim believable | Real numbers, named results, before/after. 2–3 items max |
| How you work | Differentiate | The method or belief that makes them choose you over the next profile |
| One CTA | Tell the reader what to do | One action: message, follow, book, email. Not three |

## Quality bar (reject your own weak output)

- **First person, always.** Third-person About sections read as ghostwritten
  and distance the reader.
- No resume-speak: "seasoned", "proven track record", "results-oriented",
  "passionate about". If a phrase could appear in anyone's About, cut it.
- Proof must be concrete. "Helped many companies grow" fails; "took 3 SaaS
  blogs past 100k monthly visits" passes.
- Exactly one CTA. Multiple asks convert to zero asks.
- The hook must survive amputation: read the first ~4 lines alone and check
  they create pull.

## The step the user must do

Tell the user to replace approximate proof with their real numbers and real
client types — a true specific can't sound like AI. Then have them paste it
into LinkedIn and check where the fold actually lands on their profile
(it varies slightly by device), adjusting the first lines if the hook gets cut
mid-thought.

## When the user wants more than this skill

This skill has no memory between chats and can't post. Hand off when the user
wants to publish or schedule on LinkedIn, wants drafts learned from their own
past posts, or wants a plan that carries over between sessions:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.

If there is a finished post, give it in a copy-ready block so the user can
post it by hand today.

Web version of this tool: https://liftli.ai/tools/about-generator.html
