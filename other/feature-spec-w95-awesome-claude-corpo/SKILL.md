---
name: feature-spec
description: "Write detailed feature specifications with functional requirements, edge cases, data models, API contracts, and UX flows. Create comprehensive technical specifications that enable clear implementation."
---

# Feature Spec

## Overview
The Feature Spec skill enables product managers to write detailed, implementation-ready feature specifications that bridge design and engineering. It combines functional requirements, technical specifications, and UX flows into a single source of truth.

## When to Use This Skill
- Defining technical requirements for features
- Specifying API contracts and data models
- Documenting edge cases and error handling
- Creating UX flows and wireframes
- Ensuring design and engineering alignment
- Providing engineering with complete specifications
- Documenting complex interactions and workflows

## Feature Specification Template

### Executive Summary

**Feature Name:** [Clear, descriptive name]
**Feature ID:** [Unique identifier]
**Owner (PM):** [Name]
**Owner (Engineering):** [Name]
**Status:** [Draft / Review / Approved / In Development]
**Last Updated:** [Date]

**One-sentence description:**
[What does this feature do in user terms]

**Business context:**
[Why are we building this, customer problem, business goal]

**Key metrics:**
[How success will be measured]

---

## Functional Requirements

### Primary Use Cases

**Use Case 1: [Name]**
- Actor: [Who]
- Precondition: [System state before]
- Main flow:
  1. [Step 1]
  2. [Step 2]
  3. [Step 3]
- Alternative flows:
  - [If condition], then [steps]
- Postcondition: [System state after]
- Error handling: [What goes wrong]

### Detailed Functional Specifications

**Requirement 1: Real-Time Updates**

Description: When a team member updates a task, all other team members viewing that project should see the update within 2 seconds.

Acceptance criteria:
- Update broadcasts to all connected clients within 2 seconds
- Update includes: task ID, new status, old status, timestamp, user who made change
- Broadcast uses WebSocket (not polling)
- Works across different devices and browsers
- Offline users receive update upon reconnection

Technical notes:
- Requires persistent connection management
- Handle network failures gracefully
- Broadcast to all except sender (to avoid echo)

**Requirement 2: Activity Feed Display**

Description: Users can view a timeline of all changes to a project in reverse chronological order.

Acceptance criteria:
- Feed shows all activities (task updates, comments, assignments, status changes)
- Sorted by timestamp, newest first
- Each item shows: actor, action, target object, timestamp, context
- Feed loads initial 20 items, pagination for more
- User can filter by: activity type, assignee, task, date range
- Search activity by keywords

Technical notes:
- Paginate to prevent massive data loads
- Create composite activity from multiple sub-events (group updates in same minute)
- Store in activity table with denormalized fields for performance

**Requirement 3: Notification Delivery**

Description: Users receive notifications when activities relevant to them occur.

Acceptance criteria:
- User receives notification within 5 seconds of event
- Notification includes: who, what action, what object, context link
- User can configure which activity types trigger notifications
- User can choose delivery method: in-app, email, Slack, mobile push
- User can set do-not-disturb hours (no notifications outside hours)
- Notifications grouped to prevent fatigue (max 1 email per hour)

Technical notes:
- Different notification channels have different latency (email slower than in-app)
- Respect user preferences in configuration
- Implement batching for notifications

---

## Edge Cases and Error Handling

### Error Scenarios

**Scenario 1: Network Disconnection During Status Update**
- User updates task status on mobile
- Network drops before confirmation
- Expected behavior:
  - UI shows "pending" state
  - Auto-retry when connection restored
  - Show error if retry fails after 3 attempts
  - Allow manual retry
- Technical approach:
  - Queue updates locally (IndexedDB)
  - Sync when connection restored
  - Handle conflicts if status changed during disconnect

**Scenario 2: Duplicate Update Event**
- Same update received twice (network retry)
- Expected behavior:
  - Deduplicate on client and server
  - No duplicate activity feed entry
  - Idempotent update (safe to apply twice)
- Technical approach:
  - Include event ID with update
  - Check for duplicate on server before processing
  - Return 200 OK even if already processed

**Scenario 3: Concurrent Updates to Same Task**
- Two users update same task simultaneously
- Expected behavior:
  - Both updates apply (not last-write-wins)
  - No data loss
  - Feed shows both updates in order
  - No conflicts or corruption
- Technical approach:
  - Use operational transformation or conflict-free replicas
  - Timestamp-based ordering for feed
  - Test with load testing

**Scenario 4: User Permissions Changed During Viewing**
- User viewing project loses permission (removed from team)
- Expected behavior:
  - Activity feed disappears or error message
  - User redirected to accessible page
  - No sensitive data leaked
- Technical approach:
  - Server checks permission before returning data
  - Client handles 403 Forbidden gracefully
  - Show clear error message

**Scenario 5: Very Large Activity Feeds** (1000+ items)
- Project with year-long history of activities
- Expected behavior:
  - Feed still loads quickly
  - Pagination works smoothly
  - Search performance acceptable
- Technical approach:
  - Index on timestamps and filters
  - Database query optimization
  - Virtual scrolling on client

---

## Data Model Specifications

### Database Schema

**Table: activities**
```sql
CREATE TABLE activities (
  id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(id),
  actor_id UUID NOT NULL REFERENCES users(id),
  action_type VARCHAR(50) NOT NULL,
    -- task_status_changed, task_comment_added, task_assigned, etc.
  target_type VARCHAR(50) NOT NULL,
    -- task, comment, assignment, project
  target_id UUID NOT NULL,
    -- ID of the object being changed
  old_value JSONB,
    -- Previous state (for updates): { "status": "todo" }
  new_value JSONB,
    -- New state: { "status": "done" }
  metadata JSONB,
    -- Extra context: { "duration_hours": 8, "effort_score": 5 }
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

  CONSTRAINT check_values CHECK (
    (old_value IS NOT NULL OR new_value IS NOT NULL)
  )
);

CREATE INDEX idx_activities_project_created
  ON activities(project_id, created_at DESC);

CREATE INDEX idx_activities_actor_created
  ON activities(actor_id, created_at DESC);
```

**Table: notification_preferences**
```sql
CREATE TABLE notification_preferences (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES users(id),

  -- Activity type toggles
  task_status_changed BOOLEAN DEFAULT true,
  task_comment_added BOOLEAN DEFAULT true,
  task_assigned_to_me BOOLEAN DEFAULT true,

  -- Delivery method (can choose multiple)
  email_enabled BOOLEAN DEFAULT true,
  in_app_enabled BOOLEAN DEFAULT true,
  slack_enabled BOOLEAN DEFAULT false,
  mobile_push_enabled BOOLEAN DEFAULT true,

  -- Do not disturb
  dnd_enabled BOOLEAN DEFAULT false,
  dnd_start TIME,  -- 22:00
  dnd_end TIME,    -- 08:00

  -- Batching
  email_batch_frequency VARCHAR(20) DEFAULT 'hourly',
    -- realtime, daily, weekly, never

  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Table: activity_subscriptions**
```sql
CREATE TABLE activity_subscriptions (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  resource_type VARCHAR(50) NOT NULL,  -- task, project
  resource_id UUID NOT NULL,
  subscription_type VARCHAR(50) NOT NULL,
    -- all_activities, mentions_only, assigned_only
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_user_resource_subscription
  ON activity_subscriptions(user_id, resource_type, resource_id);
```

### Data Dictionary

**Field: action_type**
- Type: VARCHAR(50)
- Valid values:
  - task_status_changed: Task moved to different status
  - task_comment_added: Comment added to task
  - task_assigned: Task assigned to user
  - task_unassigned: Task unassigned from user
  - task_description_updated: Description field modified
  - task_due_date_changed: Due date modified
  - task_priority_changed: Priority modified
  - project_created: Project created
  - project_deleted: Project deleted
  - team_member_added: Team member added to project
  - team_member_removed: Team member removed from project

**Field: old_value and new_value**
- Type: JSONB
- Structure depends on action_type
- Examples:
  ```json
  // For task_status_changed
  {
    "old": { "status": "todo" },
    "new": { "status": "in_progress" }
  }

  // For task_comment_added
  {
    "new": {
      "comment_id": "abc123",
      "text": "This is a comment",
      "commenter": "Sarah"
    }
  }

  // For task_assigned
  {
    "new": {
      "assignee_id": "user123",
      "assignee_name": "John"
    }
  }
  ```

---

## API Specifications

### Endpoint: Get Activity Feed

**Request:**
```
GET /api/v1/projects/{projectId}/activities

Query parameters:
- limit: number (default: 20, max: 100)
- offset: number (default: 0)
- action_type: string (optional, filter)
- actor_id: string (optional, filter)
- start_date: ISO8601 (optional, filter)
- end_date: ISO8601 (optional, filter)
- search: string (optional, keyword search)

Headers:
- Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": "activity-123",
      "project_id": "proj-456",
      "actor": {
        "id": "user-789",
        "name": "Sarah Chen",
        "avatar_url": "https://..."
      },
      "action_type": "task_status_changed",
      "action_label": "changed status",
      "target": {
        "type": "task",
        "id": "task-999",
        "name": "Build user auth",
        "url": "/tasks/task-999"
      },
      "old_value": { "status": "todo" },
      "new_value": { "status": "in_progress" },
      "created_at": "2024-02-20T14:30:00Z",
      "metadata": {
        "duration_in_status": "2 days"
      }
    }
  ],
  "pagination": {
    "total": 250,
    "offset": 0,
    "limit": 20,
    "has_more": true
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

**Response (403 Forbidden):**
```json
{
  "error": "Forbidden",
  "message": "You don't have access to this project"
}
```

### Endpoint: Update Task Status (triggering activity)

**Request:**
```
PATCH /api/v1/tasks/{taskId}

Body:
{
  "status": "in_progress"
}

Headers:
- Authorization: Bearer {token}
- Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "id": "task-999",
  "name": "Build user auth",
  "status": "in_progress",
  "updated_at": "2024-02-20T14:30:00Z",
  "activity_id": "activity-123"
}
```

**Activity created automatically:**
- action_type: task_status_changed
- old_value: { "status": "todo" }
- new_value: { "status": "in_progress" }

### Endpoint: Update Notification Preferences

**Request:**
```
PUT /api/v1/notifications/preferences

Body:
{
  "email_enabled": true,
  "in_app_enabled": true,
  "slack_enabled": false,
  "mobile_push_enabled": true,
  "email_batch_frequency": "hourly",
  "dnd_enabled": true,
  "dnd_start": "22:00",
  "dnd_end": "08:00"
}
```

**Response (200 OK):**
```json
{
  "id": "pref-123",
  "user_id": "user-789",
  "email_enabled": true,
  "in_app_enabled": true,
  "slack_enabled": false,
  "mobile_push_enabled": true,
  "updated_at": "2024-02-20T14:30:00Z"
}
```

### WebSocket: Real-time Activity Broadcast

**Connect:**
```
WS /api/v1/ws?token={token}&project_id={projectId}
```

**Subscribe to project activities:**
```json
{
  "type": "subscribe",
  "project_id": "proj-456"
}
```

**Receive activity (broadcasted):**
```json
{
  "type": "activity_created",
  "data": {
    "id": "activity-123",
    "project_id": "proj-456",
    "action_type": "task_status_changed",
    "actor": { "id": "user-789", "name": "Sarah Chen" },
    "target": { "type": "task", "id": "task-999", "name": "Build user auth" },
    "new_value": { "status": "in_progress" },
    "created_at": "2024-02-20T14:30:00Z"
  }
}
```

---

## User Experience Flows

### Flow 1: Viewing Activity Feed

**Screen 1: Activity Feed List**
```
┌─────────────────────────────────────┐
│ Activity Feed                       │
├─────────────────────────────────────┤
│ [Filter ▼] [Search _______________] │
├─────────────────────────────────────┤
│ Sarah Chen changed status           │
│ "Build auth" → in progress          │
│ 2 hours ago                         │
│                                     │
│ John Lee added comment              │
│ "Build auth" - "Great progress"     │
│ 3 hours ago                         │
│                                     │
│ Project created "Mobile App"        │
│ by Jane Doe                         │
│ Yesterday                           │
│                                     │
│ [Load more]                         │
└─────────────────────────────────────┘
```

**Interactions:**
- Click on activity → navigate to task/object
- Click filter → show options (type, date, assignee)
- Type in search → filter by keywords
- Scroll to bottom → load more items
- Real-time: New activities appear at top

### Flow 2: Updating Task Status (triggering activity)

**Current state:** Task in "todo" status

**User action:** Click task, change status dropdown to "in_progress"

**System behavior:**
1. API call to update task (PATCH /api/v1/tasks/{id})
2. Server updates task status
3. Server creates activity record automatically
4. Server broadcasts activity via WebSocket
5. Client receives broadcast
6. Activity appears in feed in real-time for all connected users
7. UI shows optimistic update (status changes immediately)

### Flow 3: Configuring Notifications

**Screen: Notification Settings Modal**
```
┌──────────────────────────────────────┐
│ Notification Preferences             │
├──────────────────────────────────────┤
│ Activity Types                       │
│ ☑ Task status changed                │
│ ☑ Task assigned to me                │
│ ☑ New comments                       │
│ ☐ Task description updated           │
│                                      │
│ Delivery Methods                     │
│ ☑ Email                              │
│ ☑ In-app                             │
│ ☐ Slack                              │
│ ☑ Mobile push                        │
│                                      │
│ Email Settings                       │
│ Batch frequency: [Hourly ▼]          │
│                                      │
│ Do Not Disturb                       │
│ ☑ Enabled                            │
│ From: [22:00] To: [08:00]            │
│                                      │
│ [Save] [Cancel]                      │
└──────────────────────────────────────┘
```

---

## Performance Requirements

### Response Time Targets

| Operation | Target | Acceptable | Unacceptable |
|-----------|--------|-----------|-------------|
| Get activity feed | 500ms | 1s | >2s |
| Real-time broadcast | 2s | 3s | >5s |
| Update task status | 1s | 2s | >3s |
| Search activities | 1s | 2s | >3s |
| Load notifications settings | 500ms | 1s | >2s |

### Scalability Requirements

- Support 10,000 concurrent WebSocket connections per server
- Handle 1,000 activities created per minute
- Activity feeds with 100,000+ items must load <2 seconds
- Database queries must return in <500ms for p95

### Data Volume Estimates

- Activities table: ~100M rows (1 year of data)
- Notification preferences: 1M rows (1 user per row)
- Daily activities created: 50K - 500K (depends on usage)

---

## Acceptance Criteria

- [ ] All functional requirements implemented
- [ ] All acceptance criteria met and tested
- [ ] All edge cases handled appropriately
- [ ] All error scenarios tested
- [ ] Performance targets met (p95 latency)
- [ ] Scalability tested with load testing
- [ ] Security review completed
- [ ] Data consistency verified
- [ ] Documentation complete
- [ ] QA testing approved
- [ ] Product Manager sign-off obtained
- [ ] Ready for launch

---

## Output Deliverables

1. **Feature Specification Document** - Complete spec (20-30 pages)
2. **Data Model Diagrams** - Schema visualization
3. **API Documentation** - OpenAPI/Swagger definition
4. **UX Flow Diagrams** - User journey for each feature
5. **Wireframes** - UI mockups for each screen
6. **Error Handling Guide** - Edge cases and responses
7. **Performance Baseline** - Load testing results
8. **Implementation Checklist** - Engineer handoff document
