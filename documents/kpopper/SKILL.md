---
name: kpopper
description: "The kpopper method: a knowledge record (GROUNDING.yaml) for work that gets revisited - what is known, where each piece came from, and what would make each conclusion wrong. Use when asked what kpopper is or how to keep a record, when choosing which kpopper skill fits a moment, or when no narrower one does. The occasions have their own skills: ground (read the record before answering), record (write what the work found), map (map existing materials), annotated-doc (a standalone HTML document with evidence), hub (the record's visual home), consolidate (hypotheses and merges), watch (background checks)."
---

# kpopper

In ordinary conversation, name the product **kpopper** and describe the action in the user's language. Reserve the exact skill name `kpopper:kpopper` for invocation instructions, technical documentation, debugging, or explaining this specific skill. Fold the product name into the explanation of the action; no extra announcement is needed.

Start with the work the user wants to move forward. A project may span documents, conversations, calendars, task systems and earlier sessions;
code and repositories are one important setting among these. Keep the goals, commitments, constraints, decisions, sources and open questions that help later sessions continue.
The connection to the user's goal determines what belongs, rather than the mere availability of a tool or folder.

*Named for Popper: nothing here is ever verified, only exposed to refutation. Every judgment
must say what would make it wrong, and one that cannot be wrong is an opinion.*

This is **epistemic** bookkeeping. The record's subject is not the work but the state of
knowledge about the work: what is known, what each conclusion rests on, what the world looked
like when someone last checked, and where a hole was *declared* rather than filled. Do not
oversell that — it is not modal logic and there are no K operators here. Its nearest formal
relative is a truth-maintenance system, where `rests_on` is a justification and a changed input
invalidates everything downstream of it; what this adds is Popper's asymmetry, that a judgment
is never confirmed, only left standing.

That makes the record **self-evolving**, in one exact sense worth being precise about: nothing
here rewrites your conclusions. What the record does on its own is re-check every judgment
against what it was last checked against, and put the ones that no longer hold in front of you.
Nobody maintains a list of what went stale. Staleness is derived, so it cannot be forgotten,
cleared by accident, or survive a revert — and the page's sections fill themselves from the
same derivation, which is why an arrangement written last week still shows this week's problem.

Work that gets revisited needs one thing sessions usually throw away: **where each piece came from.** Keep that while you work. This is not a data-modeling exercise, and it should not change what you produce — only what you keep.

## Three things worth keeping

**Simple** shares one graph with named competing hypotheses; **Advanced** adds branch contexts and `pending_grounding` for shareable, feature-independent contributions, even with one checkout. Several sessions may work on one hypothesis.
Non-Git projects default to Simple; new Git projects to Advanced; existing registered shared records retain their behavior. Mode changes are explicit and preserve records.
Private or unclear permission means a structured private draft outside Git. Preserve the exact scope of measured facts. Merge incorporates content without proving truth or refreshing `seen`.
Ordinary reads show relevant pending knowledge; committed artifacts use explicit frozen reads. See [project modes](../../docs/project-modes.md).

Everything the record holds is one of three kinds, and each is written the moment it exists,
by the session doing the work:

1. **Something taken from a source** - a number, a date, a quoted clause, a position someone
   stated. Recorded with the source *and the location within it*, and with how faithful the
   text is: quoted, paraphrased, or your reading of it.
2. **Something worked out** - the rule, never the result. New calculations use [structured expressions](EXPRESSIONS.md), computed by the local Lean core.
3. **Something concluded or composed** - a recommendation, a comparison, a summary. It says what
   it rests on, carries `seen` (what those held when it was written) and `wrong_if` (what would
   make it wrong). A judgment that cannot be wrong is an opinion.

The [record skill](../record/SKILL.md) is where these are written; the
[shape reference](references/shape.md) shows the file they land in.

## Which skill, when

| the moment | skill (Claude Code · Codex) |
|---|---|
| before answering about the project's state, a number, a date, a decision or a source; before changing a value the record may hold; when the opener or a grounding line names entries | [ground](../ground/SKILL.md) · `/kpopper:ground` · `$ground` |
| something worth keeping exists: a fact from a source, a rule, a decision, a measurement, a correction, an open question - and before finishing a session that produced any | [record](../record/SKILL.md) · `/kpopper:record` · `$record` |
| the user asks to map or investigate what already exists, or a workspace with no record needs the one-time starting offer | [map](../map/SKILL.md) · `/kpopper:map` · `$map` |
| Annotated Documents is explicitly requested or refreshed | [annotated-doc](../annotated-doc/SKILL.md) · `/kpopper:annotated-doc` · `$annotated-doc` |
| explicitly use kpopper Hub, its layout or verification | [hub](../hub/SKILL.md) · `/kpopper:hub` · `$hub` |
| hypotheses wait or an id is CONTESTED; a write was refused into a hypothesis; a branch's record must be reconciled before a merge; a dry run or remeasure is red | [consolidate](../consolidate/SKILL.md) · `/kpopper:consolidate` · `$consolidate` |
| branch compatibility in the background, shared external facts, a daily review | [watch](../watch/SKILL.md) · `/kpopper:watch` · `$watch` |

Compatibility names: [page](../page/SKILL.md) forwards to hub; [document](../document/SKILL.md) forwards to annotated-doc.

The plugin's hooks open every session with the record's head and what needs a person, and name
the skill for the next move in that host's own syntax. What they never carry is a value: values
are pulled by subject when the work asks. The long-form of the method - when structure is added,
what a view is, how the shape changes, where the reader lives - is in
[references/method.md](references/method.md); the record's shape in
[references/shape.md](references/shape.md); what makes a falsifier honest in
[references/falsifiers.md](references/falsifiers.md).

## The part that does not change

Everything above is open to revision — the sections, the field names, the operators, the views.
Four things are not, because they are what the rest is built on:

1. **Every entry declares what it rests on.** Something with no declaration does not go in.
2. **Do not store an output when you can store what produces it.**
3. **Invalidation spreads automatically; re-running a judgment never applies itself.**
4. **A change to the shape is valid only with a migration that leaves the build green.**

A record that can rewrite its own rules will drift — slowly, unnoticed — unless something in it
is not up for revision. These four are that floor.

## Never do these

Each is recognizable while you are doing it. If you catch yourself, stop.

- Designing a structure before meeting the evidence, including during a selected mapping.
- Starting a second record, or renaming `GROUNDING.yaml` to something you like better.
- Creating a category with one member. One is a case, two a coincidence, three a category.
- Recording things nobody asked about, for completeness. Completeness is not the goal.
- Renaming or reorganizing because it would be tidier, with no question behind it.
- Building something general when only two specific cases exist.
- Recording anything a person would have to maintain by hand afterwards. That is the definition of bureaucracy, and it is how this fails.
- **Asking the user how to structure their data.** That is your job, not theirs, and asking makes the method cost them something on the very first turn.
- Spending a whole turn on the record when nobody asked for it. It is a byproduct of the work; if it becomes the work, something has gone wrong.
- Repairing the project inside the turn that records it, without saying so first. Record, say what you found, then fix — as work the person can see.
- Presenting your reading of a source as the source's own words.
- Inventing a number, a date or a threshold so that something becomes computable.
- **Filing something as a judgment because that is the only slot available.** A live question goes
  in `open:`, an un-evaluable predicate says `blocked_on`. Shaping the record to pass a checker
  produces records that look right and are not.
- **Declaring which of the capabilities above a project has.** Which ones exist is visible in the
  files — does a views file exist, does the build fail on a broken reference, do judgments carry
  verdicts. So derive it, and if it is worth surfacing, have the build write it down beside the
  evidence and the trigger that bought it. A hand-declared stage can contradict reality with
  nobody noticing, and a number at the top of a file turns into something to increment.

## Check yourself

- **Keep first use proportionate.** Offer a short optional choice at a suitable moment;
  preserve progress on the task and never repeat an explanation just because a session restarted.
  A chosen mapping is work in its own right, with scope and a useful result.
- Pick three specific claims from what you produced — a figure, a date, a statement about what some document says. Each should trace to a recorded origin, a rule, or a stated judgment. If one cannot, it was invented.
- Take one thing you presented as quoted and find it in its source. If you cannot, it was a paraphrase wearing quotation marks.
- Search your output for material that also sits in the record. If it appears as literal text in both places, it will drift — reference it instead.
- Every judgment says what would make it wrong, and carries `seen` so that "wrong" can actually be noticed.
- Anything you could not ground is **written down as unverified**, never given an invented source.
- Nothing you recorded requires a human to keep it up to date.

## What would show this was not worth it

The method promises exactly one measurable thing: **the opening cost of session number N.**
Today that cost is flat — every session re-reads, re-verifies, and sometimes re-invents. If it
is working, a later session reads only what is marked as moved.

An optional introduction should earn its small cost through useful work; a selected mapping
should return the picture the user asked for. If it takes more than the ladder in [references/method.md](references/method.md) to explain when to add
structure, the ladder failed. And if after five sessions the sixth does not open cheaper, the
method did not return what it cost, and you can drop it with a clear conscience.

There is no target state here. Refinement is driven by use, not by steps: what gets asked about
gets sharper, what nobody asks stays rough forever, and that is correct. An agent that believes
there is a finished version to converge on will keep polishing when nobody asked.
