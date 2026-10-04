---
name: jira-rca-ticket
enabled: true
description: Create Jira tickets from incident RCA findings. Automatically generates structured tickets with root cause analysis, severity classification, and remediation steps.
required_connections:
  - prefix: atlassian
    label: "Jira / Atlassian"
config_fields:
  - key: project_key
    label: "Project Key"
    required: true
    placeholder: "e.g., OPS"
  - key: issue_type
    label: "Default Issue Type"
    required: false
    placeholder: "e.g., Bug"
features:
  - RCA
---

# Jira RCA Ticket Creation

Create structured Jira tickets from incident Root Cause Analysis findings.

## Prerequisites

Before executing this skill, ensure:
1. The RCA analysis has been completed and findings are available in context
2. The Atlassian connection is configured with Jira access
3. The target project `{{config.project_key}}` exists and is accessible

## Discovery

<critical>
**Run discovery first to get the cloudId and validate the project:**
```bash
bun run ./_skills/connections/jira/tracking-jira/scripts/discover.ts
```
This provides the `cloudId`, available projects, and issue types.
</critical>

## Workflow

### Step 1: Validate Project and Issue Type

```typescript
const resources = await getAccessibleAtlassianResources();
const cloudId = resources[0].id;
const siteUrl = resources[0].url;

const metadata = await getJiraProjectIssueTypesMetadata({
  cloudId,
  projectIdOrKey: '{{config.project_key}}'
});
```

Verify that the configured issue type exists in the project. If `{{config.issue_type}}` is not specified, default to "Bug". If the specified issue type does not exist, fall back to "Bug" or "Task".

### Step 2: Extract RCA Information

From the RCA context, extract and structure the following:

| Field | Source | Required |
|-------|--------|----------|
| Incident title | RCA summary | Yes |
| Root cause | RCA root cause analysis | Yes |
| Severity | RCA severity classification | Yes |
| Impact | RCA impact assessment | Yes |
| Timeline | RCA incident timeline | Yes |
| Remediation steps | RCA recommendations | Yes |
| Affected services | RCA scope analysis | If available |
| Evidence | RCA supporting data | If available |

### Step 3: Format the Ticket Description

Structure the Jira ticket description using this template:

```
h2. Incident Summary
{summary_from_rca}

h2. Root Cause
{detailed_root_cause}

h2. Severity
*Level:* {severity_level}
*Justification:* {severity_justification}

h2. Impact
*Scope:* {impact_scope}
*Duration:* {impact_duration}
*Affected Services:* {affected_services}

h2. Timeline
{chronological_timeline_of_events}

h2. Remediation Steps
# {step_1}
# {step_2}
# {step_3}

h2. Prevention Measures
{long_term_prevention_recommendations}

h2. Evidence
{supporting_data_metrics_logs}
```

### Step 4: Create the Jira Ticket

```typescript
const result = await createJiraIssue({
  cloudId,
  projectKey: '{{config.project_key}}',
  issueTypeName: '{{config.issue_type}}' || 'Bug',
  summary: `[RCA] ${incidentTitle}`,
  description: formattedDescription
});

const ticketUrl = `${siteUrl}/browse/${result.key}`;
```

### Step 5: Set Priority and Labels

After creating the ticket, update it with appropriate metadata:

```typescript
await editJiraIssue({
  cloudId,
  issueIdOrKey: result.key,
  fields: {
    priority: { name: mapSeverityToPriority(severity) },
    labels: ['rca', 'incident', severityLabel]
  }
});
```

**Severity to Priority mapping:**
- Critical -> Highest
- High -> High
- Medium -> Medium
- Low -> Low

## Output

After successful creation, report:
1. The ticket key and URL: `{{config.project_key}}-XXX`
2. A brief summary of what was captured in the ticket
3. Any fields that could not be populated due to missing RCA data

## Error Handling

| Scenario | Action |
|----------|--------|
| Project not found | Report error with the configured project key `{{config.project_key}}` |
| Issue type not found | Fall back to "Bug", then "Task" |
| Permission denied | Report the permission error and required Jira permissions |
| Missing RCA data | Create ticket with available data, note missing sections |

## Formatting Rules

- Use Jira wiki markup (not Markdown) for the description field
- Use `h2.` for section headers
- Use `#` for ordered lists (remediation steps)
- Use `*` for unordered lists
- Use `*bold*` for emphasis
- Use `{code}` blocks for technical details
- Prefix the summary with `[RCA]` for easy filtering

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "We can skip some steps for this case" | Adapt the workflow steps, don't skip them | Skipped steps are where incidents and oversights originate |
| "The user seems to already know what to do" | Complete all workflow phases with the user | The workflow catches blind spots that experience alone misses |
| "This is a minor case, full process is overkill" | Scale the process down, don't turn it off | Minor cases become major when unstructured; the process scales, not disappears |
| "I'll fill in the details later" | Complete each section before moving on | Deferred details are forgotten; real-time capture is more accurate |
| "The template output isn't necessary" | Always produce the structured output format | Structured output enables comparison, audit trails, and handoff to other teams |

