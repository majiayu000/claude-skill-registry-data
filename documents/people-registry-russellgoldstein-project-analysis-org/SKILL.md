---
name: people-registry
description: Build and maintain the people registry from context over time, tracking names, roles, teams, and expertise as they appear in documents. Use when processing documents that mention people or when updating people profiles.
---

# People Registry Management

Build and maintain people profiles from document context. The registry grows organically as documents are processed.

## Person Profile Structure

Each person gets a profile at `knowledge/people/<firstname>-<lastname>.md`:

```markdown
---
type: person
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
name_variations:
  - John
  - John S.
  - John Smith
  - jsmith
  - @john.smith
---

# John Smith

## Basic Info

| Field | Value | Confidence | Source |
|-------|-------|------------|--------|
| Role | Senior Engineer | High | sprint-review.md |
| Team | Platform Team | High | team-sync.md |
| Department | Engineering | Medium | inferred |
| Location | San Francisco | Low | mentioned once |

## Expertise Areas

| Area | Evidence |
|------|----------|
| Backend systems | Presented architecture review |
| API design | Led API redesign initiative |
| Python | Mentioned as primary language |

## Responsibilities

- Lead technical design for Project Alpha
- Code review for platform services
- On-call rotation for data pipeline

## Active Projects

| Project | Role | Since |
|---------|------|-------|
| Project Alpha | Tech Lead | 2024-01 |
| API Gateway | Contributor | 2023-10 |

## Document Mentions

| Date | Document | Context |
|------|----------|---------|
| 2024-01-15 | sprint-review.md | Led sprint review presentation |
| 2024-01-10 | team-sync.md | Discussed migration timeline |
| 2024-01-05 | 1-on-1-notes.md | Performance review mentioned |

## Working Relationships

| Relationship | Person | Context |
|--------------|--------|---------|
| Works with | Jane Doe | Same project team |
| Reports to | Bob Wilson | Mentioned as manager |
| Collaborates | Sarah Kim | API design partner |

## Notes

- Prefers async communication
- Usually presents in sprint reviews
- Expert on legacy migration
```

## Name Recognition

### Identifying the Same Person

Track name variations to recognize the same person:

**Matching Criteria:**
- Same full name (case-insensitive)
- First name matches with contextual confirmation
- @mention username maps to known name
- Email prefix matches known name

**Variation Examples:**
```
John Smith
├── John
├── John S.
├── J. Smith
├── jsmith
├── @john.smith
├── john.smith@company.com
└── JS (initials, if contextually clear)
```

### Handling Ambiguity

When name is ambiguous:
1. Check context clues (team, project, role)
2. If still ambiguous, create separate entry with note
3. Flag for human review
4. Later merges can consolidate

```markdown
## Review Needed

- "John" mentioned without last name - could be John Smith or John Davis
- Context suggests Platform team, likely John Smith
```

## Information Extraction

### Role Detection

Look for role indicators:
- Explicit titles: "John, our Tech Lead..."
- Action indicators: "John will present the architecture"
- Responsibility context: "John is handling the deployment"

**Role confidence levels:**
- **High**: Title explicitly stated
- **Medium**: Role inferred from consistent actions
- **Low**: Single mention or ambiguous

### Team Detection

Look for team associations:
- Explicit: "the Platform team's John Smith"
- Meeting context: "Platform team sync" with John speaking
- Project association: If project maps to team

### Expertise Detection

Infer expertise from:
- Topics they present or explain
- Questions directed to them
- "Ask John about X" patterns
- Technologies they discuss in detail

## Profile Updates

### Adding New Information

When new document mentions a known person:
1. Read existing profile
2. Compare new information with existing
3. Add new information with source
4. Update confidence if evidence strengthens
5. Update `updated` date
6. Add document to sources list

### Handling Contradictions

If new info contradicts existing:
```markdown
## Possible Updates

**Role Change?**
- Previous: Senior Engineer (source: doc1.md, 2024-01)
- New: Staff Engineer (source: doc2.md, 2024-03)
- Action: Likely promotion, update role
```

### Information Aging

Note when information might be stale:
- Roles may change over time
- Team assignments shift
- Project involvement ends

Mark old information:
```markdown
## Historical

| Field | Value | Period |
|-------|-------|--------|
| Team | Mobile Team | 2023-01 to 2023-09 |
| Role | Junior Engineer | 2022-06 to 2023-06 |
```

## Cross-Linking

### Link to Projects
```markdown
See also:
- [[project-alpha-status]] - Current project
- [[project-alpha-tasks]] - Active tasks
```

### Link to Other People
```markdown
## Team

- [[jane-doe]] - PM for Project Alpha
- [[bob-wilson]] - Engineering Manager
```

## Quality Guidelines

### Minimum for New Profile
- Full name (or best guess with flag)
- At least one context mention
- Source document reference

### Don't Create Profile For
- Mentioned once with no context
- External people (unless relevant to project)
- Clearly hypothetical mentions

### Flag for Review
- Name conflicts (multiple Johns)
- Inferred information
- Significant role/team changes
- First-name-only mentions

## Registry Maintenance

### Periodic Review Tasks
- Merge duplicate entries
- Update stale information
- Consolidate name variations
- Remove irrelevant entries

### Merge Procedure
When merging two profiles:
1. Keep the more complete profile as base
2. Add unique info from other profile
3. Combine sources lists
4. Update name_variations
5. Archive or delete duplicate
