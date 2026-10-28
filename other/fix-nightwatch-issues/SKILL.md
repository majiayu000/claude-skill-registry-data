---
name: fix-nightwatch-issues
description: Triage open Laravel Nightwatch production issues by root cause, fix the legit ones, and resolve them with evidence.
disable-model-invocation: true
argument-hint: "Optional issue numbers or a type filter (exception, route, job, command, scheduled_task); defaults to all open issues"
compatibility: "Requires the Laravel Nightwatch MCP server"
---

# Fix Nightwatch Issues

Open Nightwatch issues are real production signals: exceptions, and slow routes, jobs,
commands, and scheduled tasks. Many are stale, ops problems, or third-party blips, so
read the stack trace and the occurrence stats, not the headline. Walk from the newest
last-seen to the oldest.

**Project context.** Read `.agents/nightwatch.md` when the repo has one. It holds the
application and environment names, the deploy model, the infra paths, and the known
false premises. Then follow the repo's `AGENTS.md` / `CLAUDE.md` rules for tests, cache
clears, and a dirty tree.

## 1. Resolve the target

Use the Nightwatch MCP tools. If they are not loaded, discover them first.
`list_applications` gives the application id and `list_environments` gives the
production environment. `list_issues` (status `open`, sorted by last seen) is the
working set. `get_issue` returns the stack trace, code context, occurrence stats, and
execution context.

An empty application list or issue list can mean collection is off, not that production
is healthy. Check the project context (or the infra config) and report "collection is
off" when that is the cause.

## 2. Cluster by root cause

Nightwatch groups issues by message text, **not by cause**, so one cause fans out into
many issues. For example, one root-run command that leaves a root-owned log file
surfaces as a separate "Permission denied … while attempting to log: <message>" issue
for every message it swallowed. Read enough issues to group them by shared cause
before you fix anything. Fix each cause once, then dispose of every issue in its
cluster.

Completion criterion: every open issue in scope belongs to a cluster, even a cluster of one.

## 3. Classify each cluster

For each cluster, open the `file:line` from `get_issue` on current `main` and read the
commits around it. Compare last-seen with deploys (`git log --oneline -- <file>`): if
it stopped at a deploy of a fix, it is STALE. Then write one line per issue:

```
Issue #NNN: [STALE | INFRA/OPS | EXTERNAL/TRANSIENT | NOISE | LEGIT] — <one-line evidence>
```

- `Issue #131: STALE — last seen 2026-05-02, path fixed in a1b2c3d (deployed 2026-05-03); no occurrences since`
- `Issue #110: INFRA/OPS — root-owned daily log file; consequence of #106; fix is logging sink + entrypoint, not app code`
- `Issue #144: EXTERNAL/TRANSIENT — single queue receive timeout, 1 occurrence in 30d`
- `Issue #150: NOISE — 404 from a bot scan on /wp-login.php`

Categories:

- **INFRA/OPS**: permissions, a missing or disabled PHP capability, the log sink, a
  container user mismatch, or an env var. Fix these in container or infra config, not
  app code.
- **EXTERNAL/TRANSIENT**: a third-party timeout or 5xx, or a network blip. Judge by
  count and spread. Add a retry only if it recurs and the retry is cheap.
- **NOISE**: bot 404s, aborted requests, and health-check probes. Filter these in
  Nightwatch sampling, not in code.
- **LEGIT**: a cause that still reproduces against current `main`. One occurrence in 30
  days with no users affected rarely justifies code. A steady daily count does.

Completion criterion: every issue has a line.

## 4. Fix each LEGIT cluster at the right layer

The symptom rarely points at the layer that needs the fix:

- App logic: fix the code, with a test.
- Environment or permissions: fix the container setup or the infra env config.
- A slow route, job, or command: add an index (check the schema first), eager-load,
  chunk, or move the work to a queue.

Make the minimal change. Verify it locally where you can. For infra that cannot run
locally, say so plainly. Commit one logical fix per commit, and list every Nightwatch
ref the commit covers in its body (for example `Nightwatch: #106, #107-#115`). **Use
plain refs only, never `fixes #NNN`**: a GitHub auto-close keyword would close the
unrelated GitHub issue that has the same number.

## 5. Resolve in Nightwatch

For each fixed issue, `add_issue_comment` with the root cause and the fix sha, then
`update_issue` to `resolved`. For a cluster, do this for every member and point back to
the lead cause. A fix is not verified until it is deployed and last-seen goes quiet, so
note "resolved pending deploy verification" where that applies.

If an issue is LEGIT but needs an operator (a secret rotation, a CI secret, an infra
apply, a vendor), commit the code part, leave the issue OPEN, and comment with exactly
what unblocks it. Resolve only issues whose cause is fixed. If an issue recurs after
deploy, reopen it and correct its classification.

Completion criterion: every issue in scope is resolved with a comment, or stays open
with a comment that names its blocker. Report the tally with one line per cluster, starting ✅ resolved or ⚠️ open with a blocker.

## 6. Offer a deploy re-check

If any issue is pending deploy verification, ask once whether to re-check it in 24–48
hours. On yes, schedule a one-time run where the harness can (in Claude Code, the
`schedule` skill's cloud routine; failing that, `CronCreate` with `recurring: false`,
which fires only while this session stays open, so say so). The prompt is plain text,
since a slash command for this skill cannot run from a schedule: "With the Nightwatch
MCP, read last-seen for issues #<ids>; reopen and comment on any seen after <deploy
date>." Otherwise, or on no, end the report with the issue ids and the re-check date.
