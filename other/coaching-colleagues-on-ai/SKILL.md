---
name: coaching-colleagues-on-ai
version: "1.1.1"
description: >
  Guides informal AI coaching conversations with Loxihart colleagues — from
  first questions to skeptic conversations to helping power users go deeper.
  Activates when a colleague asks about AI tools, when someone is skeptical
  about AI at work, when a teammate needs help getting started with Claude,
  when someone is stuck on a specific AI task, when a peer asks if AI is
  appropriate for their work tasks, when someone expresses concern about AI
  replacing jobs, when facilitating one-on-one AI onboarding, or when
  helping a coworker get a better result from a prompt. Also triggers on:
  colleague asking about Claude, show someone AI, help coworker with AI,
  AI skeptic, explain AI to teammate, coworker AI question, peer AI
  coaching, informal AI training, one-on-one AI session, AI adoption
  conversation, someone wants to learn AI, colleague frustrated with AI.
---

# Colleague AI Coaching

Handles informal AI coaching conversations at Loxihart. Reads the opener,
calibrates to the person, gives one concrete thing, and follows up.

---

## Evals

**Should trigger:**
1. "A coworker asked me how they'd even get started using Claude — what do I tell them?"
2. "One of my teammates thinks AI is useless and doesn't see the point — how do I talk to them about it?"
3. "A peer tried Claude, got a bad result, and asked me why it didn't work"

**Should NOT trigger:**
1. "Help me get better at using Claude for my own work" — that's improving your own usage, not coaching another person; this skill doesn't fit (no specific alternative — just out of scope)
2. "Write a leadership brief about AI adoption for [PERSON]" — formal leadership communication → briefing-loxihart-leadership

---

## Decision Tree

```
What's the opener?
  ├─ "I want to try this / how do I start?" → Curious Beginner (Section 2)
  ├─ "I tried it but the results weren't useful" → Disillusioned (Section 3)
  ├─ "I'm not sure AI is right for me / my work" → Skeptic (Section 4)
  ├─ "I'm already using it — I want to do more" → Power User (Section 5)
  └─ "I'm worried about my job / AI replacing people" → Existential (Section 6)
```

If the opener is ambiguous, ask one question: "Have you tried it yet,
or are you just starting to think about it?"

---

## Section 1: Core Principles

Full conversation patterns in `references/conversation-patterns.md`.
Adoption signal logging in `references/adoption-signals.md`.

**Ask before explaining.**
"What have you tried so far?" surfaces the actual blocker faster than
any tutorial. Most colleagues who ask for help have already tried
something — find out what before restarting from zero.

**Give one thing, not a curriculum.**
The most common coaching mistake is overwhelming the person with
options. Identify the single highest-value thing they could try based
on their actual work tasks. One thing. Not three. Not a list.

**Acknowledge before redirecting skeptics.**
A colleague who is worried about AI is not ready for a demonstration.
They need acknowledgment first. "That's a real concern a lot of people
have" is not patronizing — it's the prerequisite for any productive
next step.

**Follow up once.**
Three days after a session, send a single Slack message: "How did
[the thing you showed them] go?" One follow-up. Not a check-in series.
The follow-up signals you care and creates accountability without
pressure.

**Log the signal.**
After every coaching conversation, note in your adoption log what the
person tried, what their blocker was, and whether they're using AI now.
This is the qualitative data that the survey misses. See
`references/adoption-signals.md`.

---

## Section 2: Curious Beginner

Someone who wants to try but hasn't started, or has just started and
wants guidance.

**Opener pattern:**
1. "What kind of work tasks take up the most of your time right now?"
2. Map their answer to a single AI use case for that task
3. Show it live — open Claude, type the prompt, show the output
4. Let them try one variation while you're there
5. "Try this on a real task this week and let me know how it goes"

**The one-thing selection guide:**
- Lots of writing / documentation → show prompt-for-draft pattern
- Lots of research / reading → show summarization pattern
- Repetitive tickets or requests → show template generation
- Troubleshooting → show "explain this error" pattern
- Uncertainty about format or tone → show rewrite/reformatting

**What not to do:** Don't open with "so, AI is really changing
everything..." — start with their task, not the technology.

---

## Section 3: Disillusioned

Someone who tried Claude (or another AI tool) and got bad results.

**Opener pattern:**
1. "What did you try and what happened?"
2. Diagnose the gap: bad prompt, wrong tool, unrealistic expectation,
   or real limitation?
3. Show the fix for the specific thing that failed — not a general
   tutorial
4. "The output you got makes sense given how it was prompted — here's
   the adjustment."
5. Let them re-run their actual failed task with the fix applied

**Common gaps and fixes:**

| What happened | Likely cause | Fix |
|---|---|---|
| Output was too generic | Prompt had no context | Add role, context, and constraints |
| Output was wrong/hallucinated | Treated it as a search engine | "Claude reasons, it doesn't look things up — verify factual claims" |
| Output was too long / too short | No length instruction | Add "in 3 bullet points" or "in one paragraph" |
| Didn't do what I asked | Ambiguous ask | Rewrite ask as a command with explicit output format |
| Got worse results than expected | Expectations were calibrated to demos | "Demos show best-case — real use requires iteration" |

**What not to do:** Don't minimize their frustration ("oh it works
great once you learn it") — diagnose what actually went wrong.

---

## Section 4: Skeptic

Someone uncertain whether AI is appropriate for their work, or
doubtful it will be useful.

**Opener pattern:**
1. "What specifically concerns you about using it?" — don't assume
   the concern; ask for it
2. Reflect the concern back accurately before responding to it
3. Find the smallest possible demonstration relevant to their actual
   concern
4. "What would it take for you to think it was worth trying on one task?"
5. Agree on that one low-stakes task. Don't push further.

**Common concerns and responses:**

| Concern | Response approach |
|---|---|
| "I might make mistakes / publish something wrong" | Agree that verification is required. Show how to use it as a draft, not a final output. |
| "It doesn't know our systems or processes" | "That's right — it's a thinking and writing tool, not a database. Show me a task where thinking or writing is the bottleneck." |
| "I don't have time to learn a new tool" | "What's the one task that takes the longest and requires the least judgment? That's where 20 minutes pays off immediately." |
| "It's not accurate enough" | "For what specifically? Let's find one task where accuracy is verifiable — so you can check it and decide." |

**What not to do:** Don't argue with the concern. Don't demonstrate
something impressive unrelated to their actual work. Don't push for
immediate adoption.

---

## Section 5: Power User

Someone already using AI tools who wants to go deeper.

**Opener pattern:**
1. "What's the highest-friction thing in your workflow right now —
   even if you're not sure AI can help?"
2. Look for: repetitive tasks with structure (automation candidates),
   multi-step tasks (chaining candidates), knowledge retrieval
   tasks (context-injection candidates)
3. Show one pattern upgrade: system prompt, multi-turn strategy, or
   tool use pattern appropriate to their current level
4. Share one resource (a specific skill, a specific prompt pattern)
   rather than a general "here's more to explore"

**Don't overwhelm with options.** A power user's risk is breadth
without depth — they know a lot of mediocre approaches instead of
a few excellent ones. Help them go deeper on one thing they're
already doing.

---

## Section 6: Existential Concern

Someone worried about AI replacing their job. This is a real concern
and cannot be bypassed with a demonstration.

**This conversation is not a coaching session — it is a human
conversation first.**

1. Don't start with "well, actually AI creates jobs too..."
2. Acknowledge the concern directly: "That's not a paranoid thing to
   worry about — a lot of roles are changing."
3. Ask: "What specifically are you worried about — is it your current
   role, or something longer-term?"
4. Based on their answer: either discuss what's actually changing in
   their specific domain, or (if they're open to it) explore how
   learning AI tools could strengthen their position specifically
5. Do not push toward adoption. This conversation has succeeded if
   they feel heard.

**If they're open to exploration after the above:** treat them as a
curious beginner and run Section 2.

---

## Self-Verification

Before any coaching session:
- [ ] I know what kind of conversation this is (beginner / disillusioned /
  skeptic / power user / existential)
- [ ] I have one specific thing prepared to show, not a curriculum
- [ ] I will ask what they've tried before demonstrating anything
- [ ] I have the follow-up reminder set for 3 days out

After any coaching session:
- [ ] Logged the adoption signal (see references/adoption-signals.md)

---

## CLAIMS
- Giving one concrete thing to try is more effective than a comprehensive
  overview — it reduces decision paralysis and creates a clear
  success-or-failure signal the person can report back on
- Asking what they already tried before explaining anything surfaces the
  actual blocker faster than a tutorial approach
- Logging coaching conversation signals creates the qualitative data that
  quantitative adoption surveys consistently miss

## COUNTEREXAMPLE
- The "one thing" approach fails when the underlying concern is existential
  (job threat) rather than practical — that conversation requires
  acknowledgment before any task demonstration is appropriate

## CONTRADICTIONS
- "Don't give a tutorial" conflicts with situations where someone
  genuinely needs step-by-step onboarding — read the opener; some
  people need the structured walkthrough, especially for first-ever use
