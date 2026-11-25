---
name: po-pm-writing
description: >
  Writes or rewrites text for Product Owners and Project Managers: bottom line
  first, decision or ask stated outright, technical detail turned into user
  impact, scope, dates and risk. Stacks BLUF, plain language, bureaucratese
  inversion, Zinsser and a consultative register, per the LLM Writing Styles
  Catalog. Use when user says "write this for the PO", "explain to product",
  "message to the PM", "make this PO-friendly", "status update for product",
  "escalate this blocker to the PO", "non-technical version", or invokes
  /po-pm-writing.
---

# Writing for Product Owners and Project Managers

POs and PMs decide scope, priority and dates. They do not read code. They have
little time, so they skim. Every message must answer: **what happened, what it
means for users or the plan, and what you need from them.**

Source: `09.Research/md/llm-writing-styles-catalog.md` in the Obsidian vault. Its
Chooser (ch. 47) gives the stack for busy readers: substance → structure (BLUF,
ch. 23) → sentences (Zinsser, ch. 15) → register (consultative, ch. 27) →
verification. Plain language (ch. 37) and bureaucratese inversion (ch. 31) give
the word-level rules.

## The Five Passes

Run them in order. Restyling before the facts are right makes wrong text
prettier.

### Pass 1 — Substance (no style yet)

List the bare facts before you write any prose:

- **What changed or what we found.** One fact per line.
- **Impact.** Which users, tenants, features or flows. Use numbers.
- **Plan impact.** Scope, dates, sprint, effort. Say if it moves or stays.
- **Ask.** A decision, a priority call, information, or "none, FYI".
- **Deadline for the ask.** A date, and the reason for it.
- **Unknowns.** Say what we do not know yet and when we will know.

If the ask or the impact is missing, ask the user for it. Do not invent dates,
numbers or owners.

### Pass 2 — Structure (BLUF)

- **First sentence = the bottom line.** The reader can stop after it and act.
  It has the decision, the ask or the outcome. It does not just name the topic.
  - Bad: "Update on the scheduler sync issue."
  - Good: "Scheduler sync will slip one sprint unless we drop recurring appointments from v1. Need your call by Thursday."
- **Then the reasons, in order of importance.** Detail below is optional reading.
- **Put the ask in its own line**, labelled `Decision needed:` or `Ask:`, with
  the options and your recommendation.
- **Bad news:** you may put one line of context or acknowledgment before the
  bottom line. Only one, or you bury the news.
- **Long docs:** open with a `TL;DR:` that holds the answer, the number or the
  decision, not the topic. It is one line for a message and one short paragraph
  for a report.

### Pass 3 — Translate the technical (plain language, curse of knowledge)

The reader does not share your context. For each technical term:

1. **Drop it** if the reader can act without it.
2. **Replace it** with the effect: "the Lambda times out" → "the save fails for large clinics".
3. **Keep it once, explained**, if the PO must repeat it to others:
   "PlatformSync (the bridge that copies data from Classic to NewGen)".

Lead with the user or business effect, then the cause. Put file paths, stack
traces, table names, PR numbers and query details in a `Technical detail`
section at the end, or link to them. Jira keys (e.g. `ROAD-1930`, `SIQ-307`)
can stay, because POs use them.

### Pass 4 — Sentences (bureaucratese inversion + Zinsser)

- **Name the actor.** "It was decided" → "Rebecca and I decided". "Mistakes were made" → who made them.
- **Commit or decline.** "We will look into it" → "We will answer by Friday" or "We cannot take this on this sprint".
- **Count things.** "Several tenants" → "4 of 31 tenants". "Soon" → a date.
- **Pick one level of certainty.** Use "confirmed", "likely" or "unknown". Do not stack hedges ("could potentially perhaps").
- **Revive verbs.** "Perform an investigation" → "investigate".
- **Cut clutter.** Remove throat-clearing, hollow qualifiers and clichés ("circle back", "low-hanging fruit", "robust", "seamless").
- Keep sentences under 25 words and paragraphs to 3–5 sentences.

For the full substitution table, use the `zinsser` skill.

### Pass 5 — Register and verification

- **Consultative register.** Write as a professional who talks to a peer. Use
  "we" and "you", contractions where they read naturally, and no blame. Be warm,
  but keep dates and numbers exact.
- **Shift tone at most one level from the input.** A casual Slack thread does not
  become a formal memo.
- **Check before output:**
  - [ ] First sentence passes the BLUF test: could the PO act on it alone?
  - [ ] Ask, options, recommendation and deadline are explicit, or the text says "FYI, no action needed".
  - [ ] Every impact has a number or a named scope.
  - [ ] Every unknown has a "we will know by" date or owner.
  - [ ] There is no jargon above the `Technical detail` line that a PO would have to look up.
  - [ ] Every passive has an actor and every promise has a date.
  - [ ] Facts, dates, ticket keys and names are unchanged from the source.

## Templates

Pick the template that fits the message. Drop any section that has nothing in it.

**Status update**

```
<Project> is <on track | at risk | late by N>: <one-line reason>.
- Done: <user-visible outcome>
- Next: <what, by when>
- Risk: <what could slip, likelihood, mitigation>
Ask: <none | specific ask by date>
```

**Decision request**

```
Decision needed by <date>: <question in one line>.
Recommendation: <option> — <one-line why>.
Options:
| Option | User impact | Effort | Date impact | Risk |
Why the deadline: <what blocks if we wait>.
```

**Blocker or risk escalation**

```
<Feature/ticket> is blocked: <effect on users or plan>.
Cause: <plain-language cause>. Owner to unblock: <person/team>.
What we need from you: <specific ask>.
If not resolved by <date>: <consequence for scope/date>.
```

**Delay (bad news)**

```
<One acknowledgment clause, optional.> <Project> moves from <old date> to <new date>.
Cause: <plain cause>. What we are doing: <action, owner>.
What stays on track: <items>. Next update: <date>.
```

## Exceptions

- **Do not simplify quoted text**, commands, SQL, config values, legal or
  compliance wording, or numbers. Copy them verbatim.
- **Do not drop a risk to make the message shorter.** Short and incomplete is
  worse than long.
- If the PO asked a technical question, answer it technically, but put the
  bottom line first.
- If the user wants ASD-STE100 (e.g. ROAD analyses), use the `asd-ste100` skill
  for the sentence rules and keep this skill's structure.

## Examples

### Delay email

**Before:**
> "Hi team, I hope everyone had a good week. I wanted to give you an update on
> Project Falcon. Unfortunately, we've run into some challenges with the payment
> provider integration — their sandbox environment has been unstable, which has
> slowed our testing. As a result, we're looking at roughly a two-week delay on
> the launch. I know this is disappointing. We're working with the provider to
> resolve the issues, and I'll keep everyone posted."

**After:**
> "Falcon launch moves two weeks, from May 2 to May 16. The payment provider's
> test system fails daily, and testing is stuck at 60%. We call the provider
> every day. All other workstreams are on track. Next update: Friday.
> Ask: none. If the new date is a problem for the customer launch, tell me by Wednesday."

Rules that fired: BLUF, count things, commit to a date, explicit ask, clutter cut.

### Technical finding → PO message

**Before:**
> "The inbound resolver for AppointmentUpdated throws a FK violation on
> rt_scheduler.appointment.provider_id because the provider row isn't hydrated
> yet when the event arrives; the message goes to ERROR status and isn't retried."

**After:**
> "Since Monday, 212 appointment changes made in Classic did not reach
> SchedulerIQ for 3 tenants. Front-desk staff see old times for these
> appointments. Cause: the change arrives before the provider record does, and we
> do not retry it. Fix: retry these messages automatically. We estimate 2 days,
> and it fits this sprint.
> Decision needed by Thursday: ship the fix in this sprint, which delays
> SIQ-412 by 2 days (recommended), or put it in the next sprint.
>
> Technical detail: FK violation on `rt_scheduler.appointment.provider_id` in the
> AppointmentUpdated inbound resolver. The rows go to ERROR status and are not retried."

Rules that fired: impact before cause, jargon moved below the line, numbers,
explicit decision with recommendation and deadline.
