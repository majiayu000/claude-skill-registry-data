---
name: "bd-issue-pop"
description: "Pop a bead (epic) into a worktree branch, decompose it into child beads, then"
---

# bd-issue-pop command

Apply this command workflow. Treat any text after its invocation as the command input.

Pop a bead (epic) into a worktree branch, decompose it into child beads, then
hand off to `/do-work`. Mirrors the gh flow: this command sets up, `/do-work`
does the work, and its last pass merges the PR and closes the epic.

Two stores, and keeping them separate matters. The epic's **code** lands on the
one `bd-<id>-<slug>` branch and merges via its single PR. The **bead tracker**
lives in the shared main-repo database — worktrees reach it through a
`.beads/redirect` — and persists with `bd sync`. Bead status never rides the
code branch.

## Input

$ARGUMENTS

A bead ID. Without one, run `bd list` and ask which.

## Phase 0-2 -- Sync, fetch, gather context

```bash
gh repo view --json nameWithOwner -q .nameWithOwner   # <owner>/<repo>, for Phase 5
git pull && bd sync
git branch --show-current                             # must be main, not a worktree
bd show <id>
```

Stop if you are not on `main` in the main checkout, or if the bead is already
done. Show the bead's title and description.

Read `docs/VISION.yaml`, `docs/ARCHITECTURE.yaml`, `docs/road-map.yaml`,
`docs/constitutions/design.yaml` where they exist, plus the READMEs relevant to
the bead. Probe the build tool once — its output gates every later mage step,
and a repo without mage skips them silently:

```bash
mage -l 2>/dev/null || true
```

Run the consistency check if one exists (`mage audit`, or `mage analyze` where
it is named that way) and `mage stats` if present. Summarize the project state.

## Phase 3 -- Propose Breakdown

Decompose the bead into child beads — the beads-native equivalent of an epic's
sub-issues. For each child, specify:

- Title and type (documentation or code)
- Required Reading: mandatory list of files
- Files to Create/Modify: explicit file list
- Structure: Requirements, Design Decisions (optional), Acceptance Criteria
- `Estimated LOC` for code children
- Dependencies: which sibling children must finish first
- Code task sizing: 300-700 lines of production code, no more than 5 files per child

Present the children and their dependency ordering explicitly (a short list or
a small graph — "C depends on A, B") for approval. This is the single
interactive pause. Do not create any beads until the user agrees.

If the natural breakdown is a single unit of work, say so — no child beads are
created; the parent bead is worked directly (the single-unit path in Phase 4).

## Phase 4 -- Create the worktree and the bead graph

After approval, slug the title (kebab-case, ≤30 chars) and set up:

```bash
git checkout main
git fetch origin main
git merge --ff-only origin/main          # branch from current code, not a stale main
git worktree add --no-checkout ../bd-<id>-<slug> -b bd-<id>-<slug>
if [ -d .git/git-crypt ]; then ln -s ../../git-crypt .git/worktrees/bd-<id>-<slug>/git-crypt; fi
git -C ../bd-<id>-<slug> checkout        # the conditional serves git-crypt repos (the filter looks for the key in the worktree's own git dir); a no-op elsewhere
cd ../bd-<id>-<slug>
bd sync                                  # writes the worktree redirect, rebuilds from issues.jsonl
bd update <id> --status in_progress && bd sync
```

The fetch matters twice over here. `git worktree add` branches from whatever
`main` points at with no complaint about its age, and `bd sync` rebuilds the
bead graph from `issues.jsonl` — which lives on `main`, so a stale checkout
gives a stale graph as well as a stale base. `--ff-only` rather than `pull`: a
diverged `main` is a state to report, not one to resolve on the user's behalf.
Re-check the bead is still open here if the approval in Phase 3 took a while
(`bd show <id>`); the gh sibling learned that the hard way.

`bd sync` is what wires beads to the worktree: one database lives in the main
checkout, and the worktree reaches it through a local `.beads/redirect`. If
`bd` still cannot find it, write the relative path to the main repo's
`.beads/` into that file — it is gitignored, never commit it.

Every `bd` change is tracker state in the shared database. Persist with
`bd sync`, which writes and pushes `issues.jsonl`; never `git add .beads/` on
the code branch.

For a multi-child breakdown, create each child **labelled with the parent id**
— that label is what scopes `/do-work`'s ready queue to this epic — then wire
the dependency edges so the parent stays blocked until its children finish:

```bash
bd create "<child title>" --label <id>     # capture <child-id>
bd dep add <child-id> <prereq-child-id>    # one per prerequisite
bd dep add <id> <child-id>                 # parent depends on the child
bd sync
```

For a single-unit breakdown, create no children; `/do-work` works the parent
bead directly.

Commit the marker on the branch and push. The marker embeds the **epic
bead's body verbatim** (`bd show <id>`): the commit is where the planning
record survives when the history moves without its tracker. Copy the body
as written — do not summarize or trim it.

```bash
git commit --allow-empty -F - <<'EOF'
Pop <id>: <title> into worktree

## Epic <id>

<the epic bead's body, verbatim>

## Children

- <child-id>: <title>          # one line per child; omit the section when there are none

Bead: <id>
Skill: bd-issue-pop
Called-by: <invoking skill, or 'user'>
EOF
git push -u origin bd-<id>-<slug>
```

## Working the epic — run `/do-work` once

Popping built the worktree and the bead graph; `/do-work` does the work,
child after child without stopping between them, on the shared branch. It
detects beads mode, takes the
next child from the parent-scoped queue (`bd ready --label <id>`), implements
it under the real-work bar (no stubs), records `Actual LOC`, and closes it with
`bd update --status done`, which unblocks its dependents.

**Only ever implement beads belonging to this epic** — never one from another
epic that happens to be ready.

One worktree, one PR per epic. A child too big to finish gets split into
siblings under this epic in the same worktree; `/do-work` never pops again.
When the last child closes, `/do-work` runs Phase 5 automatically.

## Phase 5 -- Merge and Close the Epic

The last `/do-work` pass reaches this automatically after it closes the final
child. It opens the PR, merges it to `main`, closes the epic, and cleans up — no
manual step. (Verify first that every child is done and the work is real; do not
merge a stub branch.)

1. Close the epic in the tracker. All children are done, so its dependencies are
   satisfied. This is a tracker update in the shared database, persisted with
   `bd sync` — not a commit on the code branch (beads has no git auto-close, and
   the code PR carries only code):
   ```bash
   bd ready --label <id>   # this epic's children — none should remain
   bd update <id> --status done
   bd sync                 # writes and pushes issues.jsonl from the shared db
   ```

2. Open a pull request against `main` for the code:
   ```bash
   gh pr create --repo <owner>/<repo> \
     --base main \
     --head bd-<id>-<slug> \
     --title "bd-<id>: <title>" \
     --body "$(cat <<'EOF'
   ## Summary

   <2-3 sentence summary of what this delivered>

   ## Changes

   <bulleted list of what was produced>

   ## Test plan

   <if a consistency-check target is available:>
   - [ ] the consistency check (`mage audit` / `mage analyze`) passes
   - [ ] All tests pass
   - [ ] Documentation reviewed for consistency

   Bead: <id>
   Actual LOC: <n> (est <m>)
   EOF
   )"
   ```

3. Merge the pull request and delete the remote branch:
   ```bash
   gh pr merge --repo <owner>/<repo> --merge --delete-branch
   ```

4. From the main repo directory, pull the merged code and sync beads (the tracker
   already reflects the closed epic and children — `bd sync` reconciles it):
   ```bash
   cd -                    # back to the main repo checkout on `main`
   git pull origin main
   bd sync
   ```

5. Remove the worktree and delete the local branch:
   ```bash
   git worktree remove ../bd-<id>-<slug>
   git branch -d bd-<id>-<slug>
   ```

6. Report the PR URL, that it merged, and that the epic and its children are
   closed.

## Skill Tracing

Each skill records provenance as git trailers on the commits it authors:

- `bd-issue-pop` marker commits carry `Skill: bd-issue-pop`, `Called-by: user`, and `Bead: <epic-id>`, and embed the epic bead's body verbatim.
- `do-work` implementation commits carry `Skill: do-work`, `Called-by: bd-issue-pop`, `Bead: <child-id>`, and `Epic-Bead: <epic-id>`, and embed the child bead's Requirements, Acceptance Criteria, and Design Decisions.

The id trailers keep the trace resolvable against `issues.jsonl` even when
the history moves without its tracker database.
