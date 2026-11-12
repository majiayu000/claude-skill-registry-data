---
name: gh-issues-by-severity
description: List open GitHub issues for the current repo grouped by severity, highest first, using the repo's own severity:* labels. Use when the user asks to see open issues by severity or wants a standup-style issue scan.
---

# gh-issues-by-severity

List open issues, grouped by severity (most severe first), sorted by issue
number ascending within each group. Generic across repos: discovers whatever
`severity:*` labels the repo actually has rather than assuming a fixed set.

## Process

1. **Discover the severity label vocabulary** for this repo:
   ```
   gh label list --json name --jq '[.[].name | select(startswith("severity:"))]'
   ```
   If this is empty, the repo has no severity scheme — every issue falls into
   a single `unlabeled` bucket. Say so, then continue (still produce the list,
   sorted by issue number).

2. **Rank the discovered labels.** Strip the `severity:` prefix and match each
   value (case-insensitive) against these clusters, highest severity first:
   - `critical`, `blocker`, `p0`, `sev1`
   - `high`, `major`, `p1`, `sev2`
   - `medium`, `moderate`, `p2`, `sev3`
   - `low`, `minor`, `trivial`, `p3`, `p4`, `sev4`

   Any discovered value that matches none of these clusters is "unrecognized" —
   rank it below all recognized clusters, ordered alphabetically among other
   unrecognized values. `unlabeled` (no `severity:*` label on the issue) always
   ranks lowest of all.

   Build a rank map, e.g. for a repo with `critical`/`high`/`medium`/`low`:
   ```json
   {"critical": 4, "high": 3, "medium": 2, "low": 1, "unlabeled": 0}
   ```

3. **Fetch open issues and sort server-side via jq** — don't hand-sort the
   list yourself:
   ```
   gh issue list --state open --limit 1000 --json number,title,labels \
     | jq --argjson rank '<rank map from step 2>' '
       map({
         number,
         title,
         severity: ((.labels[] | select(.name | startswith("severity:")) | .name | sub("^severity:";"")) // "unlabeled"),
         labels: [.labels[].name | select(startswith("severity:") | not)]
       })
       | map(. + {rank: ($rank[.severity] // -1)})
       | sort_by([-.rank, .number])
     '
   ```
   (If the user named a different repo, add `--repo <owner>/<name>`.)

4. **Render** the sorted JSON as grouped markdown, one section per severity
   level present (in descending rank order), with a count in the header:

   ```
   ## critical (2)
   #42  Auth bypass on login            [bug, needs-triage]
   #58  Data loss on export             [bug]

   ## high (1)
   #61  Slow query on dashboard         [enhancement, needs-info]

   ## low (3)
   #12  Typo in README                  []
   #19  Flaky test in CI                [needs-triage]
   #30  Missing alt text                []
   ```

   Show every label except the `severity:*` one — no further filtering.
   Omit the trailing `[]` bracket if an issue has no other labels, or leave
   it empty; either is fine, just be consistent within one run.

## Notes

- 1000-issue limit is for completeness on typical repos; if a repo somehow
  exceeds it, mention that the list may be truncated.
- If `gh` isn't authenticated or the directory isn't a GitHub repo, surface
  the `gh` error directly rather than guessing at a fix.
