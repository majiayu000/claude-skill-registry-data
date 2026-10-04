---
name: consolidate
description: "Test, fold or refute hypotheses beside the knowledge record, and reconcile records across branches. Use when open or check say hypotheses wait or an id is CONTESTED, when a write was refused into a hypothesis, before merging a branch whose record changed, and when a pull request's dry run or remeasure is red. Covers consolidate --dry-run, the fold, --refute, --from, same and distinct at the fold, and remeasure."
---

# Consolidate

A hypothesis is a claim the base does not yet hold: a refused reading, a proposal not yet approved, a branch's record, a what-if. Nothing here decides for a person; the dry run tests, the fold and the refutation are the person's acts, recorded so the question never returns. Run `kpop` or `kpopper` from the native runtime and prefer the canonical executable in `KPOPPER_AGENT_CONTEXT.command`. Do not guess a path or silently use PATH.

In ordinary conversation, name the product **kpopper** and describe the action in the user's language. Reserve the exact skill name `kpopper:consolidate` for invocation instructions, technical documentation, debugging, or explaining this specific skill. Fold the product name into the explanation of the action; no extra announcement is needed.

One record is written by everyone, from any session or branch, as long as the write is consistent
with it. **A contradiction opens a hypothesis**, and the reader tells one by the id and the day.
`set` of a reading no newer than the base's (its `of:`, else its source's read date) that differs is
refused - two readings of one day that disagree are two writers, not the world moving; a newer
reading updates the base and flags what rests on it. `add` of an id the base holds is refused, and
with a different value or verdict it is a contradiction: a standing judgment is replaced in the base
only when its own `wrong_if` holds now, and otherwise the rewrite waits beside the record until a
person takes it by name at the fold (`--take <id>`). The same verdict on other grounds - another
why, other dependencies, another condition - is a decision written again and goes the same way. A
replacement that rests on less names each dependency it drops, with the reason: `--drop "<id>:
<why>"`. Every replacement leaves a trail - one `replaced:` line on the judgment, and the body it
replaced kept whole in `.kpopper/replaced.yaml` - so `open` and `check` say *reversed on <day>*
until someone reviews it, `set` of a reading only a replaced judgment listened to says so, and
`pull <id> --history` shows what stood before. A reading dated after today is refused: a day is
the record's clock. Nothing written into the body opens that door - every session's first write is a
source carrying what it was asked, so a field read as a person's authority would be a key every
session already holds. `request: s.<date>_<slug>` - a session source whose `asked:` is the person's
request verbatim, rested on - still names whose asking the change was taken from, said *on the word
of* on every surface: provenance the person weighs at the fold, and permission for nothing.
A write resting on what only a hypothesis holds belongs in that hypothesis. Each refusal names the
command that writes the same thing into `.kpopper/hypotheses/<name>.yaml` beside the record - the base
untouched - named after the id contradicted and a mark of the claim written, unless `--hypothesis
NAME` on `set`, `add` or `review` names it. The first write stamps `born` in the head; `claim:`, a
head `wrong_if:` and `folds: never` are the one thing a hand writes there. Three uses: a concurrent
writer whose reading was refused; a proposal not yet approved - a branch's record *is* this, and
travels with the branch; a what-if, `folds: never`, evaluated at every dry run and never written.

**The consolidation walk.** `consolidate --dry-run` lays the hypotheses named - every one, when none
is - over the base by id and runs the reader's own `check` on it, reported in a fixed order:
arrived, updates (the readings a hypothesis replaces, and what rests on each), reversed (a verdict,
or other grounds, over a standing judgment - both sides' because, rests_on and wrong_if beside each
other), moved / falsified, contested, candidates, new subjects. Three lists ask three answers, each
recorded by a command so the question
never returns: a candidate pair is the **same** subject (`same a b`) or **different** (`distinct a b
"why"`); a **contradictory** id - two hypotheses on one, or a reading the door refuses - is read
again on a later day, `set` in the base, or in the hypothesis that read it when the newer reading
bears its claim out but not its number, so the fold still carries what else it brought; or it is
refuted. The run exits non-zero on a contested id, a falsifier that holds, a hole, or a head
`wrong_if` it cannot decide; a premise that moved under a judgment leaves it green and blocks only
the fold, and `review <id> --hypothesis NAME` refreshes the snapshot against the record as it stands
under the hypothesis. `consolidate` runs the same test and, only when it is clean, writes the union
through the write path: every replacement passes the one door a `set` passes, asked with the base's
own readings, so a reading born of a same-day refusal waits until someone reads again on a later
day. A verdict, or other grounds, over a standing judgment is **reversed**: it folds when the base's
own condition has broken the judgment on what the base holds - a hypothesis that brings the reading
that breaks a judgment together with the verdict that repairs it has not broken it here, and the
report says its readings would - or when a person names it, `consolidate NAME --take <id>`; until
then the run is red and nothing folds. Taking by name is the person's act, and the session's part is
to put the decision in front of them in the words of the work - which verdict would replace which, on
what grounds, what it stops resting on - and ask whether it stands. On their word the session runs the
take itself and reports what folded. The command is the session's to run, never a request to the
person: a session that hands it over as their task has hidden the decision behind the mechanism. And
never take on the session's own word, the way the refusal into a hypothesis was built for. A
replacement that rests on less names each dropped dependency at the fold too, `--drop "<id>: <why>"`,
asked of the person the same way - why the decision stops resting on it - and run by the session.
A subject does not change kind at the fold - an entry under a judgment's id or the reverse, an
arrangement replaced by what is not one or a judgment that would become one - and no name takes
those: write it as its own decision. Across
the branch line a reading from another source than the base's, with another value, is contested the
same way; a review - the same decision, its seen refreshed - does not travel; a branch's record folds
onto a committed base only, and the fold ends with the commit that makes it a commit of its own. The
result is read back and undone whole if `check` then says anything new; what the fold replaced is
kept beside the record; the folded files go, and what to commit is printed.

**Pending findings, in the same run.** In an Advanced project a live dry run over every hypothesis -
none named, no `--from` - then lays each active finding of the pending ledger over the base alone,
under its own `pending` heading: the ids two findings hold differently, what accepting each would
change and break, and what only all of them together break. A finding that would falsify a judgment,
leave a hole, bring a reading the door refuses or reverse a standing verdict makes the run red, and
so does one the base cannot read as written, or would read its own judgments otherwise beside
(`check` names why a finding cannot be read at all); a premise it moves leaves it green. Nothing
adopts a finding and nothing else waits on it - the fold, commits and merges go on - and a frozen
run, which CI makes, has no pending part. Put what breaks in front of the person in the work's words
and ask whether the finding is right: a wrong one is rejected with their reason (`kpop pending reject
<revision> --reason "<why>"`, the revision from `kpop pending status`), run by the session; one that
stands is read again and `set` in the base, or accepted in the knowledge PR.

Before accepting a material consolidation, examine affected judgments for a failure that arises
only when the changes are combined, even if each change passes separately. Use the same
[failure search](../kpopper/references/falsifiers.md#look-for-a-failure-the-current-check-would-miss) to expose shared assumptions
or newly incompatible decisions. Record any resulting objection or additional condition, and
repeat the dry run after changing the record; a passing dry run covers the declared checks.

**One rule, two containers.** What stands is contested only by something recorded: a rival claim, in
a hypothesis; or a doubt with no rival value yet, an open question that names the id. The page says
*a hypothesis contests this arrangement*, or *a question* does, `check` notes the same, and both
stand until a person consolidates, or answers the question with `answer`. Deleting the file is neither,
and `correct` is no way around the fold: it refuses anything already landed.

**How a merge goes.** git merges the files: additions in id order rarely meet, and hypothesis files
meet only when two branches claim the same thing under one id, since the name carries both - two
readings that agree, and either head is the whole of them; two that disagree are two files git
merges, and which of them stands is the dry run's question for a person. The dry run tests the
result: the pull request runs it on the merged tree, and the push to `main` runs it again as the
second net, for two pull requests each consistent alone that contradict together. Fold a hypothesis
the dry run proves *before* the pull request, so `main` receives base changes; let an unproven one
merge as a file, and `main` carries an open hypothesis the opener counts. Nothing crosses branches
unasked: `pull <seed> --from <ref>` lays what another branch committed beside your pull, and
`consolidate --from <ref> --dry-run` tests its record as one more hypothesis named after the ref - a
pull, never a push, and how a dead branch's facts are harvested. Every write - `set`, `add`,
`review`, `same`, `distinct`, the fold, the refutation - takes an exclusive lock on the record's
directory where the platform has one - Windows has none - so two sessions on one file take turns
instead of the last one discarding the first. In the tree each worktree writes its own copy and git
merges them; out of the tree every worktree writes the one file, and only the lock stands between
them.

## The tree, measured against the record

`remeasure` is how the tree answers for the record. `check` compares `seen` against the record's
own stored value and never against the tree, so a count that is wrong about the tree passes as
long as it agrees with itself. An entry whose value is a fact about the tree - lines of a file,
files a package ships, places in the code where something is decided - names the recipe that
takes it, `measure: <name>`, and `.kpopper/measure.yaml` beside the record holds that name's
argument list. The name is all the record carries: a bare name, refused by `add` and failed by
`check` when it is not one or stands on anything but a stored scalar reading. `kpop remeasure`
prints the plan and runs nothing; `--run` runs each cited recipe once, from the checkout's root,
without a shell, and lays what differs over the record as one more hypothesis, `tree/<commit>`,
through the same dry run that tests any hypothesis - red on a falsifier that holds on the measured
value, a hole, or a reading the tree contests; green, with the `set` command that refreshes it, on
an older reading that moved without crossing a line. A hypothesis that replaces a measured entry
carries the line with it, since the fold takes its block over whole. The pull request runs it; nothing that reads
the record does. Name a recipe only where a command honestly takes the count the entry's `at:`
describes - a survey, a hand-scored run, a prior has none, and their honest form is the reading
with its date.

**A stopped Git merge.** Use `kpop consolidate --resolve --dry-run`, then `--resolve` to write a checked local resolution of independent entries. Resolve and stage other conflicted paths first. The command preserves supported history and refuses competing claims or manual conflict-file edits. It leaves the resolved record unmerged for review. For compact history it stages only the generated union manifest, so aborting the merge removes that metadata too; other indexed content stays as the user staged it. Ordinary and legacy history resolution leave the index unchanged. Review the record, `git add` it, then finish the existing merge. No fetch, commit, push or pending adoption is implied. Check installed `--help` and the [supported layouts and limits](../../docs/coding-and-ci.md#resolve-a-stopped-git-merge-locally); an unsupported format is not permission to take one side.

## The commands

```bash
kpop consolidate --dry-run [NAME ...]     # the union, tested; every hypothesis when none is named
kpop consolidate [NAME ...]               # folded into the base when the test is clean
kpop consolidate NAME --take <id>         # a reversal the person confirmed, run on their word, folded with its trail
kpop consolidate NAME --drop "<id>: <why>"   # a dependency the replacement drops, named at the fold
kpop consolidate --refute NAME "why"      # one negative finding stays; the file goes
kpop consolidate --from <ref> --dry-run   # another branch's committed record as one more hypothesis
kpop pull <id> --history                  # the versions a judgment's replacements kept
kpop same <a> <b> | distinct <a> <b> "why"   # the two answers the candidates list asks for
kpop remeasure [--run]                    # the entries that name a recipe, taken again from the tree
```

The pull request runs the dry run and the remeasure on the merged tree, and the push to `main`
runs them again; [coding-and-ci.md](../../docs/coding-and-ci.md) shows the steps and how to
inspect another branch's record before merging.
