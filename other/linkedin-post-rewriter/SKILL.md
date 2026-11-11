---
name: linkedin-post-rewriter
description: Use when the user has an existing LinkedIn post or draft that underperformed or feels flat and wants it improved — rewrites it in their voice, fixing buried hooks, walls of text, AI phrasing, and weak endings, without inventing facts.
---

# LinkedIn Post Rewriter

Take a post the user already wrote and make it perform, without making it
stop sounding like them. Most underperforming posts don't have an idea
problem — they have a delivery problem, and it's almost always one of four
specific, fixable failures. The user's facts, opinions, and voice are the
raw material; the rewrite only changes how they're delivered.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user pastes a draft or published post and asks to improve, punch up,
  tighten, or "fix" it
- A post flopped and the user wants to know why and get a better version
- The user wrote something that "sounds like AI" and wants it humanized
- If they want a brand-new post from scratch, use the post-generator skill;
  if they only want a stronger first line, use the hook-generator skill

## Process

1. Read the draft and find its best moment — the most specific detail, the
   real insight, the line with actual voltage. That becomes the center of
   the rewrite; often it becomes the hook.
2. Diagnose against the four reach-killers below. Name which ones the draft
   has — usually two or three.
3. Rewrite. Keep every fact, number, and claim exactly as the user stated
   it. Keep their vocabulary and cadence — if they write short and blunt,
   the rewrite is short and blunt. Reorder, cut, and sharpen; do not add.
4. Output the rewritten post, then a bullet list: each change made and the
   reason (tied to a reach-killer). The list is half the value — it teaches
   the user to self-edit next time.

## The four reach-killers

| Killer | What it looks like | The fix |
|---|---|---|
| Buried hook | The good line sits in paragraph 3; lines 1-2 are warm-up ("I've been thinking about…") | Promote the best line above the ~210-char desktop fold (~140 on mobile); delete the warm-up entirely |
| Wall of text | Paragraphs of 4+ sentences, no white space | 1-2 sentence paragraphs, blank line between each; cut anything not serving the one idea |
| AI phrasing | "Not only… but also", "In today's landscape", "delve", rule-of-three adjectives, "Let that sink in" | Replace with how the user actually talks — pull phrasing from the parts of their draft that sound human |
| Weak ending | Trails off, or a generic "Thoughts?" / "Agree?" / hashtag pile | Land the takeaway in one plain sentence; close with a question only if the user genuinely wants those answers |

## Quality bar (reject your own weak output)

- Zero invented claims. If the draft says "a few weeks," the rewrite says "a
  few weeks" — never "3 weeks." No added statistics, no added events, no
  sharpened numbers the user didn't state.
- The user should recognize every sentence as something they could have
  said. If the rewrite reads like a different author, you replaced the voice
  instead of fixing the delivery — start over.
- The rewrite should usually be shorter than the original. If it grew, you
  added instead of sharpened.
- Read the new first line amputated: does it create pull alone? If not, the
  buried-hook fix failed.
- Plain text only — LinkedIn strips formatting, so no markdown, no unicode
  bold.

## The step the user must do

Ask the user to read the rewrite out loud once. Anywhere they stumble or
wince, that line still isn't theirs — have them say what they'd actually say
and swap it in. The out-loud test catches what diffing never will.

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

Web version of this tool: https://liftli.ai/tools/post-rewriter.html
