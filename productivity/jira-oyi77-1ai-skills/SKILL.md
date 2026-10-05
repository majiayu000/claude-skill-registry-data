---
name: jira
description: 'Use when skill: jira. See SKILL.md body for details. Use when this domain
  is relevant.'
domain: operations
author: oyi77
license: Apache-2.0
subdomain: business-operations
tags:
- business-ops
- jira
- management
- operations
version: 1.0.0
category: operations
---


## Overview

Atlassian Jira is the industry-standard issue tracking and project management platform. This skill covers the Jira REST API, JQL (Jira Query Language), workflow transitions, sprint/scrum automation, webhook integration, and operational patterns for teams running Jira Cloud or Server/Data Center.

## Capabilities

- Issue CRUD via REST API (`/rest/api/3/issue`)
- JQL querying and bulk search (`/rest/api/3/search`)
- Sprint and board management (`/rest/agile/1.0/`)
- Epic/story hierarchy and issue linking
- Workflow transitions and custom fields
- Project configuration and permission schemes
- Webhook subscriptions for real-time events
- Time tracking via Tempo API

## When to Use

**Trigger phrases:**
- "jira"
- "Help me with jira"

**Use cases:**
- Automating issue creation from monitoring alerts or CI/CD pipelines
- Syncing Jira with external systems (GitHub, Slack, GitLab, Sentry)
- Generating custom dashboards and reports from JQL queries
- Automating sprint ceremonies (sprint creation, burndown reports)
- Bulk issue migration, status transitions, or field updates
- Building CLI tools or scripts for Jira operations

## When NOT to Use

- Task is about analysis, not action (use analyzing-* skills)
- You need to implement security controls (use implementing-* skills)
- Task requires compliance audit planning (consult compliance professionals)
- You don't have API access to the target Jira instance
- Task is better suited to a simpler tool (Linear, GitHub Issues, Trello)

## Authentication

### API Token (Cloud — Recommended)

Generate at `https://id.atlassian.com/manage-profile/security/api-tokens`. Format: `ATATT3xFfGF0...` (64+ chars).

```bash
curl -s -H "Authorization: Bearer YOUR_JIRA_TOKEN" \
  "https://your-domain.atlassian.net/rest/api/3/myself"
```

Never commit tokens to source code. Use environment variables.

### Personal Access Token (Server/Data Center)

```bash
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "https://jira.company.com/rest/api/2/myself"
```

Create PATs in Jira Server under user profile → Personal Access Tokens. Scoped to the creating user's permissions.

### OAuth 2.0 (3LO — Cloud)

For applications acting on behalf of users (not service accounts):

1. Create an OAuth integration in [Atlassian Developer Console](https://developer.atlassian.com/console/myapps/)
2. Get `client_id` and `client_secret` with scopes (`read:jira-work`, `write:jira-work`, `manage:jira-project`)
3. Redirect user to authorization URL:
   `GET https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=...&scope=read:jira-work%20write:jira-work&redirect_uri=...&response_type=code`
4. Exchange code for tokens:

```bash
curl -s -X POST "https://auth.atlassian.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{"grant_type": "authorization_code", "client_id": "...", "client_secret": "...", "code": "AUTH_CODE", "redirect_uri": "https://..."}'
```

5. Use the access token: `Authorization: Bearer $ACCESS_TOKEN` against `https://api.atlassian.com/ex/jira/{cloudId}/rest/api/3/...`

Discover cloud ID via `GET https://your-domain.atlassian.net/_edge/tenant_info`.

### Basic Auth (Deprecated — Cloud)

Basic auth with `email:password` was deprecated on July 1, 2023 for Cloud. Use API tokens instead. Still works for Server/Data Center.

## REST API Core Endpoints

All examples use Cloud endpoints (`/rest/api/3/`). Server/Data Center uses `/rest/api/2/` (equivalent but older). Agile endpoints use `/rest/agile/1.0/`.

### Issue CRUD

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create issue | `POST` | `/rest/api/3/issue` |
| Get issue | `GET` | `/rest/api/3/issue/{issueIdOrKey}` |
| Update issue | `PUT` | `/rest/api/3/issue/{issueIdOrKey}` |
| Delete issue | `DELETE` | `/rest/api/3/issue/{issueIdOrKey}` |

**Create issue with ADF description** (ADF = Atlassian Document Format, required for Cloud):

```bash
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "issuetype": {"name": "Bug"},
      "summary": "Login fails on Safari 17",
      "description": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Steps to reproduce"}]}]
      },
      "priority": {"name": "High"},
      "labels": ["frontend"],
      "assignee": {"accountId": "712020:abc123"},
      "duedate": "2026-08-15"
    }
  }'
```

**Update issue (partial):**

```bash
curl -s -X PUT "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"fields": {"summary": "Updated title", "priority": {"name": "Critical"}}}'
```

### Workflow Transitions

Transition IDs are numeric and instance-specific. Always fetch dynamically:

```bash
# Get available transitions
curl -s "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions" \
  -u "user@example.com:$JIRA_TOKEN" \
  | jq '.transitions[] | {id, name, toStatus: .to.name}'

# Transition to "Done" with resolution
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"transition": {"id": "31"}, "fields": {"resolution": {"name": "Done"}}}'
```

### Search / JQL

```bash
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/search" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{
    "jql": "project = PROJ AND status = \"In Progress\" AND assignee = currentUser()",
    "startAt": 0, "maxResults": 50,
    "fields": ["summary", "status", "assignee", "priority"]
  }'
```

### Projects and Boards

```bash
# List projects
curl -s "https://your-domain.atlassian.net/rest/api/3/project" -u "user@example.com:$JIRA_TOKEN"
# Get board configuration
curl -s "https://your-domain.atlassian.net/rest/agile/1.0/board/42/configuration" -u "user@example.com:$JIRA_TOKEN"
```

### Sprints

```bash
# List sprints for board
curl -s "https://your-domain.atlassian.net/rest/agile/1.0/board/42/sprint?state=active,future" \
  -u "user@example.com:$JIRA_TOKEN"

# Create sprint
curl -s -X POST "https://your-domain.atlassian.net/rest/agile/1.0/sprint" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"name": "Sprint 42", "originBoardId": 42, "goal": "Auth migration", "startDate": "2026-08-01T09:00:00.000Z", "endDate": "2026-08-14T17:00:00.000Z"}'

# Move issues to sprint
curl -s -X POST "https://your-domain.atlassian.net/rest/agile/1.0/sprint/123/issue" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"issues": ["PROJ-123", "PROJ-124"]}'
```

### Epics

Epics are issue type "Epic" linked via a custom field (`customfield_*`).

```bash
# Discover Epic Link field ID
curl -s "https://your-domain.atlassian.net/rest/api/3/field" \
  -u "user@example.com:$JIRA_TOKEN" \
  | jq '.[] | select(.name | test("Epic Link"; "i")) | .id'

# Link issue to epic
curl -s -X PUT "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-124" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"fields": {"customfield_10014": "EPIC-123"}}'

# Get issues in an epic
curl -s "https://your-domain.atlassian.net/rest/agile/1.0/board/42/epic/EPIC-123/issue" \
  -u "user@example.com:$JIRA_TOKEN"
```

### Custom Fields

```bash
# Discover all custom fields
curl -s "https://your-domain.atlassian.net/rest/api/3/field" \
  -u "user@example.com:$JIRA_TOKEN" \
  | jq '.[] | select(.custom == true) | {id, name, schema_type: .schema.type}'

# Write custom fields (types vary)
curl -s -X PUT "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"fields": {
    "customfield_10010": {"value": "Frontend"},   # select
    "customfield_10020": "2026-08-01",             # date
    "customfield_10030": 42                         # number
  }}'
```

Custom field value formats: Select → `{"value": "..."}`, Multi-select → `[{"value": "A"}, {"value": "B"}]`, User → `{"accountId": "..."}`, Labels → `["urgent"]`.

### Issue Links

```bash
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/issueLink" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{"inwardIssue": {"key": "PROJ-123"}, "outwardIssue": {"key": "PROJ-456"}, "type": {"name": "Relates"}}'
```

Link types: `Relates`, `Blocks`/`is blocked by`, `Clones`/`is cloned by`, `Duplicate`/`is duplicated by`.

## Code Examples

### Python (requests)

```python
import os, requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://your-domain.atlassian.net"
AUTH = HTTPBasicAuth(os.environ["JIRA_EMAIL"], os.environ["JIRA_TOKEN"])
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

def create_issue(project, summary, issue_type="Task", priority=None):
    fields = {"project": {"key": project}, "issuetype": {"name": issue_type}, "summary": summary}
    if priority:
        fields["priority"] = {"name": priority}
    resp = requests.post(f"{JIRA_URL}/rest/api/3/issue", json={"fields": fields}, auth=AUTH, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()  # {"id": "10001", "key": "PROJ-124"}

def search_jql(jql, fields=None, max_results=50):
    payload = {"jql": jql, "maxResults": max_results}
    if fields:
        payload["fields"] = fields
    resp = requests.post(f"{JIRA_URL}/rest/api/3/search", json=payload, auth=AUTH, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["issues"]

def transition_issue(issue_key, transition_id, resolution=None):
    payload = {"transition": {"id": str(transition_id)}}
    if resolution:
        payload["fields"] = {"resolution": {"name": resolution}}
    resp = requests.post(f"{JIRA_URL}/rest/api/3/issue/{issue_key}/transitions",
                         json=payload, auth=AUTH, headers=HEADERS)
    resp.raise_for_status()

def iterate_all_issues(jql, fields=None, batch_size=100):
    """Iterate ALL matching issues with pagination."""
    all_issues, start_at = [], 0
    while True:
        payload = {"jql": jql, "startAt": start_at, "maxResults": batch_size}
        if fields: payload["fields"] = fields
        data = requests.post(f"{JIRA_URL}/rest/api/3/search", json=payload, auth=AUTH, headers=HEADERS).json()
        all_issues.extend(data["issues"])
        if start_at + batch_size >= data["total"]:
            break
        start_at += batch_size
    return all_issues

# Usage
issue = create_issue("PROJ", "Automated bug report", "Bug", "High")
issues = search_jql("project = PROJ AND status = 'To Do' ORDER BY priority DESC")
transition_issue("PROJ-124", "21")  # To In Progress
```

### Python (jira library)

```python
from jira import JIRA
jira = JIRA(server="https://your-domain.atlassian.net",
            basic_auth=(os.environ["JIRA_EMAIL"], os.environ["JIRA_TOKEN"]))

issue = jira.create_issue(project="PROJ", summary="High CPU",
                          issuetype={"name": "Bug"}, priority={"name": "Critical"})
issues = jira.search_issues('project = PROJ AND status in ("To Do", "In Progress")', maxResults=50)
jira.transition_issue(issue, "21")
jira.add_comment(issue.key, "Deploying fix.")
```

### JavaScript / Node (axios)

```javascript
const axios = require('axios');
const BASE = 'https://your-domain.atlassian.net';
const AUTH = Buffer.from(`${process.env.JIRA_EMAIL}:${process.env.JIRA_TOKEN}`).toString('base64');
const headers = {'Authorization': `Basic ${AUTH}`, 'Accept': 'application/json', 'Content-Type': 'application/json'};

// Create issue
const resp = await axios.post(`${BASE}/rest/api/3/issue`, {
  fields: { project: { key: 'PROJ' }, issuetype: { name: 'Task' }, summary: 'Add rate limiting' }
}, { headers });

// Search
const search = await axios.post(`${BASE}/rest/api/3/search`, {
  jql: 'project = PROJ AND created >= -7d ORDER BY priority DESC', maxResults: 25
}, { headers });
for (const issue of search.data.issues) console.log(`${issue.key}: ${issue.fields.summary}`);
```

### Bash (curl)

```bash
#!/usr/bin/env bash
set -euo pipefail
JIRA_URL="https://your-domain.atlassian.net"
AUTH_ARGS=(-u "$JIRA_EMAIL:$JIRA_TOKEN")
JSON_HEADER=(-H "Content-Type: application/json")

create_issue() {
  curl -s -X POST "${JIRA_URL}/rest/api/3/issue" "${AUTH_ARGS[@]}" "${JSON_HEADER[@]}" \
    -d "{\"fields\": {\"project\": {\"key\": \"$1\"}, \"issuetype\": {\"name\": \"$3\"}, \"summary\": \"$2\", \"priority\": {\"name\": \"$4\"}}}" | jq -r '.key'
}

search_jql() {
  curl -s -X POST "${JIRA_URL}/rest/api/3/search" "${AUTH_ARGS[@]}" "${JSON_HEADER[@]}" \
    -d "{\"jql\": \"$(echo "$1" | sed 's/"/\\"/g')\", \"maxResults\": ${2:-50}}" | jq -r '.issues[].key'
}
```

## JQL Patterns

### Basic Filters

```jql
project = PROJ
issuetype = Bug
status = "In Progress"
priority in (Highest, High)
assignee = currentUser()
reporter = "john@example.com"
```

### Date Functions

```jql
-- Relative
created >= -7d          -- last 7 days
updated >= -24h         -- last 24 hours
due < now()             -- overdue
due = startOfDay()      -- due today
duedate >= "2026-08-01" AND duedate <= "2026-08-31"

-- Date functions
created >= startOfWeek()
updated >= startOfMonth(-1)
resolutiondate >= "-30d"
```

### Status and Workflow

```jql
status in ("To Do", "In Progress", "In Review")
status changed AFTER "2026-08-01"
status WAS "In Progress" BEFORE "2026-08-15"
resolution = Unresolved
resolution = Empty                  -- unresolved
status CHANGED FROM "In Progress" TO "Done" DURING (startOfDay(), now())
```

### Users and Assignees

```jql
assignee = currentUser()
assignee in (membersOf("jira-software-users"))
assignee is EMPTY
assignee is not EMPTY
assignee != currentUser()
reporter = currentUser()
watcher = currentUser()
```

### Custom Fields

```jql
-- Epic Link (ID varies)
"Epic Link" = EPIC-123
cf[10010] = "Frontend"
"Story Points" = 5
"Story Points" > 3 AND "Story Points" <= 8
labels in ("frontend", "auth")
labels is EMPTY
summary ~ "login"
description ~ "crash"
```

### JQL Functions

```jql
votedIssues()
watchedIssues()
linkedIssues(PROJ-123)
issuesInEpics(EPIC-123)
-- Cloud only:
issueFunction in commented("by bob@example.com AFTER startOfWeek()")
issueFunction in issuesInEpics("project = EPIC AND status != Done")
```

### Complex Queries

```jql
-- Unresolved bugs older than 30 days
project = PROJ AND issuetype = Bug AND resolution = Unresolved AND created < -30d ORDER BY created ASC

-- My work in active sprint
assignee = currentUser() AND sprint in openSprints() ORDER BY priority DESC, duedate ASC

-- Sprint planning candidates
project = PROJ AND status = "To Do" AND "Story Points" is not EMPTY ORDER BY priority DESC

-- Stale issues (not updated in 2 weeks)
project = PROJ AND updated < -14d AND status != Done

-- Cross-project blocker bugs
resolution = Unresolved AND issuetype = Bug AND priority = Highest ORDER BY created ASC

-- Velocity helper
project = PROJ AND issuetype in (Story, Bug) AND status = Done AND resolutiondate >= startOfYear()
```

### Pagination

JQL results default to `maxResults=50`, maximum `100` per request. For large datasets:

```python
# Traditional offset pagination
def paginate_jql(jql, batch_size=100):
    all_issues, start_at = [], 0
    while True:
        data = requests.post(f"{JIRA_URL}/rest/api/3/search",
            json={"jql": jql, "startAt": start_at, "maxResults": batch_size},
            auth=AUTH, headers=HEADERS).json()
        all_issues.extend(data["issues"])
        if start_at + batch_size >= data["total"]:
            break
        start_at += batch_size
    return all_issues
```

Jira Cloud also supports cursor-based pagination via `/rest/api/3/search/jql` with `nextPageToken` in the response. Prefer this for result sets over 1K issues.

## Webhook Integration

### Register Webhook (Cloud)

```bash
curl -s -X POST "https://your-domain.atlassian.net/rest/api/3/webhook" \
  -H "Content-Type: application/json" \
  -u "user@example.com:$JIRA_TOKEN" \
  -d '{
    "url": "https://your-server.com/jira-webhook",
    "events": ["jira:issue_created", "jira:issue_updated", "jira:issue_deleted"],
    "filters": {"issue-related-events-section": "project = PROJ"}
  }'
```

Events: `jira:issue_created`, `jira:issue_updated`, `jira:issue_deleted`, `jira:worklog_updated`, `comment_created`, `comment_updated`, `sprint_*`, `board_*`, `project_*`.

### Webhook Payload

```json
{
  "timestamp": 1771234567890,
  "webhookEvent": "jira:issue_updated",
  "user": {"accountId": "712020:abc123", "displayName": "John Doe"},
  "issue": {
    "id": "10001", "key": "PROJ-123",
    "fields": {"summary": "Fix login bug", "status": {"name": "In Progress"}}
  },
  "changelog": {
    "items": [{"field": "status", "fromString": "To Do", "toString": "In Progress"}]
  }
}
```

### Handler (Python / Flask)

```python
from flask import Flask, request
import hmac, hashlib, os

app = Flask(__name__)
SECRET = os.environ.get("JIRA_WEBHOOK_SECRET")

@app.route("/jira-webhook", methods=["POST"])
def handle_webhook():
    if SECRET:
        sig = request.headers.get("X-Hub-Signature", "")
        expected = "sha256=" + hmac.new(SECRET.encode(), request.data, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected): return ("", 403)

    event = request.json
    event_type = event.get("webhookEvent")
    issue = event.get("issue", {})
    changelog = event.get("changelog", {})

    if event_type == "jira:issue_created":
        handle_created(issue["key"], issue["fields"])
    elif event_type == "jira:issue_updated":
        for item in changelog.get("items", []):
            if item["field"] == "status":
                handle_transition(issue["key"], item["fromString"], item["toString"])

    return ("ok", 200)

@app.route("/jira-webhook", methods=["GET"])
def verify(): return ("ok", 200)  # Jira sends GET to verify URL on creation
```

### Incoming Webhooks (Jira Automation)

Jira Automation supports incoming webhooks that trigger rules. Create an Automation rule with trigger "Incoming webhook", then call the generated URL:

```bash
curl -s -X POST "https://automation.atlassian.com/pro/hooks/YOUR_WEBHOOK_ID" \
  -H "Content-Type: application/json" \
  -d '{"issueKey": "PROJ-123", "message": "Deploy completed"}'
```

## Sprint Management

### Automated Sprint Lifecycle

```python
import datetime

def create_sprint(board_id, name, start, end, goal=""):
    return requests.post(f"{JIRA_URL}/rest/agile/1.0/sprint", auth=AUTH, headers=HEADERS, json={
        "name": name, "originBoardId": board_id, "goal": goal,
        "startDate": start.isoformat(), "endDate": end.isoformat(),
    }).json()

def start_sprint(sprint_id):
    requests.post(f"{JIRA_URL}/rest/agile/1.0/sprint/{sprint_id}", json={"state": "active"}, auth=AUTH, headers=HEADERS)

def close_sprint(sprint_id):
    requests.post(f"{JIRA_URL}/rest/agile/1.0/sprint/{sprint_id}", json={"state": "closed"}, auth=AUTH, headers=HEADERS)

def get_active_sprint(board_id):
    resp = requests.get(f"{JIRA_URL}/rest/agile/1.0/board/{board_id}/sprint?state=active", auth=AUTH, headers=HEADERS)
    values = resp.json().get("values", [])
    return values[0] if values else None

def move_to_sprint(sprint_id, issue_keys):
    requests.post(f"{JIRA_URL}/rest/agile/1.0/sprint/{sprint_id}/issue",
                  json={"issues": issue_keys}, auth=AUTH, headers=HEADERS)

# Weekly sprint automation
board_id = 42
sprint_name = f"Sprint {datetime.date.today().isocalendar()[1]}"
if not get_active_sprint(board_id):
    sprint = create_sprint(board_id, sprint_name, datetime.date.today(),
                           datetime.date.today() + datetime.timedelta(days=14))
    move_to_sprint(sprint["id"], ["PROJ-123"])
    start_sprint(sprint["id"])
```

### Sprint Burndown

```python
def sprint_burndown(sprint_id):
    issues = []
    for start in range(0, 99999, 100):
        data = requests.get(f"{JIRA_URL}/rest/agile/1.0/sprint/{sprint_id}/issue",
            params={"startAt": start, "maxResults": 100}, auth=AUTH, headers=HEADERS).json()
        issues.extend(data["issues"])
        if start + 100 >= data["total"]: break
    total = sum(i["fields"].get("customfield_10016", 0) or 0 for i in issues)
    done = sum(i["fields"].get("customfield_10016", 0) or 0 for i in issues if i["fields"]["status"]["name"] == "Done")
    return {"total": total, "completed": done, "remaining": total - done}
```

## Common Patterns

### Sprint Planning Automation

1. Close completed issues at sprint end, move incomplete to backlog
2. Calculate team velocity (average completed story points over last 3 sprints)
3. Pull highest-priority backlog items matching capacity
4. Create sprint with issues pre-populated
5. Notify team via Slack/email

### Release Management

```python
def create_version(project_key, name, description, release_date):
    return requests.post(f"{JIRA_URL}/rest/api/3/version", auth=AUTH, headers=HEADERS, json={
        "project": project_key, "name": name, "description": description,
        "releaseDate": release_date.isoformat(),
    }).json()

def release_version(version_id):
    requests.put(f"{JIRA_URL}/rest/api/3/version/{version_id}",
        json={"released": True, "releaseDate": datetime.date.today().isoformat()},
        auth=AUTH, headers=HEADERS)
```

### Cross-Project Issue Linking

```python
def link_issues(inward, outward, link_type="Relates"):
    requests.post(f"{JIRA_URL}/rest/api/3/issueLink", auth=AUTH, headers=HEADERS, json={
        "inwardIssue": {"key": inward}, "outwardIssue": {"key": outward}, "type": {"name": link_type}})
```

### Time Tracking with Tempo API

```python
TEMPO_URL = "https://api.tempo.io/4"

def log_work(issue_key, account_id, description, seconds, date=None):
    requests.post(f"{TEMPO_URL}/worklogs", headers={"Authorization": f"Bearer {os.environ['TEMPO_TOKEN']}"},
        json={"issueKey": issue_key, "authorAccountId": {"accountId": account_id},
              "description": description, "timeSpentSeconds": seconds,
              "startDate": date or datetime.date.today().isoformat(), "startTime": "09:00:00"})
```

## Red Flags

| Issue | Impact | Mitigation |
|-------|--------|------------|
| **Rate limiting (Cloud)** | 6-8 req/s per instance; 403 on burst | Exponential backoff, batch requests, use webhooks instead of polling |
| **Rate limiting (Server)** | Configurable low defaults | Check with admin; cache responses with ETag/If-None-Match |
| **maxResults=100 ceiling** | Full export of 5K issues needs 50 API calls | Use cursor pagination (`/search/jql`), iterate with `startAt` |
| **JQL injection** | Concatenated user input can bypass auth or delete data | Parameterize JQL; validate input; never trust user-provided JQL fragments |
| **2FA kills basic auth** | Basic auth + 2FA = immediate 403 | Use API tokens (Cloud) or PATs (Server) — they bypass 2FA |
| **Transition ID drift** | IDs change after workflow edits | Always fetch `/transitions` dynamically; never hardcode |
| **Custom field ID drift** | IDs differ per instance | Discover via `/rest/api/3/field`; cache; use name aliases where possible |
| **ADF requirement (Cloud)** | Plain text descriptions rejected | Always use ADF for Cloud: `{"type":"doc","version":1,"content":[...]}` |
| **Server vs Cloud drift** | `/api/3` vs `/api/2` have subtle differences | Test against both deployment types; Server lacks many Cloud features |
| **Large export timeout** | 10K+ issues can timeout | Use `/search/export` (Data Center) or schedule CSV exports (Cloud) |
| **Webhook delivery failures** | Jira retries 24h, then drops | Monitor webhook health; implement idempotent handlers with dedup keys |

### Rate Limit Safety

```python
import time
def jira_request(method, url, **kwargs):
    for attempt in range(5):
        resp = requests.request(method, url, auth=AUTH, headers=HEADERS, **kwargs)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", 2 ** attempt)))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limit retries exhausted")
```

## Verification

- [ ] API token / PAT has correct project and issue permissions
- [ ] Transition IDs fetched dynamically from `/transitions`, not hardcoded
- [ ] Custom field IDs discovered via `/rest/api/3/field`
- [ ] JQL queries tested against target instance before automation
- [ ] Issue descriptions use ADF format (Cloud) or plain text (Server)
- [ ] Pagination handles `total > maxResults` with proper iteration
- [ ] Rate limits accounted for with retry/backoff logic
- [ ] Webhook endpoints idempotent (duplicate delivery doesn't double-process)
- [ ] Webhook handler responds within 10s (Jira timeout is 30s)
- [ ] OAuth tokens scoped correctly (`read:jira-work`, `write:jira-work`)
- [ ] Authentication secrets in env vars, not source code
- [ ] JQL injection prevented — input validated, not concatenated
- [ ] Release versions created before being referenced as fixVersion
- [ ] Cloud ID discovered for OAuth-based API calls

## Process

1. **Prepare** — Choose auth method (API token for Cloud, PAT for Server). Set env vars. Determine Jira URL and API version (`/api/3` vs `/api/2`).
2. **Discover** — Fetch project keys (`/project`), custom field IDs (`/field`), transition IDs, board/sprint IDs. Cache these — they change less than auth but more than code.
3. **Execute** — Build and test the Jira operation. Handle pagination for large result sets. Use exponential backoff for rate limits.
4. **Verify** — Read back created data. Confirm fields, statuses, and links are correct. Check permission schemes if access is denied.
5. **Monitor** — Set up webhook handlers for real-time events. Log API interactions. Monitor rate limit headers.
6. **Maintain** — Re-validate field IDs after workflow/custom field changes. Update tokens before expiry. Review API deprecation notices regularly.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Hardcoding transition IDs is faster" | IDs change when workflows are edited. Fetch dynamically or automation breaks silently. |
| "Basic auth works fine for my script" | Cloud deprecated basic auth in 2023. Use API tokens now. |
| "My webhook handler returns 200 immediately" | You must process the event before returning 200. Jira retries for 24h on errors. |
| "JQL is like SQL — I can concatenate user input" | `summary ~ " OR 1=1 --"` bypasses access controls. Validate or parameterize everything. |
| "100 maxResults is enough" | 5K issues = 50 calls. Use cursor pagination for Cloud; offset pagination for Server. |
| "Jira can replace our entire workflow" | Jira excels at structured tracking but is poor at CI/CD, doc review, or HR. Use purpose-built tools and integrate. |
| "Marketplace add-ons are always stable" | Tempo, ScriptRunner, Structure have their own API versions, rate limits, and failure modes. |
| "Cloud and Server have the same API" | Endpoints, field formats, and features differ significantly. Test against your deployment type. |
| "Jira Automation handles everything" | Complex cross-project workflows still need custom scripts. Jira Automation has a 100-rule limit on Cloud. |
