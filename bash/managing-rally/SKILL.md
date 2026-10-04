---
name: managing-rally
description: |
  Use when working with Rally — broadcom Rally (formerly CA Agile Central)
  project management covering workspaces, projects, user stories, defects,
  iterations, and velocity analytics. Use when auditing Rally usage, managing
  stories and defects, analyzing iteration health, or reviewing portfolio-level
  metrics.
connection_type: rally
preload: false
---

# Managing Rally

Rally agile project management analysis via the Rally REST API (WSAPI).

## Discovery Phase

```bash
#!/bin/bash
RALLY_BASE="https://rally1.rallydev.com/slm/webservice/v2.0"

echo "=== Current User ==="
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/user" | jq '.User | {ObjectID, UserName, DisplayName, EmailAddress}'

echo ""
echo "=== Workspaces ==="
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/subscription?fetch=Workspaces" \
  | jq -r '.Subscription.Workspaces._ref' | xargs -I{} curl -s -H "ZSESSIONID: $RALLY_API_KEY" "{}" \
  | jq -r '.QueryResult.Results[] | "\(.ObjectID)\t\(.Name)"' | column -t

echo ""
WORKSPACE_ID="${1:?Workspace ObjectID required}"
echo "=== Projects ==="
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/project?workspace=/workspace/$WORKSPACE_ID&fetch=Name,State,Iterations&pagesize=20" \
  | jq -r '.QueryResult.Results[] | "\(.ObjectID)\t\(.Name[0:30])\t\(.State)"' | column -t

echo ""
echo "=== Current Iterations ==="
TODAY=$(date +%Y-%m-%d)
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/iteration?workspace=/workspace/$WORKSPACE_ID&query=(StartDate <= \"$TODAY\") AND (EndDate >= \"$TODAY\")&fetch=Name,StartDate,EndDate,Project&pagesize=10" \
  | jq -r '.QueryResult.Results[] | "\(.Name[0:25])\t\(.Project.Name[0:20])\t\(.StartDate[0:10])\t\(.EndDate[0:10])"' | column -t
```

## Analysis Phase

```bash
#!/bin/bash
RALLY_BASE="https://rally1.rallydev.com/slm/webservice/v2.0"
PROJECT_ID="${1:?Project ObjectID required}"

echo "=== User Stories by Schedule State ==="
for STATE in "Defined" "In-Progress" "Completed" "Accepted"; do
  COUNT=$(curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
    "$RALLY_BASE/hierarchicalrequirement?project=/project/$PROJECT_ID&query=(ScheduleState = \"$STATE\")&pagesize=1" \
    | jq '.QueryResult.TotalResultCount')
  echo -e "$STATE\t$COUNT"
done | column -t

echo ""
echo "=== Defects ==="
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/defect?project=/project/$PROJECT_ID&query=(State != Closed)&fetch=FormattedID,Name,State,Priority,Severity&pagesize=15&order=Priority" \
  | jq -r '.QueryResult.Results[] | "\(.FormattedID)\t\(.State)\t\(.Priority)\t\(.Severity)\t\(.Name[0:35])"' | column -t

echo ""
echo "=== Iteration Burndown ==="
TODAY=$(date +%Y-%m-%d)
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/iteration?project=/project/$PROJECT_ID&query=(StartDate <= \"$TODAY\") AND (EndDate >= \"$TODAY\")&fetch=Name,PlannedVelocity,StartDate,EndDate&pagesize=1" \
  | jq '.QueryResult.Results[0] | {name: .Name, planned_velocity: .PlannedVelocity, start: .StartDate[0:10], end: .EndDate[0:10]}'

echo ""
echo "=== Unestimated Stories ==="
curl -s -H "ZSESSIONID: $RALLY_API_KEY" \
  "$RALLY_BASE/hierarchicalrequirement?project=/project/$PROJECT_ID&query=(PlanEstimate = null) AND (ScheduleState != Accepted)&pagesize=1" \
  | jq '{unestimated_stories: .QueryResult.TotalResultCount}'
```

## Output Format

```
RALLY PROJECT HEALTH: [project_name]
Workspace:       [name]
Current Sprint:  [name] ([start] - [end])

STORY DISTRIBUTION
Schedule State   Count
Defined          [n]
In-Progress      [n]
Completed        [n]
Accepted         [n]

DEFECTS
Open Defects:    [count]
Critical:        [count]
High Priority:   [count]

VELOCITY
Planned:         [n] pts
Unestimated:     [count] stories
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

