---
description: "STUB — not yet hydrated for this project. Pull the agent infrastructure forward from the repo you adopted it from: diff since the watermark, triage commit by commit, port what applies. Hydration is the watermark at `.claude/skills/update-muthur/watermark.json` — the procedure below is usable as written. Use when the user says \"update muthur\", \"update the agent infra\", \"sync muthur\", \"sync the source\", or \"/update-muthur\"."
---

> ⚠️ **STUB.** This skill has no watermark to run on. Before it can be invoked,
> fill in `.claude/skills/update-muthur/watermark.json` — `lastSyncedSha` (the
> source's HEAD when you cloned it), `lastSyncedAt`, `lineage` — and write
> `divergence.md` beside it for whatever your repo took differently or declined.
> `repo` already names the template, and needs changing only if you adopted from
> a repo that itself adopted from it. Delete this banner once you have, and drop
> `STUB` from the description above. If you took a one-time snapshot and do not
> intend to re-sync, delete the skill instead.
>
> **Hydration here is a few JSON fields and a record, not a procedure.** Unlike
> the other stubs, every step below this banner is usable exactly as written.

## What this skill is for

A repo that took its agent infrastructure — `CLAUDE.md`, `.claude/`, `scripts/`,
whatever else — from another repo has a **source** that keeps editing those
files. This skill finds what changed there since the last sync, decides commit
by commit what applies here, and ports the ones that do: _pull the vendored
agent infrastructure forward from the repo I took it from._

This is a path-scoped diff, not a fork merge. It never tries to reconcile whole
histories — it reads a bounded set of paths, commit by commit, and re-expresses
what applies.

**The name is the infrastructure's, not your source's.** `muthur` is where this
skill and everything it syncs came from; the repo it actually pulls from is
whatever `repo` says in the watermark below, which for a spun-off sibling is its
parent rather than the root. So `/update-muthur` in a repo two hops down still
syncs from one hop up.

**The verb splits: the command updates, the fields say synced.** `lastSyncedSha`
and `lastSyncedAt` are on-disk in every downstream watermark, so renaming them
to match orphans every adopter's file at once — and the prose below follows the
fields, not the command.

## The watermark

`.claude/skills/update-muthur/watermark.json` is where the sync stands, and
nothing else:

```json
{
  "repo": "<owner>/<repo>",
  "lastSyncedSha": "<source HEAD at the last sync>",
  "lastSyncedAt": "<YYYY-MM-DD>",
  "lineage": [
    { "repo": "<owner>/<root>",   "atSha": "<root HEAD when the parent was born>" },
    { "repo": "<owner>/<parent>", "atSha": "<parent HEAD when this repo was born>" }
  ]
}
```

What this repo took differently or declined is § "The divergence record"'s,
below.

- **`lineage`** — optional provenance: the whole ancestry, **root first**, so
  the repo actually synced from leads and each later entry is one hop further
  from it. Each entry names an ancestor and its HEAD **at the moment the next
  link was created**. `@.claude/skills/spinoff/SKILL.md` is what writes it, and
  owns how.

**Where the ancestry is complete, `lineage[0]` names the same repo as `repo`,
and that is not duplication — the two SHAs are different facts.**
`lastSyncedSha` is where this repo has synced _to_, and it advances on every
sync; `lineage[0].atSha` is where it started _from_, and it never moves. They
coincide until the first sync and diverge forever after, which is what earns the
field its place: that first sync overwrites the only other trace of the birth
point.

**An empty array means no ancestors; a missing one means nobody wrote them
down.** The root ships `[]`, which is complete. A watermark filled in by hand
from `docs/adopting/sync.md` has no `lineage` at all, and that gap is not
recoverable from anything else in the file — so a partial array, its first entry
naming something other than `repo`, is valid rather than malformed.

**Nothing syncs from `lineage`.** This procedure reads `repo` and
`lastSyncedSha` and nothing else. A sync that walked the ancestry would multiply
the triage at every link, which is exactly the cost `/spinoff`'s
always-point-at-the-root rule declines to pay.

A repo with two sources would make **`repo`** an array. Nothing here precludes
that and nothing here builds it — and it is a separate question from `lineage`,
which is provenance nothing syncs from.

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
record's: paths re-expressed here (ported to another language, split across
files, generalized past the source's interface), paths and ideas declined, and
differences that cut across many paths — "this repo's `AGENTS.md` is upstream's
`CLAUDE.md`" — stated once rather than per path.

**The form is free.** Order, headings and grouping are whatever reads best for
this repo, which its own agent knows better than this file does. Three things
are not free, because the procedure below depends on them:

1. **Every path the record discusses is named literally**, in backticks, from
   the repo root. Step 3 answers "does the record say anything about `P`?" with
   `grep -F`, and a path named only by description reads as unmentioned — taken
   as is — so its next upstream change gets ported over the local version.
2. **A decline reads as a decline**, its reason a condition in the present tense
   — _work is tracked in Linear_, _no CI yet_ — because most conditions can
   flip, and **every sync re-reads them** to re-offer a path whose condition
   stopped holding. A repo that declined the issue skills for Linear and has
   since moved to GitHub issues is asked again. A permanent refusal says
   "never", and is the one that needs no re-reading.
3. **It states the current difference, never the sync that produced it.** A sync
   that changes a difference rewrites the passage saying it (Step 7); which
   upstream commit prompted the change, and when, is the sync PR's to record.
   Appending a paragraph per sync is what grows the record without bound.

**A record may split into files under `divergence/` beside it**; the record is
then `divergence.md` and all of them, and every step below that reads or greps
it covers both.

A re-expressed path still surfaces every upstream commit that touches it, which
is the point — upstream's later changes to the original are worth reading for
the idea even though the file itself never lands. Expect `translate` rather than
`take` on those commits.

## Three invariants

Each holds at every link in the chain, so they live here rather than in the
watermark.

### Never sync the watermark or the divergence record

Both live inside `.claude/`, which a sync covers — so a naive one overwrites
this repo's watermark with the source's. That silently repoints the sync at a
repo this one may not be able to clone and resets `lastSyncedSha` to a foreign
history. **The failure surfaces one sync later, as an unresolvable SHA**, by
which point the cause is several commits back. A source that adopted from
somewhere itself carries a record too, describing _its_ differences from _its_
source, and porting it would replace this repo's account with a stranger's.

Exclude both unconditionally.

### Never sync the source's cost rows

A source that has not migrated its rows to its ledger branch still carries them
in `.claude/costs/sessions/`, the one path in `.claude/costs/` that is data
rather than machinery: porting it would add the source's spend to this repo's
totals, and no later report could tell the two apart. Exclude it unconditionally
too, whether or not this repo runs the ledger.

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
No record means nothing here differs from the source.

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

**Bash `cwd` resets between calls in this harness** — chain `cd <clone> && …` in
every command that needs to be inside it.

### Step 3 — Build the candidate set

```bash
cd tmp/muthur-source && git log --oneline --name-only <lastSyncedSha>..HEAD
```

Record `git rev-parse HEAD` **now**, before triage — that value is a whole
sync's boundary regardless of how the triage goes.

The log is unfiltered, so a source that puts agent infrastructure somewhere new
— a `.github/` workflow, another top-level directory — surfaces like anything
else. Sort each path it names, minus the ones § "Three invariants" excludes, by
two questions — does it exist here, and does the record mention it
(`grep -rF '<path>' divergence.md divergence/`, the path and each directory
above it):

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
attached** rather than as a bare "upstream added `/foo`, want it?".

- **Taken** → the path lands in the tree, which is the record of a verbatim
  take; anything other than a verbatim copy also gets its difference written
  into the record. Then **re-run the closure check**: a new skill can
  `@`-reference a sibling this repo declined.
  `bash scripts/check-skill-catalog.sh` is that check where it was adopted.
- **Declined** → the record declines the path, with the reason.

Either way the question does not come back.

**A path the source's catalog marks `never` is not offered**: the entry has
answered for every adopter, and what it says the sync does instead, if anything,
is the whole verdict. Nothing goes in the record.

**An opt-in entry is offered by its own path, the same way**, even when the
directory around it was taken. The catalog marks such an entry `opt-in: ask`, as
it does `.claude/costs/`, and a parent directory having been taken says nothing
about whether the operator wants what it costs. Ask with the entry's criteria; a
no is declined in the record under the entry's own path.

### Step 5 — Apply by intent, not by patch

`git cherry-pick` and `git apply` are useless here. The local files are
de-vendored rewrites, not copies, so every hunk conflicts. Read the source's
diff to understand what changed and why, then re-express it in this repo's
vocabulary and file layout.

**`.claude/model-capabilities.md` is merged by lesson, never ported or
skipped.** Each repo's copy holds what its own delegations and reviews taught,
so it differs from the source's by design and the record never mentions it. Read
the source's file whole — not the diff, since an entry the source folded away
may still be news here — and fold in each lesson this file lacks that holds for
the models and setup this repo runs, in its own words, keeping every lesson of
its own. The result stays under its 100-line cap; where the two disagree, this
repo's own runs win over the source's.

### Step 6 — Consistency sweep

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

If this repo adopted the sync path without the PR loop, land the sync however it
normally lands changes — the triage table still belongs wherever that record
goes.

**The squash record names the change, not the sync.** The `<essence>`
`@.claude/skills/squash-message/SKILL.md` asks a title for is what landed in
_this_ tree — `chore: one job per loop skill, and a size cap on squash bodies`,
not `chore: sync the template forward to <source sha>`. A source SHA is a commit
in another repository, unresolvable from the log it sits in, and "sync forward"
names the transport: the second title sends every reader to the diff.

Provenance needs no prose. `watermark.json`'s `lastSyncedSha`, committed in Step
7, is the precise record and the only one that survives the squash. "The repo we
vendor from moved" is still the honest _why_, so it earns one clause of the
body's opening sentence and nothing more.

## Offered at session start

A `SessionStart` hook runs `scripts/muthur-sync.sh nudge`. When the source has
moved past the trunk's watermark and nobody holds a fresh lock, it prints the
commit titles, the changed files marked `here` or `not here`, and the rules for
making the offer. A lock over a day old is printed instead, with its holder and
session link, for the operator to decide on; only their say-so makes
`claim --takeover` right.

**The nudge is an offer, not a sync.** Nothing is cloned, read or claimed before
the operator says yes, so an offer nobody answers holds nothing. The price is
that a parallel session may claim the sync in between: a claim that exits 3
after the yes means saying who holds the lock and dropping the offer.

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
