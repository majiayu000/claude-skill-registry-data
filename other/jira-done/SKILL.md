---
name: jira-done
description: Close out a Jira ticket after its PR is merged - confirm the merge, move the ticket to Done with a closing comment, and clean up the local branch.
argument-hint: <JIRA-KEY>
disable-model-invocation: true
---

# Close Jira ticket $ARGUMENTS

Jira helper: `.claude/scripts/jira.sh`. KEY = first word of the arguments, uppercased.

1. **Find the PR:** `gh pr list --state all --search "<KEY> in:title" --json number,title,state,url,mergedAt,headRefName`.
2. **Require a merge.** If the PR is not `MERGED`, report its state (open / review status / checks via `gh pr view <n> --json reviewDecision,statusCheckRollup`) and stop — do not move the ticket to Done. Only proceed on an unmerged PR if the user explicitly says to.
3. **Update Jira:**
   - `.claude/scripts/jira.sh comment <KEY> "Merged to main in [PR #<n>|<url>] on <date>."`
   - `.claude/scripts/jira.sh transition <KEY> done`. If no direct transition exists, list the available ones and step through intermediate statuses only if the path to Done is obvious; otherwise ask.
4. **Tidy up locally:** `git fetch origin --prune`, `git switch main`, `git pull --ff-only`. Delete the local branch with `git branch -d <branch>` (lowercase `-d` only; if it refuses because of a squash merge, confirm the PR is merged and ask before using `-D`).
5. Report: ticket now Done (with link), PR link, branch cleaned up.
