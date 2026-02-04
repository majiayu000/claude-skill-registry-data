---
name: obsidian-meeting-prep
description: Prepares meeting materials by gathering context from Obsidian vault, enriching with research, and creating comprehensive meeting documentation. Generates both internal prep notes with background and external agendas with structure, all saved as properly linked markdown notes in vault.
---

# Meeting Preparation

Prepares you for meetings by gathering context from your Obsidian vault, enriching it with research, and creating comprehensive meeting materials. Generates internal prep notes for attendees and external-facing agendas for meetings.

## Quick Start

When asked to prepare for a meeting:

1. **Understand meeting context**: Gather meeting details and objectives
2. **Search vault**: Find related project notes, previous meetings, specs
3. **Read relevant notes**: Extract key context and background
4. **Enrich with research**: Add insights and additional context
5. **Create prep note**: Internal background document for attendees
6. **Create agenda**: External-facing meeting structure
7. **Link resources**: Connect all documents appropriately

## Meeting Prep Workflow

### Step 1: Gather meeting details

Collect essential information:

**Meeting basics:**
- Topic/Title
- Date and time
- Duration
- Location (physical/virtual)

**Participants:**
- Internal attendees
- External participants (clients, partners)
- Meeting owner/facilitator

**Meeting purpose:**
- Decision-making
- Status update
- Brainstorming
- Planning session
- Customer demo
- Problem-solving
- Knowledge sharing

**Context:**
- Related project or initiative
- Background/history
- Key topics to cover
- Desired outcomes

### Step 2: Search vault for context

**Project-related search:**
```bash
# Find project notes
find /path/to/vault/projects -name "*project-name*"

# Search project folder
grep -r "relevant term" /path/to/vault/projects/project-name/
```

**Previous meetings:**
```bash
# Find meeting notes
find /path/to/vault/meetings -name "*topic*" -o -name "*project*"

# Recent meetings
find /path/to/vault/meetings -name "*.md" -mtime -30
```

**Specifications and designs:**
```bash
# Find specs
grep -l "type: specification" /path/to/vault/**/*.md

# Find designs
find /path/to/vault -path "*/designs/*" -name "*.md"
```

**Tasks and issues:**
```bash
# Find related tasks
grep -l "project: \[\[project-name\]\]" /path/to/vault/tasks/*.md

# Find open issues
grep -l "status: open" /path/to/vault/**/*.md | grep -i "issue\|bug"
```

**Decision records:**
```bash
# Find decisions
grep -l "type: decision" /path/to/vault/**/*.md

# Recent decisions for project
grep -l "project.*project-name" /path/to/vault/decisions/*.md
```

**Dataview query:**
```dataview
TABLE type, updated, tags
FROM "projects" OR "meetings" OR "specs"
WHERE contains(file.name, "project-name")
   OR contains(tags, "#project-tag")
SORT updated DESC
LIMIT 20
```

### Step 3: Read and extract context

For each relevant note:

```bash
# Read note
cat /path/to/vault/path/to/note.md
```

Extract:
- **Project status**: Current state and progress
- **Recent updates**: What changed recently
- **Decisions made**: Past decisions affecting meeting
- **Open questions**: Unresolved issues
- **Action items**: Outstanding tasks
- **Background**: Historical context
- **Stakeholder info**: Relevant people and roles

Organize information by relevance and importance.

### Step 4: Enrich with additional research

**Add context:**
- Industry best practices
- Technical background
- Competitive landscape
- Relevant frameworks or methodologies

**Anticipate questions:**
- What might participants ask?
- What context might be missing?
- What decisions need background?

**Identify discussion points:**
- Topics needing alignment
- Areas of potential disagreement
- Opportunities for input

### Step 5: Create internal prep note

Generate background document for internal attendees:

```bash
touch /path/to/vault/meetings/prep/meeting-name-prep.md
```

**Prep note structure:**
```markdown
---
type: meeting-prep
meeting: "[[meetings/meeting-name]]"
date: YYYY-MM-DD
project: "[[projects/project-name]]"
attendees:
  - "[[people/person-1]]"
  - "[[people/person-2]]"
tags:
  - meeting-prep
  - PROJECT-TAG
visibility: internal
---

# Meeting Prep: [Meeting Name]

> [!info] Meeting Details
> **Date**: YYYY-MM-DD HH:MM
> **Duration**: X hours
> **Location**: [Where/Link]
> **Attendees**: [[person-1]], [[person-2]]

## Purpose
Clear statement of meeting objectives.

## Background

### Project Context
Current state and relevant history.
- Status: [description]
- Recent changes: [what's new]
- Related: [[project-note]], [[spec-note]]

### Previous Discussions
Summary of relevant prior meetings.
- [[previous-meeting-1]]: Key outcomes
- [[previous-meeting-2]]: Decisions made

### Key Decisions
Important decisions affecting this meeting.
- [[decision-1]]: What was decided and why
- [[decision-2]]: Impact and implications

## Current Situation

### What's Working Well
Positive developments and progress.

### Challenges
Current obstacles and issues.
- Challenge 1: [[related-task]]
- Challenge 2: [[related-issue]]

### Open Questions
Unresolved issues needing discussion.
1. Question 1
2. Question 2

## Key Discussion Topics

### Topic 1: [Name]
**Context**: Background and why this matters
**Current state**: Where things stand
**Options**: Potential approaches
**Our position**: Recommended direction

### Topic 2: [Name]
[Continue for each major topic]

## Data & Metrics
Relevant numbers and trends.
- Metric 1: Current value (trend)
- Metric 2: Current value (trend)

## Stakeholder Perspectives

### Internal Team
- View 1: [[person-1]]'s perspective
- View 2: [[person-2]]'s perspective

### External Participants
- Client needs and concerns
- Partner requirements

## Potential Objections
Anticipated concerns and responses.

## Goals for This Meeting
What we want to achieve.
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Materials to Reference
- [[spec-document]]
- [[design-mockups]]
- [[data-report]]

## Follow-Up Considerations
Potential next steps and actions.

## Quick Reference
Critical facts and figures for easy access.
```

See [reference/prep-note-template.md](reference/prep-note-template.md) for full template.

### Step 6: Create meeting agenda

Generate external-facing agenda document:

```bash
touch /path/to/vault/meetings/agenda/meeting-name-agenda.md
```

**Agenda structure:**
```markdown
---
type: meeting-agenda
date: YYYY-MM-DD
project: "[[projects/project-name]]"
duration: X hours
attendees:
  - "[[people/internal-1]]"
  - "External Person Name"
tags:
  - agenda
  - PROJECT-TAG
visibility: external
---

# Meeting Agenda: [Meeting Name]

**Date**: YYYY-MM-DD HH:MM
**Duration**: X hours
**Location**: [Where/Video link]

## Attendees
- Internal: [[person-1]], [[person-2]]
- External: Name 1, Name 2

## Meeting Objectives
1. Objective 1
2. Objective 2
3. Objective 3

## Agenda

### 1. Welcome & Introductions (5 min)
- Brief introductions
- Meeting objectives overview

### 2. Topic 1: [Name] (20 min)
**Objective**: What we want to accomplish
**Discussion points**:
- Point 1
- Point 2
- Point 3

**Desired outcome**: Decision/alignment on X

### 3. Topic 2: [Name] (15 min)
[Continue for each topic with time allocations]

### 4. Topic 3: [Name] (20 min)
...

### 5. Action Items & Next Steps (10 min)
- Summarize decisions
- Assign action items
- Schedule follow-up

## Background Materials
- [[Reference document 1]]
- [[Reference document 2]]

## Parking Lot
Topics for future discussion if time doesn't permit.

---

## Post-Meeting
Meeting notes: [[meetings/meeting-name-notes]]
Action items: [[tasks/meeting-name-actions]]
```

See [reference/agenda-template.md](reference/agenda-template.md) for full template.

### Step 7: Link and organize

**Create meeting folder:**
```
meetings/
└── meeting-name/
    ├── prep.md          # Internal prep note
    ├── agenda.md        # External agenda
    └── notes.md         # Post-meeting notes (placeholder)
```

**Link from project:**
```markdown
## Upcoming Meetings
- [[meetings/meeting-name/agenda]] - YYYY-MM-DD
```

**Link in prep note and agenda:**
```markdown
## Related
- Prep notes: [[meetings/meeting-name/prep]]
- Agenda: [[meetings/meeting-name/agenda]]
- Project: [[projects/project-name]]
- Spec: [[specs/feature-spec]]
```

## Meeting Types and Approaches

### Decision Meeting
Focus: Options, trade-offs, recommendation
Prep: Research alternatives, gather data, prepare analysis

### Status Update
Focus: Progress, blockers, timeline
Prep: Collect metrics, identify issues, note changes

### Brainstorming
Focus: Ideas, possibilities, creativity
Prep: Relevant examples, constraints, desired outcomes

### Planning Session
Focus: Timeline, resources, milestones
Prep: Current state, dependencies, capacity

### Customer Demo
Focus: Features, value, feedback
Prep: Demo script, talking points, Q&A prep

### Problem-Solving
Focus: Issue, root cause, solutions
Prep: Problem analysis, attempted solutions, data

## Search Strategies

### By Time Period
```bash
# Recent notes (last 30 days)
find /path/to/vault -name "*.md" -mtime -30

# Notes from specific month
find /path/to/vault -name "2025-10*.md"
```

### By Participant
```bash
# Notes mentioning specific person
grep -r "\[\[people/person-name\]\]" /path/to/vault/
```

### By Topic
```bash
# Multi-keyword search
grep -r "keyword1" /path/to/vault/ | grep "keyword2"
```

### By Project
```bash
# All project-related content
find /path/to/vault/projects/project-name -name "*.md"
grep -r "project:.*project-name" /path/to/vault/
```

## Best Practices

1. **Prepare early**: Don't wait until last minute
2. **Be comprehensive**: Gather all relevant context
3. **Distinguish internal/external**: Separate prep from agenda
4. **Time-box topics**: Allocate realistic time slots
5. **Anticipate questions**: Think ahead about what might be asked
6. **Link extensively**: Connect to all relevant notes
7. **Update regularly**: Keep prep notes current as context changes
8. **Follow up**: Connect to post-meeting notes and actions

## Prep Note vs Agenda

**Internal Prep Note:**
- Comprehensive background
- Internal perspectives and strategy
- Detailed context and history
- Potential objections and responses
- Confidential information
- Talking points and recommendations

**External Agenda:**
- High-level structure
- Discussion topics only
- Time allocations
- Meeting objectives
- Professional tone
- Appropriate level of detail

## Post-Meeting Integration

After meeting, link prep to outcomes:

```markdown
## Meeting Outcome
Actual meeting notes: [[meetings/meeting-name/notes]]

### Decisions Made
- Decision 1: [[decisions/decision-name]]
- Decision 2: [Description]

### Action Items Created
- [[tasks/action-1]]
- [[tasks/action-2]]

### Follow-Up Required
- [ ] Schedule follow-up meeting
- [ ] Update project plan
- [ ] Communicate to team
```

## Dataview Queries

**Upcoming meetings:**
```dataview
TABLE date, project, attendees
FROM "meetings"
WHERE type = "meeting-agenda"
  AND date >= date(today)
SORT date ASC
```

**Recent prep work:**
```dataview
LIST
FROM "meetings"
WHERE type = "meeting-prep"
SORT file.mtime DESC
LIMIT 10
```

**Meetings by project:**
```dataview
TABLE date, type
FROM "meetings"
WHERE contains(string(project), "project-name")
SORT date DESC
```

## Common Issues

**"Can't find relevant context"**:
- Broaden search terms
- Check related project folders
- Search by tags
- Ask participants for key docs

**"Too much information"**:
- Prioritize most recent and relevant
- Focus on key decisions and changes
- Summarize rather than include everything

**"Participants from different contexts"**:
- Create layered prep (basics to advanced)
- Provide glossary of terms
- Include background section

**"External participants need context"**:
- Keep agenda appropriate for audience
- Link to public-facing docs only
- Provide necessary background without revealing internal info

## Scripts

`scripts/find_meeting_context.py`: Automated context gathering
`scripts/generate_agenda.py`: Generate agenda from template
`scripts/meeting_summary.py`: Summarize related notes
`scripts/extract_action_items.py`: Pull action items from notes

## Examples

See [examples/](examples/) for complete workflows:
- [examples/decision-meeting-prep.md](examples/decision-meeting-prep.md)
- [examples/status-update-prep.md](examples/status-update-prep.md)
- [examples/client-demo-prep.md](examples/client-demo-prep.md)
