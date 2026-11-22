---
name: objection-handler
description: >-
  Objection Handler. Answers every objection, and knows a no when it hears one. Matches what they said
  ("it isn't built yet", "what if you never ship it", "why pay up front", "too expensive", "I need to ask my
  CFO") to an honest answer filled in from your own terms, and shows why it works. A real no gets no answer
  at all: it stops the deal for good. Every answer is a draft for your yes. Use when the user says "they
  said", "how do I answer this", "what do I say to", "they pushed back", "objection", "they think it's too
  expensive", or pastes a reply they don't know how to answer.
argument-hint: "<what they said>"
---

# objection-handler

When you're asking for money before the product exists, the objections are good ones. So the answers have to be
honest, specific and short. This skill has the answer ready, filled in from your real terms. It also knows the
difference between a worry, which deserves an answer, and a no, which deserves to be left alone.

`${CLAUDE_SKILL_DIR}` below is this skill's folder (where this SKILL.md lives).

```bash
python3 "${CLAUDE_SKILL_DIR}/objections.py" match --deal north-pier --text "What if you never ship it?"
python3 "${CLAUDE_SKILL_DIR}/objections.py" match --text "It looks great, but it's too expensive for us right now."
python3 "${CLAUDE_SKILL_DIR}/objections.py" list
```

The answers live in `objections.json`, so the user can change the words.

## A worry or a no?

- **A worry is a question, even when it sounds like a no.** "That's a lot of money." "We're busy." "I'd have to ask my CFO." Answer it, once.
- **A no is a no.** "Not interested." "We're all set." "Please stop." `match` won't give you an answer for those, even if the same sentence has an
  objection in it. Run `/follow-up stop` with their words. They hear nothing else.
- **Not sure?** Ask one honest question and don't assume. "Is this something you'd like me to drop, or is it the timing?"

## Steps

1. Log their reply: `followup.py reply`. A no stops everything there.
2. `objections.py match --deal <id> --text "<what they said>"`. It shows the label, what to say and why.
3. Rewrite it in the user's voice and for this person, using their words from the call. Keep it to 3 sentences. Fill any `[fill: ...]`, or ask the
   user: never make one up. No match means asking them a question, not guessing.
4. **Ask.** Show it. "Send this reply to Renee? Reply yes or no." One message per question.
5. **Send.** On a yes, in the same thread from the user's account. If they push back again on the same point, stop answering it and ask what would
   have to be true. One answer per objection: the third round is pestering.

## What it knows

| they say | it answers |
| --- | --- |
| It isn't built yet | You're right, and here's what you get instead: the date, a say in it, the refund. |
| What if you never ship it? | Fair question. Here's the way out, in writing. Want to talk first? |
| Why pay up front? | Paying is what gets it built your way. If all of it is hard, tell me what you could do. |
| It's too expensive | Agree, put it next to what they pay today, find out which part is the problem. |
| Not the right time | What would need to be true? If there's a date, come back then and not before. |
| I need to think | Is there one thing you'd want answered first? |
| I have to ask my boss | Here's one page to forward. Happy to join. |
| We already have someone | When does that come up for renewal? |
| Who else uses it? | You'd be one of the first, which is why it's priced like this. |

## Example from the reel's board

Renee: "It looks great, but what if you never ship it?" The answer: "Fair question, and you should ask it. If it has not shipped by the promised date, or
we can't build what you asked for, you get every dollar back. You pay through Stripe and you get a receipt, and I'll put the refund in writing. Want to
talk on a call before you decide?" (Illustrative: Renee is fictional.)

## What it never does

- Never answers a no, and never tries to talk someone out of one.
- Never sends a reply by itself.
- Never invents a customer, a result, a discount or a deadline to win an argument. "You'd be one of the first" is the honest answer, so it says that.
- Never says anything untrue or unkind about a competitor.

## Consent and truth

- Nothing is sent or charged without the user's explicit yes for that exact message. Claude drafts, the user says "yes", then it goes out from the
  user's own accounts. One yes per message. Never "yes to all".
- Stop at the first "no" or any sign of disinterest. A request to stop is honoured forever, across every skill.
- Never invent a number, a result, a client or a deadline. Fill in only what is true and ask when something is missing.
