---
name: internal-comms
description: Write consistent, high-quality internal communications (status reports, 3P updates, newsletters, FAQs, incident reports). Use company standards and formats for all internal messaging.
compatibility:
  use-case: Internal communication, status updates, team coordination
  frameworks: Company communication standards, documentation templates
---

# Internal Communications

## Use This Skill When

- Writing progress, plans, and problems (3P) team updates
- Creating company-wide newsletters or announcements
- Responding to FAQs or common questions
- Drafting status reports for leadership
- Documenting project updates or milestones
- Writing incident reports or postmortems
- Any internal company communication requiring consistent format

## When NOT to Use

- External communications (PR, customer-facing messaging)
- Marketing copy or promotional content
- Personal messages not following company standards
- Highly sensitive legal/compliance matters

## Context: Communication Standards Maturity

**Undeveloped**: Inconsistent formats, unclear messaging, no structure.

**Target**: Follow company templates, consistent tone, clear structure for each communication type.

**Optimized**: Automated formatting, tone consistency checking, cross-team alignment.

## Core Principle

**Consistency builds clarity.** Using standardized formats for internal comms ensures information is where people expect it, leadership gets the signals they need, and team alignment increases.

## Instructions

### Step 1: Identify Communication Type

**Determine which category your communication falls into:**

| Type | Purpose | Frequency | Audience |
|------|---------|-----------|----------|
| **3P Update** | Progress, Plans, Problems | Weekly | Team + Manager |
| **Company Newsletter** | Broad updates, announcements | Monthly/Quarterly | All-hands |
| **FAQ Response** | Answer common questions | As-needed | Public/Team |
| **Status Report** | Leadership summary | Bi-weekly/Monthly | Executives |
| **Project Update** | Specific project progress | As milestone reached | Stakeholders |
| **Incident Report** | Critical issue documentation | Urgent + Postmortem | Team + Leadership |

### Step 2: Load Appropriate Template

**Reference the company's guideline file:**

- **3P Updates** → `examples/3p-updates.md`
  - Format: Progress, Plans, Problems
  - Length: 3-5 paragraphs
  - Frequency: Weekly Monday

- **Company Newsletters** → `examples/company-newsletter.md`
  - Format: Highlights, wins, upcoming events
  - Length: 2-3 pages
  - Audience: All employees

- **FAQ Responses** → `examples/faq-answers.md`
  - Format: Question + answer + context
  - Length: Concise but complete
  - Searchability: Important for discovery

- **General Communications** → `examples/general-comms.md`
  - Format: Flexible but structured
  - Use when type doesn't match above

### Step 3: Follow Template Structure

**Example: 3P Update Template**

```markdown
# 3P Update: [Your Name/Team] — [Week of DATE]

## Progress ✅
- [Completed milestone 1] — [brief context]
- [Completed milestone 2] — [brief context]
- [Progress on major item] — [% complete or status]

*Key win this week*: [Highlight one significant achievement]

## Plans 📋
- [Next priority 1] — starting [date]
- [Next priority 2] — starting [date]
- [Blocking item] — need [resource] by [date]

*Key upcoming milestone*: [Major deliverable date]

## Problems ⚠️
- [Issue 1] — impact: [X], resolution timeline: [Y]
- [Issue 2] — impact: [X], resolution timeline: [Y]

*How to help*: We need [specific ask] to unblock progress
```

**Example: Company Newsletter Template**

```markdown
# Company Newsletter — [Month/Date]

## 🎉 This Month's Highlights

### Major Wins
- [Achievement 1] — [brief context]
- [Achievement 2] — [brief context]

### Customer Stories
- [Customer success 1]
- [Customer success 2]

## 📢 Announcements

### [Category]: [Announcement Title]
[Details and context]

### [Category]: [Announcement Title]
[Details and context]

## 🗓️ Upcoming Events
- [Event 1] — [date/time]
- [Event 2] — [date/time]

## 💡 Spotlight: [Team or Person]
[Recognition and context]

## 📊 By The Numbers
- [Metric 1]: [Value]
- [Metric 2]: [Value]
```

### Step 4: Gather Required Information

**Before drafting, collect:**

| Communication Type | Key Info Needed |
|-------------------|-----------------|
| **3P Update** | Last week's progress, current blockers, next week's priorities |
| **Newsletter** | Wins from team, announcements, events, metrics |
| **FAQ** | Common question, answer options, context |
| **Status Report** | Metrics, milestones, risks, budget status |
| **Project Update** | Current status, next steps, dependencies |
| **Incident Report** | Timeline, impact, root cause, prevention |

### Step 5: Draft Following Guidelines

**Tone guidelines by communication type:**

- **3P Update**: Direct, factual, concise (assume reader is busy)
- **Newsletter**: Warm, celebratory, engaging (build community feeling)
- **FAQ**: Clear, helpful, jargon-minimized (assume reader is new)
- **Status Report**: Professional, metrics-driven, executive-level summary
- **Project Update**: Technical but accessible, clear next steps
- **Incident Report**: Objective, blameless, focus on learning

### Step 6: Quality Checklist

**Before sending:**

- [ ] Matches company template structure
- [ ] Tone consistent with communication type
- [ ] Length appropriate (not overly verbose)
- [ ] All key info included, no critical gaps
- [ ] Names and dates spelled correctly
- [ ] Links working and formatting clean
- [ ] If sensitive, review with manager first
- [ ] Proofread for grammar/typos

## Output

**Deliver:**

1. **Draft communication** using appropriate template
2. **Tone verification** (consistent with type)
3. **Completeness check** (all required info included)
4. **Ready-to-send version** formatted per company standards