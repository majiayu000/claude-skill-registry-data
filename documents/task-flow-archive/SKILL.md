---
name: task-flow-archive
kind: pattern
rule: task-flow
description: Pattern of rule task-flow. Load when the texts are up to date and the task folder is taken apart by the last commit before the PR opens. The move to the archive, the work queue audit, the rules review of the closed work and what to do with the findings.
---
<!-- rt-kit v0.34.0 · patterns/task-flow-archive.md · 071fa754d189 · правится надстройкой, не здесь -->

# Taking the task folder apart and the rules review of the work

Pattern of the rule `task-flow`. What must be true meanwhile — the law
`docs/constitution/work-conduct.md`. What comes before it — lifting the draft, merging the agreement
and bringing the texts up to date — pattern `task-flow-close`.

## When to use

- The agreement is merged, the domain texts are up to date, and the task folder is taken apart by
  the last commit of the branch — before the PR opens, not after approval.
- The work is merged by a person, and it is reviewed by the rules.
- The review returned findings, and they need a place.

## State `разбор-кончился`: the task folder is taken apart

The taking-apart here is one's own step, not someone else's. The state name speaks of the task
folder taken apart in the next step — not of the PR a reviewer reads, nor of the owner's request
whose grill began the work. In the state's language one word covers all three, and on a skim the
name looks like someone else's step. The executor told the owner they were waiting for review and
took the next task, while finished work stood one turn too many and came back to work by the owner's
hand.

There is nothing to wait for in this state. Its entry is two signs, both read in the tree: the suite
is green and the texts are up to date. The owner's approval is no entry, and work waiting for it
with both signs met stands idle.

The taking-apart goes by three outcomes, not two.

**First, the standing requirement is picked out.** Everything that stays true tomorrow becomes an
article of a law, a point of a rule or a section of a pattern — by what it speaks of. The sign is
one and written here in advance: would the text stop being true if everything were redone tomorrow.
It would — that is a story about what happened; it would not — that is a requirement, and its place
is the rules layer. The law is not edited in the branch: its article goes to the owner as text.

**Second, the story of the move that happened is picked out.** It goes to the archive and names, for
every decision moved out, where it went. Otherwise a decision that became a rule and a decision lost
in the move look the same — a record nobody refers to.

**Third, the rest is deleted.**

The order is exactly this: starting with the move, the executor carries the standing part away with
it — at the end of the work that is cheaper than sorting.

Nothing moves to the archive whole: `docs/archive/` is a place for records of what happened that
somebody reads, not a dump of progress files. The table below speaks of what is left after the first
pick.

| File | Where |
| --- | --- |
| `grill.md` | to `docs/archive/` in the owner's language — the owner's answers cannot be recovered, and this is the only record of why the task was set this way. A grill in the layer's language is rewritten at the move; the quoted request stays verbatim |
| `progress.md` | to `docs/archive/` if it holds decisions along the way with reasons; otherwise deleted |
| `plan.md` | deleted — after the rollout its question is answered by the code, and "how it works" by the domain spec |
| review findings | written straight next to the epic plan — they do not move from here; work outside an epic shows them to the owner in the same turn |

Findings do not live in the task folder at all. The review runs in the background, and nobody knows
when it ends: by that minute the folder is taken apart, and the branch may already be merged and
removed. Neither date is set by the executor, so a move "from the folder to the epic plan" would
rest on a coincidence that may never come. A finding noticed not by the review but along the way
uses the same place.

Findings that came back after the branch left travel by the branch of the next task: a push into a
removed branch does not update it but creates it anew, and the commit stays outside main. By that
minute the next task is already taken — its branch carries the cleanup after the previous one, in
the same order in which someone else's task folder is taken apart. The epic is over and there is no
next task — the findings leave as a task of their own.

What leaves is filed as one file with a telling name, not a folder of three:

```bash
cat docs/tasks/<КЛЮЧ>-<номер>-<slug>/grill.md > docs/archive/<ЧТО_РЕШАЛИ>.md
rm -r docs/tasks/<КЛЮЧ>-<номер>-<slug>
```

The taking-apart goes by the last commit of the branch, before the PR opens: opening with the folder
in place is refused by the delivery guard. Before, the cleanup stood after approval — the plan was
thought to be needed on disk for the whole review. But the merge button is pressed by a person on
the host, where the guard does not reach, and they merge as soon as they see green. After the
cleanup there is no plan on disk on purpose, and an edit after remarks is let through by the
progress guard on the sign from the branch history.

### Work that takes apart someone else's folder takes apart two

Such work has a folder of its own — it is created like everyone else's, no exception. Both are
removed by the last commit, and the order between them is one: first someone else's, then one's own.
Starting with one's own, the executor loses the plan on disk while it is still needed — the guard
refuses an edit without it, and an edit after review remarks goes into the same branch.

```bash
cat docs/tasks/<чужая>/grill.md > docs/archive/<ЧТО_РЕШАЛИ_ТАМ>.md
rm -r docs/tasks/<чужая>
cat docs/tasks/<своя>/grill.md > docs/archive/<ЧТО_РЕШАЛИ_ЗДЕСЬ>.md
rm -r docs/tasks/<своя>
```

Two records in the archive, not one: the works differ, and so do the decisions in them. After this
the work queue audit names no folder at all — that is how it is checked that both are taken apart.

**Next move:** the taken-apart folder goes into the branch by the same commit, the work queue audit
follows, and the same turn opens the PR — pattern `task-flow-close`.

## State `папка-разобрана`: the work queue audit

```bash
npm run check:board   # a closed task's folder among the current ones, abandoned drafts
npm run check:specs   # the agreement is merged, the bindings are in place
npm run check:docs    # the paths named in the texts exist
```

**Next move:** discrepancies named by the audits are fixed in the same turn; nothing to fix — the
same turn opens the PR as a draft and names the number to the owner, pattern `task-flow-close`.

## State `влито`: the work is reviewed by the rules — in the background, right after the PR

A step about the rules layer, not about the product: what was loaded for this work, what helped,
what was missing and where the text of a rule diverged from the tree. Only the session that led the
work knows this — a day later nobody does.

The review is led by the closed-task review role, if the tree laid it out; a tree that did not leads
it itself, by the same questions. The role edits no files — it brings ready-made wording, and the
owner decides whether to put it in.

**The review is launched in the background, right after the PR opens, and the turn does not end on
it.** The role asks nothing while it works and goes no faster for being waited on. The next task is
taken in the same turn that launched the review.

The order is one and cannot be rearranged:

1. **The digest is gathered before the launch** — while the task is still in mind. What was done,
   what went wrong, what was loaded and what each rule gave, which pitfalls of the environment were
   hit. Gathered two tasks later, it retells the branch history instead of what happened.
2. **The role goes to the background** — by the role launch tool, with the path to the list of what
   was loaded and the digest whole. The turn goes on with the next task.
3. **The returned findings are accepted in one turn** — write them down and go back to what was
   before. A review put off "until a convenient moment" never happens at all: the session ends
   first.

### Cargo records are moved to "done" in the same turn

Work begun from cargo that arrived ends here, not at the folder's taking-apart: before the merge the
edit is not in the tree, and the mark would claim what does not yet lie in main. This is the only
state where the merge has already happened while the turn about the task still goes on.

The keys are taken from the archive — the task folder is no longer on disk by this minute — and
passed whole, as the intake read prints them:

```bash
npm run cargo:mark -- --state fixed \
    --proposal <полный ключ> --proposal <полный ключ> \
    --fix '<чем исправлено: статья правила, гард, проверка, правка кода>'
```

One fix per call, so the records go in batches by what closed them, not by the whole task at once.
The reply is read: "moved 0" means this review moved nothing.

**Next move:** while the role reviews, the same turn is busy with the next task. The cargo records
are moved to "done" in this same turn, and the returned findings are accepted in one turn — write
them down and go on with what was before. The owner hears of them when the epic is over.

## Review findings land next to the epic plan and wait for the owner

The role's reply lives in the conversation and dies with it, so it lands on disk at once. The
executor writes it: the role writes no files.

**Findings are written straight into a file next to the epic plan, not into the task folder.** The
review runs in the background, and nobody knows when it ends. By then the task folder may already be
taken apart, and the branch merged and removed. Neither date is set by the executor, so a move "from
the folder to the epic plan" rests on a coincidence that may never come. A finding noticed not by
the review but along the way uses the same place. Work outside an epic shows the findings to the
owner in the same turn.

**The findings file is named after the plan, not invented by the session.** The file is `<plan
name>-findings.md` next to the plan itself: the plan `<theme>.md` gathers findings in
`<theme>-findings.md`. A name chosen on the spot is read only by the session that gave it. The next
one looks for this epic's findings by walking the plans directory and, not finding them, starts a
second file on the same thing — and the owner reads one of two. A single fixed place is not enough
here: each epic has its own file, found by name by whoever came to the plan, not to the directory.
The form of the file — the findings template among the package templates.

**Findings that came back after the branch left travel by the branch of the next task.** A push into
a removed branch does not update it but creates it anew: the commit stays outside main and
disappears with it. By then the next task is already taken — its branch carries the cleanup after
the previous one. The epic is over and there is no next task — the findings leave as a task of their
own.

**The cumulative findings file is split before the append, not after.** The length is looked at with
one command before the first written line. A task's section takes tens of lines, and it crosses the
document length limit in silence. The push gate shows the excess when the append is already
committed — then the split goes after the fact, together with editing every reference to the file.
It does not fit — the next part is started, and the section is written straight into it.

**A part is named after the task that started it, not by its ordinal.** The name is `<plan
name>-findings-<КЛЮЧ>-<номер>.md`. One epic is led by several working trees at once, and each of
them sees "the next part" as its own. Two branches start a file under one name, and the clash shows
only when main is merged in: a conflict over the whole file, where both sides are right and adding
them up resolves nothing. A task number belongs to that task alone and cannot fall to two trees. The
first part carries no number and is not renamed after the fact: a rename edits the references in
every text that points at it, for the sake of an even row of names. No order between parts is needed
— findings do not continue one another, and the owner reads them all at once.

**The line of a finding closed by other work is marked with that work's number.** From the list's
side a finding fixed in parts cannot be told from one not done. Both of its misses were closed by
tasks of their own and recorded by subject, each under its own subdomain — and the review went into
finding out there was nothing to fix. The number stands in the line itself, and the next reader does
not walk this path.

**An item of a combined finding is checked for being alive before it is taken into work.** Small
things written off into one item do not age together. Of four misses two turned out alive, one was
closed by other work, the fourth did not reproduce — and finding this out took longer than the edits
themselves. A combined task therefore costs exactly as much as the exploration of its parts, and
this is said to the owner before it is taken.

**Without the owner's word only the digest of observations leaves outward.** It says what was used
and what was never used once — that is a fact, and it does not turn into an opinion. A proposal is
another matter: it is a draft of an edit to someone else's tree, and some drafts fall away at the
first reading. Sent unreviewed, it becomes the work of someone who did not order it.

The order is this. Findings gather at the epic plan → the epic is over → the owner reads them all at
once and says which are right → what they named is shaped as a proposal and leaves. What sends it —
the rules-layer skill, if the tree laid it out.

Every finding names its address, and there are three:

| Where | What goes there |
| --- | --- |
| the rules layer — as a proposal | what is true for any tree of this class: an article, a point of a rule, a pattern |
| the names of this tree | what is true here: the rule's companion, the profile, the gate map |
| an override over the laid-out file | what sounds different here than in the package |

Without an address the edit lands where its author sees it — in their own tree — and the common part
settles in one place, unknown to everyone else.

**A review without an edit does not count as closed.** Out of it comes either an edit of the rules
layer or a proposal outward; neither came — it is a complaint, and it will repeat. A proposal the
owner spoke aloud about leaves outward in the same turn: written and not sent, it lies in the tree
indistinguishable from a sent one.

## Common misses

- **The folder is taken apart before the PR opens — later nobody remembers it.** The work queue
  audit counts a task closed by the merge. After it nobody answers for the folder — the work has
  moved to the next task, and the finding falls to someone else's session. The delivery guard holds
  this: opening the PR is refused while the folder lies in the branch.
- **The folder is taken apart by the last commit, after the push gate has passed whole.** The order
  is one. Merge of main, merging the agreement, bringing the domain texts up to date, all linters
  and checks green, taking the folder apart — and only then the PR. The cheap step stands before the
  costly one: a session that spent its window on the run hit the fill threshold on four binding
  lines, and there was nothing left to write them with. The second argument is stronger: a run that
  stands after the merge checks the merge itself — otherwise it looks at a state of the tree that
  will not reach main.
- **No plan on disk after the taking-apart, and the folder is not assembled again.** An edit after
  review remarks and a fix of a red run pass the progress guard on the sign from the branch history.
  A folder removed by its commit is the sign of handed-in work. A folder assembled anew would bring
  back the delivery guard's refusal on the very next call.
- **If the folder is simply deleted, `grill.md` is the first to go.** Deleting is easier than taking
  apart, and the owner's words are written only there, with nowhere to recover them from. So the
  guard demands that the branch add a record to the archive. What exactly was moved it does not
  check — the owner looks at that in review.
- **The folder of a task created after the work enters by a commit of its own.** The next commit
  takes it apart. A folder assembled and removed between two commits leaves no trace: the owner may
  merge the PR in that minute, and the grill is gone.
- **The closing steps are not agreed with the owner — they are listed here.** The rules review of
  the work is part of closing, as are merging the agreement and taking the folder apart. The owner
  decides not whether to launch it but what to do with the findings. A turn that ended with such a
  question is refused by the conversation guard: no rules were read in the turn, and the answer
  stands in them. Only what the rules lack is asked.
- **A ready-made code block in a pattern goes stale from someone else's edit.** It is bound to
  nothing: the spec audit reads the rule's statements and does not read the sample under them at
  all. Two fields made mandatory in someone else's work made the sample in a neighbouring pattern
  unbuildable. The sample itself changed by not a character and got into no task footprint, because
  not one word of that work is in it. The pattern is found by the name of the edited symbol, not by
  the theme of the work.
- **The epic plan is edited only where "how it ended" is written in.** The epic's boundaries and the
  order of its tasks stay as they were, while the work has already broken them. A task that decided
  to read the specs left above itself the boundary "specs — second turn", and the next executor
  reads it as in force. The epic's boundaries are re-read whole by the same session as the outcome
  of the work.
- **The archive is not updated after the rollout.** What went there describes the day of the move,
  and it is edited only together with an admission that it described it wrongly.
