---
name: write-story
description: Describe the strategy you have in mind and I'll write it up as a Trade Story.
argument-hint: "[a name for the setup, or the setup in your own words]"
---

# Write a Trade Story

The run opens at step 3, whose message is written out in full there — the
opening line, step 2's naming line where there is one, and the question, as one
message. Steps 1 and 2 send no message of their own on the way to it, unless
step 2 finds the name taken.

Follow `${CLAUDE_SKILL_DIR}/../../story-skills.md` for **Operating rules**,
**Paths**, **Output**, **Running** and **Explaining**. Its opening line naming
the story is step 2's, said as soon as a name is settled. **Finding the story**
does not apply: this skill makes one.

Node is needed only at the end, and only if the trader asks for the checks.

Work the steps in order, and say only the words a step gives you. Reading a
file, listing a folder and handing work to an agent are silent: each step says
what it prints; print nothing else. Never narrate the step you are on, your
reasoning, or what you are about to do or skip.

## 1. Take what the argument holds

Either a name for the setup, or the setup in the trader's own words — usually a
summary missing some of the detail. Sometimes both.

The argument might be:

- **Missing.** This is the normal path; say nothing about it.
- **A name.** Given one, use it. Given only a description, draw a short name out
  of it.
- **Setup details.** The trader's initial description of their trade setup - usually a
summary missing some of the detail.
- **Combination of a specific name and the setup details.**

Don't say that you've read the argument.

## 2. Check the name

Run this section as soon as there is a name to check — from the argument, or
drawn out of the setup once the trader has described it — and again whenever the
name changes (e.g. the trader opts to change it).

If there isn't yet a name or a way to determine the name, don't say this; just silently skip the rest of this section.

The name maps to one story file, so the check here is on the filename.

The name is the filename — lowercase, punctuation dropped, words joined by
hyphens, `.trade` on the end, nothing else — in `stories/your-stories/` unless
the trader specifies somewhere else.

List `stories/` and its subfolders, `.settings/` aside, and hold the listing
rather than making it again for the next name. The check is on the name, so a
story anywhere under `stories/` counts as taken.

Available: say nothing about the check, and name the story to the trader in one
chatty line — the name as they would say it, not the filename. It goes at the
top of the next message they get, under the opening line where that message is
step 3's, and is never sent on its own or as a turn of its own. Say it once for
the name that stands, and again only if the name changes. A reply that only
changes the name leaves the question under it still to answer — put it again,
with the new naming line on top.

A name the trader gave:

> Great — **<name>** it is.

A name you drew out of the setup yourself:

> I'll call this one **<name>**, unless you'd rather it was something else.

Taken: a single `AskUserQuestion` carrying the question alone, and nothing above
it. The run has not opened here. A name the trader gave:

> Looks like you already have a story with that name. How should we proceed?

A name you drew out of the setup yourself:

> I've picked this name but it looks like you already have a story with the same
> name. What should we do?

Either way, the same two answers:

- **Work on that story instead** — one line, and stop there. The run is over:

  > No problem, let's talk about what you'd like to change.

- **Choose a different name** — the option's description asks them to type the
  new name. Where the answer came without one, ask for it in a line. Check that
  name the same way, and the one after it, until a name is available.

## 3. Get the setup

One of the following, printed whole as a single message of ordinary output, and
it is the last thing said in this turn. Where step 2 has a naming line, it sits
between the opening line and the question.

The argument contained setup details:

> I'll write a Trade Story based on your setup.
>
> Sounds good. Anything else you want to add before I dig into the details?
> I'll ask for more details as we go along.

It did not:

> I'll write a Trade Story based on your setup.
>
> Tell me briefly what the setup is — what you watch, your entry signals, and
> your take profit and invalidation levels. Or say **ask me** and I'll walk you
> through it.

Every part goes out together — the opening line is never sent on its own, and
never as a turn of its own.

The turn ends on that message. Nothing at all follows it — no reading, no
listing, no agent, no line of your own. The trader's reply opens the next turn,
and step 4 is the first thing done in it.

## 4. Load what the interview needs

The trader's reply has arrived. Before acting on any part of it, read all of the
following in one tool call — not one at a time — and hold them from there:

- `${CLAUDE_SKILL_DIR}/../../../dsl/keywords.md` — the question behind each keyword
- `${CLAUDE_SKILL_DIR}/../../../dsl/syntax-rules.md` — which keywords are mandatory
- `${CLAUDE_SKILL_DIR}/../../../dsl/lint-rules-interview.md` — what to raise while the trader talks
- `${CLAUDE_SKILL_DIR}/../../shared/answers-log.md` — the format for logging the answers
- `stories/.settings/lint-overrides.md` — the rules to skip
- `stories/.settings/defaults.trade` — the clauses already answered

The two under `stories/.settings/` may not be there. Missing is the ordinary
case, not a failure: carry on with what the others hold.

That is the whole of it, and it happens once. Nothing is printed for it: step 5
is the next thing said.

## 5. Ask what is missing

Their reply to step 3 was one of:

- **Ask me** - they don't have a setup description, so prompt them with every keyword as specified next.
- **the description of their trade setup.**
- **additional details of their trade setup** - in addition to the description that they put in the argument.

Work the keywords in `keywords.md` order — what must hold, what triggers, what
it does, what closes it. A guide, never a form.

**Ask only what has not been answered**, including where the trader said it
under a different keyword than the one you have reached.

**Something counts as answered only where it answers that keyword's own
question.** A condition does not become the `Given` by being the first one the
trader stated. Where nothing answers a keyword's question, it is still to ask; a
setup that takes any regime is the trader's answer to give, never one to assume
for them.

**A question carries the keyword's own words, all of them.** `keywords.md` is
the wording. Adding to it is fine where the setup makes something specific worth
asking; dropping or narrowing any of it is not. Ask what, never whether.

`defaults.trade` answers a keyword too. One with a default there is filled:
do not ask about it. Say so before the first question, naming the file and what
it covers:

> Just a heads-up, there are defaults set up in
> `stories/.settings/defaults.trade`. These cover <the clauses they fill>, but
> say if you want different values in this story.

No defaults, no line. A trader who takes that offer up has answered the keyword:
log it as any other answer.

**Let the trader talk.** Ask in plain prose, openly, one keyword at a time, and
wait. Take a long answer whole where it runs past what was asked, and cross off
every keyword it covered.

Say with each question that they can ask for it to be explained, or for an
example. Asked for an example, give a quick illustrative one: write the clause
from what they have said where enough of the setup is known, and only where it
is not, open a subject folder under `stories/` and take one from a story there,
never from `stories/your-stories/`. Open that folder at this point and never
ahead of it.

Close the **first** question, and only the first, with the offer of more:

> If you want more guidance, say **Guide me**.

**Guide me** switches to multiple choice for the rest: an `AskUserQuestion`
carrying candidate answers, the conventional one named as such, and always one
more for an answer of their own. A candidate may come from a story of the
trader's where one sits close, said as theirs. Stay in multiple choice once it
has been asked for, and never repeat the offer.

**Never write a value the trader did not give.** Offering candidates is fine —
that is what **Guide me** is for — but filling a gap because they did not answer
is not.

An answer nothing could be coded from is not yet an answer: "when RVI is low"
needs a number. Ask once more for the part that is missing, offering candidates.
Take the second answer as it comes and leave it to `/verify-story` if it is
still short.

**"I don't know yet" is an answer.** Log it as undecided and carry on — the
trader is asking for the story now and the detail later. The story breaks at the
checks; say so at the hand-over rather than letting it surprise them.

Every keyword listed under Mandatory keywords in `syntax-rules.md` has to be
answered, unless the defaults fill it. The rest are asked where the setup calls
for them; `keywords.md` gives the question each one puts. A trader who says a
clause does not apply has answered it.

### Raising a concern

Check the argument and the setup description against the rules as soon as you
have them, then every answer as it lands. Skip anything listed in
`lint-overrides.md`.

Raise it as help, never as a refusal. Say what it would cost this setup, offer
the way round that the rule itself gives, and let them choose. These prompts may
be multiple choice whatever mode the questions are in: a concrete alternative
alongside what they said is easier to weigh than a paragraph about it. **Always
offer leaving it as it is** — `It's fine, carry on` or words to that effect — as
one of the options, and never as the last resort among them.

Their answer settles it and goes in the log. Taking the advice, write it their
new way. Declining, write it as they first said, and say a warning will come up
later that they can override then. Nothing goes into `lint-overrides.md` here
and nothing is recorded anywhere. Never raise the same concern twice.

**Never offer a candidate answer the rules would flag.** Where what their own
wording implies is something the rules rule out, that is the concern to raise —
not an option to offer.

### The log

Log every answer as it arrives, in the format `answers-log.md` gives. Start the
log once the name is settled, putting into it everything said up to that point,
and move it if the stem changes.

## 6. Hand it to the writer

The file is written by the `story-writer` agent, not here. Give it four things:
the Trade Stories directory (`${CLAUDE_SKILL_DIR}/../../..`), the path to the
answers log, the name settled for the story, and the path to write the story to,
as step 2 settled it.

Called again after the review, it is given those four again, the fixes, anything
more the trader has said, and the path it wrote.

It comes back with the path it wrote, or with what stopped it. A path from the
first call goes to step 7; a path from the call after it goes to **Finishing**,
which names it.

Stopped instead: say in one line what is missing, in the trader's own terms, and
stop there — no checks to offer. Stopped on the second call, say whether the
story file survived, as the writer reported it.

The interview stays here: the writer is handed only what has already been
answered.

## 7. The review

With the story written and before the trader sees it, hand it to the
`new-story-reviewer` agent, giving it the Trade Stories directory
(`${CLAUDE_SKILL_DIR}/../../..`), the story, and its answers log. It reports up
to three lists.

**Fix** — every one is applied. There is nothing to ask about.

**Ask** — put each to the trader in their own terms, never as something a check
turned up. One `AskUserQuestion` covering them together where there are few
enough, with candidate answers as in step 5. Log what they say.

**Expected** — say nothing at all. These are the trader's own decisions coming
back.

Where there was a **Fix**, or the trader answered an **Ask**, hand it back to
`story-writer` as step 6 says. Nothing to fix and nothing asked leaves the file
as it is.

One pass, however it goes. Anything still open after it belongs in the hand-over
line, not in another round of questions.

## Finishing

One line naming the file as ordinary output, then a single `AskUserQuestion`
carrying the question alone:

> I've written the story to `<path>`.

> Shall I go ahead and run some checks on it?

Where a clause was left undecided, or the review left something open, one more
line of ordinary output before the question, naming what is open and saying the
checks will flag it.

- **Sure, go ahead** — run `/verify-story <path>`. Say nothing about what running
  it brings with it.
- **Not right now** — one line, and stop:

  > Run `/verify-story` when you want it checked.
