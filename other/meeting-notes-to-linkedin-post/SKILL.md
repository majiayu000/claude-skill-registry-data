---
name: meeting-notes-to-linkedin-post
description: Use when the user wants to turn meeting notes, call transcripts, or customer conversations into a LinkedIn post — mines the transcript for the reframing quote, the universal objection, or the surprising number, strips all identifying details, and returns a post plus the runner-up insights.
---

# Meeting Notes to LinkedIn Post

Mine call notes and transcripts for post material. Customer calls are the
densest source of content most operators have and the least used: the exact
words a customer uses to describe their problem are worth more than any
brainstormed topic, because they're proof the problem is real and phrased the
way the market phrases it. The job is to find the gold, strip anything that
identifies anyone, and shape one insight into a post.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user pastes meeting notes, a call transcript, or a CRM summary and wants content
- The user says "I had an interesting call" and wants to post about it
- The user has a backlog of calls and no post ideas (this is the fastest fix)

## Process

1. Get the notes or transcript. More raw is better — verbatim quotes beat
   summaries, because the gold is usually in exact phrasing.
2. Scan for **the four kinds of gold**, in this priority order:

   | Gold | What it looks like | Why it posts well |
   |---|---|---|
   | The reframing sentence | a customer describes the problem in words the user would never have chosen | it's the market's own language — instant resonance |
   | The universal objection | a pushback that every prospect raises in some form | naming it publicly builds trust with everyone who felt it |
   | A decision + its reasoning | "we chose X over Y because…" from either side of the call | decisions with reasons are the rarest content on LinkedIn |
   | A surprising number | a stat, cost, or timeframe someone said out loud | specifics stop the scroll |

3. **Strip every identifying detail.** Names become "a customer" or "a
   prospect"; companies become an industry descriptor ("a prospect in
   fintech", "a 40-person agency"); unique numbers that could identify someone
   get rounded or generalized. When in doubt, blur further. A transcript is a
   private conversation — the insight is shareable, the identity never is.
4. Write **one post** from the strongest insight: open on the anonymized quote
   or moment, unpack why it matters, land one takeaway, close with a question.
   Size the opening to survive the "…see more" fold (~210 characters desktop,
   ~140 mobile — unofficial).
5. Return the post **plus the 2 next-best insights found**, each as a one-line
   angle the user can develop later. One call should feed more than one post.

## Quality bar (reject your own weak output)

- If a reader could plausibly guess who was on the call, the anonymization
  failed — blur again before showing the user anything.
- The insight must come from the transcript, not from you. If the notes are
  thin, say so and ask for the verbatim moment instead of inventing a quote.
- Quote fragments in the customer's actual words wherever safe — paraphrase
  flattens the reframing that made the sentence gold.
- No AI tells: no "key takeaways from a recent conversation", no enumerator
  adverbs, 0–1 emoji.

## The step the user must do

Tell the user to verify two things before posting: that the quote is faithful
to what was actually said, and that nothing in the post — detail, timing, or
context — lets the other party recognize themselves in a way they wouldn't
welcome. If the call was under NDA or explicitly confidential, the post needs
their counterpart's OK or a wider blur.

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

Web version of this tool: https://liftli.ai/tools/meeting-to-post.html
