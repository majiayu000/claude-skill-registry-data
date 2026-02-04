---
name: datadog-auto-detector
description: Automatically detects Datadog resource mentions (URLs, service queries, natural language) and intelligently fetches condensed context via datadog-analyzer subagent when needed for the conversation (plugin:schovi@schovi-workflows)
---

# Datadog Auto-Detector Skill

**Purpose**: Detect when user mentions Datadog resources and intelligently fetch relevant observability data.

**Architecture**: Three-tier pattern (Skill → Command → Subagent) for context isolation.

## Detection Patterns

### Pattern 1: Datadog URLs

Detect full Datadog URLs across all resource types:

**Logs**:
- `https://app.datadoghq.com/.../logs?query=...`
- `https://app.datadoghq.com/.../logs?...`

**APM / Traces**:
- `https://app.datadoghq.com/.../apm/traces?query=...`
- `https://app.datadoghq.com/.../apm/trace/[trace-id]`
- `https://app.datadoghq.com/.../apm/services/[service-name]`

**Metrics**:
- `https://app.datadoghq.com/.../metric/explorer?query=...`
- `https://app.datadoghq.com/.../metric/summary?metric=...`

**Dashboards**:
- `https://app.datadoghq.com/.../dashboard/[dashboard-id]`

**Monitors**:
- `https://app.datadoghq.com/.../monitors/[monitor-id]`
- `https://app.datadoghq.com/.../monitors?query=...`

**Incidents**:
- `https://app.datadoghq.com/.../incidents/[incident-id]`
- `https://app.datadoghq.com/.../incidents?...`

**Services**:
- `https://app.datadoghq.com/.../services/[service-name]`

**Events**:
- `https://app.datadoghq.com/.../event/stream?query=...`

**RUM**:
- `https://app.datadoghq.com/.../rum/...`

**Infrastructure/Hosts**:
- `https://app.datadoghq.com/.../infrastructure/...`

### Pattern 2: Natural Language Queries

Detect observability-related requests:

**Metrics Queries**:
- "error rate of [service]"
- "check metrics for [service]"
- "CPU usage of [service]"
- "latency of [service]"
- "throughput for [service]"
- "request rate"
- "response time"

**Log Queries**:
- "logs for [service]"
- "log errors in [service]"
- "show logs from [service]"
- "check [service] logs"
- "error logs"

**Trace Queries**:
- "traces for [service]"
- "trace [trace-id]"
- "slow requests in [service]"
- "APM data for [service]"

**Incident Queries**:
- "active incidents"
- "show incidents"
- "SEV-1 incidents"
- "current incidents for [team]"

**Monitor Queries**:
- "alerting monitors"
- "check monitors for [service]"
- "show triggered monitors"

**Service Queries**:
- "status of [service]"
- "health of [service]"
- "[service] dependencies"

### Pattern 3: Service Name References

Detect service names in context of observability:
- Common patterns: `pb-*`, `service-*`, microservice names
- Context keywords: "service", "application", "component", "backend", "frontend"
- Combined with observability verbs: "check", "show", "analyze", "investigate"

## Intelligence: When to Fetch

### ✅ DO Fetch When:

1. **Direct Request**: User explicitly asks for Datadog data
   - "Can you check the error rate?"
   - "Show me logs for pb-backend-web"
   - "What's happening in Datadog?"

2. **Datadog URL Provided**: User shares Datadog link
   - "Look at this: https://app.datadoghq.com/.../logs?..."
   - "Here's the dashboard: [URL]"

3. **Investigation Context**: User is troubleshooting
   - "I'm seeing errors in pb-backend-web, can you investigate?"
   - "Something's wrong with the service, check Datadog"

4. **Proactive Analysis**: User asks for analysis that requires observability data
   - "Analyze the performance of [service]"
   - "Is there an outage?"

5. **Comparative Analysis**: User wants to compare or correlate
   - "Compare error rates between services"
   - "Check if logs match the incident"

### ❌ DON'T Fetch When:

1. **Past Tense Without URL**: User mentions resolved issues
   - "I fixed the error rate yesterday"
   - "The logs showed X" (without asking for current data)

2. **Already Fetched**: Datadog data already in conversation
   - Check conversation history for recent Datadog summary
   - Reuse existing data unless user requests refresh

3. **Informational Discussion**: User discussing concepts
   - "Datadog is a monitoring tool"
   - "We use Datadog for observability"

4. **Vague Reference**: Unclear what to fetch
   - "Something in Datadog" (too vague)
   - Ask for clarification instead

5. **Historical Context**: User providing background
   - "Last week Datadog showed..."
   - "According to Datadog docs..."

## Intent Classification

Before spawning subagent, classify the user's intent:

**Intent Type 1: Full Context** (default)
- User wants comprehensive analysis
- Fetch all relevant data for the resource
- Example: "Analyze error rate of pb-backend-web"

**Intent Type 2: Specific Query**
- User wants specific metric/log/trace
- Focus fetch on exact request
- Example: "Show me error logs for pb-backend-web in last hour"

**Intent Type 3: Quick Status Check**
- User wants high-level status
- Fetch summary data only
- Example: "Is pb-backend-web healthy?"

**Intent Type 4: Investigation**
- User is debugging an issue
- Fetch errors, incidents, traces
- Example: "Users report 500 errors, investigate pb-backend-web"

**Intent Type 5: Comparison**
- User wants to compare metrics/services
- Fetch data for multiple resources
- Example: "Compare error rates of pb-backend-web and pb-frontend"

## Workflow

### Step 1: Detect Mention

Scan user message for:
1. Datadog URLs (Pattern 1)
2. Natural language queries (Pattern 2)
3. Service names with observability context (Pattern 3)

If none detected, **do nothing**.

### Step 2: Check Conversation History

Before fetching, check if:
- Same resource already fetched in last 5 messages
- Recent Datadog summary covers this request
- User explicitly requests refresh ("latest data", "check again")

If already fetched and no refresh requested, **reuse existing data**.

### Step 3: Determine Intent

Analyze user message to classify intent (Full Context, Specific Query, Quick Status, Investigation, Comparison).

Extract:
- **Resource Type**: logs, metrics, traces, incidents, monitors, services, dashboards
- **Service Name**: If mentioned (e.g., "pb-backend-web")
- **Time Range**: If specified (e.g., "last hour", "today", "last 24h")
- **Filters**: Any additional filters (e.g., "status:error", "SEV-1")

### Step 4: Construct Subagent Prompt

Build prompt for `datadog-analyzer` subagent:

```
Fetch and summarize [resource type] for [context].

[If URL provided]:
Datadog URL: [url]

[If natural language query]:
Service: [service-name]
Query Type: [logs/metrics/traces/etc.]
Time Range: [from] to [to]
Additional Context: [user's request]

Intent: [classified intent]

Focus on: [specific aspects user cares about]
```

### Step 5: Spawn Subagent

Use Task tool with:
- **subagent_type**: `"schovi:datadog-auto-detector:datadog-analyzer"`
- **prompt**: Constructed prompt from Step 4
- **description**: Short description (e.g., "Fetching Datadog logs summary")

### Step 6: Present Summary

When subagent returns:
1. Present the summary to user
2. Offer to investigate further if issues found
3. Suggest related queries if relevant

## Examples

### Example 1: Datadog URL

**User**: "Look at this: https://app.datadoghq.com/.../logs?query=service:pb-backend-web%20status:error"

**Action**:
1. Detect: Datadog logs URL
2. Check: Not in recent conversation
3. Intent: Full Context (investigation)
4. Prompt: "Fetch and summarize logs from Datadog URL: [url]"
5. Spawn: datadog-analyzer subagent
6. Present: Summary of error logs

### Example 2: Natural Language Query

**User**: "Can you check the error rate of pb-backend-web service in the last hour?"

**Action**:
1. Detect: "error rate" + "pb-backend-web" + "last hour"
2. Check: Not in recent conversation
3. Intent: Specific Query (metrics)
4. Prompt: "Fetch and summarize metrics for error rate. Service: pb-backend-web, Time Range: last 1h"
5. Spawn: datadog-analyzer subagent
6. Present: Metrics summary with error rate trend

### Example 3: Investigation Context

**User**: "Users are reporting 500 errors on the checkout flow. Can you investigate?"

**Action**:
1. Detect: "500 errors" (observability issue)
2. Check: Not in recent conversation
3. Intent: Investigation
4. Prompt: "Investigate 500 errors in checkout flow. Query Type: logs and traces, Filters: status:500 OR status:error, Time Range: last 1h. Focus on: error patterns, affected endpoints, trace analysis"
5. Spawn: datadog-analyzer subagent
6. Present: Investigation summary with findings

### Example 4: Already Fetched

**User**: "Show me error rate for pb-backend-web"

[Datadog summary for pb-backend-web fetched 2 messages ago]

**Action**:
1. Detect: "error rate" + "pb-backend-web"
2. Check: Already fetched in message N-2
3. **Skip fetch**: "Based on the Datadog data fetched earlier, the error rate for pb-backend-web is [value]..."

### Example 5: Past Tense (No Fetch)

**User**: "Yesterday Datadog showed high error rates"

**Action**:
1. Detect: "Datadog" + "error rates"
2. Check: Past tense ("Yesterday", "showed")
3. **Skip fetch**: User is providing historical context, not requesting current data

### Example 6: Comparison

**User**: "Compare error rates of pb-backend-web and pb-frontend over the last 24 hours"

**Action**:
1. Detect: "error rates" + multiple services + "last 24 hours"
2. Check: Not in recent conversation
3. Intent: Comparison
4. Prompt: "Fetch and compare metrics for error rate. Services: pb-backend-web, pb-frontend. Time Range: last 24h. Focus on: comparative analysis, trends, spikes"
5. Spawn: datadog-analyzer subagent
6. Present: Comparative metrics summary

## Edge Cases

### Ambiguous Service Name

**User**: "Check the backend service error rate"

**Action**:
- Detect: "backend service" (ambiguous)
- Ask: "I can fetch error rate data from Datadog. Which specific service? (e.g., pb-backend-web, pb-backend-api)"
- Wait for clarification before spawning subagent

### URL Parsing Failure

**User**: Provides malformed or partial Datadog URL

**Action**:
- Detect: Datadog domain but unparseable
- Spawn: Subagent with URL and note parsing might fail
- Subagent will attempt to extract what it can or report error

### Multiple Resources in One Request

**User**: "Show me logs, metrics, and traces for pb-backend-web"

**Action**:
- Detect: Multiple resource types requested
- Intent: Full Context (investigation)
- Prompt: "Fetch comprehensive observability data for pb-backend-web: logs (errors), metrics (error rate, latency), traces (slow requests). Time Range: last 1h"
- Spawn: Single subagent call (let subagent handle multiple queries)

## Integration Notes

**Proactive Activation**: This skill should activate automatically when Datadog resources are mentioned.

**No User Prompt**: The skill should work silently - user doesn't need to explicitly invoke it.

**Commands Integration**: This skill can be used within commands like `/schovi:analyze` to fetch Datadog context automatically.

**Token Efficiency**: By using the subagent pattern, we reduce context pollution from 10k-50k tokens to ~800-1200 tokens.

## Quality Checklist

Before spawning subagent, verify:
- [ ] Clear detection of Datadog resource or query
- [ ] Not already fetched in recent conversation (unless refresh requested)
- [ ] Not past tense reference without current data request
- [ ] Intent classified correctly
- [ ] Prompt for subagent is clear and specific
- [ ] Fully qualified subagent name used: `schovi:datadog-auto-detector:datadog-analyzer`
