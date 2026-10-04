---
name: managing-qase
description: |
  Use when working with Qase — qase test management platform monitoring and
  analysis. Covers project organization, test case management, test run
  execution tracking, defect linking, shared step libraries, and environment
  configuration. Use when managing test cases in Qase, reviewing test run
  results, or tracking QA coverage and defects.
connection_type: qase
preload: false
---

# Qase Test Management Skill

Manage and analyze Qase projects, test cases, runs, and defects.

## Core Helper Functions

```bash
#!/bin/bash

# Qase API helper
qase_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Token: ${QASE_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://api.qase.io/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Token: ${QASE_API_TOKEN}" \
            "https://api.qase.io/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover projects and suites before querying specific test cases or runs.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Qase Projects ==="
qase_api GET "project?limit=20" | jq -r '
    .result.entities[] | "\(.code)\t\(.title)\tcases=\(.counts.cases)\truns=\(.counts.runs)"
' | column -t

echo ""
echo "=== Active Test Runs ==="
PROJECT_CODE="${1:?Project code required}"
qase_api GET "run/${PROJECT_CODE}?limit=10&status=active" | jq -r '
    .result.entities[] | "\(.id)\t\(.title)\tstatus=\(.status_text)\tpassed=\(.stats.passed)\tfailed=\(.stats.failed)"
' | column -t

echo ""
echo "=== Test Suites ==="
qase_api GET "suite/${PROJECT_CODE}?limit=20" | jq -r '
    .result.entities[] | "\(.id)\t\(.title)\tcases=\(.cases_count)"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

PROJECT_CODE="${1:?Project code required}"

echo "=== Test Case Summary ==="
qase_api GET "case/${PROJECT_CODE}?limit=100" | jq '{
    total: .result.total,
    by_status: (.result.entities | group_by(.status) | map({status: .[0].status_text, count: length})),
    by_priority: (.result.entities | group_by(.priority) | map({priority: .[0].priority, count: length}))
}' | head -20

echo ""
echo "=== Run Results ==="
RUN_ID="${2:-}"
if [ -n "$RUN_ID" ]; then
    qase_api GET "result/${PROJECT_CODE}?run=${RUN_ID}&limit=50" | jq -r '
        .result.entities[:20][] | "\(.case.title // "Case #\(.case_id)")\t\(.status_text)\t\(.time_spent)s"
    ' | column -t
fi

echo ""
echo "=== Open Defects ==="
qase_api GET "defect/${PROJECT_CODE}?status=open&limit=10" | jq -r '
    .result.entities[] | "\(.id)\t\(.title)\tseverity=\(.severity_text)\tstatus=\(.status_text)"
' | column -t

echo ""
echo "=== Environments ==="
qase_api GET "environment/${PROJECT_CODE}" | jq -r '
    .result.entities[] | "\(.slug)\t\(.title)\t\(.description // "no description")"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use API pagination (limit/offset) for large datasets
- Never dump full test case steps — show title and status only

## Anti-Hallucination Rules
- NEVER guess project codes — always discover via API
- NEVER fabricate test results — query actual run data
- NEVER assume suite hierarchy — check suite structure first

## Safety Rules
- NEVER create or delete test runs without explicit user confirmation
- NEVER modify test cases without user approval
- NEVER close defects without user consent

## Output Format

Present results as a structured report:
```
Managing Qase Report
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

