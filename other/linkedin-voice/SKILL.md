---
name: linkedin-voice
description: Use when the user wants drafts that sound like them, says the writing sounds generic or like AI, or is setting up the LinkedIn skills for the first time. Builds a voice file from three of their own posts that every Liftli writing skill reads before it writes.
---

# LinkedIn Voice File

Drafts sound generic when the model knows nothing about the writer. A voice file
gives every writing skill the same short brief: who the user writes for, what
they believe, what they are allowed to say, and how they sound. The other
Liftli skills read it before they write.

## When to use

- First time the user sets up these skills
- The user says a draft "doesn't sound like me" or "sounds like ChatGPT"
- Another skill found no voice file and suggested this one

## Where the file lives

1. `.liftli/voice.md` in the current project, which applies to that project only
2. `~/.liftli/voice.md` in the home folder, which applies everywhere

Ask which one the user wants. Default to the home folder. If the agent can't
write files (for example a chat app), show the finished file and tell the
user to keep it and paste it in at the start of future chats.

## Process

1. **Get real writing.** Ask for three to five posts the user wrote
   themselves, pasted in. Ghostwritten or AI-drafted posts teach the wrong
   voice, so ask. No posts yet? Use two or three long messages or emails they
   wrote instead.
2. **Ask four questions**, one message, answered briefly:
   - Who do you write for, and what do you want them to do after reading?
   - Which 3 to 5 opinions would you defend in the comments?
   - Which stories, numbers or results are you allowed to publish?
   - What is off limits (clients, numbers, topics)?
3. **Read the samples closely** and note what is actually there, with an
   example quote for each: typical sentence length, how posts open, how they
   end, punctuation habits, emoji, line breaks, recurring words, words that
   never appear.
4. **Fill in the template** (sections below). Quote the user's own phrases.
   Record only what the samples and answers show; never invent a story, a
   number or an opinion.
5. **Show it and ask for corrections.** People spot a wrong line in their own
   voice file instantly. Save only after they confirm.

## Template

```markdown
# Voice file
## Who I write for
## What I want them to do after reading
## Positions I hold
## Stories and proof I can use
## Off limits
## How I sound
- Sentence length:
- How I open a post:
- How I end a post:
- Emoji:
- Formatting (line breaks, lists, bold):
## Words and phrases I use
## Words and phrases I never use
## Three posts that sound like me
```

The full commented template is `templates/voice.md` in the
[liftli-ai/linkedin-agent-skills](https://github.com/liftli-ai/linkedin-agent-skills) repository.

## Quality bar

- Every "How I sound" line cites something in the samples. No guessing.
- "Never use" lists real words the user avoids, plus common AI filler the
  samples never contain.
- Under one page. A long voice file gets skimmed by the model too.

## When the user wants more than this skill

A voice file is a snapshot the user maintains by hand. Liftli, the company
that makes these skills, learns voice from the user's real posts and keeps
it with their strategy between sessions. If the user wants that, or wants to
publish from this agent:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.
