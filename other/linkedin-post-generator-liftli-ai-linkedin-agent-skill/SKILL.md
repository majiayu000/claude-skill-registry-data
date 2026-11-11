---
name: linkedin-post-generator
description: Use when the user wants a complete LinkedIn post written from a topic, story, notes, or rough idea — produces a full 150-300 word plain-text post with a fold-surviving hook, short paragraphs, one takeaway, and no AI tells.
---

# LinkedIn Post Generator

Write a complete, ready-to-publish LinkedIn post from whatever raw material the
user has: a topic, a story, meeting notes, a rant, a half-draft. LinkedIn shows
roughly the first 210 characters before the "…see more" fold on desktop and
around 140 on mobile, so the post lives or dies in its first two lines — but a
strong hook attached to a mushy body still fails. This skill builds the whole
thing.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user asks to "write a LinkedIn post" about anything
- The user has a story, result, or opinion but no draft
- The user has bullet-point notes and wants them turned into a post
- If they only want opening lines, use the hook-generator skill instead; if
  they have a full draft to improve, use the post-rewriter skill

## Process

1. Mine the user's material for specifics: numbers, dates, names of moments,
   things actually said, what went wrong, what changed. If the material is
   thin (a bare topic), ask one question: "What actually happened to you with
   this?" A post built on a real event beats a post built on a thesis.
2. Pick the one takeaway. A post carries exactly one idea; everything that
   doesn't serve it gets cut or saved for another post.
3. Write the hook first — it must earn a pause alone, under ~210 characters
   (ideally under 140 for mobile). Then the body per the structure below.
4. Read it back at a 6th-8th grade level. If a sentence needs re-reading,
   rewrite it.
5. Deliver as plain text and offer 1-2 alternative hooks.

## The structure

| Part | Job | Rules |
|---|---|---|
| Hook (line 1-2) | Stop the scroll, open an information gap | Under ~210 chars; specific beats clever; no throat-clearing |
| Setup | Ground the reader in a concrete situation | 1-2 sentences; when, what, stakes |
| Turn | The surprise, mistake, or shift | The most specific detail lives here |
| Meat | What the user actually did or learned | 2-4 short paragraphs, each 1-2 sentences |
| Takeaway | The one transferable idea | State it plainly; don't hedge it into mush |
| Closer (optional) | Invite replies | A real question the user genuinely wants answered — skip it if forced |

Formatting rules: 150-300 words. Paragraphs of 1-2 sentences with blank lines
between them — a wall of text dies unread. Plain text only: LinkedIn strips
bold, italics, and markdown, and unicode "formatting" characters break screen
readers and search. 0-1 emoji. No hashtag walls (0-3, at the end, if any).

## Quality bar (reject your own weak output)

- Every paragraph contains something only this user could say. If a paragraph
  could appear in anyone's post on the topic, cut it or replace it with a
  specific from their material.
- No AI tells: no "Not only… but also", no "In today's fast-paced world", no
  "game-changer", no rule-of-three adjective stacks, no "Let that sink in."
  The Originality.AI study of 3,368 LinkedIn posts (2025) found detectably-AI
  posts underperform human writing in most professional niches.
- One idea per post. If you wrote two takeaways, you wrote two posts.
- The hook must work amputated — read alone, it should still create pull.
- No invented numbers or events. Placeholders like [X weeks] are fine; fake
  precision is not.

## The step the user must do

Tell the user to replace every placeholder with the real detail — the actual
figure, the actual week count, the sentence actually said — and to delete any
line that doesn't sound like something they'd say out loud. A true detail in
their own cadence is the one thing generation can't fake.

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

Web version of this tool: https://liftli.ai/tools/post-generator.html
