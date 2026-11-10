---
name: platform-activity
description: Use when something in a Platform org broke or needs triage, such as errors, open notifications, the audit log, failed GitHub Actions runs, and fixing a failure with a pull request.
---

# Activity and fixes

## Triage

1. `activity.notifications`: the open problems the dashboard shows.
2. `activity.errors`: errors with type, message, where, count and stack.
3. `activity.log`: who did what, from where, and the status. Use it to find what changed before a failure.
4. `org.trends`: daily counts, to see when it started.

Report the cause from the evidence, with the error id. Do not guess.

## Close the loop

- `activity.resolve_error` and `activity.resolve_notification` once the cause is fixed. One comes back when it happens again.
- `activity.reopen_*` if it was closed too early.
- `activity.delete_error` and `activity.delete_notification` need confirm. Resolve instead, unless the person asks to delete.

## Failed CI runs

1. `activity.ci_runs`: the latest GitHub Actions runs of each repo on the org's CI list.
2. With the GitHub service connected: list the run's jobs and read the failed job's log with the `github.*` actions tools.
3. Find the cause in the log. Reproduce it in the code before you change anything.
4. Fix it on a new branch and open a pull request with the `github.*` tools.

The write rule of `github.*` tools:

- Writes go only to the repos on the org's CI list (Activity, CI tab), when the list has any. `activity.set_ci_repos` changes the list and needs `settings:write`.
- A file write names a branch that is not the default branch. Push to a new branch, then open a pull request.
- A merge runs only when the pull request is open and every check on its head commit passed.
- GitHub writes need confirm.

Never skip or delete a test to make a run green.
