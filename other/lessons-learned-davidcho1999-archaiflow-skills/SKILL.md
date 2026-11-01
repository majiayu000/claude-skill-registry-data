---
name: lessons-learned
description: "Keeps a lessons-learned log in docs/practice/lessons.md: what happened, what it cost or saved, why it happened as stated, and what to do differently, each entry tagged by phase and topic so it can be found when the situation recurs. Trigger on \"lessons learned\", \"post-mortem\", \"what went wrong\", \"remember this for next time\", \"add a lesson\", \"lessons-learned\", the close of a project, or the start of one, when the right move is reading the log rather than writing it. Lessons are recorded as you state them: the skill never invents a lesson, softens one, or assigns blame beyond what you said. At project start or before a phase it reads back the entries whose tags match, which is the entire return on writing them. A lesson is one incident; recurring patterns become visible because the log accumulates, not because the skill generalizes."
license: MIT
metadata:
  title: "Lessons Learned"
  summary: "Record what a project taught you, and read it back next time"
  discipline: "practice-contracts"
  tags: "Project Management"
---

# Lessons Learned

Every firm pays tuition: the detail that got redrawn three times, the
consultant scope nobody carried, the clause that would have covered the
claim. The tuition is only wasted if nothing is written down. This keeps
the log, and, more importantly, reads it back at the moment the same
situation comes around again.

## Scope and limits — read first

**What this does.** Maintains `docs/practice/lessons.md`: one entry per
incident, with what happened, what it cost or saved as you state it, the
cause in your words, what to do differently, and tags for phase and topic.
On request, or at the start of a project or phase, it searches the log by
tag and situation and reads back what applies.

**What this does not do.**

- **It does not write lessons for you.** It can prompt with questions at a
  project close, but every entry's content is yours. An invented lesson is
  advice wearing the authority of experience.
- **It does not assign blame.** Causes are recorded as you state them,
  about process and documents, and it will ask you to restate a cause
  aimed at a person into one aimed at a step.
- It does not generalize. One entry is one incident. If five entries share
  a tag, the pattern is visible in the reading, and the conclusion is
  yours to draw.
- It does not rank or score lessons, and it does not archive old ones;
  a lesson from ten years ago about a phase you still run is still live.
- It is office memory, not project management. Open items on the current
  project belong in `project-tracker`; a lesson is written when the dust
  has settled.

**What you need before starting.** Nothing but an incident worth the ink,
or a project starting, which is when the log pays.

## Workflow

### Step 1. Bootstrap if needed

Check whether `docs/practice/lessons.md` exists. If not, copy
`assets/lessons-template.md` there. If the project has no `docs/` folder
at all, confirm before creating one. Offices that keep one log across
projects point this at that file instead; ask which.

### Step 2. Capture an entry

One incident, six fields, your words:

- **What happened**, concretely: documents, dates, the sequence.
- **Effect**: what it cost or saved: money, time, a relationship, as you
  state it.
- **Cause**, stated about the process, not the person.
- **Next time**: the change that would have caught it, specific enough to
  act on.
- **Tags**: phase (programming, CDs, bidding, CA, closeout, ...) and topic
  (consultants, contracts, envelope, drawings, client, fees, ...), from
  the words you use; reuse the log's existing tags before coining new ones.
- **Project and date.**

At a project close, offer the prompt set: what would you do again, what
would you never do again, what surprised you, what did the client teach
you. Record only what comes back.

### Step 3. Read back

The half that earns the writing. On "starting a project", "starting CA",
or any stated situation: match tags and words, and return the entries that
apply, whole, with their project and date. Oldest lessons included; age is
not decay here. If nothing matches, say so rather than stretching a
loosely related entry into relevance.

### Step 4. Notice patterns, carefully

When a reading returns three or more entries sharing a tag, say so, count
them, and stop. "Four entries tagged consultants + scope" is information;
what it means is the reader's call.

## Rules

- **Entries verbatim.** Tighten grammar if asked; never tighten the
  meaning.
- **Causes are about process.** Ask to restate, do not restate silently.
- **Read back whole entries**, with project and date, not summaries; the
  detail is where the lesson lives.
- **Reuse tags.** A log where the same topic wears five tags cannot be
  read back.
- **Never delete or archive.** The log only grows, and that is the point.

## Anti-patterns

- Writing the lesson yourself because the close-out meeting ran long.
- Sanding a costly mistake into a neutral observation nobody will heed.
- Summarizing five entries into a policy the user never stated.
- Skipping the read-back at kick-off, which converts the whole log into a
  diary.
- Coining a new tag per entry until every lesson is filed alone.

## Resources

- `assets/lessons-template.md` — the log this creates, empty.

No reference files. The lessons come from your projects, not from here.
