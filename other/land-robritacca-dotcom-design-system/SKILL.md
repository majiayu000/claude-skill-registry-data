---
name: land
description: Triage every piece of pending work in the repo and resolve all of it in one pass. Sweeps worktrees, local and remote branches, the working tree, and stashes; assesses each one as worth landing, worth keeping, or junk; then merges what lands into a local main, archives and deletes the junk, and verifies the combined result. Never pushes and never deploys. Use when asked to land the work, combine parallel sessions, clean up branches and worktrees, or work out what is worth shipping.
icon: flight_land
displayDescription: "Resolves every piece of pending work in the repo in one pass. Sweeps worktrees, branches, uncommitted changes and stashes, reads each one to judge whether it is finished, superseded or abandoned, and proposes a disposition for all of it at once: land, keep, or delete. Approved work merges into a local main one branch at a time and the combined result runs the full verify; anything deleted is archived to a recoverable tag first, and nothing is ever pushed."
invoke: ["land the work","combine my branches","clean up the branches","what's worth shipping"]
---

# land

Resolve **all** the pending work in the repo in one pass. Some of it is finished and should ship, some is half-built and should wait, some is stale and should go. `land` finds every piece, forms a view on each, gets one decision from Rob, and leaves the repo in the state that decision implies.

The end state: a local, unpushed `main` carrying the work that was worth keeping and passing `npm run verify`, with everything discarded archived to a recoverable tag and every branch and worktree that no longer earns its place gone.

One of the shipping verbs (CLAUDE.md's Shipping vocabulary owns the roster). `ship` makes one line of work live, `checkpoint` saves it, `park` shelves it; `land` is the one that runs when several of them have piled up and it is no longer obvious what is worth shipping.

## When invoked

Use this skill when pending work has accumulated and needs sorting out — phrases like "land the work", "combine my branches", "clean up the branches", "what's worth shipping". It is the right skill whether the work arrived from parallel sessions, from experiments that were parked and forgotten, or from a working tree that drifted.

**If asked to "merge and push"**: that's the retired ambiguous skill name, and it now maps onto more than one verb. Confirm the intended end state before doing anything: `ship` (merge into `main`, push, deploy), `checkpoint` (push the branch, keep working), or `land` (combine several pieces of pending work into a local `main`, pushing nothing).

**It never pushes and never deploys.** Landing is local, deliberately: a batch of accumulated work reaching robertritacca.com is a decision, not a side effect of tidying up. When `main` is landed and green, `ship` takes it live.

## Instructions

### 1. Establish the base

```bash
git branch --show-current
git rev-parse main
git fetch --prune
```

**Record the `main` SHA before anything moves.** It is the unwind handle for step 8, the diff anchor for step 7, and belongs in the final report; nothing else can restore a half-landed `main`.

Then check divergence with `git rev-list --left-right --count main...origin/main`. If `main` is behind, `git pull --ff-only`. If it has genuinely diverged, stop and report: something pushed elsewhere, and reconciling that is its own decision.

The primary checkout should be on `main`. Uncommitted changes there are **not** a blocker — they are a candidate like any other, handled in step 2. Do not bounce out to `checkpoint`.

### 2. Sweep every source of pending work

Five places work hides. Sweep all of them; a session that ended may have left any combination.

```bash
git status --short                          # the working tree
git worktree list --porcelain               # worktrees (exclude the primary checkout)
git worktree prune --dry-run -v             # registrations whose directory is gone
git branch --no-merged main                 # local branches carrying work
git branch -r --no-merged origin/main       # remote branches carrying work
git branch --merged main                    # merged leftovers: cleanup only, nothing to land
git stash list                              # forgotten stashes
git tag -l 'archive/*'                      # what past runs already archived
```

- **The working tree is a candidate.** Uncommitted changes usually contain more than one concern. Classify them into piles by what they belong to, not by file type, and treat each pile as its own candidate. This repo's generated files (see step 6) often span piles, because regenerating reflects everything in the tree at once.
- **Merged branches** carry nothing. They skip triage and go straight to disposal.
- **Stale worktree registrations** are normal, not a problem to investigate: agent worktrees auto-remove when they end unchanged.
- **Existing `archive/*` tags** are reported, not acted on. They are the recovery trail from earlier runs. Only propose pruning one when its work has demonstrably shipped by another route.

### 3. Read each candidate, then judge it

```bash
git log --oneline main..<branch>            # what it carries
git log -1 --format='%ci (%cr)' <branch>    # how old the tip is
git diff --stat main...<branch>             # how wide it reaches
git -C <worktree-path> status --short       # what is NOT in those commits
```

**Read the diff, never the branch name.** Agent branches are auto-named (`claude/musing-sanderson-5a94ee`) and say nothing about their contents. Even hand-named branches describe the intent at creation, not what survived.

Then test whether `main` has moved out from under it — the difference between *old* and *stale*:

```bash
git log --oneline main --not <branch> -- $(git diff --name-only main...<branch>)
```

Commits here are changes `main` made to the very files the candidate touches. A short list means the work still applies. A long list, or a rewrite of the same component, means the candidate is probably superseded and its conflicts are not worth resolving.

Form an actual view on each candidate, and say it plainly in step 5:

- **Finished** — coherent, complete, matches current conventions. A landing candidate.
- **Unfinished** — mid-build, or its own notes record it as still being tuned. Keep, do not land.
- **Superseded** — `main` solved this another way, or rewrote underneath it. Delete.
- **Abandoned** — old, narrow, and nothing since referenced it. Delete.

**The dirty-worktree rule.** Uncommitted changes in a worktree are not on its branch, so merging the branch silently drops them and removing the worktree destroys them. Treat any dirty worktree as a session possibly still in flight: name every uncommitted file, and never land or remove it on an assumption. Committing another session's half-finished work is not this skill's call.

Do not run `npm install` in a worktree, and do not lint one with no `node_modules`. A fresh worktree has none, installing root plus the website workspace in each is slow, and step 8's combined `npm run verify` carries the real signal.

### 4. Predict the collisions

For every landing candidate, before anything moves and without touching the working tree:

```bash
git merge-tree --write-tree --name-only main <branch>
```

Exit 0 is clean; exit 1 conflicts. On a conflict the first output line is the merged tree's object id, not a path — conflicted paths are the lines after it, up to the blank line. Read the exit status directly and **never pipe this through `head`**, for the same reason `verify` is never piped: the pipeline reports the wrong command's status.

Two honesties for the report: predictions are against **today's** `main`, so once one branch lands the rest are provisional and get re-predicted before each merge; and two branches that each merge cleanly can still conflict with each other.

### 5. Propose a disposition for everything, then confirm once

Present **one table covering every candidate**, with a proposed disposition and the reason for it:

| Candidate | Kind | Age | Carries | Conflicts | Proposed | Why |
|---|---|---|---|---|---|---|

Dispositions are exactly three:

- **Land** — merge into `main` in this run
- **Keep** — leave exactly as it is, changing nothing
- **Delete** — archive to a tag, then remove the branch and worktree

Follow the table with a short plain-English reading of anything non-obvious, especially every **Delete** proposal. A delete needs a stated reason, not just an age.

**Confirming at scale.** The candidate count is unbounded, and `AskUserQuestion` caps at four options, so never ask per candidate. Ask **one** question about the triage as a whole, with options along the lines of: accept as proposed; accept the landings but keep everything marked delete; land nothing and only dispose; stop and change nothing. Rob names exceptions in free text ("delete these 4", "keep cosmic-wind"). Apply any exceptions, re-present the amended table in two or three lines, and proceed without asking a second full question.

The default is that **nothing lands and nothing is deleted until it is named**. Silence is not approval.

If predicted conflicts make the order matter, recommend one: fewest conflicts first, so the hardest merge happens against the most complete `main` and gets resolved once.

**Mixed candidates.** When a branch is partly worth landing, offer to land a subset by `git cherry-pick <sha>` rather than forcing all-or-nothing, and archive the full branch before deleting the remainder. This is the one place cherry-picking is sanctioned; `ship` bans it because there it means dodging a merge, which is a different act from deliberately selecting commits.

### 6. Land what lands

One branch at a time, each as its own merge:

```bash
git merge <branch>
```

**Never octopus-merge** (`git merge a b c`): it refuses outright on any conflict and leaves history that cannot be bisected. Never rebase another session's branch. Never force anything.

Uncommitted piles that were approved for landing get committed on `main` in the repo's conventional style (`feat(scope):`, `fix(scope):`, `chore(scope):`), one commit per concern, with a 1–3 sentence body explaining the why. **Never `git add -A`, `git add .`, or `git add` on a directory** — always explicit paths. When piles must be committed separately but share generated output, stash the other pile by pathspec, regenerate, commit, restore, regenerate, commit — so each commit carries a generated state that matches its own sources.

**Conflict policy** — three cases resolve mechanically, one never does:

- **Generated surfaces** (everything the generator scripts at the front of the `validate-registry` entry rewrite — the corpus, skills content and component-API files under `website/src/data/`, the barrels, the token registry, the marked regions of `README.md`, the generated trees under `website/public` — the blueprint copies, the per-component `components/*.md` pages, and the consumer agent skill under `skill/robr0-design-system/`): never hand-merge. Take either side to get a resolvable tree, run `npm run validate-registry` to rebuild them from the merged sources, and commit the result. The generator scripts at the front of the `validate-registry` entry in the root `package.json` are the authoritative list of what gets rewritten. A hand-merged generated file is wrong even when it looks right, and CI's drift guard catches it later at a worse moment.
- **Registry entries that are lists** (the Registries table in `CLAUDE.md` is the authoritative roster; the list-shaped ones are those holding an array or keyed map of entries — as opposed to the generated surfaces above and the single-tuned-state case below; a keyed map has no ordering, so the ordering half below does not apply to it): two branches each adding an entry is a textual conflict, not a semantic one. Keep both, then restore the ordering the registry requires (components alphabetical by `name`; skills and case studies in their curated order). Dropping one side is a silent feature loss no validator can see — or, for the cover registries and the page summaries, a build failure on whichever branch's entry was dropped, since those are held to their parents in both directions.
- **Registries that are a single tuned state**, not a list — `website/src/data/shader-background.json` is the current example: keeping both sides is meaningless and actively breaks things. Its `blobs` array is a fixed-size set the shader's `BLOB_COUNT` must match, and its `params` are one coherent look, so a merged pair fails `validate-shader-background.mjs` or produces a design nobody chose. Treat two sessions retuning the background as a semantic conflict and use the stop-and-ask rule below.
- **Version bumps**: keep the single higher version. This repo publishes no package, so a version is only ever the app manifest's own.
- **Source, CSS, and prose conflicts**: stop and ask. A semantic conflict between two sessions' intentions is not resolvable from inside a batch cleanup.

### 7. Check the prose the landed work invalidated

Landed work can make a sentence elsewhere in the repo false, and no validator can see it. This runs before the verify so its fixes are covered by the same green run.

`land` has an exact anchor for the scope, which `ship`'s equivalent check does not — it works from "this session's diff", while here everything landed in this run is one range:

```bash
git diff --name-only <pre-land-sha>..main
```

From that diff, take the identifiers it touched — component and prop names, script names, token names, moved or deleted paths, and any rule the work made stricter — and grep the prose surfaces for them: `.claude/skills/`, `README.md`, and every root spec (the doc list in `scripts/validate-doc-refs.mjs` is the authoritative set). Then judge whether any claim just became false.

Two classes matter most, because both actively mislead:

- **An instruction that now contradicts the build.** The worked example: a page moved from a curated subset to full coverage with a validator enforcing it, while `CLAUDE.md` still told the next agent that skipping an entry was fine. Following the doc would have produced a build failure the doc called acceptable. Whenever landed work makes a rule *stricter*, the instructions that describe the old latitude are the first place to look.
- **A false claim in `README.md`**, which ships inside the npm tarball and so reaches every consumer.

Fix what drifted, in this run, as its own `docs(...)` commit. Any prose the landing itself wrote follows `content-design.md`. `scripts/validate-doc-refs.mjs` catches dead references mechanically, but only a reader catches a sentence that is now wrong.

### 8. Verify the combined result

```bash
npm run verify
```

Run it plainly and let its exit status be the verdict. **Never pipe it through `tail`, `head`, or `grep`** — a pipeline reports the last command's exit code, not verify's. This is the step the skill is built around: each candidate may have been green alone, and only the combined result is what would ship. Run it even when nothing merged, if anything at all was committed to `main`.

**If verify fails**: nothing is pushed, so nothing is broken in public. Identify the merge or commit that introduced it, report it, and offer to unwind to the SHA from step 1 with `git reset --hard <pre-land-sha>`. That is destructive, so it is offered and confirmed, never automatic. **Dispose of nothing while verify is red** — an unwound merge needs its branch and worktree to still exist.

### 9. Dispose of the junk

**Archive before deleting. Always, without being asked.**

```bash
git tag archive/<short-name> <branch>
```

A tag keeps the commit reachable permanently, costs nothing, never appears in `git branch`, and is not pushed unless someone asks. It is what makes deleting unmerged work a reversible act, and it is the difference between a cleanup and a loss. Name tags for the work, not the branch (`archive/cosmic-wind`, not `archive/claude-musing-sanderson`). Do this for every candidate marked **Delete**, including remote-only ones, before a single deletion runs.

Then:

```bash
git worktree remove <worktree-path>
git branch -d <branch>                      # merged branches
git branch -D <branch>                      # unmerged, only once archived and approved
git push origin --delete <branch>
git worktree prune
```

- `git worktree remove` **never** takes `--force`. If it refuses, the worktree is dirty: return to step 3's rule and ask. Note that the permission classifier may block a force-removal anyway, so a dirty worktree that must go is finished by Rob in his own terminal, not retried here.
- `git branch -D` is sanctioned **only** for a candidate that was archived in this step and explicitly approved for deletion. Everywhere else, `-d`, and its refusal is the safety net.
- Deleting a remote branch is the one outward-facing action in this skill. It removes work from GitHub, so it runs only against an approved, archived candidate, and every deletion is named in the report.

For every candidate marked **Keep**: change nothing. No commits, no deletions, no tidying of stray files. Name each in the report with its branch and worktree path so it stays a resume handle.

### 10. Report

- **Landed**: each branch or pile, its merge or commit, and a one-line summary of what it carried
- **Kept**: each one, why, and its resume handle
- **Deleted**: each one, its `archive/*` tag, and the recovery line — `git checkout -b <name> archive/<tag>`
- Conflicts resolved, how, and which were regeneration rather than a judgement call
- Prose the landed work invalidated, and the fix — or explicitly that nothing drifted
- The `npm run verify` result and the pre-land SHA as the unwind handle
- Branches and worktrees removed, local and remote
- Closing line: `main` carries unpushed commits and nothing deployed. Say `ship` to take it live, or leave it local.

## Guardrails

- **Never push, ever** — not `main`, not a branch. This skill ends local. Deploying is `ship`, always a separate ask
- **Never delete anything that was not archived first.** No `-D`, no remote deletion, no worktree removal without a tag already written
- Never remove a worktree with uncommitted changes, and never reach for `--force`, `git reset --hard`, or `git checkout -f` inside a worktree this session did not create. Those changes are the only copy, and another session may still be writing them
- Never land, commit, or delete anything not explicitly approved, and never read "clean up" as blanket permission to delete
- Never commit another session's uncommitted work to make a merge clean. Report it and stop
- Never hand-merge a generated file; never drop one side of a registry conflict; never resolve a source conflict silently
- Never commit `ga-analysis/output/`, `ga-analysis/service-account.json`, `.env*`, or anything credential-shaped, however it arrived in a merge
- If there are no candidates, say so and stop. A clean sweep is a valid outcome
