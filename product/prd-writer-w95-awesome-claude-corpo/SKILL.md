---
name: prd-writer
description: "Write comprehensive Product Requirements Documents with user stories, acceptance criteria, technical specifications, wireframe descriptions, and prioritization frameworks (RICE, MoSCoW). Create clear specifications for product teams."
---

# PRD Writer

## Overview
The PRD Writer skill guides product managers in creating clear, actionable Product Requirements Documents that align teams around feature specifications. It combines user-centered design, technical clarity, and business context to ensure successful implementation.

## When to Use This Skill
- Defining new features or products for development
- Communicating requirements to engineering teams
- Prioritizing features across roadmap
- Documenting feature specifications before development
- Communicating product vision to stakeholders
- Creating specifications for design and QA teams

## PRD Template and Structure

### Executive Summary

**Feature Name:** [Clear, descriptive name]
**Owner (PM):** [Name]
**Stakeholders:** [Engineering, Design, Marketing, Legal, etc.]
**Status:** [Draft, Under Review, Approved, In Development]
**Last Updated:** [Date]

**Vision Statement:**
[1-2 sentences describing the big picture)
Example: "Enable users to collaborate on projects in real-time, reducing communication overhead and improving team alignment."

**Business Objective:**
- Primary goal: [Increase retention/revenue/efficiency]
- Measurable target: [X% improvement in metric]
- Time frame: [Quarter/year target]

**User Problem Being Solved:**
[Describe the pain point this feature addresses]
"Users currently spend 30+ minutes in meetings synchronizing project status manually. This feature enables asynchronous updates, reducing meeting time by 50%."

**Success Criteria:**
- Adoption: [% of users adopting within 3 months]
- Engagement: [% of users using feature weekly]
- NPS impact: [Target +5 NPS points]
- Revenue: [$X MRR increase or $X cost savings]

---

### User Stories and Use Cases

**Primary Use Cases:**

**Use Case 1: Team Real-Time Collaboration**
- Actor: [Project team member]
- Precondition: [User is logged in, project open]
- Main flow:
  1. User updates task status
  2. Update broadcasts to team instantly
  3. Notification appears in activity feed
- Postcondition: [All team members see updated status]
- Alternative flows: [Connection lost, offline mode]

**Use Case 2: Asynchronous Status Reporting**
- Actor: [Remote team member]
- Precondition: [User is in different timezone]
- Main flow:
  1. User adds comment to task
  2. Comment appears in feed
  3. Manager receives daily digest
  4. Manager responds asynchronously
- Postcondition: [No synchronous meeting required]

### User Stories Framework

**Story 1: View Real-Time Updates**
```
As a [project manager]
I want to [see live updates of task status]
So that [I can monitor progress without status meetings]

Acceptance Criteria:
- When a team member updates task status, I see the update within 2 seconds
- Status changes show in the main project view
- Activity timeline shows all updates with timestamps
- Notifications alert me to priority changes
- I can filter updates by assignee or task type

Definition of Done:
- Code reviewed and approved
- Unit tests pass (>80% coverage)
- QA tested on Chrome, Firefox, Safari
- Product Manager has signed off
- Updated help documentation
```

**Story 2: Receive Activity Notifications**
```
As a [team lead]
I want to [control which activities trigger notifications]
So that [I'm not overwhelmed with alerts]

Acceptance Criteria:
- Notification settings are accessible in preferences
- I can enable/disable alerts by activity type
- I can choose delivery method (in-app, email, Slack)
- Settings persist across devices
- Changes apply immediately

Definition of Done:
- Backend stores notification preferences
- Frontend UI implemented and tested
- Email delivery tested
- Slack integration verified
- Analytics event added for tracking
```

**Story 3: Mobile Notification Delivery**
```
As a [remote employee]
I want to [receive notifications on my phone]
So that [I stay informed while away from desk]

Acceptance Criteria:
- Push notifications delivered to iOS and Android apps
- Notifications respect local time zone
- User can tap notification to jump to relevant item
- Notification includes context (project, task, change)
- Deep linking to specific feature works

Definition of Done:
- Push service integrated (Firebase Cloud Messaging)
- iOS and Android implementations complete
- Battery/battery testing on both platforms
- Deep linking tested on Android and iOS
```

---

### Detailed Specifications

#### Feature Specification Overview

**Feature Name:** [Name]
**Scope:** [What's included and explicitly NOT included]
**Dependencies:** [Features that must exist first]
**Data Model Changes:** [Database schema updates]

#### Functional Requirements

**Requirement 1: Real-Time Status Updates**
- System shall broadcast task status changes to all project members within 2 seconds
- Broadcast includes: task ID, new status, previous status, timestamp, user who made change
- System shall maintain 99.9% uptime for status broadcasting
- System shall handle up to 1,000 concurrent status updates per project

**Requirement 2: Activity Feed Display**
- Feed shall show all activity in reverse chronological order
- Each activity item shall include: actor, action, object, timestamp, context
- Feed shall paginate in 20-item increments
- User can filter feed by: activity type, assignee, task, date range
- Feed loads within 1 second for initial load, 500ms for pagination

**Requirement 3: Notification Delivery**
- System shall deliver notifications within 5 seconds of activity trigger
- User can choose delivery method per activity type: in-app, email, Slack, mobile push
- Notifications shall respect do-not-disturb hours (if configured)
- System shall batch notifications to prevent notification fatigue (max 1 email per hour)

#### Technical Specifications

**Technology Stack:**
- Frontend: [React 18, TypeScript]
- Backend: [Node.js, Express]
- Database: [PostgreSQL]
- Real-time: [WebSockets, Socket.io]
- Notifications: [SendGrid for email, FCM for mobile, Slack API]

**API Endpoints:**

```
POST /api/tasks/{taskId}/status
Updates task status, triggers broadcast

GET /api/projects/{projectId}/activity
Fetches activity feed with pagination

PUT /api/notifications/preferences
Updates user notification settings

POST /api/notifications/subscribe
Subscribes to WebSocket for real-time updates
```

**Database Schema Changes:**

```sql
CREATE TABLE activity_feeds (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  actor_id UUID REFERENCES users(id),
  action_type VARCHAR(50), -- task_updated, comment_added, etc.
  target_id UUID, -- task, comment, project
  target_type VARCHAR(50),
  changes JSONB, -- before/after values
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notification_settings (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  activity_type VARCHAR(50),
  email BOOLEAN DEFAULT true,
  in_app BOOLEAN DEFAULT true,
  slack BOOLEAN DEFAULT false,
  mobile_push BOOLEAN DEFAULT true,
  dnd_start TIME,
  dnd_end TIME
);
```

---

### UI/UX Specifications

#### Wireframe Descriptions

**Screen 1: Activity Feed**
```
[Header: "Activity"]
[Filter bar: Activity Type dropdown, Date range picker]
[Activity Item 1]
├─ [Avatar] [Name] [Action] [Context]
├─ [Timestamp] [2 hours ago]
└─ [Details: Task name, Previous → New status]

[Activity Item 2]
...
[Load more button]
```

**Screen 2: Notification Settings Modal**
```
[Header: "Notification Preferences"]
[Tabs: Delivery Methods | Do Not Disturb]

[Activity Type Toggles]
├─ Task Status Updated
│  ├─ ☑ Email ☑ In-app ☑ Mobile Push
│  ├─ Batch these notifications (dropdown: real-time, daily, weekly)
├─ New Comment
│  ├─ ☑ Email ☑ In-app ☑ Mobile Push
├─ Task Assigned to Me
│  ├─ ☑ Email ☑ In-app ☑ Mobile Push

[Save] [Cancel]
```

#### Design Considerations

- **Visual hierarchy:** Activity items show most important info first
- **Progressive disclosure:** Click item to see full details
- **Accessibility:** Color not only indicator (✓ + color for status changes)
- **Performance:** Virtual scrolling for large feeds (1000+ items)
- **Mobile:** Single-column layout, touch-friendly tap targets (44px min)

---

### Prioritization Framework: RICE

**RICE Scoring Formula:** (Reach × Impact × Confidence) / Effort

**Reach** (How many users affected in 3-month period)
- Example: 80% of active users = 8,000 users
- Scale: 0-10,000+

**Impact** (How much does this change user outcome)
- Massive (3x): Huge improvement in workflow
- High (2x): Significant improvement in efficiency
- Medium (1x): Noticeable improvement
- Low (0.5x): Minor improvement

**Confidence** (How confident are we in this estimate)
- High (100%): Based on customer data/usage patterns
- Medium (75%): Some user feedback, some assumptions
- Low (50%): Speculative, needs validation

**Effort** (How many person-weeks to implement)
- Small: 1-2 weeks
- Medium: 3-4 weeks
- Large: 5-8 weeks
- XL: 8+ weeks

**RICE Calculation Example:**
- Reach: 8,000 users
- Impact: 2x (high)
- Confidence: 75%
- Effort: 4 weeks

Rice Score = (8000 × 2 × 0.75) / 4 = 3,000

---

### Alternative Prioritization: MoSCoW

**Must Have** (Feature shipping incomplete without)
- Real-time status updates
- Activity notification system
- Notification delivery via email

**Should Have** (Important, ships in first iteration)
- Mobile push notifications
- Notification settings/preferences
- Activity feed filtering
- Do-not-disturb scheduling

**Could Have** (Nice to have, future iteration)
- Slack integration
- Custom notification batching
- Advanced activity analytics
- Activity timeline visualization

**Won't Have** (Explicitly out of scope)
- SMS notifications
- Voice notifications
- Calendar integration for notifications

---

### Timeline and Release Planning

**Phase 1: MVP (4 weeks)**
- Real-time status broadcasting (WebSocket)
- Activity feed (basic display)
- Email notifications
- Core notification settings
- **Release:** Target Quarter end

**Phase 2: Enhancement (3 weeks)**
- Mobile push notifications
- Advanced filtering and search
- Do-not-disturb scheduling
- Activity analytics
- **Release:** 2 weeks into next quarter

**Phase 3: Integration (4 weeks)**
- Slack integration
- Calendar sync
- Notification customization UI improvements
- **Release:** Mid-quarter

---

### Success Metrics

**Adoption:**
- Feature discoverability: 60% of users discover feature within 30 days
- Initial activation: 40% of users send at least one notification within week 1
- Weekly active users: 70% of users using feature weekly by month 3

**Engagement:**
- Daily active users: 50% of active users daily
- Activity feed views: Average 8 views per user per day
- Notification opens: 35% of delivered notifications opened

**Business Impact:**
- Time savings: Users report 30% reduction in status-checking time
- Meeting reduction: Average meeting duration reduced by 15 minutes/week
- Retention: Feature users have 10% higher 12-month retention

**Quality Metrics:**
- Notification delivery: 99.9% successful delivery rate
- Latency: 95% of updates delivered within 2 seconds
- Error rate: <0.1% of operations result in error

---

### Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| WebSocket scalability issues | High | Medium | Load test with 10K concurrent users before launch |
| Notification fatigue causing opt-outs | High | Medium | Implement smart batching and do-not-disturb by default |
| Mobile app notification permissions | Medium | High | Provide clear education on benefits before permission request |
| Slack integration delays | Low | Medium | Build without Slack first, add as phase 2 |

---

## PRD Approval Checklist

- [ ] User stories clear and testable
- [ ] Acceptance criteria comprehensive
- [ ] Technical feasibility confirmed by engineering
- [ ] Design mockups reviewed and approved
- [ ] Success metrics defined and measurable
- [ ] Timeline realistic and estimated
- [ ] Risks identified and mitigation planned
- [ ] Dependencies documented
- [ ] Stakeholder sign-offs obtained
- [ ] PRD reviewed by design, engineering, QA, marketing
- [ ] Open questions resolved
- [ ] Ready for development kick-off

## Output Deliverables

1. **Full PRD Document** - All sections above, 15-20 pages
2. **Design Mockups/Wireframes** - High-fidelity or detailed wireframes
3. **Technical Specification** - API contracts, data models, schemas
4. **User Stories & Acceptance Criteria** - JIRA-ready format
5. **Success Metrics Dashboard** - Definition of all KPIs
6. **Timeline/Roadmap** - Phased release plan
7. **Risk Register** - Risks and mitigation strategies
