---
name: devlog-to-linkedin-post
description: Use when the user wants to turn commits, PR titles, a changelog, or "what I built this week" into a build-in-public LinkedIn post — finds the one moment with tension and writes a micro-story with a lesson, never a changelog dump.
---

# Devlog to LinkedIn Post

Turn a week of building — commits, PR titles, or a described sprint — into a
build-in-public post people actually read. The failure mode of build-in-public
is the changelog dump: "This week I shipped X, fixed Y, refactored Z." Nobody
outside the repo cares about the list. They care about the *moment*: the bug
that took three tries, the feature you cut, the refactor you dreaded that paid
off. One moment with tension beats ten bullet points of progress.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user asks to turn their commits, PRs, or dev work into a post
- The user says "I want to post about what I built" but has only a feature list
- The user is in a code repo and wants build-in-public content from real activity

## Process

1. Get the raw material. If you're running inside a repo, **offer to read the
   recent git log yourself** (`git log --oneline` over the relevant window, plus
   PR titles if available) instead of making the user summarize. Otherwise take
   their commits, changelog, or a spoken description of the week.
2. Scan the material for **the one moment with tension**. Look for:
   - a bug that resisted (multiple fix commits for the same thing, reverts)
   - a feature that was cut or descoped (and the reason)
   - a refactor or rewrite (dread → payoff, or payoff that never came)
   - a decision between two roads (and what tipped it)
   - a number that changed (build time, latency, users, lines deleted)
   If several candidates exist, present 2–3 and let the user pick the one that
   actually hurt or surprised them.
3. Write the post as a **micro-story with a lesson**:
   - Hook: start inside the moment, sized to survive the "…see more" fold
     (roughly the first 210 characters on desktop, ~140 on mobile — unofficial)
   - Middle: what happened, in 3–6 short paragraphs, concrete beats abstract
   - Lesson: one transferable takeaway a non-developer could apply
   - Close: a question or the takeaway restated, not "thoughts?"
4. **Translate the jargon.** Every technical term either gets a plain-language
   gloss in the same sentence or gets cut. "Race condition" becomes "two parts
   of the system finishing in the wrong order." The reader is a founder or
   operator, not a compiler.

## Quality bar (reject your own weak output)

- If the post reads as a list of things shipped, it's a changelog dump — start
  over from the single strongest moment.
- The tension must be real: something failed, cost time, got cut, or nearly
  didn't work. "I shipped a feature and it went fine" is not a story.
- The lesson must transfer beyond code. "Delete the clever thing" works for a
  marketer; "memoize your selectors" does not.
- No AI tells: no "I'm excited to share", no "journey", no enumerator adverbs,
  0–1 emoji.
- Keep real specifics from the log: the actual number of attempts, the actual
  thing deleted, the actual duration. Don't round them into vagueness.

## The step the user must do

Tell the user to check the story against what actually happened and restore any
detail you softened — the real error message, the real number of hours, the
real reason the feature got cut. Build-in-public only compounds when readers
can trust the log.

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

Web version of this tool: https://liftli.ai/tools/devlog-to-post.html
