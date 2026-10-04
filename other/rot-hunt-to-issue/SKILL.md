---
name: rot-hunt-to-issue
description: Run a rot hunt and land the findings on the repo's issue tracker — checks open `rot-hunt`-labeled issues first to skip already-filed patterns, then posts each new finding as a GitHub/GitLab issue with the `rot-hunt` label. Use when the user wants a rot hunt whose findings are filed as issues, or asks to hunt rot "and file it" / "as issues". For a report-only hunt use `rot-hunt`.
---

# Rot hunt → issue

Wraps `rot-hunt` with a tracker ledger: past hunts live as open `rot-hunt`-labeled issues, so a hunt neither re-investigates a known pattern nor files a duplicate, and every new finding lands as an issue.

## Check the ledger

Before hunting, read the ledger so already-detected patterns are skipped.

Detect the host from `git remote get-url origin` (github.com → `gh`, gitlab domain → `glab`), then list open `rot-hunt` issues:

- GitHub: `gh issue list --label rot-hunt --state open --json number,title,body`
- GitLab: `glab issue list --label rot-hunt`

If an open issue already covers a pattern the user asked about (same seed or same search token), stop for that pattern and report the existing issue number instead. If the CLI is missing or unauthenticated, tell the user and continue with filing skipped.

Done when every pattern to hunt is either cleared as new or matched to an existing issue number.

## Hunt

Call the Skill tool with `rot-hunt`. Run it in full — its report table is the input to filing. A "no valid candidate" result from the hunt is itself the finding: report it and file nothing.

## File the issue

Each new pattern's report row becomes one tracker issue, labeled `rot-hunt` so future ledger checks find it.

1. Ensure the label exists (create it once, then reuse):
   - GitHub: `gh label create rot-hunt --description "Recurring bad pattern traced to its seed commit. Fix the seed, not the copies." --color D93F0B` (ignore "already exists")
   - GitLab: `glab label create --name rot-hunt --description "Recurring bad pattern traced to its seed commit - fix the seed, not the copies" --color "#D93F0B"` (ignore "already exists")
2. File it — title `rot-hunt: <one-line pattern description>`, body = the report row (seed with file + SHA, copies, fork, verdict, fix order, rung) plus the seed search token verbatim so a later ledger check can match on it:
   - GitHub: `gh issue create --label rot-hunt --title "..." --body "..."`
   - GitLab: `glab issue create --label rot-hunt --title "..." --description "..."`
3. Report the issue URL back to the user.

Done when every new pattern has an issue URL, or the user was told why filing was skipped.

## When this skill is the wrong fit

- Report-only hunt, no tracker involvement wanted → `rot-hunt`
