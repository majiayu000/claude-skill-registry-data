---
name: report-comment
description: >-
  Turn the git commits for a Jira ticket into a short, business-friendly implementation report and save it as local markdown. Use when the user wants to report finished work on a Jira ticket: a Jira report, update, or comment, a summary of their commits or changes for the ticket, or a note telling PM/QA what shipped.
---

# Jira Report Comment

Generate a short Jira comment describing what shipped on a ticket, and save it as a local markdown file.

The reader — a PM, QA engineer, or architect — already has the ticket open. Every sentence that paraphrases the ticket back at them is a sentence they skip, and after two of those they stop reading the whole comment. So the comment carries only what the ticket cannot: what actually shipped, and what someone downstream now has to do differently.

By default that is one summary paragraph. Bug fixes add a Root Cause. Verify and Deploy sections appear only when the diff gives a concrete reason.

## Step 1 — Resolve the issue key

In order: the key the user gave you; otherwise the first `[A-Z]+-[0-9]+` match in `git branch --show-current`; otherwise ask.

Confirm before continuing: "I detected **CX-4328** from your branch. Use this issue key?"

Then reserve the output file, and write to this same path for the rest of the session — re-running the skill for the same issue updates the file rather than adding another:

```bash
mkdir -p docs/jira-reports
touch "docs/jira-reports/$(date +%Y-%m-%d-%H%M%S)-<ISSUE_KEY>.md"
```

## Step 2 — Fetch the ticket

Try the Atlassian MCP server's `getJiraIssue` tool with the key. If it is unavailable, ask the user to paste the title, description, and acceptance criteria.

Read the title, description, type, and status. **This is the material to leave out, not material to write from.** Use it as the exclusion list.

## Step 3 — Gather the diff

```bash
git log --grep="<ISSUE_KEY>" --format="%H %s" --reverse
```

If that finds nothing, retry with `--all`. If still nothing, diff the branch against its base — try `main`, then `master`, then `develop`:

```bash
git diff $(git merge-base HEAD main)..HEAD --stat
git diff $(git merge-base HEAD main)..HEAD
```

With commits found, diff across the whole range for the net result rather than the incremental steps:

```bash
git diff <FIRST_COMMIT>^..<LAST_COMMIT> --stat
git diff <FIRST_COMMIT>^..<LAST_COMMIT>
```

If the first commit is the repository's initial commit, use `git diff $(git hash-object -t tree /dev/null)..<LAST_COMMIT>`. If no meaningful diff turns up, say so and stop.

Over ~50 files, work from the stat summary and read selectively — config, migrations, and tests usually reveal intent faster than the implementation does.

## Step 4 — Decide which sections exist

Read `references/output-format.md` for the skeleton, limits, and style.

**Root Cause** — when the ticket fixes an existing problem: the description mentions broken behaviour, a wrong result, a defect, or a regression. Issue type Bug is a strong signal but not required; some Stories and Tasks fix problems too. Derive the cause and the fix approach from the diff and commit messages — the ticket describes the symptom, and repeating it defeats the section.

**Verify** — when at least one is true:

- The diff adds a feature flag and the test path depends on its state
- The diff fires a side effect the ticket doesn't mention (email, webhook, log, metric)
- The diff adds a code path triggered by an input value the ticket doesn't name
- The diff changes behaviour for a role or permission level the ticket doesn't call out

**Deploy** — when at least one is true:

- The diff adds or renames an environment variable
- The diff adds a feature flag (name it, and state its default)
- The diff adds a migration needing manual coordination — backfill, lock-heavy schema change
- The diff adds a queue, scheduled job, or cron entry
- The diff needs a config change in another system (CDN, IAM, DNS)

No trigger fires — the comment is the summary and nothing else. That is the expected outcome for most feature work, not a sign you missed something.

## Step 5 — Draft, audit, save

Write the summary first, then add only the sections whose triggers fired. Then audit:

- **Delete any bullet describing routine work** — pushing code, restarting services, clearing caches, running a standard migration. The reader assumes these happened.
- **Strip ticket paraphrases.** Re-read against the ticket text from Step 2 and cut every phrase that echoes it.
- **Never describe a change the diff does not show.**

Write to the path reserved in Step 1 and confirm: "Report saved to `<path>`." Leave the file untracked — never stage or commit it. If the `humanize-text` skill is available, run the report through it before presenting.

### Example — bug fix

`BUG-789` "Cancellation email sent twice when a user cancels their subscription". Diff removes the legacy `onCancellation` handler registration, leaving `onSubscriptionCancelled` to send alone; adds a single-send test.

> ## BUG-789
>
> Cancellation now sends a single confirmation email.
>
> ### Root Cause
>
> - Two handlers were subscribed to the cancellation event after a partial refactor, and both were firing.
> - Removed the legacy registration so the newer handler is the single source of truth.

No Verify (the test path is what the ticket already implies) and no Deploy (routine code change).

### Example — with Deploy

`XYZ-456` "Send weekly digest email to active members". Diff adds a cron job, a `weekly_digest_enabled` flag defaulting off, and a `DIGEST_SENDER_EMAIL` env var.

> ## XYZ-456
>
> Weekly digest emails now ship every Monday at 9am to active members, skipping accounts with no activity in the last 7 days.
>
> ### Deploy
>
> - Set `DIGEST_SENDER_EMAIL` in production before enabling the feature
> - Toggle `weekly_digest_enabled` on after a smoke test
> - First scheduled run lands the Monday after deploy

Deploy fires on three counts: the env var, the flag, and the cron entry. Verify does not — the test path matches what the ticket describes.

## When things fail

- **Issue not found** — tell the user the key looks invalid and ask them to check it.
- **No commits** — report it plainly; suggest the branch or a different key format in commit messages.
- **MCP unavailable** — ask for the ticket context manually.
- **Write fails** — show the error and check directory permissions.
