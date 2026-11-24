---
name: sciwrite-process
description: >
  Plan and run the writing process for a scientific paper or thesis chapter —
  pre-writing and organisation, drafting fast without perfectionism, revision,
  and the final pre-submission checklist — following Stanford's Writing in the
  Sciences. Use this skill whenever someone is stuck, procrastinating, or asking
  how to approach a piece of writing rather than asking about the text itself:
  "I don't know where to start", "I've been staring at this for weeks", "I'm
  about to write chapter 3", "how do I stop rewriting the same paragraph", "how
  long should this take", "what should I check before I submit", "my draft is a
  mess and I don't know why". Also use it when someone asks how to organise
  sources and notes before writing, or wants a revision strategy for a finished
  draft. Do NOT use it for editing prose (sciwrite-prose) or for what belongs in
  each section, or the order in which to write the sections (sciwrite-manuscript).
---

# The writing process

Most of the pain people feel while writing comes from doing three different jobs
at once. Separate them and the work gets faster and the result gets better.

Answer in whatever language the user writes to you in.

---

## Three phases, and how the time should split

```
Pre-writing   70 %   gather, organise, work out the take-home messages
Drafting      10 %   compose prose, badly, quickly
Revision      20 %   where the elegance actually happens
```

Most people invert this, spending the bulk of their time on the drafting step.
That is why writing feels awful: composing prose is the hardest, most
attention-hungry part, and they are doing it for the longest, while also
researching and editing at the same time.

**When someone says they are stuck, ask which phase they are in.** They usually
turn out to be drafting without having pre-written — trying to compose sentences
while hunting for the statistic that goes in them. Two sentences in thirty
minutes, and no writing actually done.

---

## Pre-writing (70 %)

The purpose is to have every fact at your fingertips and the shape of the piece
decided *before* you open the blank document.

**Gather into one place.** Read your sources and pull out, as you go, every
statistic, detail, quote and idea you might use — into a single ongoing document.
It will get long (60 pages is normal for a feature). Keep the original sources
filed in case you need them again.

Put borrowed passages **in quotation marks as you paste them**, so that months
later you cannot mistake someone else's words for your own. This is the practical
defence against accidental plagiarism, and it costs nothing at the time.

**Then move the material around** until everything belonging to one section sits
together. This is where the organisation happens, and it is cheap here and
expensive later.

**Build a roadmap, not an outline.** An outline with A/B/C and 1/2/3 is more
trouble than it is worth. A roadmap lays out the sections in broad terms, and
roughly what goes in each paragraph, with the relevant material already sitting
under each heading. When you finally write, you are only putting known content
into prose.

**Think away from the computer.** A blank document is a confining place to have
ideas. Structure, take-home messages, the right word, the framing that makes the
whole thing click — these tend to arrive while exercising, driving, waiting in
line. Carry something to capture them with.

**Two organisation rules that save whole revisions:**

- **Group like ideas.** If the same topic appears in three paragraphs scattered
  through the paper, bring them together. Merging usually reveals repetition you
  could not see while they were apart.
- **Do not bait-and-switch on controversies.** Argument A, counter-A, rebuttal-A,
  then argument B, counter-B, rebuttal-B is exhausting to read. Put all the
  arguments, then all the counterarguments, then all the rebuttals.

For a manuscript specifically, pre-writing includes finalising the tables and
figures — see **sciwrite-manuscript**.

---

## Drafting (10 %)

**Do not be a perfectionist here.** This is the one instruction that matters.

The goal for a first draft is narrow and deliberately low: **get the ideas down,
in complete sentences, in the right order.** That is all. The sentences do not
have to sound good. They will not sound good.

Why the bar is set low: sentence-level problems are cheap to fix in revision.
Structural problems — muddled take-home messages, wrong organisation — are
expensive, because fixing them means rewriting everything downstream. So spend
the draft on the expensive things and let the cheap ones be bad for now.

The other reason: this is the hardest step. Minimise time spent in it.

Sainani's own first drafts, from the course, contain the exact defects she teaches
against — *there is* constructions, *to be* verbs, wordiness. They became good
prose in revision. That is the process working, not failing.

**When the task feels too big, shrink the goal.** *Today I will write 400 words.*
Choose a target so modest it cannot intimidate. What usually happens is you hit it
in a couple of hours and keep going with momentum; and on the bad days, 400 words
still counts as a successful day. Setting out to write the whole manuscript today
guarantees you write nothing.

---

## Revision (20 %)

Where the elegance comes from. Concrete techniques, in the order to apply them:

**Read it out loud.** The brain processes speech differently from text. Awkward
rhythm, repetition and wordiness that are invisible on the page are obvious in
the ear. Reading into a recorder and playing it back works even better.

**Do the verb check.** Take two or three paragraphs and underline the main verb of
every sentence. Look at the list alone. How many *to be* verbs? How many passive?
How many sit far from their subject? Changing four or five verbs often lifts a
whole passage, and this takes two minutes.

**Do the organisational review.** Tag every paragraph in the margin with a short
phrase naming its one idea. Then read only the tags. Repeated tags mean scattered
material — move those paragraphs together and probably merge them. The tag
sequence also shows you the logical flow at a glance, which prose does not.

**Cut ruthlessly.** Dead weight, blobs, long-for-short, jargon, acronyms,
repetition, adverbs. See **sciwrite-prose** for the full passes and the lexicons.

**Get outside eyes.** Ask someone *outside your niche* — intelligent, scientific,
not an expert in your area — to read it. Then ask them to tell you back three
things: the main findings, the take-home message, and why the work matters. They
should be able to do that without a technical background. Wherever they struggle,
ask them to point at the sentences and paragraphs; those are where to spend your
revision effort.

---

## The final-draft checklist

Before it goes to a journal or a supervisor. See
`references/final-checklist.md` for the full version; this is what it covers:

- **Internal consistency.** Nothing in one section contradicting another. The
  course's example: Methods says minimum two years of follow-up, Results says
  average follow-up 1.5 years. Both cannot be true, and a reviewer who sees it
  starts doubting everything.
- **Numerical consistency.** Abstract numbers matching body numbers; percentages
  matching raw counts; tables matching figures. Mismatches usually come from
  sloppy copy-paste or from re-running an analysis and updating only part of the
  manuscript — but what they *look* like from outside is several versions of the
  dataset in circulation.
- **References that go somewhere.** Check that each cited paper actually contains
  what you say it does. It very often does not.
- **Primary sources.** Do not inherit citations from other papers' reference
  lists. Statistics degrade as they propagate — the course traces a widely
  quoted prevalence figure back through fifty different attributions to three
  small 1980s surveys that could not support it.

Run the scripts:

```bash
# The scripts ship in sciwrite-prose/scripts/. Find that skill wherever it was
# installed: plugin, `npx skills add` (project or global), or a manual copy.
SCIWRITE=$(for d in "${CLAUDE_PLUGIN_ROOT:-.}/skills" .claude/skills .agents/skills \
                    ~/.claude/skills ~/.agents/skills; do
  [ -f "$d/sciwrite-prose/scripts/prose_audit.py" ] && { (cd "$d/sciwrite-prose/scripts" && pwd); break; }
done)

python "$SCIWRITE/numeric_consistency.py" paper.tex
python "$SCIWRITE/keyword_consistency.py" paper.tex
python "$SCIWRITE/prose_audit.py" paper.tex
```

If `$SCIWRITE` comes back empty, the sciwrite-prose skill is not installed: do
these checks by reading, and tell the user that
`npx skills add dvdsosa/scientific-writing-skills` adds the scripts.

---

## Helping someone who is stuck

Diagnose before prescribing. The useful questions:

- *What are you trying to say in this paragraph?* If they cannot answer, that is
  the problem, and no amount of rewriting will fix it. Confusing prose is almost
  always unresolved thinking.
- *Have you got your material organised, or are you looking things up as you
  write?* If the latter, stop drafting and pre-write.
- *Are you editing sentences as you write them?* If so, that is why it is taking
  forever. Give them permission to write badly.
- *Do the tables and figures exist yet?* For a manuscript, drafting before they
  are settled means drafting twice.

Two things worth saying out loud when someone is anxious about writing:

**Writing is hard for everyone**, including people who do it professionally every
day. Finding it difficult is not evidence of a deficiency.

**Inspiration is not a prerequisite.** Waiting to feel ready is procrastination
with better branding. Being *prepared* — which is what pre-writing produces — is
what actually makes writing possible.

---

## Reference files

| File | Read it when |
|---|---|
| `references/final-checklist.md` | a draft is close to submission |

Related: **sciwrite-manuscript** for what goes in each section and the order to
build them; **sciwrite-prose** for the revision passes in detail;
**sciwrite-publish** for what happens after submission.
