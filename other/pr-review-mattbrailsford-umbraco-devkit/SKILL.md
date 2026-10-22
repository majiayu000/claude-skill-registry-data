---
name: pr-review
description: >-
  Reviews a pull request from outside the core team on an open-source Umbraco package: runs
  the `reviewer` agent, then checks what's unsafe to build locally, security, contribution
  rules, docs, and whether the diff does what it claims. Drafts the review for approval;
  never posts or merges on its own. Use for community PRs. For your own task's diff, use
  `reviewer` through `feature-build` or `quick-fix`.
user-invocable: true
argument-hint: <PR number or URL>
---

# Review a contribution

For a pull request filed against an Umbraco package's public repo by someone outside the core
maintainer team. Most packages in this space are open source, so this is a steady trickle, not
an edge case. The diff didn't come from your own `builder`/plan-folder pipeline, so three
things are different from a normal in-house review: you don't know the author's intent beyond
what the PR says, you haven't vetted the code that's about to run on your machine, and the
trust bar for "does this quietly break something" needs to sit higher by default.

This skill doesn't replace `reviewer` — it wraps it. `reviewer` already carries the
Umbraco-aware checklist that matters most here: public API impact, a renamed manifest `alias`,
multi-version/provider parity, layering, and the security skills. This skill adds the handful
of checks that only exist *because* the diff came from outside.

## Scope

- IN: a PR on a package's public repo, opened by someone who isn't a core maintainer. Fetching
  it, reviewing it, drafting a review comment.
- OUT: a `feature-build` task's own diff (dispatch `reviewer` directly — that's what
  `feature-build`/`quick-fix` already do); merging, approving, or requesting changes without
  you confirming the drafted comment first; fixing the contribution yourself (if it's close
  but needs a small push, say so in the comment and let the contributor or a maintainer decide
  who pushes it).

## Argument

`$ARGUMENTS` is a PR number or URL. If empty, ask which PR.

## Workflow

1. **Fetch the PR, don't run anything yet.**
   `gh pr view <number> --json title,body,author,baseRefName,headRefName,additions,deletions,files`
   and `gh pr diff <number>`. Read the diff before touching your working tree.

2. **Scan for anything that would execute on your machine before you build or test.** A
   malicious or careless PR can put code where CI, a build, or a package restore will run it
   automatically. Flag any of these as `Critical` and read them by hand before continuing:
   a changed `.github/workflows/*`, a build script (`.ps1`, `.sh`, `csproj`/`build.cake`
   targets), `NuGet.config` (a changed package source can redirect where packages come from),
   a new or changed `npm`/`package.json` `scripts` entry (`postinstall` runs unattended), or
   any new binary/executable file. None of these block the review outright, but don't run
   `dotnet build`/`npm install` against the PR branch until you've read what they'd execute.

3. **Check out the branch.** `git status` first (per this project's own safety rules — don't
   discard uncommitted work). Then `gh pr checkout <number>`.

4. **Treat the PR's own description as its task.** There's no `PLAN.md` task text for an
   outside contribution — the PR title/body (and the issue it links, if any) is the closest
   equivalent. Read it before judging the diff: `reviewer` needs a task to judge scope against
   in its own step 8, and "what the PR says it does" is that task here.

5. **Dispatch `reviewer`** (Agent tool, `subagent_type: reviewer`), passing the PR's stated
   intent as the task. With the PR branch already checked out, its own step 1 (`git diff`
   against the base branch) finds the same diff you just scanned. Let it run its full
   workflow — build, test, docs/sibling comparison, consumer-impact, entry-point trace, ghost
   code, multi-version/provider parity, verdict.

6. **Add the checks `reviewer` doesn't know to make for outside code:**
   - **The security skill runs unconditionally.** `reviewer` only reaches for
     `umbraco-security` when the diff visibly touches auth, user input, the Management API,
     or secrets. For a PR from outside the team, load `umbraco-security` yourself regardless
     of what the diff looks like it touches, and whether or not `reviewer` ran. A security
     pass from memory doesn't replace it: the skill holds the Umbraco-specific checks you
     won't think of unprompted. An external diff is a new trust boundary, and "doesn't look
     security-relevant" is exactly the blind spot a deliberately disguised change would aim
     for.
   - **Contribution hygiene.** If the repo has a `CONTRIBUTING.md`, check the PR follows it:
     target branch, commit/PR conventions, sign-off trailer (DCO/CLA) if the repo requires
     one, tests included for new behavior.
   - **Docs flag, no assumed location.** If the diff adds or changes a public feature, flag
     that it probably needs a docs update — but don't assume where. Only Umbraco HQ-owned
     packages keep docs in the UmbracoDocs repo; everyone else keeps docs in their own repo, a
     separate site, or nowhere formal. Say "this looks like it needs a docs update, check
     wherever this project keeps its docs" and leave it there.
   - **Intent match.** Compare the diff against the PR's own stated purpose (and linked issue,
     if any). Flag anything beyond it — an unrelated reformat, a drive-by refactor of a file
     the stated fix never needed to touch — as a `Suggestion` if small and harmless, `Important`
     if it changes behavior outside the stated scope. This isn't `reviewer`'s own scope check
     (step 8 in its workflow), which judges against a plan-folder task; here there is no plan,
     so the PR's own description is the only scope boundary there is.

7. **Check every finding before it reaches the contributor.** A wrong finding on an outside
   PR costs the contributor a round trip and makes the next finding easier to ignore. Do
   this on every PR, however small, and don't check the findings yourself instead: you
   collected them, so you're the wrong one to doubt them. Dispatch one fresh general-purpose
   subagent (Agent tool) on the checked-out branch with every finding from steps 5 and 6.
   Tell it to try to disprove each one by reading the code around the cited file:line and
   beyond the diff: a guard in a base class, attribute or caller, a handler elsewhere that
   already covers it, an API that doesn't behave the way the finding assumes. It returns
   each finding as confirmed, refuted, or unsure, with the evidence. Drop refuted ones, and
   turn unsure ones into a question for the contributor instead of a demand. List what was
   dropped, and why, for the user under the draft, not in it.

8. **Draft the review, don't post it yet.** Combine `reviewer`'s verdict and the findings
   that survived step 7 into one comment. Before the first finding, give one line with the
   verdict and the count per tier, such as `Changes needed: 1 Important, 2 Suggestions`;
   with nothing to fix, say so in those words. Then the findings, grouped the same way
   `reviewer` tiers them (Critical / Important / Suggestion / Pre-existing). Pre-existing
   ones are for the maintainer, so say plainly the contributor doesn't need to fix them.
   Write it following `plain-writing` — a contributor who doesn't know this codebase needs to be able to act on
   it. Say what's blocking and what's a nice-to-have; don't bury a `Critical` finding in a
   wall of Suggestions.

9. **Show the draft and ask before posting.** A PR comment on a public repo is visible to the
   contributor and anyone else watching the repo — confirm with the user first, every time.
   Once confirmed, post with `gh pr review <number> --comment --body-file <path>` for a plain
   comment, or `--request-changes`/`--approve` instead of `--comment` only if the user
   explicitly wants the review state set, not just a comment left. Never pass `--approve`
   without the user having said so. Same sanity rules as `git-workflow`: never `--no-verify`,
   never force-push, re-check the diff for secrets before anything is staged locally.

## Hand off

One line: the PR, the verdict (`reviewer`'s tier plus anything step 6 added), and whether the
comment was posted or is still waiting on confirmation.
