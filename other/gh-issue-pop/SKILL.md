---
name: "gh-issue-pop"
description: "Pop a GitHub issue, decompose it into sub-issues on a worktree branch, and open"
---

# gh-issue-pop command

Apply this command workflow. Treat any text after its invocation as the command input.

Pop a GitHub issue, decompose it into sub-issues on a worktree branch, and open
a PR when they are all closed. Sub-issue progress shows on the parent issue
page.

## Input

$ARGUMENTS

An issue number (`42`, `#42`) or a URL. With neither, list open issues and ask
which.

## Phase 0-2 -- Fetch and gather context

```bash
gh repo view --json nameWithOwner -q .nameWithOwner        # <owner>/<repo> for everything below
gh issue view <number> --repo <owner>/<repo> --json number,title,body,labels,state
```

Stop and report if the issue is not open. Show its title, body, and labels.

Read `docs/VISION.yaml`, `docs/ARCHITECTURE.yaml`, `docs/road-map.yaml`,
`docs/constitutions/design.yaml`, and the READMEs relevant to the issue. List
any sub-issues already attached — this may be a resumed session.

Probe the build tool once; its output gates every later mage step, and a repo
without mage skips them silently:

```bash
mage -l 2>/dev/null || true
```

Run the consistency check if one exists (`mage audit`, or `mage analyze` where
it is named that way) and `mage stats` if present. Summarize the project state.

### Operational-issue detection

If the issue is a release rather than a code/doc change — the title starts with
`Recurring: Run release push`, or the body contains a `## Release Workflow`
section or a `mage tag` release recipe — do **not** create a worktree or
sub-issues. Instead run `/gh-release-push` on `main` (it requires `main` and
produces no branch or PR). After the release completes, handle recurrence
(Phase 6) and close the issue. Skip Phases 3–5 entirely.

## Phase 3 -- Propose sub-issues

Decompose the epic into units, each with: type (documentation or code),
Required Reading, Files to Create/Modify, Requirements, Acceptance Criteria,
and Design Decisions where they matter. Size code units at 300-700 production
lines across no more than 5 files. No more than 10 sub-issues.

Present the breakdown and **create nothing until the user agrees**.

If the natural breakdown is a single unit, say so — "this fits in one task, so
I will work the parent issue directly" — and take the single-issue path in
Phase 4.

## Phase 4 -- Create Worktree and Sub-Issues

After user approval:

1. Ensure the main repo is on `main` and level with the remote (the worktree
   keeps main untouched):

   ```bash
   git checkout main
   git fetch origin main
   git merge --ff-only origin/main
   ```

   The fetch is not optional. `git worktree add` branches from whatever `main`
   points at and says nothing about how old that is, so a repository that has
   not pulled since someone else merged produces a branch built on stale code.
   `--ff-only` rather than `pull`: a diverged `main` is a state to report, not
   one to resolve by merging on the user's behalf.

2. Re-read the issue, immediately before branching:

   ```bash
   gh issue view <number> --repo <owner>/<repo> \
     --json state,closedByPullRequestsReferences \
     --jq '"\(.state) closed-by: \([.closedByPullRequestsReferences[]?.number] | join(", "))"'
   ```

   Stop if it is no longer open, and name the PR that closed it — the operator
   needs to see what already landed, not just that the pop failed. Phase 0-2
   checked this too, and that check is not sufficient: Phase 3 waits for a
   human to approve the breakdown, and the issue can close in that window.
   Not hypothetical — a pop of `writing-skills` GH-28 read `OPEN` about a
   minute after a PR merged and closed it, then rebuilt the entire fix on a
   stale base. Nothing caught it until Phase 5.

3. Create a git worktree with a new branch:

   ```bash
   git worktree add --no-checkout ../gh-<number>-<slug> -b gh-<number>-<slug>
   if [ -d .git/git-crypt ]; then ln -s ../../git-crypt .git/worktrees/gh-<number>-<slug>/git-crypt; fi
   git -C ../gh-<number>-<slug> checkout
   ```

   The conditional serves git-crypt repositories, where a plain
   `git worktree add` dies in the smudge filter: the key lives in the shared
   git dir and the filter looks in the worktree's own. In an unenrolled
   repository it is a no-op and the sequence equals plain `git worktree add`.

   The worktree lives at `../gh-<number>-<slug>` (sibling of the current repo directory).
   All subsequent work happens inside this worktree. Record the path: `WT=../gh-<number>-<slug>`

### Create the sub-issues and the marker

With 2+ sub-issues, create each one (`gh issue create` with its Required
Reading, Files to Create/Modify, Requirements, Acceptance Criteria), then link
it to the parent so the progress checklist appears:

```bash
gh api repos/<owner>/<repo>/issues/<parent-number>/sub_issues \
  --method POST --field sub_issue_id=$(gh api repos/<owner>/<repo>/issues/<sub-number> --jq '.id')
```

With exactly one, skip sub-issue creation and claim the parent instead:
`gh issue edit <number> --repo <owner>/<repo> --add-assignee @me`.

Either way, commit the marker and push. The marker embeds the **epic issue
body verbatim**: issues do not follow a repository across an org migration,
so the commit is where the planning record survives. Copy the body as
written — do not summarize or trim it. `Issue-URL:` is the full URL, not
`#N`; after a migration the number no longer resolves, the URL still names
the source.

```bash
cd ../gh-<number>-<slug>
git commit --allow-empty -F - <<'EOF'
Pop GH-<number>: <title> into worktree

## Epic GH-<number>

<the epic issue body, verbatim>

## Sub-issues

- #<n>: <title>          # one line per sub-issue; omit the section on the single-issue path

Issue-URL: https://github.com/<owner>/<repo>/issues/<number>
Skill: gh-issue-pop
Called-by: <invoking skill, or 'user' if run directly>
EOF
git push -u origin gh-<number>-<slug>
```

Report the parent issue URL, and the sub-issue URLs if there are any.

### Epics and further breakdown

After `gh-issue-pop`, run `/do-work` once — it works the sub-issues one after another without stopping between them, and when the last one closes, Phase 5 opens the PR. Decomposition is one level deep and one worktree per epic.

`/do-work` routes each sub-issue by deliverable: documentation, prose, or code. A sub-issue whose output is prose a person reads — a paper section, a README, a post — takes the Prose workflow, which learns the repository's voice from `writing-voice/` before drafting and scans the result with filter-tells. Nothing changes in a repository without that directory.

If, while running `/do-work`, a sub-issue turns out too big to finish in one pass, do not pop again — nested worktrees are not supported. Split that sub-issue into smaller **sibling** sub-issues under the same epic with `/gh-issue-push`, work them in the same worktree, and let the epic's single PR close them all. `gh-issue-pop` is only ever run from `main`, never from inside a worktree.

## Phase 4b -- Generator mode (alternative)

**Gated on the cobbler orchestrator.** If the Phase 2 probe did not list
`generator:start`, skip this section and do not mention it.

Use it instead of Phase 4 only when the user asks for autonomous execution
("use generator mode", `--generator`). It drives `mage generator:start/run`
instead of hand-creating sub-issues: Claude proposes tasks via
`cobbler:measure` and executes them via `cobbler:stitch`. The interactive path
is the default, and it trades review-before-execution for review-after.

First confirm in `configuration.yaml` that `cobbler.issues_repo` matches this
repo, that `claude.args` carries the required flags, and — for library repos
whose Go source must survive — that `generation.preserve_sources` is true.
Check the Claude credentials file exists.

```bash
git checkout main
git fetch origin main && git merge --ff-only origin/main   # as in Phase 4: never generate onto a stale main
COBBLER_GEN_NAME=gh-<number>-<slug> mage generator:start   # creates generation-gh-<number>-<slug>
mage generator:run                                         # measure+stitch until no open issues
mage generator:resume                                      # after an interruption
```

When `generator:run` reports no open issues, the generation branch holds the
work: run Phase 5 against it, substituting the generation branch name for
`gh-<number>-<slug>`.

## Phase 5 -- Open a Pull Request

Trigger when the work is complete: on the single-issue path, when the parent's
work is done; on the multi-sub-issue path, when every sub-issue is closed.

1. **If the issue is recurring** (see Phase 6), do Phase 6 now — before merging
   — so the next instance exists before this one closes.

2. **Verify the units are actually done.** Multi-sub-issue path:

   ```bash
   gh api repos/<owner>/<repo>/issues/<number>/sub_issues \
     --jq '[.[] | {number, title, state}]'
   ```

   A sub-issue is not done until it has both a completion comment and an
   `Actual LOC:` line stated against its `Estimated LOC`. If any lacks either,
   stop and report which. Single-issue path: write that comment on the parent
   now.

3. **Push, then open the PR** against `main`, titled `GH-<number>: <title>`,
   with sections: Summary (2-3 sentences), Changes, Stats (`mage stats` deltas
   where that target exists, otherwise the diff, plus Estimated vs Actual LOC),
   and Test plan (consistency check, tests, docs — where those exist). End with one `Closes #N` line per issue: the parent
   and every sub-issue.

   Those `Closes` lines are what auto-close the issues at merge. Sub-issue
   commits carry their own as a redundant safeguard.

4. **Merge and clean up:**

   ```bash
   gh pr merge --repo <owner>/<repo> <pr-number> --merge --delete-branch
   git pull origin main            # from the main checkout, already on main
   git worktree remove ../gh-<number>-<slug>
   git branch -d gh-<number>-<slug>
   ```

5. **Verify every issue actually closed** — the parent and each sub-issue.
   GitHub's auto-close is not guaranteed:

   ```bash
   gh api repos/<owner>/<repo>/issues/<number>/sub_issues \
     --jq '[.[] | select(.state=="open") | {number, title}]'
   ```

   Anything still open, warn the user and close it explicitly with
   `gh issue close <N> --comment "Completed via PR #<pr>. Auto-close did not trigger."`

6. **Close a drained tech-debt epic.** `do-work` files out-of-scope follow-ups
   under an open epic labeled `tech-debt` and creates that epic when none is
   open, but nothing closes it again. An epic whose last sub-issue just closed
   is finished work that still reads as outstanding in `gh issue list`, so
   close it here rather than leaving it for the operator to notice:

   ```bash
   parent=$(gh api repos/<owner>/<repo>/issues/<number> \
     --jq '.parent_issue_url // empty' | grep -oE '[0-9]+$')
   [ -n "$parent" ] && gh api repos/<owner>/<repo>/issues/"$parent" --jq '
     select(.state == "open")
     | select([.labels[].name] | index("tech-debt"))
     | select(.sub_issues_summary.total > 0
              and .sub_issues_summary.completed == .sub_issues_summary.total)
     | .number'
   ```

   A number means the epic drained: close it with
   `gh issue close "$parent" --comment "Drained: every sub-issue closed. Re-create a tech-debt epic when the next follow-up needs a home."`
   No output means the issue had no parent, the parent is not a tech-debt
   epic, or sub-issues remain open — leave it alone. An epic with no
   sub-issues at all has not drained and stays open.

7. Report the PR URL and confirm all issues are closed.

**Note:** Phase 5 may happen in a later session. When running `/do-work` and closing the last sub-issue, check the open sub-issue count and execute Phase 5 automatically if it reaches 0.

## Phase 6 -- Re-create Recurring Issues

A GitHub issue is recurring if its title starts with "Recurring:" or its body contains a "## Recurrence" section. After Phase 5 closes a recurring issue, re-create it so the next run can pick it up.

1. Detect recurrence: check whether the original issue title starts with `Recurring:` or the body contains `## Recurrence`.

2. If recurring, create a new issue with the same title, labels, and body as the original, except update the "Previous Runs" or "Previous Audits" section to append a line referencing the just-closed issue:
   ```
   - #<number> (<date>): <one-line summary of what this run produced>. PR #<pr-number>.
   ```

3. Create the new issue:
   ```bash
   gh issue create --repo <owner>/<repo> \
     --title "<same title>" \
     --label "<same labels, comma-separated>" \
     --body "<updated body>"
   ```

4. Report the new issue URL so the user knows the recurring issue is ready for the next run.

## Skill Tracing

Each skill records provenance as git trailers on the commits it authors, so `git log` reconstructs which skills ran and which called which — no separate log file.

- `gh-issue-pop` marker commits carry `Skill: gh-issue-pop`, `Called-by: <invoking skill, or 'user'>`, and `Issue-URL: <full epic URL>`, and embed the epic issue body verbatim.
- `do-work` implementation commits carry `Skill: do-work`, `Called-by: gh-issue-pop`, `Issue-URL: <full sub-issue URL>`, and `Epic-URL: <full parent URL>`, and embed the sub-issue's Requirements, Acceptance Criteria, and Design Decisions.

The URL trailers are what keep the trace resolvable after a repository
migrates to another org: issue numbers stay behind, full URLs still name the
source.

View the roster and the call graph:

```bash
# per-commit: which skill produced it
git log --pretty='%h %s [%(trailers:key=Skill,valueonly,separator=%x20)]'

# call graph: caller -> skill, with counts
git log --format='%(trailers:key=Called-by,valueonly,separator=%x20) -> %(trailers:key=Skill,valueonly,separator=%x20)' \
  | grep -vE '^ *-> *$' | sort | uniq -c | sort -rn
```

Limitation: `make-work` and `gh-issue-push` make no commits, so they do not appear in commit-trailer traces. Capturing them needs a provenance line on the issues they create (follow-up).
