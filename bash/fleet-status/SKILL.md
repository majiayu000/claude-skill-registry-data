---
name: fleet-status
description: Read-only AppSec roll-up of every app in NightVision - which apps exist, when each was last scanned, and where the open Critical and High findings are. Use when a user asks "who is building what", wants scan posture across all apps, asks which apps have never been scanned or have stale scans, or needs an AppSec roll-up for a CISO. It starts no scans and changes nothing.
allowed-tools: Bash, Read, mcp__nightvision__list-projects, mcp__nightvision__list-targets, mcp__nightvision__list-scans, mcp__nightvision__get-scan-status, mcp__nightvision__get-target-details, mcp__nightvision__export-report
---

# NightVision Fleet Status

One table that answers "what apps do we have, and what is the scan posture on each." It is for an AppSec lead or CISO governing many apps: a hundred developers shipping apps, and one person who has to know which exist, which have been scanned, and where the open Critical and High findings are.

This skill is read-only. It lists projects, targets and scans, and prints a status table plus a short summary. It never starts a scan, creates or edits a target, or marks a finding. If the user wants an app scanned, hand off to `app-security-scan`.

Everything here works with the NightVision CLI alone, so it runs on any coding agent. The NightVision MCP tools are an optional faster path (see "With the NightVision MCP").

## What you need

- The NightVision CLI, logged in (`nightvision login`) or with a token in `NIGHTVISION_TOKEN`, and `jq`. Check with `nightvision project list`.
- The stale threshold in days. Default 30. If the user states one ("anything not scanned in two weeks"), use theirs.
- Optionally a project filter. Default is every project the user can see.

The roll-up covers only what the logged-in account can see. Say whose view it is if the user expects the whole organization.

## Workflow

1. **List the projects.** `nightvision project list -F json`. Use all of them unless the user named some.
2. **List the targets in each project.** `nightvision target list -p <project> -F json`. Each target is one app. Keep `name`, `type` and `location` (the URL). The target list is the inventory: a target with no scans still appears here, which is how never-scanned apps are found.
3. **Find the scans for each target.** `nightvision scan list -p <project> -F json`, then match scans to targets on `target_name`. Keep two scans per target: the most recent one of any status, and the most recent one with `status_value` `SUCCEEDED`.
4. **Classify each target.** A target can carry more than one flag.
   - **Never scanned**: no scans at all.
   - **Stale**: it has scans, but no `SUCCEEDED` scan newer than the threshold. A target whose only recent scans failed is stale.
   - **Open Critical/High**: `issues_statistics.Critical` or `issues_statistics.High` is above zero on the most recent successful scan.
   - **Last scan did not succeed**: the most recent scan is `FAILED` or `ABORTED`. Report the counts from the last successful scan and give its date, because a failed scan's counts are incomplete. A scan still in progress is not a failure: show its status and use the last successful scan's counts.
5. **Print the table**, attention first. Order: never scanned, then open Critical/High (most Critical first, then most High), then stale, then everything else by project and target name. Columns:

   ```
   Project | Target | Type | Last scan | Status | Critical | High | Medium | Low | Flags
   ```

   Show `-` for counts on a never-scanned target, not `0`. A zero there reads as "clean".
6. **Write the summary**, five lines or fewer:
   - total apps, and how many projects;
   - scanned versus never scanned, with the never-scanned apps named (or the first ten and a count);
   - how many are stale at the threshold used, stating the threshold;
   - how many have open Critical or High, and the totals;
   - the worst offenders by name, most Critical first.

   Lead with the never-scanned apps. Those are the apps nobody has looked at, and they are the reason to run this.

## Getting the data with the CLI

All three commands are read-only. Pass `-F json`; the default output is text. Each returns a JSON list of objects.

- `nightvision project list -F json`: projects, each with `name`.
- `nightvision target list -p <project> -F json`: targets, each with `name`, `type` (`URL` for a web app, `OPENAPI` for an API), `location`, `project_name`, and `own_user` (the account that created the target). It does not include the target's tags.
- `nightvision scan list -p <project> -F json`: scans, each with `id`, `target_name`, `target_type`, `status_value` (`SUCCEEDED`, `FAILED`, `ABORTED`, or an in-progress status), `created_at`, `last_updated_at`, `issues_count`, and `issues_statistics` with the keys `Critical`, `High`, `Medium`, `Low`, `Informational`, `Unknown`, `Unspecified`.

Run `scan list` once per project with `-p`. Without `-p` it covers only the CLI's current project, and scans carry a target name but no project name, so a per-project call is what keeps two same-named targets in different projects apart.

Quick look at one project: the latest scan per target, worst first.

```bash
nightvision scan list -p "<project>" -F json | jq -r '
  group_by(.target_name)
  | map(sort_by(.created_at) | last)
  | sort_by(-(.issues_statistics.Critical // 0), -(.issues_statistics.High // 0))
  | .[]
  | [.target_name, .created_at[0:10], .status_value,
     (.issues_statistics.Critical // 0), (.issues_statistics.High // 0)]
  | @tsv'
```

That shows only targets that have a scan. The full roll-up starts from the target list so never-scanned apps appear:

```bash
STALE_DAYS=30
tmp=$(mktemp -d)
nightvision project list -F json | jq -r '.[].name' | while IFS= read -r project; do
  nightvision target list -p "$project" -F json > "$tmp/targets.json"
  nightvision scan list -p "$project" -F json > "$tmp/scans.json"
  jq -r --arg project "$project" --argjson days "$STALE_DAYS" \
        --slurpfile scans "$tmp/scans.json" '
    (now - $days * 86400 | strftime("%Y-%m-%dT%H:%M:%SZ")) as $cutoff
    | ($scans[0] // []) as $all
    | .[]
    | .name as $t
    | ($all | map(select(.target_name == $t)) | sort_by(.created_at)) as $s
    | ($s | last) as $latest
    | ($s | map(select(.status_value == "SUCCEEDED")) | last) as $ok
    | [ $project, $t, .type,
        ($latest.created_at // "never")[0:10],
        ($latest.status_value // "NEVER_SCANNED"),
        ($ok.issues_statistics.Critical // "-"),
        ($ok.issues_statistics.High // "-"),
        ($ok.issues_statistics.Medium // "-"),
        ($ok.issues_statistics.Low // "-"),
        ([ (if $latest == null then "never-scanned" else empty end),
           (if $latest != null and ($ok == null or $ok.created_at < $cutoff)
              then "stale" else empty end),
           (if (($ok.issues_statistics.Critical // 0)
                + ($ok.issues_statistics.High // 0)) > 0
              then "crit-high" else empty end),
           (if $latest != null and $ok != null and $latest.id != $ok.id
              then "counts-from-" + $ok.created_at[0:10] else empty end)
         ] | join(",")) ]
    | @tsv' "$tmp/targets.json"
done > "$tmp/fleet.tsv"
cat "$tmp/fleet.tsv"
```

One row per target: project, target, type, last scan date, last scan status, then Critical, High, Medium and Low from the last successful scan, then the flags. Timestamps are UTC ISO 8601, so comparing them as strings orders them correctly. Set `STALE_DAYS` to the user's threshold. To roll up a single project, replace the `project list` pipeline with `printf '%s\n' "<project>"`.

Sort and count from the TSV rather than by eye, then format the table in step 5 from it. If a project's scan list looks cut short for the number of targets it has, say so instead of reporting those targets as never scanned.

`scan list` can take a minute or more on a project with a long scan history, so a roll-up across a large fleet may run for several minutes. Let it finish rather than reporting partial data; tell the user it is a one-pass read if they expect it to be instant.

## With the NightVision MCP

If your agent has the NightVision MCP server wired up, the same data comes from read tools without shelling out. Nothing in the workflow requires them.

- `list-projects`, then `list-targets` per project, then `list-scans` per target. Each scan carries the same `issues_statistics`, `status_value`, `created_at`, `last_updated_at` and `issues_count` as the CLI output.
- `get-scan-status` confirms whether a scan that looks in-progress has reached a terminal status. `get-target-details` returns one target's metadata.
- `export-report` in `project` mode returns a project roll-up in one call: a row per target with `target_name`, `scanned_at`, `status`, per-severity counts and `total_open`. It is the fastest route when the user wants one project. Check its rows against `list-targets` so a target with no scans is not dropped, and apply the stale threshold yourself.

Use only these read tools. Do not call `start-scan`, `run-app-security-scan`, `create-target` or `delete-target` from this skill.

## Limits to state honestly

- **This is scan posture, not authorship.** Targets can carry tags, but the CLI list does not return them. A target tagged "Agent created" was set up by an AI coding agent through the NightVision MCP; when the user wants to know what agents have onboarded, point them to the dashboard's Applications page, where tags show and can be filtered. A tag says how a target was created, not which team owns the code. Otherwise, "who built it" comes from the project and target names, plus `own_user`, which is the account that created the target. That account is often a CI token or the person who onboarded the app, not the team that owns the code. Present it as "created by", never as "owner".
- **"No open Critical or High" is not "secure."** It means the latest successful scan found none. It says nothing about what that scan could not reach, code that changed since, or classes of flaw a dynamic scan does not test.
- **Counts are per scan, not deduplicated across apps**, and they reflect the scan's findings as triaged in NightVision at the time of the scan list.
- **An app with no target is invisible here.** The roll-up can show a target that was never scanned; it cannot show an app nobody registered. If the user has an app inventory elsewhere, compare it with the target list.
- **A never-scanned app is the real gap.** Do not let it sink below a table of findings. Name those apps first.

## Related skills

`app-security-scan` scans an app that shows up here as never scanned or stale. `scan-report` turns one scan or one project into a shareable PDF. `ci-cd-integration` sets up the merge gate so apps stop going stale.
