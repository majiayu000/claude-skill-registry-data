---
name: triage-security-alerts
description: "Use for \"review security alerts\", \"triage dependabot\", \"look at the security tab\". Pulls a repo's open Dependabot alerts, groups them by package and advisory, recommends bump, dismiss, or defer per group, and carries out what the human decides. Files tasks in the tracker for bumps, dismisses through the GitHub API. Dependabot only. Code scanning and secret scanning are different jobs."
---

# Triage security alerts

Turn a stale queue of Dependabot alerts into a short list of decisions. Group first, so five advisories on one package are one decision. Recommend an action per group. The human decides, and you do exactly that. Never dismiss an alert or file a task without a yes.

## Config

One file per project, not per repo: a project's repos share a tracker, an assignee, and conventions.

`~/.config/squirrel/security-triage.<project>.json`:

```json
{
  "project": "myapp",
  "repos": [
    {
      "owner": "my-org",
      "name": "myapp-web",
      "localPath": "~/code/myapp-web",
      "ecosystem": "npm",
      "primaryLockfile": "package-lock.json",
      "packageManager": "npm"
    },
    {
      "owner": "my-org",
      "name": "myapp-api",
      "localPath": "~/code/myapp-api",
      "ecosystem": "pip",
      "lockfiles": ["requirements.txt", "requirements-development.txt"],
      "lockfileNote": "pip-tools. development is a superset of production. Both tracked on purpose. Dedupe at the advisory level.",
      "subProjects": [
        { "path": "chat", "ecosystem": "npm", "primaryLockfile": "chat/pnpm-lock.yaml", "packageManager": "pnpm" }
      ]
    }
  ],
  "tracker": {
    "assignee": "who gets the bump tasks",
    "priority": "normal",
    "dismissalComment": "Dismissed during {date} security triage. {reason}"
  }
}
```

First time on a project, ask for owner and name, ecosystem, and assignee. Probe the lockfile layout yourself. Save the file after the first session.

## Before pulling anything

1. `gh auth status` works. If not, ask the human to log in.
2. `gh api repos/<owner>/<name>` answers, so you have access.
3. Dependabot is on. If the alerts endpoint returns 404 or "disabled", stop and say so.
4. If a local path is configured, its origin matches the repo. Codepath checks depend on that.

## Lockfiles

More than one lockfile isn't always a problem. Tell these apart.

- **npm with two lockfiles and no `packageManager` in package.json.** Accidental. Each drifts on its own, Dependabot scans both, and roughly half the alerts are duplicates. Say so, offer a cleanup task first, triage against the primary lockfile only, and say how many alerts the cleanup clears.
- **pip-tools with `requirements.txt` and `requirements-development.txt`, both with pip-compile headers.** Intentional. Every production package is in both, so every advisory shows twice. Track both, dedupe by advisory, don't recommend cleanup.
- **A confusing Python mix,** Pipfile.lock next to requirements.txt, poetry.lock next to requirements.txt. Ask which is canonical.
- **A sub-project in another ecosystem,** a JS app inside a Python repo. Its own triage scope, its own section in the matrix, its own task. Save it under `subProjects`.

## Pull the alerts

```bash
gh api --paginate "repos/<owner>/<name>/dependabot/alerts?state=open&per_page=100"
```

Without `--paginate` the list silently truncates past a hundred alerts. The output can be several concatenated JSON arrays; parse them all. The list payload has everything the first pass needs: severity, package, advisory, scope, manifest, fix version.

## Group

Group by package name and scope. `runtime` is user-facing risk, `development` build and test tooling with lower real-world impact. Pip alerts often all say runtime, so use the manifest path as a second signal.

Within a package, dedupe by advisory: one advisory across two manifests is one fix. Show both numbers, "django: 24 alerts, 12 advisories". The decision is "fix this advisory", never "handle this alert id".

Sort runtime groups first, then dev-only. Inside each, by worst severity, then by count. Show a matrix:

```
### Runtime

| # | Package | Alerts | Advisories | Worst | Proposed | Resolves |

### Dev only

| ... same shape ...

### Sub-project: <name> (<ecosystem>)

| ... same shape ...
```

Proposed is one of:

- **Bump to at least X.** A fix exists and the package is in use. Work out the risk tier first, below.
- **No upstream fix.** `first_patched_version` is null, usually abandoned or free-tier libraries. Needs a replacement-library decision.
- **Resolves through <other package>.** A transitive of something else being bumped: follow-redirects through axios, urllib3 through requests.
- **Already tracked in <task>.** The human names an existing task.
- **Dismiss, tolerable risk.** Low severity, dev only, not going to be fixed upstream soon.
- **Check the codepath first.** The exploit needs one specific API. Offer to grep before deciding.

## Decisions

A fixed menu per group:

```
(t) file a task to fix it
(d) dismiss, tolerable risk
(n) dismiss, not used    (codepath gets verified first)
(s) skip, leave open
(a) already tracked in <task>
```

Bulk is the default at five groups or more. Take shorthand. "2: t, 3: t, 4: t check _.template, 8: d". "Approve all your recommendations." "Do the dismissals first, then the bumps."

## Codepath verification

`not_used` is the strongest claim GitHub offers. Never take it on faith. Always before `(n)`, and optionally before `(t)` when the advisory names one function: the grep is cheap and changes the task's urgency.

1. Name the function or pattern from the advisory.
2. Grep the local checkout's application code. Skip node_modules, dist, build output, virtualenvs.
3. Show the count and a few hits.
4. Zero hits, `not_used` is defensible. Hits, push back and ask for a different option.
5. For a task, put the finding in the description. "The exploit needs X. We don't call X. This bump is hygiene, not mitigation."

## Filing a task

Read the pinned version from the lockfile and compare it to the fix version. Bucket each group:

- **Safe.** Patch or minor within the same major on a stable library. Regen the lockfile and smoke test.
- **Medium.** Minor on a 0.x library, or a major on a package with a stable API. Quick API check.
- **Heavy.** A major with real breaking changes. Every code path that uses it gets tested.
- **Replace.** No upstream fix. A different library.

One task per tier, so safe bumps never wait on heavy testing. Replacements get one task per package.

Each task carries: a title with the tier and the concrete alert count; the groups with current and target versions and one line on what each resolves; what's deferred to which other task; acceptance including "open alert count drops by at least N"; where the lockfiles live and how to regenerate them; the assignee and priority from config, priority raised if any advisory is critical.

File it through whatever tracker skill is installed, and don't skip that skill's own confirmation step.

## Dismissing

```bash
gh api -X PATCH "repos/<owner>/<name>/dependabot/alerts/<n>" -f state=dismissed -f dismissed_reason=tolerable_risk -f dismissed_comment="<reason>"
```

`not_used` is the same call with that reason. The comment is the human's words if they gave any, otherwise the config template with the date and a reason drawn from the scope. One decision covers every alert in the group; fire the calls together.

## Confirmation

Single group: say what you're about to do and wait for yes. Bulk: list every action once at the start and take one yes for the batch. Never touch an alert without a decision in the same turn. Every `(n)` shows its grep evidence before firing, bulk or not.

## After

Tasks filed with links, by tier. Alerts dismissed, by reason. Skipped. Resolving through a parent fix, and which task. Sub-project status. The remaining open count, which GitHub may take a few minutes to update. Then ask whether to do another repo.

## Not this skill

Code scanning alerts, where the fix is code, not a bump. Secret scanning, where the fix is rotation and audit. Other vulnerability sources. Repos without Dependabot.
