---
name: git-disaster-recovery
type: Skill
title: "git-disaster-recovery — get the shared folder back to GitHub main, fast"
description: "One-time recovery when a shared checkout has drifted far from GitHub main: hundreds ahead/behind, stacked worktrees and PRs, a dirty tree nobody owns. Use when tempted to reset or force-push. NOT for the ordinary 30-minute release loop (operations/INTEGRATION_MAINTAINER.md)."
tags: [operations, git, worktrees, branches, pull-requests, recovery]
timestamp: 2026-09-20T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/git-disaster-recovery/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# git-disaster-recovery

**This should never run twice.** The real system is a release every 30 minutes:
pull, merge, run the release script, under a minute. At our pace every 30
minutes is a day of work, so a checkout that skips releases for a day is a
quarter behind and every remote agent is writing against stale code. This
skill exists only because the release agents once let that happen. It is a
pre-launch tool for a six-week push. Its methods are unusual and they end
the moment the folder matches GitHub again.

**The one goal:** make the shared folder and GitHub `main` the same thing as
fast as possible, without deleting unique product. Everything else in here
is in service of that. The name of the game is to reduce the volume of stuff
in front of your face. Decide fast, land fast, delete fast, and only then
look hard at the little that is left.

**GitHub `main` is the truth.** Local `main` is a stale view. While the local
agents were not doing their jobs, GitHub kept moving. Every comparison in
this skill is against `origin/main` after a fresh fetch, by patch, never by
`ahead/behind` or `--merged`.

Companions, read only when pointed:
- [owners-and-prompts.md](owners-and-prompts.md): how to find who owns the
  few hard leftovers and the three short messages to send them.
- [evals.md](evals.md): proof record. This skill is not proven.

## Hard bans

- Never force-push.
- Never leave a local worktree or a local branch behind. There is no intake-worktree exception either: land with git plumbing
  (`merge-tree --write-tree`, `commit-tree`, push the commit to main) or by
  pathspec commits in the shared checkout. The `unify-main` skill has the
  exact recipe. Remote branches are tolerated; local ones are forbidden.
- The ordinary way dirty files go live is `./ship.sh`: it commits every uncommitted file in
  the checkout and pushes it, constantly, by design (`policies/shared-checkout.md`). This skill
  is only for a checkout that has drifted far from GitHub.
- Never merge onto the dirty shared checkout or reset it "to make room".
  Landing happens with plumbing against current `origin/main`, never by
  touching another lane's files.
- Never delete unique **product** GitHub does not have. Older copies, files
  GitHub already rewrote, trees that would unwind later `main`, and scratch
  are junk. Delete those.
- Never splice a code file by "keep both lines". Take a whole valid file, or
  a complete new file. A line-union of two TypeScript files does not compile.
- Never take a whole dirty neighborhood because one file in it is unique.
  Extract the unique file or hunk. Parking a cluster is not extracting the
  product.
- Never tell a leftover owner they were interrupted or cut off. Nobody was.
- Never question a database change itself. Migrations are judged only for
  collision and regression. What they change is the owner's business.

## Who runs it

A senior session runs the whole thing. A junior who finds this pile
inventories and escalates. Subagents do the mechanical passes (migration
ledger check, dirty-file classification, owner hunt); the senior decides and
lands. Arman is involved only for a real two-writer conflict, and then as one
line with one recommendation.

## The order of operations

Do these in order. Do not start step 4 while step 2 still has obvious work.

### 1. Freeze and fetch

`git fetch origin`. Do not move `HEAD` or the working tree. Count with
ordinary git: worktrees, local and remote branches, open PRs, stashes,
dirty and untracked paths, `git rev-list --left-right --count origin/main...HEAD`.
If a script goes silent for a minute, kill it and count by hand. If
`git cherry HEAD origin/main` hangs, kill it; the direction that finds unique
local work is `git cherry origin/main HEAD`.

All landing goes to `origin/main` by plumbing: `git merge-tree --write-tree
origin/main <ref>`, `git commit-tree`, push the commit to main; a single
file lands through a temporary index built from `origin/main`. Re-fetch
before every land. No worktree, ever.

Then run the same count in **every sibling repo** under the workspace, and
list every registered worktree, every local branch, every remote branch
besides main, and every unregistered directory under `.wt/`. The disease
is never in one repo: on 2026-09-20 the frontend was the loud one while
aidream, matrx-extend, matrx-local and common-docs each carried dozens of
branches and worktrees of their own. One inventory table for all repos is
what Arman and the other lanes work from.

Report two sentences: what the status line implied, what the patches say.
Then start step 2 immediately. No approval is needed for anything below
except a real conflict.

### 2. Shrink the dirty set

This is the most important step and it comes first. Over ninety percent of
what looks dirty is already live or worthless. Every modified or untracked
path gets exactly one fate, decided against `origin/main`, not local `main`:

| Fate | Test | Action |
|---|---|---|
| Drop | Content matches `origin/main`, or is an older version of what GitHub has, or restores something GitHub deleted | `git checkout origin/main -- path` or delete the untracked file. Not a review item. |
| Drop | Junk: `.wt/`, lockfile-only, generated stamps, scratch, review notes, agent residue | Delete. |
| Land now | Skill, doc, comment, lesson, coverage-only test, or a whole new file GitHub never had and that nothing on GitHub supersedes | Commit the whole file to main by pathspec, push. Do it in batches this hour. |
| Land now | Migration whose bytes are already in the applied ledger, or whose objects already exist live | Land it. It is inconsequential. |
| Land now | Migration not yet applied, no collision with any other migration on GitHub or in the pile, no regression of a live object | Land it. Do not question what it changes. |
| Hold | Migration that collides (same number, same object written twice) or would regress a live object | Name it in one line with a recommendation. |
| Hold | Unique product hunk in a file GitHub also changed, and the two change the same behavior | Keep the file where it is; it goes to step 4 with the three facts. |

"Exists on GitHub and differs" is not unique. Prove a unique hunk or drop
the file. Several dirty blobs in past piles were exact earlier GitHub
commits, and deleting "dirty" files would have dropped SQL GitHub still had.

A dirty file that is a rewind (older version number, older config) is junk.
A migration that only looks dirty because local `main` froze is already
live. Check the ledger, not your feelings.

Dispatch two subagents at once for this step: one classifies every
non-migration path (match, older, junk, new, unique-hunk), one checks every
migration against the applied ledger and the live schema. You act on their
tables the same hour.

### 3. Land PRs and clean leftover branches

Every open PR and every leftover branch or worktree whose unique patches are
not on `origin/main` lands now unless someone can name the exact files where
the same behavior is written twice. Draft is not a hold. Red CI is not a
hold unless it proves this change broke boot, auth, data, or a shared
contract. "The family needs inspection" is not a hold. Name the conflict or
land it.

Mechanics:
- Compare by patch: `git cherry origin/main <tip>`. Same message already on
  GitHub means landed. Cherry `+` on an old branch is often a stale ancestor
  under a newer namesake tip; merging it can delete an enormous amount of
  later work. Extract the unique commit or hunk, never merge the ancestor.
- Unique commits that exist only on stale local `main` are cherry-picked in
  order onto `origin/main` in git's database, not merged as objects.
- One leftover at a time onto `origin/main`, then push. Re-probe `merge-tree`
  against the new tip after every push.
- Mechanical git conflicts (two imports, two changelog lines, two ledger IDs)
  are keep-both, with the later filing taking the next free ID.
- After the work is reachable from `origin/main`, delete the branch, the PR,
  and the worktree. Re-cherry immediately before each delete.
- A worktree whose commit is on `origin/main` is a delete, unless another
  session is landing from it this minute. A hollow tree (thousands of ` D`) is not product; if
  `worktree remove --force` hangs, skip it and keep going.
- A stash is dropped only when every file in it is on GitHub. A mixed stash
  has its unique lines landed first.
- Same-area families (several leftovers touching one feature) are split:
  additive files land, and only the parts that rewrite the same live
  behavior two ways are held.

**Ancient work.** Older than 72 hours and never on `main` is more likely
junk than not, but this is a rule of thumb, not a law. Junk-check it first
and delete what is junk. A whole feature that simply missed the boat for a
week is not junk. If it is a clearly separated chunk, land it. If it is
questionable, hold it as one line.

### 4. What is left is small. Decide it, in this order

**The target is zero: zero dirty files, zero worktrees, zero local branches,
zero remote branches besides main, zero PRs, everything on main and pushed.
And nothing lost.** For
every leftover that still holds work not on main, apply these three options
in order. An agent with no access to Arman stops at option 2 and ships.

**Option 1. Find the owner and hand it back.** Send a quick lane (Sonnet)
to find the conversation that wrote it: worktree or branch name, distinctive
paths, transcripts from the last 48 hours across Claude Code, Cursor and
Codex. If it has a real send door to that chat, it sends the four-line
message from [owners-and-prompts.md](owners-and-prompts.md). If not, it
writes the one paste line for Arman. Do not wait on the reply; go to
option 2 at once.

**Option 2. Judge the code and ship it.** Read the actual diff. Write down
three facts: the feature it belongs to, the time of its last change, and
whether it is destructive (drops, deletes, rewinds, or replaces a live
behavior with an older one) or obviously bad (does not compile, breaks a
guard, contradicts a ruling). If it is not destructive, not obviously bad,
and cannot break the whole app, put it on main, delete the worktree or
branch, push, and have a subagent verify the touched area compiles and its
tests pass. You ship regardless of whether the owner ever answers. Stale is
not a reason to hold: a lane that missed a week still wrote product.

**Option 3. Bring the rest to Arman, one item, three facts.** Only what
failed option 2: destructive, obviously bad, or would break the whole app.
Give him the feature, the time of the last change, and exactly why it is
dangerous, with your recommendation. Never a list of paths, never a
question without a recommendation.

Two owners on one file is a real conflict: option 3.

#### Finding owners

Read [owners-and-prompts.md](owners-and-prompts.md) for the hunt and the
three messages.

The deliverable is a paste-ready list for Arman, one line per item:
**exact conversation title, one sentence of what that agent must do.** Not a
research dump. Not a wave report. If this session has a real send door to
that chat, send it yourself and say so. Otherwise hand him the list.

Two owners on one file is a real conflict: hold it and say so.

### 5. Point the shared folder at GitHub

The success condition is the shared folder being a clean match of
`origin/main`. Do this as soon as every remaining dirty path is proven
dropped, landed, or committed to a named branch. No approval is needed for
that. Immediately before, re-diff the dirty set against current
`origin/main` one more time: new files appear while you work.

If the checkout's guard refuses `reset --hard` or `restore .`, restore every
named disagreeing path from `origin/main` and point local `main` at that
tip. Same outcome. Do not invent a third tree.

Then tell Arman, in plain sentences: the folder matches GitHub, these named
branches hold what is still unresolved, these are the one-line real
conflicts with your recommendation.

If the repo has a generate step that is the live schema contract (aidream's
`db/generate.py`), run it once the folder matches GitHub and commit that
output before replaying anything parked. Generate is truth for
schema-shaped output only. It is not a license to wipe hand-written methods.

### 6. Release, and go back to the 30-minute loop

Pull, merge, run the release script. If the release script halts on
anything other than a failed build or a failed live health check, that is a
bug in the gate: get past it, keep merging, and fix the class. Then the
ordinary loop: pull first, commit, resolve, release, every 30 minutes.

One halt seen twice in one day: a down-migration sitting at the top level of
the migrations folder. The release sweep reads it as pending forward work and
refuses it. It belongs in the repo's inverse directory with the header that
directory requires. Move it, do not "fix" its SQL.

Fresh dirty files after this point with no real conflict are committed on
the ordinary cadence. Real conflicts go to Arman immediately, one at a time,
with one recommendation.

### 7. The hours after: keep local equal to remote while lanes write

The folder is clean, but dozens of sessions write into it every minute, and
the next usage pause or crash strands their half-finished files as dirty
paths nobody owns. Do not let that pile grow back. Every 30 minutes:

- The loop between releases, in this order, every 30 minutes or sooner:
  pull with no rebase, merge, `pnpm sync-types` (API shapes and database
  types from the live schema), type-check, fix what it names, release.
  A sync that happened three hours ago is not a state.
- A gate that stops a primary script is a bug, not a safeguard. On
  2026-09-21 the install gate refused `pnpm sync-types` for hours because a
  dev preview was running. Such a gate warns with the remedy and
  proceeds; refusal is opt-in. Fix the gate the same hour, with its
  self-test proving both modes.
- Fetch, `pull --no-rebase`, push. If the pull is refused because an
  untracked file "would be overwritten", a lane pushed that file from its
  own worktree and left a copy here: if the copy is byte-identical to
  `origin/main`, delete it; if it differs, move it aside and land the
  unique hunk later. Never a blanket clean.
- Classify the dirty set again with the step 2 table. Files older than 30
  minutes with no writer are cut-off work: commit them in coherent clusters
  with explicit paths and plain messages, pull, push. Files touched in the
  last few minutes belong to a live writer: leave them.
- Type-check GitHub main after every batch (a temporary export of origin/main is fine; a worktree is not). A blind
  batch that breaks the build is undone the same hour, one file at a time,
  never by reverting the batch.
- Remove every worktree that is not the release script's own, landing its
  unique files on main first. Idle or live makes no difference: nothing
  waits in a worktree. A slow filesystem makes `worktree remove` hang: unregister it under
  `.git/worktrees/` and delete the directory in the background.
- Install the standing guard: matrx-frontend has `pnpm worktree:janitor`
  (scripts/worktree-janitor.sh, self-tested), run by the release script
  after every push. It removes every worktree and local branch whose tip is
  already on `origin/main`, deletes unregistered `.wt/` leftovers, and
  names the rest with "land it on main and remove it". Port it to any repo
  that shows the same disease; a guard you cannot demonstrate failing is
  not a guard, so keep its self-test.
- The shared-checkout guard reads the whole command line. One `checkout -- .`
  or `add -A` anywhere in a chained command refuses the entire chain before
  any of it runs. Name every path.
- Read a repo's deploy workflow before deleting a remote branch: matrx-sandbox
  `deploy/hosted` is a CI-written deploy target. Retry git commands that hit a
  contended index lock before believing the failure; in zsh build refspecs with
  `printf` or land from bash. A shared helper reached from client bundles never
  imports server-only code. Identical-second mtimes on many files mean codegen.

## Done means

1. The shared folder is a clean match of `origin/main`.
2. Nothing unique was deleted. Every held item is on a named branch with an
   owner line, or is a one-line real conflict in front of Arman.
3. Leftover PRs, branches, worktrees, and stashes are gone or named.
4. At least one release has gone out on the new tip.
5. Anything this skill did not name is folded into this file as a rule (one
   line) and said to Arman in one sentence.

"The checkout looks better" is not done. "Inventory is complete" is not
done. A parked cluster is not done.

## Rationalizations

| Excuse | Reality |
|---|---|
| "149 ahead means 149 unique commits" | Cherry by patch. Most were already on GitHub under new hashes. |
| "This dirty file exists and differs, so keep it" | Exists-and-differs is not unique. Prove a hunk or drop it. |
| "Migrations are scary, hold them all" | Ledger check. Most are already live. The rest land unless they collide or regress. |
| "I should not question the database change" | Correct. You judge collision and regression only. |
| "I'll wait to land the easy files until owners are found" | Backwards. Easy files land this hour. Owners are for the few hard leftovers left after. |
| "I'll park the whole cluster and decide later" | Parking is not extracting. Take the unique product out of the neighborhood. |
| "Keep both lines in this test file" | That is a syntax error. Whole valid file or a complete new file. |
| "Draft PR, red CI, or 'the family needs inspection'" | Name the two files with the same behavior twice, or land it. |
| "Older than 72 hours, so it is junk" | More likely junk. Junk-check it. A missed feature is not junk. |
| "I need Arman to approve the reset" | Not once every dirty path is proven dropped, landed, or on a named branch. Do it and tell him. |
| "A git conflict is a real conflict" | A real conflict is one behavior written twice, two ways. |
| "The inventory script will finish eventually" | Kill it after a minute. Count with plain git. |
| "Cherry said plus, so this leftover is newer" | A plus on an old branch is often a stale ancestor. Merging it unwinds main. |
| "It is on origin/main, delete the worktree" | Yes. Delete it. |
| "The hung worktree blocks the repo" | Skip it. Finish the rest. |
| "The first release shipped, so we are done" | Done is the 30-minute loop running again. |
| "I'll write a wave report" | Arman wants: folder state in one sentence, named branches, one-line conflicts, paste-ready owner lines. |

## Trigger relocation

Triggers dropped from the description live here so a repo grep still finds them.

| Old / extra trigger | Home |
|---|---|
| "git disaster", "insane disaster", "merge review", "second product line" | Top, step 1 |
| `origin/main`, `git cherry`, patch-equivalent, `--merged` | Step 1, step 3 |
| dirty files, untracked, exists-and-differs, rewind | Step 2 |
| migrations already applied, ledger, collision, regression | Step 2 table |
| skills, docs, tests just go in | Step 2 table |
| stash, autostash, worktree remove hangs, hollow tree | Step 3 |
| blind writer, stale ancestor, cherry-pick stale local main, launchpad series | Step 3 |
| draft PR, failing CI, family inspection | Step 3 |
| 72 hours, ancient | Step 3 tail |
| leftover owner, which chat to message, Prompt A/B/C | Step 4, owners-and-prompts.md |
| reset shared checkout, restore named paths, guard refuses reset | Step 5 |
| db/generate.py, schema truth | Step 5 tail |
| release.sh halts, stale fingerprint, illegal halt | Step 6 |
| Size 2, stop the line | operations/scheduled-tasks/aidream-release-obstacles.md |
| integration every 30 minutes | operations/INTEGRATION_MAINTAINER.md |
| unmerged work intake, three rules | policies/shared-checkout.md |
