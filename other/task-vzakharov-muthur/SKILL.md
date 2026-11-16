---
description: >-
  Take a task and decide for yourself whether it needs a plan, write the plan
  when it does, and then decide whether the operator has to look — plan and hand
  off, plan and then implement, or implement with no plan at all. Invoke as
  `/task <what to do>`. The prompt is a conditional go-ahead scoped to that one
  task.
---

The decision this skill makes, before any other: **does this task get a plan,
and does the plan block on the operator?** Those are two questions with a plan
file between them: the second judges the plan, so it is asked once the plan
exists.

**The prompt is a conditional go-ahead.** It authorizes implementation _on
condition that_ the agent judges the operator's gate unnecessary, scoped to the
task in that message and to that message alone.

`/task <what to do>` is the invocation, and it is also where an unrouted
session's first change lands: CLAUDE.md § "Plan mode & questions in web
sessions" routes here the first turn that asks for a change to this codebase,
whether that is the opening prompt or a follow-up to one that was answered, so
most tasks arrive without anyone typing the name. A task routed mid-session is
the work as the conversation now stands. A `#<N>` in that prompt means the
thread is exported and committed before anything else happens — `/take-issue`
does that and hands the number back. Both mentions stay bare rather than
`@`-references: this skill ships to adopters who track no issues at all, and
nothing here needs those files read.

**What that routing costs, plainly:** the agent makes the plan-or-not call on
every session that asks for a change, without the operator opting into it. The
gate survives that — Step 3 routes gate-worthy work back to `/plan` — but it
fires when Step 3's questions say so rather than on every task.

**Anything a caller passes beyond the task — an `<issue>`, an export path —
rides through unchanged to whichever outcome runs, and is never read here:**
this skill knows what a task is and nothing else, and what the extras mean
belongs to the skills at either end of them.

## Step 1 — Does this task get a plan?

Either reason is enough on its own.

**Writing it down would change what you build.** A plan is how an agent gets its
own head straight, and that value needs no operator:

- several parts whose order matters, or edits that only make sense landing
  together;
- a live reuse call — the mandatory `## DRY notes` is the forcing function, and
  it earns the file whenever "shared or duplicated?" has a real answer to argue;
- a shape you would otherwise discover halfway through, after building the first
  half against a different one.

The test: if you can hold the whole change in your head and name every file it
touches, the file buys nothing.

**Or any of Step 3's four signs is even arguably present.** You are not deciding
it yet — that is Step 3's call, made against the plan rather than against the
line that asked for the work. Here you only notice that the question is live.

**No to both → `@.claude/skills/go/SKILL.md` § "Planless entry"** with the task,
where the diff is the plan.

**This step is deliberately over-inclusive.** Being wrong costs a file
`/finalize` sweeps, so a close call writes one.

## Step 2 — Write it as a draft

`@.claude/skills/plan/SKILL.md` Part 1, unchanged:
`docs/plans/<slug>.draft.do-not-implement.md`, banner and all, published through
`/pr` so the operator has a surface to read and interrupt on.

**Every planning route produces a draft.** It is what a `/handle` reads if this
session dies between writing the file and flipping it — a plan awaiting a
go-ahead, which costs one round trip to re-give. The alternative, an
`*.in-progress.md` claiming a live session holds the plan right now, is a
reading someone has to untangle by hand.

It is also what makes a carve safe here. `@.claude/skills/plan/carving.md` files
nothing at plan time and leans on the draft being the gate, so a carve found
while writing this plan needs no procedure of its own: the file is already a
draft carrying its banner, and Step 3 is where it stops.

## Step 3 — Does the operator need to look?

Now the plan exists, so the question is asked against it rather than forecast
from the line that asked for the work. Any one of these is a yes:

- **The work costs far more to produce than to describe.** The plan is a page,
  the work is a day, and a wrong direction is caught for the price of the page.
- **A fork carries no recommendation** — the exception in
  `@.claude/skills/plan/SKILL.md` Part 2. Guess wrong and most of the work is
  wasted; the plan is what makes the choice the operator's.
- **The alternatives land far apart** — an operator who read the diff and asked
  for the next-best option would be asking for a rewrite, not an amendment.
- **The scope is itself the question** — you would be deciding _what_ the task
  is, not just how to do it. So is a split across sessions, an elephant or a
  pizza alike (`@.claude/skills/plan/SKILL.md` § "Splitting work across
  sessions"): the shape is the operator's to pick, so a plan that splits ends
  here.

None of these asks how important the change is. Importance is why the operator
reviews the diff; the gate is for what a diff review could only change by
rewriting the diff.

**Yes → end at `@.claude/skills/plan/SKILL.md` § "Handing off"**, and the next
session flips the draft.

**No → enter `@.claude/skills/go/SKILL.md` at its Step 1**, which flips the
draft in a commit quoting the `/task` prompt as the go-ahead, and carries on
into the work. The conditional go-ahead is what that flip records; nothing about
it is skipped because the same session wrote the plan.

## The three outcomes

Two of the three are the two ends of one route, forking at Step 3 where the plan
exists to fork on.

1. **Plan and hand off** — Step 1 yes, Step 3 yes.
2. **Go** — Step 1 no. The diff is the plan.
3. **Plan, then go** — Step 1 yes, Step 3 no.

**Report the call in the first sentence of the turn, with its reason and the
override**: "Doing this directly rather than planning it — _reason_. Say `plan`
and I'll write one instead." That costs the operator one word to reverse, and
puts the judgment on the record in the turn that acted on it.

**On that override, stop where you are.** Write the plan for the whole task and
name the commits that already exist, so the operator reviews it knowing what is
built. Leave those commits in place; reverting work nobody asked you to revert
costs more than the work does.

**When a call is close the two steps break opposite ways.** A close Step 3 goes
to the operator — being wrong toward the gate costs a round trip, being wrong
past it costs them reviewing work that should not exist. A close Step 1 writes
the file, per above.

**The pull is toward outcome 2**, which starts producing this turn and bills its
cost later, to whoever reads the result. Weigh it against that round trip rather
than against the appetite to start.
