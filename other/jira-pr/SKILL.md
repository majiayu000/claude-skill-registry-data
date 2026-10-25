---
name: jira-pr
description: After the user has verified a Jira ticket's branch, push it, open a GitHub PR against main, link the PR on the Jira ticket, and move the ticket to In Review.
argument-hint: <JIRA-KEY>
disable-model-invocation: true
---

# Raise PR for Jira ticket $ARGUMENTS

The user has verified the work and asked for the PR. Jira helper: `.claude/scripts/jira.sh`.

1. **Locate the branch.** KEY = first word of the arguments, uppercased. The current branch must contain KEY; otherwise find it with `git branch --list "*<KEY>*"` and ask before switching.
2. **Pre-flight.**
   - `git status --porcelain`: if there are uncommitted changes (e.g. fixes made during verification), show them and ask whether to commit them as `<KEY>: <message>`.
   - `git fetch origin` and check `git log --oneline HEAD..origin/main`. If main has moved, ask whether to rebase onto it; after a rebase, re-run the lint/type-checks for the parts touched.
   - If a PR already exists for the branch (`gh pr list --head <branch> --state all`), report it instead of creating another.
3. **Push:** `git push -u origin <branch>`.
4. **Create the PR** with `gh pr create --base main --head <branch>`:
   - Title: `<KEY>: <Jira summary>`
   - Body (pass via a heredoc):
     ```
     ## Jira
     [<KEY>](<jira url>) — <summary>

     ## Changes
     - server: …
     - client: …

     ## Acceptance criteria
     - [x] … (how it is met)

     ## How to test
     1. …

     ## Notes
     Assumptions / follow-ups (omit if none)

     🤖 Generated with [Claude Code](https://claude.com/claude-code)
     ```
   Build it from `.claude/scripts/jira.sh get <KEY>` and `git log main..HEAD` / `git diff main...HEAD`.
5. **Update Jira:**
   - `.claude/scripts/jira.sh comment <KEY> "Pull request raised: [<PR title>|<PR url>]"`
   - `.claude/scripts/jira.sh transition <KEY> review` — if the board has no review status, say so and leave it in progress.
6. Report the PR URL, the Jira status, and the next step: "After it is approved and merged, run `/jira-done <KEY>`."
