---
name: mission-control
description: Keep one local dashboard page of everything in flight across your repos (branches, PRs, CI, releases, what is blocked or due), built from git and GitHub, with what needs you at the top. Use when someone says "update the dashboard", "what's in flight", "what needs me", "where is feature X", "triage the backlog", "link this branch to the roadmap" or "research and plan this idea".
---

# mission-control

One page answers "what is in flight, and what needs me?" across every repo the user works in. **Git and GitHub are
the source of truth.** Where a piece of work is (local, in review, on main, released) is read from them, never typed.
The only thing a person or agent writes is the notes git cannot know: what the work is for, what is next, what
blocks it, when it is due.

**Answer first.** The page opens with one sentence on what needs the user, then the list of those items, then the
detail. The same goes for your replies: the answer, then the evidence.

## Words

Use only these for where work is: **feature** (one piece of work, named by its git branch; the same branch name in
several repos is one feature), **local** (commits only on this machine), **pushed** (on the remote, no PR),
**in review** (open PR), **on main** (merged, not in a release yet), **released** (in the newest release tag),
**planned** (notes only, no branch yet). Do not invent other stage names.

## Set up once

1. Ask the user which repos to include, or find them: the current repo, its siblings, and repos it names (a shared
   package, the website). Clone none; use the paths that exist.
2. Create the dashboard folder (default `~/.repo-dashboard`, or `$DASHBOARD_HOME`) with `config.json`:
   `{ "repos": ["/abs/path/a", "/abs/path/b"], "staleDays": 14, "releaseTag": "^v?\\d" }`. `releaseTag` is a regex
   for the tags that mark a release in these repos; check `git tag` and ask if the pattern is unclear.
3. Check `gh auth status`. Without the GitHub CLI the page still works from git alone, but has no PRs, CI or
   releases. Say so.

## Build the page

```bash
node <this skill>/scripts/build.mjs [--home ~/.repo-dashboard] [--fetch] [--days 14]
```

It writes `state.json` and `dashboard.html` in the dashboard folder and prints the headline. Read-only on every repo;
`--fetch` only runs `git fetch`. Run it at the start of a session and after any change you make. If the user wants it
kept fresh, offer a scheduled run (cron, launchd, or your agent's scheduler) and set it up only on a yes.

What it shows, in this order:
- **Headline:** how many things need the user, and the first one.
- **Repo tiles:** CI on the main branch, newest release and its age, commits on main not yet released, uncommitted
  files.
- **Needs you,** most urgent first: main is red, PR checks failing, changes requested, approved and green but not
  merged, past due, blocked, waiting for review two days or more, a due item with no branch doing it, unreleased
  commits older than `staleDays`, branches untouched for `staleDays`.
- **In flight:** one row per feature: title (from notes, else the branch), stage, repos with commits ahead and
  worktrees, PRs with their check and review state, next step and blockers, due date, last activity.
- **Shipped** in the last `--days` days, each PR marked on main, released, or merged into another branch.

**Where to put the page.** It is a local file that opens in any browser. If your agent can publish a private web page
(in Claude, an Artifact) and the user wants to see it away from this machine, publish it and update the same link
each run; otherwise give the file path.

## Rules

- A feature's notes file is `notes/<key>.json` in the dashboard folder, the branch name with every `/` as `__`
  (`feature/new-login` → `notes/feature__new-login.json`). Planned work with no branch uses `plan/<slug>`.
- Notes fields: `{ key, title, goal, next, blockers, due, target, work, by, at }`. `title` is what a user gets, in
  plain words, not the branch name. `goal` and `next` are one line each. `blockers` holds only real, current ones.
  `due` (`YYYY-MM-DD`) and `target` (a release name) only if known. `work` lists the branches doing a planned item.
  `by` names the agent and session; `at` is now in UTC ISO (`date -u +%Y-%m-%dT%H:%M:%SZ`).
- Write every file atomically: write `<file>.tmp` in the same folder, then `mv` it over the file. Keep every field
  you do not change. Never overwrite a field the user wrote by hand (`due`, `target`) unless they ask.
- Never put a key, token, password or message body in the folder.
- Never send a message, email, post, review or label for the user. Draft only; the user sends.

## "Update the dashboard" (end of a working session)

1. Find this session's feature: `git -C <repo> rev-parse --abbrev-ref HEAD`. If the session touched other repos or
   branches, each branch is its own feature (the same branch name across repos is one).
2. Read its notes file if it exists, and its entry in `state.json`.
3. Write the notes: fresh `title`, `goal`, `next`, `blockers` (remove resolved ones). If this branch does the work of
   a planned item (a `plan/<slug>` note, or another branch's note with a `due`), add this branch to that note's
   `work` instead of copying its dates here: one item, one note.
4. Rebuild the page and say in one line which notes you wrote and what the headline now says.

## "What's in flight?" / "What needs me?"

Rebuild (with `--fetch` if the last fetch is old), then answer from `state.json`: the headline, then the "needs you"
items as short lines with links, most urgent first. Do not list healthy work unless asked.

## Linking roadmap work

A planned item knows its work only through `work`. With none linked, the page says "no branch linked" and the item
looks at risk. For each planned or due item with an empty `work`, look for branches doing it, in flight or shipped in
the last six weeks: features in `state.json`, merged PR titles, `git log` on main of the repos it names. **Match on
what the change does, not on shared words:** "one price everywhere" is done by the PRs that set the price, not by
every pricing page edit. Add each branch to `work` and set `at`. When unsure, link nothing and say why. Never change
`due` or `target`.

## Matching fixes to bug reports

Open bug reports (GitHub issues, crash reports, store reviews, a `BACKLOG.md`) stay open until something says fixed.
Commits often fix them without naming the issue, so read the commits: per repo,
`git log origin/<main> --since=<14 days ago>` with full messages. A commit fixes a report only when its message names
that failure (the exception and class, the screen and fault) or its diff changes the code in the report's stack trace.
Similar names are not enough (`DidNotStartInTime` is not `DidNotStopInTime`). Check the commit is in a release
(`git merge-base --is-ancestor <sha> <tag>`). Record the match in `notes/links/<report id>.json`:
`{ state: "fixed", commits, release, why }`, `why` quoting what the commit fixed. When unsure, link nothing.

## "Triage the backlog"

Check backlog items against reality, so the user is never asked to fix something that is not real or not worth it.
Read-only on every repo. Items come from the repo's backlog file (`docs/BACKLOG.md`, `GAPS.md`, `TODO.md`; search for
it), open GitHub issues, or crash and review exports the user points to.

1. Pick the items that need a check: no triage file yet, or its item changed, or the check is over 7 days old. Skip
   items already linked as fixed. Never redo a check the user made by hand unless the item changed. At most 30 per
   run (or the number asked): highest priority first, then newest. For reports, most people affected first. Two
   reports of one problem (a review, an email and the crash behind them) get `same: <other id>`; check the one with
   most reach.
2. `git fetch -q` once per repo, then for each item:
   - **Premise first.** Many backlog entries are written by agents and rest on a "rule" (a constraint, a contract,
     a policy). Is that rule a real product decision? Look for it in the repo's agent instructions and docs, the
     notes, and what the product actually ships. An invented or unverifiable rule means `still: "not a defect"`, or
     `recommend: "ask"` if it needs the user's call. The user's earlier verdicts are product decisions: reuse them.
   - **Still real on main?** Read the code it names on the main branch (`git show origin/main:<file>`, `git log -S`,
     `gh pr list --search`). If a merged change fixed it, `still: "fixed"` with the PR or commit.
   - **Worth doing?** Who it hurts and how much: user reports, crash counts, ratings, how many people use that
     platform, whether it blocks a due item or revenue. The item's own priority is a hint, not a fact.
   - **Effort:** `S` (hours), `M` (a day or two), `L` (more).
3. Record the evidence kind: `users` only when a ticket, review, email or issue describes this exact problem (a vague
   complaint that might be related is not it); `testing` when someone saw it on a device or build; `code` when it rests
   on reading code (a hypothesis); `none` when it is not a problem claim. General numbers (a crash rate, a rating) are
   context, never evidence that this problem exists.
4. Write `notes/triage/<item id>.json` atomically: `{ still, recommend, why, evidence, seen, effort, by, at }`.
   `recommend` is `now` (seen by users or in testing and worth a lot, or worth some and effort S; never for `code` or
   `none`), `later`, `drop` (fixed, not a defect, or not worth it), or `ask` (needs a product decision). `why` is one
   plain sentence the user can act on; `evidence` names files, commits or PRs.
5. Say in one line: how many checked, and how many now, later, drop, ask.

## "Fix backlog item <id>"

1. Find the item and any link or triage file for it. Read what is wrong, the evidence, and what done looks like.
2. If a link names a branch, continue there; else make a new branch in the item's repo (follow the repo's own rules)
   and write the link at once (`state: "in progress"`, the branch).
3. Fix it with the repo's tests (see `bug-trap`). In the same PR, remove the item from the backlog file
   and put `Fixes <id>` (and `Fixes #<n>` for a GitHub issue) in the PR description.
4. Update the link with the PR, and `state: "fixed"` once it merges. Rebuild the page.

## "Research and plan the idea <title>"

The user has an idea for a feature. Research it and write a plan. Read-only on every repo: no branches, pushes or PRs.

1. Write `notes/plan__<slug>.json` with `status: "researching"`.
2. **How others do it:** the products the user names and the two or three closest competitors. Use web search, their
   docs, help pages and changelogs; note what works and what annoys people. Keep every URL you rely on.
3. **Where the project is:** on the main branch of each repo involved, find the screens, stores and services that
   would change and what they do today. Read each repo's agent instructions and the notes. Check premises as in
   triage.
4. Write the plan into the notes file, keeping every other field: `plan` (Markdown, under ~1,500 words), `sources`
   (the URLs), `status: "planned"`. Sections, in this order:
   - `## Summary`: what the user of the product gets, in two or three sentences.
   - `## How others do it`: one bullet per product, with a link.
   - `## Where we are`: what the product does today, naming files per repo.
   - `## Proposal`: the experience step by step as a user meets it; what is in the first version and what waits.
   - `## Work`: the pieces per repo, each small enough to be one PR, in order.
   - `## Questions`: the product decisions only the user can make. Do not guess them.
   - `## Risks`: data migration, sync, performance, briefly.
5. Rebuild the page. Say in one line where the plan is, and list the questions.

## "Pick up <feature or idea>"

1. Read its notes and its row in `state.json`. An idea with no `plan` gets "Research and plan" first; stop there for
   the user's answers.
2. For a planned idea the user approved: make the branch (`feature/<slug>`, the same name in every repo it touches),
   write notes under the branch key (carry `title`, `goal`, `due` over from the plan) and add the branch to the plan
   note's `work`.
3. Open each repo and worktree the feature lists. Check its PRs' state, CI and review comments (`gh pr view`,
   `gh pr checks`) and the branch's diff against main. If PRs need work, see `safe-to-merge`.
4. Work toward `next`. Clear blockers you resolve; add ones you hit. At the end, update the notes (`next`,
   `blockers`, `by`, `at`) and rebuild the page.

## "Handle this report"

A user report (an email, a chat thread, a store review, an issue) the user hands over.

1. Read the source read-only. Find the related feature, recent releases, any logs the user sent, and the code.
2. If it is a bug: find the cause, fix it on a new branch in the right repo and open a PR (follow the repo's rules).
   Note the branch as a feature with `goal` naming the report.
3. Draft a reply, never send it: a draft in the user's mail tool if one is connected, else the text (under ~600
   characters, plain) in your answer.
4. Say `fixed` only when the fix is in a published release; otherwise say which stage it is at.
