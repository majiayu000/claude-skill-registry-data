---
name: lean-out
description: Find the structural clutter in an app that is making every new change land wrong, and rank it by what it would have prevented rather than by taste. Produces a measured audit and a list that can be worked through in pieces, never a big bang refactor. Use when the codebase feels heavy, when the same kind of bug keeps coming back in a new place, when a file has grown past anyone's head, or when the app's size keeps climbing and nobody has looked at why.
---

# Lean out

**The rule: clutter is only worth fixing where you can show what it cost.** A
file being long is not evidence. A bug that happened, in that file, because of
how it is arranged, is evidence. Rank by that and the list sorts itself.

This produces an audit and a list. It does not refactor. Doing both at once is
how a tidy up becomes a week and a regression.

## When NOT to run this

- **Between cutting a build and shipping it.** The whole point of a release
  checklist is that the thing you tested is the thing you upload. Do not move
  code underneath it.
- **When the real question is bytes.** "Our download size keeps growing" is
  answered by diffing two builds, not by reading code. Do that first, it takes
  minutes, and come back if the answer is "our own code".
- **When nothing has gone wrong yet.** Without a bug list you will rank by
  taste, and a refactor ranked by taste is a rewrite with extra steps.

## 1. Gather the evidence before looking at any code

You need two things. Collect both before forming an opinion.

**The bug list.** Every defect from the last few months that reached a person,
from the project's own records: the rules file's gotchas, the release
checklist's history, recent commit messages that say "fix". For each, note the
file it lived in and, more importantly, **what shape of mistake it was**.

**The mass.** Cheap and factual:

```
# biggest files, tests excluded
find <source dirs> -name "*.<ext>" -not -path "*test*" | xargs wc -l | sort -rn | head -20
```

Now cross them. The files that appear in both lists are the audit. A long file
nobody has had a bug in is not urgent, whatever it looks like.

## 2. The shapes worth looking for

These are the ones that keep producing bugs, in roughly the order they do damage.
Each is a grep, not a judgement.

| Shape | What it looks like | Why it bites |
| --- | --- | --- |
| One fact, many readings | The same question answered several ways in one file, some of them combining sources and some not | Two of them eventually disagree, and the screen contradicts itself |
| A boolean meaning two things | `false` means both "no" and "not asked yet" | The unread state is rendered as a fact, and the UI corrects itself a beat later |
| A flag used as a proxy | A one time key named for a state, read as though it meant "on screen now" | It is true long after the thing is gone, and silently suppresses something else |
| A rule copied per surface | Each card or screen carrying its own version of a shared policy | The next one is written without it, and the bug returns somewhere new |
| Documentation contradicted by callers | A function documented one way and overridden at every call site | The next person reads the doc and concludes the opposite of the truth |
| A guard that is defined but not applied | A validator that exists and is only enforced on the shape of your own code | It never runs on the data that actually arrives |

For each hit, write down the bug it caused or could cause. If you cannot name
one, leave it out. That exclusion is the skill.

## 3. Rank by what it would have prevented

Order the list by the cost already paid, not by size or ugliness:

1. **It caused a bug that reached a person.** Top, always.
2. **It caused a bug caught internally**, or the same shape appears three or
   more times.
3. **It will cause one**: a new surface will plausibly miss the rule.
4. Everything else. This is where "long file" lives on its own.

## 4. Deliver a document and a list, not a branch

Write it where the project keeps its research or decisions, and link it from the
backlog. For each item say: the shape, the evidence, the smallest change that
removes it, and what would have to stay true afterwards (the test that pins it).

Then stop. The list is the deliverable.

## 5. The loop, and why green on its own proves nothing

The obvious method is: run everything, change things, run everything again, and
call matching results a pass. That is the right floor and it is not the test.

**A suite that was green while the bug existed will be green after you refactor
the bug.** Every defect worth fixing was, by definition, invisible to the tests
you already had. So "the same results" tells you the tests ran, not that they
were watching the thing you touched.

Three holes to expect, whatever the language:

- **Layout is usually invisible to the test runner.** Component tests prove what
  renders, almost never where. A change that wrecks spacing or pushes a control
  off screen passes.
- **Mocks that list their exports go green for the wrong reason.** Add a field
  to a store and every hand written mock returns undefined for it, quietly.
- **End to end runs are the noisiest thing you own.** Comparing a flaky red
  before against a flaky red after is not a comparison.

So add one step, and it is the one that gets skipped under time pressure:

**For every rule you extract, revert it and watch the test go red.** A test that
passes with and without your change has proven nothing about it. Put the change
back and move on. It costs a minute and it is the whole difference between a
suite that is green and a suite that is looking.

The loop that is worth trusting:

| | |
| --- | --- |
| Before | Full suite green, and note which tests actually cover what you are about to touch |
| During | One shape at a time, each with a test verified red by reverting |
| After | Full suite green, plus a screenshot of any screen whose layout moved |

## 6. When the work happens, one item at a time

- **One shape per change.** Not "tidy the screen".
- **A test first that fails for the right reason**, exactly as for a bug fix.
  A refactor with no failing test to start from cannot be shown to have
  preserved anything.
- **Prefer extracting a rule over moving code.** The win is one definition in
  one named place, not a smaller file. A 3,000 line file with one copy of each
  rule is safer than three 1,000 line files with three copies.
- **Leave the behaviour alone.** If you find a behaviour bug mid way, that is a
  separate change with its own test.

## What good looks like

A rule that existed in five places now exists in one, has a name, has a test
that walks every input, and the next surface gets it without being told. That
is worth more than any number of lines removed.
