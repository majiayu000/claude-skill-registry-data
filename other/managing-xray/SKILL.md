---
name: managing-xray
description: |
  Use when working with Xray — xray test management for Jira monitoring and
  analysis. Covers test case and precondition management, test plan and
  execution tracking, Cucumber/Gherkin integration, test set organization,
  requirement coverage analysis, and CI/CD result import. Use when managing test
  cases in Xray, tracking test executions within Jira, or reviewing BDD test
  coverage.
connection_type: xray
preload: false
---

# Xray Test Management Skill

Manage and analyze Xray test plans, executions, and coverage within Jira.

## Core Helper Functions

```bash
#!/bin/bash

# Xray Cloud API helper
xray_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    # Authenticate and get token
    if [ -z "$XRAY_TOKEN" ]; then
        XRAY_TOKEN=$(curl -s -X POST \
            -H "Content-Type: application/json" \
            "https://xray.cloud.getxray.app/api/v2/authenticate" \
            -d "{\"client_id\":\"${XRAY_CLIENT_ID}\",\"client_secret\":\"${XRAY_CLIENT_SECRET}\"}" | tr -d '"')
    fi

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${XRAY_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://xray.cloud.getxray.app/api/v2/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${XRAY_TOKEN}" \
            "https://xray.cloud.getxray.app/api/v2/${endpoint}"
    fi
}

# Jira API helper for Xray issue queries
jira_api() {
    curl -s -X GET \
        -u "${JIRA_USER}:${JIRA_API_TOKEN}" \
        -H "Content-Type: application/json" \
        "${JIRA_URL}/rest/api/3/${1}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover test plans and test sets before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Xray Test Plans ==="
PROJECT_KEY="${1:?Project key required}"
jira_api "search?jql=project=${PROJECT_KEY}+AND+issuetype='Test Plan'&maxResults=10&fields=summary,status" | jq -r '
    .issues[] | "\(.key)\t\(.fields.summary)\tstatus=\(.fields.status.name)"
' | column -t

echo ""
echo "=== Test Executions ==="
jira_api "search?jql=project=${PROJECT_KEY}+AND+issuetype='Test Execution'&maxResults=10&fields=summary,status" | jq -r '
    .issues[] | "\(.key)\t\(.fields.summary)\tstatus=\(.fields.status.name)"
' | column -t

echo ""
echo "=== Test Cases ==="
jira_api "search?jql=project=${PROJECT_KEY}+AND+issuetype='Test'&maxResults=15&fields=summary,status,labels" | jq -r '
    .issues[] | "\(.key)\t\(.fields.summary)\tstatus=\(.fields.status.name)\tlabels=\(.fields.labels | join(","))"
' | column -t

echo ""
echo "=== Test Sets ==="
jira_api "search?jql=project=${PROJECT_KEY}+AND+issuetype='Test Set'&maxResults=10&fields=summary" | jq -r '
    .issues[] | "\(.key)\t\(.fields.summary)"
' | column -t
```

### Phase 2: Analysis

```bash
#!/bin/bash

PROJECT_KEY="${1:?Project key required}"

echo "=== Test Execution Results ==="
EXEC_KEY="${2:-}"
if [ -n "$EXEC_KEY" ]; then
    xray_api GET "testexecutions/${EXEC_KEY}/tests" | jq -r '
        .[:20][] | "\(.key)\t\(.summary // "unnamed")\tstatus=\(.status // "TODO")"
    ' | column -t

    echo ""
    echo "=== Execution Summary ==="
    xray_api GET "testexecutions/${EXEC_KEY}/tests" | jq '{
        total: length,
        by_status: (group_by(.status) | map({status: .[0].status, count: length}))
    }'
fi

echo ""
echo "=== Requirement Coverage ==="
jira_api "search?jql=project=${PROJECT_KEY}+AND+issuetype+in+(Story,Bug)&maxResults=10&fields=summary,issuelinks" | jq -r '
    .issues[] | {
        key: .key,
        summary: .fields.summary,
        linked_tests: [.fields.issuelinks[] | select(.type.name == "Test") | .outwardIssue.key // .inwardIssue.key] | length
    } | "\(.key)\t\(.summary | .[0:40])\ttests=\(.linked_tests)"
' | column -t | head -15

echo ""
echo "=== Cucumber Feature Files ==="
xray_api GET "export/cucumber?keys=${PROJECT_KEY}" 2>/dev/null | head -20 || echo "No Cucumber export configured"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use JQL queries for efficient issue filtering
- Summarize coverage metrics, not full test step details

## Anti-Hallucination Rules
- NEVER guess issue keys — always discover via JQL search
- NEVER fabricate test results — query actual Xray data
- NEVER assume Xray Cloud vs Server — check API endpoint compatibility

## Safety Rules
- NEVER create or delete test executions without explicit user confirmation
- NEVER modify test status without user approval
- NEVER import results without user consent

## Output Format

Present results as a structured report:
```
Managing Xray Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

