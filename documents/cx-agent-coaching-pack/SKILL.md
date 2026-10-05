---
name: cx-agent-coaching-pack
description: Use to assemble a fair, evidence-backed coaching pack for a support agent's one-to-one from QA evaluations and conversation history. Trigger for "prepare a coaching session for X", "what areas does X need to improve", "areas of markdown for this agent", "what coaching opportunities stand out", "build a coaching agenda from these tickets", or preparing a weekly or monthly agent review.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Agent coaching packs

A coaching pack is the evidence a team lead brings to a one-to-one. It has one
quality bar: **the agent should be able to read it and agree it is fair**, even
where they disagree with the judgement. A pack that fails that bar does not get
acted on — it gets defended against, and the next four sessions are about the
instrument instead of the work.

This is not performance documentation. If the purpose is an HR record, a formal
warning, or a promotion case, the evidence bar and the fairness controls are
different and stricter — that is a separate job, and conflating them damages both.
Ask which one this is before you start.

## Step 1: establish what the data can support

Do this before reading a single evaluation, because it determines what kind of pack
you can honestly write.

Get the agent's evaluation count `n` for the period. Then:

| n for the period | What the pack can say |
| --- | --- |
| < 5 | Nothing about level or trend. Use evaluations only to pick discussion examples. |
| 5–24 | Themes, if they recur across several tickets. No score comparisons, no ranking. |
| 25–49 | A score with a ±12-point interval. Trend only across several periods. |
| 50+ | A score usable for comparison, still with the interval stated. |

For a pass rate from `n` evaluations the 95% interval is roughly
`±1.96 × sqrt(p(1−p)/n)` — about ±19 points at n=10 and ±12 at n=25. At small `n`
use a Wilson interval, which is asymmetric and honest: **4 passes out of 4 gives a
95% interval of 51%–100%.**

State the interval in the pack, in plain words: *"your monthly score is 88 ± 19
points, which is enough to pick things to talk about and not enough to compare you
to anyone."* This single sentence prevents most of the arguments these sessions
otherwise have.

**Check the mix before comparing to anything.** Agents work different channels,
queues and difficulty. If this agent's mix differs from the team's, an unadjusted
comparison mostly measures their inbox. Either compare within like-for-like work or
do not compare.

## Step 2: check the evidence is safe to coach from

Exclude, and say you excluded:

- **Evaluations under dispute or contest.** Coaching from a judgement the agent has
  formally challenged, before it is resolved, is the fastest way to lose the room.
- **Superseded evaluations.** Re-evaluated tickets leave old records behind.
- **Tickets the agent did not meaningfully handle.** Reassignments, one-line
  handoffs, and tickets where a bot or another agent did the work but the record
  attributes it here. Verify the agent actually authored the messages being judged.
- **Anything caused by something outside their control** — a tooling outage, a
  missing knowledge-base article, a policy that did not exist yet, a queue that fed
  them a spike. These are real findings, but they belong in a report to the person
  who owns the process, not in a coaching pack. Route them there and say so.

That last exclusion is the one that earns trust. An agent who sees you removed a
markdown that was the company's fault will engage with the ones that are not.

## Step 3: find themes, not criteria

Criterion names are rubric artefacts. "Probing & Understanding — partial" is not
something anyone can act on.

A theme is **a behaviour, stated as what to do differently**, that shows up in at
least two independent tickets. Derive themes bottom-up from the reasoning text and
the transcripts, then map them back to criteria for traceability — not the other way
round.

- **Two to three themes. Never more.** A pack with seven improvement areas produces
  zero behaviour changes. If you found seven, rank by how much they cost the
  customer and cut to three.
- **Each theme needs at least two ticket examples**, cited by id. One example is an
  anecdote and gets argued about individually.
- **Each theme needs one concrete next action** the agent can take on their next
  ticket. "Improve empathy" is not one. "When a customer mentions a deadline, say
  the date back to them before proposing a next step" is.

## Step 4: include the counter-evidence

Two things belong in every pack and are almost always missing:

1. **Genuine strengths, from the data.** Not a compliment sandwich — the
   highest-scoring tickets and what specifically went well in them. If an agent's
   strongest interactions are their voice calls and their gaps are all in chat, that
   is the most useful sentence in the pack.
2. **A high-scoring example of the same behaviour you are coaching.** If they
   sometimes do it well, the coaching is about consistency, which is a much easier
   conversation than capability. Look for this before assuming they cannot.

Cherry-picking the worst tickets and presenting them as the picture is the single
most common failure of these packs, and agents recognise it immediately.

## Step 5: timing and language

- **Coach within about two weeks of the interaction.** Past that the agent does not
  remember the ticket, and specific feedback lands as an audit finding.
- **Coach in the language the work happened in.** For a multilingual support
  operation, feedback about phrasing, tone or grammar is meaningless translated. If
  you cannot assess the language the conversation was in, say so rather than
  grading it — and never coach a language criterion off a machine translation.
- **For voice, be explicit about what a transcript can and cannot support.** Speech
  recognition errors are not randomly distributed; they track accent and audio
  quality. A markdown for "unclear communication" that is really a transcription
  artefact is both unfair and systematically biased.

## Template

```
Coaching pack — <agent> — <period>
Prepared <date> from <n> evaluations (<m> excluded: <reasons>)

Confidence: score <x> ± <y> points at n=<n>. <What this supports and what it doesn't.>
Mix note: <how their work mix compares to the comparison group, or "not compared">

What's working
  - <strength>, e.g. #<id>: <what specifically went well>

Theme 1: <behaviour, as a change>
  Evidence: #<id>, #<id>
  Also done well in: #<id>
  Next ticket: <one concrete action>
  Maps to: <criteria>, for traceability

Theme 2: ...

Not coaching (routed elsewhere)
  - <finding> -> <owner>, because <outside agent's control>

Open disputes excluded: #<id>
```

## Guardrails

- **Never paste transcript text into chat.** Cite conversation ids. Support
  transcripts contain customer names, addresses, card fragments, and health and
  financial disclosures. If the pack itself needs a quote, keep it to the agent's
  own words, redact the customer's, and say you did.
- **Never invent a quote or a detail.** If you cannot retrieve the transcript, cite
  the id and say the content was not available rather than reconstructing it from
  the evaluation summary.
- **Do not rank the agent against named peers** in a coaching pack. Distribution
  context ("the team median is X") is fine; a leaderboard turns coaching into
  performance management.
- **Do not aggregate a coaching pack into a performance rating.** If someone asks
  you to, say that the pack was not built to that standard and offer the stricter
  process instead.
- **One agent per pack.** Batching ten agents into one output produces ten
  unusable packs.

## Present results to the user

1. **What the data supports** — `n`, the interval, and one plain sentence on what
   can and cannot be concluded. First, not last.
2. **The pack itself**, in the template above.
3. **What you excluded and why**, with counts. Disputed, superseded, not-their-work,
   outside-their-control.
4. **Findings routed elsewhere** — the process, tooling and knowledge gaps you
   pulled out of the coaching set, with a suggested owner. Often the most valuable
   output of the exercise.
5. **What you could not assess** — languages you cannot judge, voice criteria that
   need audio, transcripts unavailable.
