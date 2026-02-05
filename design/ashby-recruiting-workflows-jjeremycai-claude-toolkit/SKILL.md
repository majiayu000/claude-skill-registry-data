---
name: Ashby Recruiting Workflows
description: This skill should be used when the user asks to "move candidate through pipeline", "schedule an interview", "manage applications", "track hiring progress", "source candidates", "advance to next stage", or mentions recruiting workflows in Ashby. Provides guidance on effective candidate pipeline management and recruiting best practices.
version: 0.1.0
---

# Ashby Recruiting Workflows

Comprehensive guidance for managing recruiting workflows in Ashby ATS. This skill covers candidate pipeline management, interview scheduling, application tracking, and hiring team coordination.

## Core Workflow: Candidate Pipeline

The standard recruiting pipeline flows through these stages:

```
Sourced → Applied → Phone Screen → Interview → Offer → Hired
                ↓           ↓          ↓
             Archived   Archived   Archived
```

### Moving Candidates Through Stages

To advance a candidate:
1. Get the application ID using `application_list` or `application_info`
2. Get available stages using `interview_stage_list` with the job ID
3. Use `application_change_stage` with the target stage ID

```python
# Example workflow
# 1. Find candidate's application
applications = application_list(candidateId="...")
app_id = applications[0]["id"]

# 2. Get available stages
stages = interview_stage_list(jobId=job_id)
next_stage = stages["Lead"]  # or "Phone Screen", "Onsite", etc.

# 3. Move to next stage
application_change_stage(applicationId=app_id, interviewStageId=next_stage["id"])
```

### Archiving (Rejecting) Candidates

When archiving an application, always provide an archive reason:

1. Get archive reasons using `archive_reason_list`
2. Use `application_change_stage` with an archived stage and `archiveReasonId`

Common archive reasons include:
- Not qualified
- Position filled
- Candidate withdrew
- No response
- Failed assessment

## Interview Scheduling Workflow

### Scheduling a New Interview

1. Identify the application using `application_list`
2. Find available interviewers using `user_list` or `user_search`
3. Create the schedule using `interview_schedule_create`

Required information:
- Application ID
- Interviewer user IDs (array)
- Start and end times (ISO 8601 format)
- Interview stage ID (optional but recommended)

```python
interview_schedule_create(
    applicationId="app-123",
    interviewerUserIds=["user-1", "user-2"],
    startTime="2024-01-15T14:00:00Z",
    endTime="2024-01-15T15:00:00Z",
    interviewStageId="stage-id"
)
```

### Rescheduling Interviews

Use `interview_schedule_update` with the schedule ID:

```python
interview_schedule_update(
    interviewScheduleId="schedule-123",
    startTime="2024-01-16T10:00:00Z",
    endTime="2024-01-16T11:00:00Z"
)
```

### Canceling Interviews

Always provide a reason when canceling:

```python
interview_schedule_cancel(
    interviewScheduleId="schedule-123",
    reason="Candidate requested reschedule"
)
```

## Candidate Management Best Practices

### Adding Candidates

When creating candidates, include as much information as possible:

```python
candidate_create(
    name="Jane Smith",
    email="jane@example.com",
    phoneNumber="+1-555-0123",
    linkedInUrl="https://linkedin.com/in/janesmith",
    location="San Francisco, CA",
    sourceId="referral-source-id"
)
```

### Tracking Candidate Sources

Always attribute candidates properly:
1. Get available sources using `source_list`
2. Set source when creating candidates or applications
3. Update source using `application_change_source` if needed

### Using Tags for Organization

Tags help filter and organize candidates:

```python
# Get available tags
tags = candidate_tag_list()

# Add tag to candidate
candidate_add_tag(candidateId="...", tagId="senior-engineer-tag")
```

Common tag strategies:
- Skill-based: "python", "react", "data-science"
- Status-based: "high-priority", "passive", "referral"
- Source-based: "conference-2024", "hackathon"

### Adding Notes

Document all candidate interactions:

```python
candidate_add_note(
    candidateId="...",
    note="Initial phone screen completed. Strong technical background, moving to onsite.",
    sendNotifications=False
)
```

## Application Workflow Patterns

### Sourcing New Candidates

1. Create candidate with `candidate_create`
2. Create application with `application_create`
3. Add to appropriate initial stage

```python
# Create and consider for job
candidate = candidate_create(name="...", email="...")
application_create(
    candidateId=candidate["id"],
    jobId="target-job-id",
    sourceId="linkedin-sourcing"
)
```

### Bulk Pipeline Review

To review current pipeline status:

```python
# Get all active applications for a job
apps = application_list(jobId="...", status="Active")

# Group by stage for reporting
for app in apps:
    stage = app["currentInterviewStage"]["name"]
    candidate = app["candidate"]["name"]
    # Process...
```

### Transferring Applications Between Jobs

Use `application_create` to consider a candidate for additional jobs without losing existing application history.

## Job Management

### Job Status Workflow

```
Draft → Open → Closed/Archived
```

- **Draft**: Job visible internally, not on careers page
- **Open**: Actively recruiting, visible on careers page
- **Closed**: Position filled
- **Archived**: No longer relevant

### Updating Job Status

```python
# Close job when position is filled
job_set_status(jobId="...", status="Closed")

# Reopen if needed
job_set_status(jobId="...", status="Open")
```

## Offer Workflow

### Creating Offers

After interview rounds complete:

```python
offer_create(
    applicationId="app-123",
    startDate="2024-02-01",
    offerDetails="Senior Engineer role, $150k base + equity"
)
```

### Tracking Offers

List and monitor offer status:

```python
offers = offer_list(applicationId="app-123")
# Check offer status, pending approvals, etc.
```

## Common Workflow Scenarios

### Scenario: Phone Screen Completed

1. Review notes from screening call
2. Add note with `candidate_add_note`
3. Move to next stage with `application_change_stage`
4. Schedule onsite with `interview_schedule_create`

### Scenario: Candidate Withdrawal

1. Get archive reasons with `archive_reason_list`
2. Find "Candidate Withdrew" reason
3. Archive with `application_change_stage` including archive reason

### Scenario: Internal Referral

1. Create candidate with `candidate_create`
2. Get referral source with `source_list`
3. Create application with source attribution
4. Add note crediting referring employee

## Pipeline Analytics

### Getting Pipeline Metrics

List applications by status to understand funnel:

```python
# Active candidates
active = application_list(jobId="...", status="Active")

# Hired
hired = application_list(jobId="...", status="Hired")

# Archived (rejected)
archived = application_list(jobId="...", status="Archived")
```

### Interview Load Analysis

Review upcoming interviews:

```python
from datetime import datetime, timedelta

schedules = interview_schedule_list(
    startTimeAfter=datetime.now().isoformat(),
    startTimeBefore=(datetime.now() + timedelta(days=7)).isoformat()
)
```

## Additional Resources

### Reference Files

For detailed Ashby API patterns, consult:
- **`references/api-patterns.md`** - Common API usage patterns and error handling

### Tools Reference

Core tools for workflows:
- `candidate_*` - Candidate management
- `application_*` - Application lifecycle
- `interview_schedule_*` - Scheduling
- `job_*` - Job management
- `offer_*` - Offers
