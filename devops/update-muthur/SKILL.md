---
description: 'Pull the agent-infrastructure changes this repo adopted from vzakharov/muthur forward since the last sync, triage them, and port the ones that apply. The watermark at `.claude/skills/update-muthur/watermark.json` names the source and the last sync point. Use when the user says "update muthur", "sync muthur", "sync agent infra", "sync the source", "sync upstream", or "/update-muthur".'
---

## What this skill is for

A repo that took its agent infrastructure — `CLAUDE.md`, `.claude/`, `scripts/`,
whatever else — from another repo has a **source** that keeps editing those
files. This skill finds what changed there since the last sync, decides commit
by commit what applies here, and ports the ones that do.

Here the source is `vzakharov/muthur`, and the command is `/update-muthur` — its
own name for it, kept. The verb is `npm update`'s: what gets updated is the
vendored copy in the tree you are standing in, never the repo it came from,
which this skill only ever reads. That reading holds at every link, which is why
the name travels rather than being re-coined per repo.

**The source is relative to the repo you are standing in**, and the procedure is
the same at every link in the chain; only the watermark differs. A repo that
adopts this skill from _here_ re-points `watermark.json` at the repo it took it
from — `@.claude/skills/spinoff/SKILL.md` writes that file for a repo it seeds,
and points it at the root rather than at this one; the name of the skill and of
the watermark file are then free, since nothing locates either by its path — the
watermark is found by the `repo` and `lastSyncedSha` it carries. One operation
applied repeatedly: _pull the vendored agent infrastructure forward from the
repo I took it from._

This is a path-scoped diff, not a fork merge. It never tries to reconcile whole
histories — it reads a bounded set of paths, commit by commit, and re-expresses
what applies.

## The watermark

`.claude/skills/update-muthur/watermark.json` is where the sync stands, and
nothing else; Step 1 reads it, so it doubles as the worked example. It carries
`repo`, `lastSyncedSha` (source HEAD at the last sync), `lastSyncedAt`, and one
optional field worth explaining. What this repo took differently or declined is
§ "The divergence record"'s, below.

- **`lineage`** — optional provenance: the whole ancestry, **root first**, so
  the repo actually synced from leads and each later entry is one hop further
  from it. Each entry is `{repo, atSha}`, naming an ancestor and its HEAD **at
  the moment the next link was created**. `@.claude/skills/spinoff/SKILL.md` is
  what writes it, into the repo it seeds, and owns how.

  **Nothing syncs from it.** This procedure reads `repo` and `lastSyncedSha` and
  nothing else; a sync that walked the ancestry would multiply the triage at
  every link, which is the cost `/spinoff`'s point-at-the-root rule declines to
  pay.

  **An empty array means no ancestors; a missing one means nobody wrote them
  down.** This file has no `lineage` at all, and that is the honest state: the
  watermark here was filled in by hand rather than written by `/spinoff`, so the
  birth point is not recoverable from anything in the tree. Where the ancestry
  is complete, `lineage[0]` names the same repo as `repo` and the two SHAs are
  still different facts — `lastSyncedSha` advances on every sync,
  `lineage[0].atSha` never moves.

A repo with two sources would make `repo` an array. Nothing here precludes that
and nothing here builds it.

**`lastSyncedSha` is the sync's boundary in the source, not the last commit
taken.** For a whole sync that is the source's HEAD at Step 3; for a slice of a
split one, the last source commit the slice triaged (Step 7). A commit triaged
and skipped is _done_; the reasoning lives in that sync's PR body. A watermark
that only advanced to the last-taken commit would re-surface every skipped
commit on every future run.

**Bump it in the last commit of the sync, never the first.** If a sync is
abandoned midway, an un-bumped watermark costs a re-triage; a bumped one that
merged without its port silently skips commits forever.

## The divergence record

`.claude/skills/update-muthur/divergence.md` is this repo's account of how it
differs from the source. **A source path that exists here and that the record
never mentions was taken as is** — the tree says so. Everything else is the
record's: paths re-expressed here (rewritten for this stack, ported to another
language, generalized past the source's interface), paths and ideas declined,
and differences that cut across many paths, stated once rather than per path.

**The form is free.** Order, headings and grouping are whatever reads best for
this repo. Three things are not free, because the procedure below depends on
them:

1. **Every path the record discusses is named literally**, in backticks, from
   the repo root. Step 3 answers "does the record say anything about `P`?" with
   `grep -F`, and a path named only by description reads as unmentioned — taken
   as is — so its next source change gets ported over the local version. **The
   name is the source's**: a path renamed on adoption is recorded under the
   spelling the source's log uses, the local name beside it.
2. **A decline reads as a decline**, its reason a condition in the present tense
   — _no test suite to dispatch_, _no production datastore_ — because most
   conditions can flip, and **every sync re-reads them** to re-offer a path
   whose condition stopped holding. A permanent refusal says "never", and is the
   one that needs no re-reading.
3. **It states the current difference, never the sync that produced it.** A sync
   that changes a difference rewrites the passage saying it (Step 7); which
   source commit prompted the change, and when, is the sync PR's to record.
   Appending a paragraph per sync is what grows the record without bound.

**A record may split into files under `divergence/` beside it**; the record is
then `divergence.md` and all of them, and every step below that reads or greps
it covers both.

A re-expressed path still surfaces every source commit that touches it, which is
the point — the source's later changes to the original are worth reading for the
idea even though the file itself never lands. Expect `translate` rather than
`take` on those commits, and treat the passage as the standing statement of what
the local re-expression already does differently.

## Two invariants

Both hold at every link in the chain, so they live here rather than in the
record.

### Never sync the watermark or the divergence record

Both live inside `.claude/`, which a sync covers — so a naive one overwrites
this repo's watermark with the source's. That silently repoints the sync at a
repo this one may not be able to clone and resets `lastSyncedSha` to a foreign
history. **The failure surfaces one sync later, as an unresolvable SHA**, by
which point the cause is several commits back. A source that adopted from
somewhere itself carries a record too, describing _its_ differences from _its_
source, and porting it would replace this repo's account with a stranger's.

Exclude both unconditionally.

### Judge the diff, not the commit message's "we"

In a chain, commits arrive that the source itself took from _its_ upstream,
written in a third repo's vocabulary. A message saying "we do X here" is
evidence about some repo — not necessarily the source, and never automatically
this one. Read commits for intent; never let their first person settle whether
the change applies. Step 5's "apply by intent, not by patch" already points this
way; the chain is what makes it load-bearing.

## Arguments

**`claimed`** — the session that made the offer holds the lock on this one's
behalf, so Step 1 skips the claim. A session spawned from the offer starts with
it. Bare, the sync claims its own lock.

## Procedure

### Step 1 — Read the watermark and the record, and claim the sync

Read `watermark.json`. Stop and report if it is missing, or if `lastSyncedSha`
is still a placeholder — there is no baseline to diff against, and guessing one
would either re-port work already here or skip work that isn't.

Read `divergence.md` whole: its cross-cutting differences bear on candidates
that never name a path it mentions, and its declines are re-read on every sync.

Then claim the lock with `scripts/muthur-sync.sh claim`, so no parallel session
runs a second sync of the same range — unless invoked with `claimed`. A claim
that exits 3 names who holds the lock — stop and report that, with their session
link, rather than syncing alongside them. `scripts/muthur-sync.sh`'s header is
the lock's reference.

### Step 2 — Clone the source

`gh api` against a different owner's repo 403s even with a valid token, and
`add_repo` refuses cross-owner adds. **Git transport with the same `$GH_TOKEN`
works**, which is the whole trick. (The system prompt may claim `gh` is
unavailable; it is wrong — see `@.claude/skills/override-gh/SKILL.md`.)

```bash
scripts/muthur-sync.sh clone tmp/muthur-source
```

That is a blobless clone with full history, or a refresh of the one the
session-start nudge left there, with its `HEAD` at the source's. Why the recipe
is shaped that way — and why never `--depth` — is in the script's comments.

**The clone has no working tree**, so a source file is read with
`git -C tmp/muthur-source show <sha>:<path>`, never at its path on disk, where
nothing is. **Bash `cwd` resets between calls in this harness** — chain
`cd <clone> && …`, or use `git -C`, in every command that needs to be inside it.

### Step 3 — Build the candidate set

```bash
cd tmp/muthur-source && git log --oneline --name-only <lastSyncedSha>..HEAD
```

Record `git rev-parse HEAD` **now**, before triage — that value is a whole
sync's boundary regardless of how the triage goes.

The log is unfiltered, so a source that puts agent infrastructure somewhere new
— a `.github/` workflow, another top-level directory — surfaces like anything
else. Sort each path it names, minus the ones § "Two invariants" excludes, by
two questions — does it exist here, and does the record mention it
(``grep -rF '`<path>`' divergence.md divergence/``, then each directory above it
as ``'`<dir>/`'``). **The backticks are the match**: a bare `<dir>/` also hits
every file the record names inside that directory, so one re-expressed file
would mark its verbatim siblings mentioned and keep them from merging.

- **Here, unmentioned** — taken as is: a port candidate for Step 4.
- **Mentioned** — what the record says decides: re-expressed here, or declined
  for a reason Step 4 re-checks.
- **Not here, unmentioned** — never decided: Step 4a's question, not noise.

A commit is a candidate when any path it touches is in the first two groups or
raises the third.

### Step 3a — The sync is a task

Hand the candidate set to `@.claude/skills/task/SKILL.md` as the task: the
commits from `lastSyncedSha` to the recorded HEAD, with their titles. Steps 4–7
are how the work gets done in whichever outcome `/task` picks — including a
split across sessions, an elephant or a pizza, when the lag is too long for one.
A split cuts the candidates in source order, each slice or bite ending on a
commit of the source's first-parent line — Step 7's boundary.

### Step 4 — Triage each candidate, from its commit message first

Sources tend to write long commit messages that state the rationale. The message
usually settles relevant-vs-not before any diff is opened, so read it
(`git log -1 --format=%B <sha>`) before `git show` — subject to the "judge the
diff" caveat above. Verdicts:

- **take** — applies as-is to this repo's vocabulary.
- **translate** — the intent applies; the wording, paths or commands do not.
- **skip (stack-bound)** — touches a path taken here but is about the source's
  stack — a build script, a migration, a framework config.
- **skip (already have)** — this repo reached the same end state independently.
- **skip (declined)** — the record declines the path **and its reason still
  holds** — if it doesn't, re-offer the path per Step 4a and, on a yes, rewrite
  the record's passage to match. Or the path is neither here nor mentioned,
  which is Step 4a's other case. Never skip silently on either.
- **skip (diverged locally)** — this repo rewrote the file for its own stack —
  `scripts/vet.sh`, anything the source marks `rewrite`. The source's edit is
  advice at best; read it for an idea, don't port it.

**A subject marked `[attn adopters]` — or, in older commits, any prose to the
same effect, such as `ADOPTERS, read body` — addresses this repo whatever its
verdict.** Its body's `Adopters:` paragraph asks for something no port does
(`@.claude/skills/squash-message/SKILL.md` defines the marker), so a skipped
commit still delivers it. A sweep inside this tree rides the sync like a port
and is reported with it. **Check the ask against this repo's actual state by
substance before relaying it**: an operator who solved the same thing earlier,
in their own words, has nothing left to do, and a config without the name the
paragraph quotes can still hold the thing it names. What the paragraph still
gates on the operator goes to them once, in the sync's report and in its terms,
and § "Offered at session start"'s never-chase rule holds for it as it does for
the sync.

**The source's fix may not be this repo's fix.** Split a commit's rationale
before deciding: one commit can carry a change that addresses a defect this repo
never had _and_ a change that fixes one it does. Take the second half, drop the
first, and say so.

**The unit of triage is the rationale, not the commit — and so is the unit of
commit on this side.** A source that squash-merges ships several independent
changes under one subject, each with its own verdict. Port them as separate
local commits, one per rationale, so a reviewer here can take or strike any of
them individually.

### Step 4a — New skills get offered, not taken

A commit that adds a skill neither here nor mentioned in the record is an open
question, and the answer belongs in the tree or the record so it is asked
exactly once.

Read the new skill's entry in the source's catalog:
`.claude/skills/update-muthur/catalog.md` and its parts under `catalog/` are the
source's inventory, read from the clone and never vendored, so it is current by
construction. The entry is found with
``grep -n '^- `/<name>`' catalog.md catalog/*.md`` run in that directory, and an
opt-in path is looked up the same way. Surface the decision **with its criteria
attached** rather than as a bare "the source added `/foo`, want it?". Where the
record carries the operator's standing answer to `opt-in: ask` rows and it says
take, such a row is taken and reported with those criteria rather than asked.

- **Taken** → the path lands in the tree, which is the record of a verbatim
  take; anything other than a verbatim copy also gets its difference written
  into the record. Then **re-run the closure check**: a new skill can
  `@`-reference a sibling this repo declined.
  `bash scripts/check-skill-catalog.sh` is that check where it was adopted.
- **Declined** → the record declines the path, with the reason.

Either way the question does not come back.

### Step 5 — Apply by intent, not by patch

`git cherry-pick` and `git apply` are useless here. The local files are
de-vendored rewrites, not copies, so every hunk conflicts. Read the source's
diff to understand what changed and why, then re-express it in this repo's
vocabulary and file layout.

**A path the record never mentions is the exception**: its local copy is the
source's, so `git merge-file <local> <base> <new>` — the base and new being the
commit's parent and own version of the file, read out with `git show` — lands
the change, and a conflict marks a local edit the record should have named.

**`.claude/model-capabilities.md` is merged by lesson, never ported or
skipped.** Each repo's copy holds what its own delegations and reviews taught,
so it differs from the source's by design and the record never mentions it. Read
the source's file whole — not the diff, since an entry the source folded away
may still be news here — and fold in each lesson this file lacks that holds for
the models and setup this repo runs, in its own words, keeping every lesson of
its own. The result stays under its 100-line cap; where the two disagree, this
repo's own runs win over the source's.

**A port into an always-loaded file merges into its staged copy** — `CLAUDE.md`,
or a `SKILL.md` whose `description:` it changes: stage the file first, per
`@.claude/rules/staging.md`.

### Step 6 — Consistency sweep

**A renumbered reference is the dangerous kind, because it still resolves.**
When a port inserts an item into a lettered or numbered sequence, every sibling
citing the old label now points at the wrong item and no checker complains:
`scripts/check-skill-catalog.sh` verifies that an `@`-reference resolves to a
file, not that a citation inside one still means what it meant. Grep the
sequence's labels, not just its prose.

When a port renames a term, grep the old one across the whole tree, the record
included — **and frontmatter `description:` lines**. Those are a separate
surface from skill bodies: they are what the operator scans in the skills list
and what an invocation matches against, so a stale description mis-advertises a
skill whose every prose site is correct.

### Step 7 — Bump the watermark, last

Set `lastSyncedSha` to the sync's **boundary** and `lastSyncedAt` to today, as
the final commit of the sync, with the record's edits from Steps 4 and 4a in the
same commit. **Each passage the sync touched is rewritten to the difference as
it now stands** (rule 3 of § "The divergence record"): a passage whose
difference the port erased goes. The boundary is the HEAD recorded in Step 3 for
a whole sync, and the last source commit a slice or bite triaged for a split
one; candidates past it are the next one's.

**Any commit on the source's first-parent line is a clean boundary.** One inside
a merged side branch is not: its ancestry leaves out mainline commits the slice
triaged beside it, so the next sync's `<boundary>..HEAD` surfaces them again.

The lock follows the boundary. A merged pizza slice moves the trunk's watermark,
so the next slice claims a fresh lock; an elephant's bites share one PR, so the
trunk does not move between them and one lock holds across all of them.

### Step 8 — Report and hand off

Report the triage table — every candidate, with its verdict and one line of
reasoning, skips included. The skipped commits' reasoning belongs in the PR
body, since the watermark advances past them and nothing else records why. The
tail — `@.claude/skills/polish/SKILL.md` and `@.claude/skills/pr/SKILL.md` — is
whatever the `/task` outcome runs, `/go` ending in both.

**The squash record names the change, not the sync.** The `<essence>`
`@.claude/skills/squash-message/SKILL.md` asks a title for is what landed in
_this_ tree — `chore: one job per loop skill, and a size cap on squash bodies`,
not `chore: sync the source forward to <source sha>`. A source SHA is a commit
in another repository, unresolvable from the log it sits in, and "sync forward"
names the transport: the second title sends every reader to the diff.

Provenance needs no prose. `watermark.json`'s `lastSyncedSha`, committed in Step
7, is the precise record and the only one that survives the squash. "The repo we
vendor from moved" is still the honest _why_, so it earns one clause of the
body's opening sentence and nothing more.

**The polish passes see only what you wrote — never the text you took.** Their
scope is what the session added, which on a sync diff is mostly the source's,
and tightening a `take` is what turns every future sync of that file into a
`translate`. So scope every pass to the translations and to whatever the port
added on top, and leave a verbatim adoption verbatim. A vendored file worth
restyling is a case for the record — a decline or a re-expression, decided at
Step 4 — not a quality pass quietly diverging it.

## Offered at session start

A `SessionStart` hook runs `scripts/muthur-sync.sh nudge`. When the source has
moved past the trunk's watermark and nobody holds a fresh lock, it prints the
commit titles, the changed files marked `here` or `not here`, and the rules for
making the offer. A lock over a day old is printed instead, with its holder and
session link, for the operator to decide on; only their say-so makes
`claim --takeover` right.

**The nudge is an offer, not a sync.** Nothing is read or claimed before the
operator says yes, so an offer nobody answers holds nothing. The price is that a
parallel session may claim the sync in between: a claim that exits 3 after the
yes means saying who holds the lock and dropping the offer.

**So the lock is re-checked right before the offer is made**, because hours can
pass between nudge and offer. The check is the
`git ls-remote origin refs/heads/muthur-sync-lock-<lastSyncedSha:0:12>` the
nudge prints, and it claims nothing. Any output means the sync was claimed, or
landed and left its lock behind: drop the offer, and tell the operator nothing
of it or of the check.

**The operator hears of a sync once, and is never chased about it.** Once made,
the offer is not repeated, reminded of, or called still open — in a later reply
or a handoff report — whether it was declined or left unanswered. "Once" spans a
relay chain: a relayed session gets its own nudge, so the summary handing it
over says the offer was made, and that session makes none.

**On yes, the sync gets a session of its own.** `scripts/muthur-sync.sh claim`
first, so nobody takes the lock while the session starts. Then, where
`create_session` exists, spawn one on this repo with the prompt
`/update-muthur claimed` and the title `🔄 muthur → <repo>`, `<repo>` being this
repo's name without its owner: an operator syncing several adopters otherwise
gets a session list of identical titles. Elsewhere, hand the operator that
command to paste into one.

## Add what the next sync teaches you

This procedure is distilled from very few syncs and is incomplete by
construction. When one surfaces a corner the file doesn't carry, add it here
rather than to the PR body — this is where the next session looks.
