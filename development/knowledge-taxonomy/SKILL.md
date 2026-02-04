---
name: knowledge-taxonomy
description: Categorize extracted information into the appropriate knowledge base subdirectory (tasks, definitions, wiki, project-status, people, jira-drafts). Use when organizing extractions into the knowledge base.
---

# Knowledge Base Taxonomy

Use these rules to categorize extractions into the correct knowledge base locations.

## Knowledge Base Structure

```
knowledge/
├── project-status/    # Status updates, sprint summaries, decisions
├── tasks/             # Action items, to-dos, work tracking
├── definitions/       # Glossary, terms, acronyms
├── wiki/              # Reference articles, how-tos, documentation
├── people/            # Team profiles, contact info
└── jira-drafts/       # Draft tickets ready to create
```

## Classification Rules

### `knowledge/tasks/`

**Content Type:** Action items, to-dos, commitments, work items

**Route here when:**
- Item has (or should have) an assignee
- Item has (or should have) a deadline
- Item represents work to be done
- Item can be marked complete
- Item tracks progress on something

**File Organization:**
- Group by project: `<project>-tasks.md`
- Or by epic: `<epic>-tasks.md`
- Or by time: `<YYYY-MM>-tasks.md`

**Do NOT route here:**
- General observations
- Completed historical items (unless tracking is needed)
- Vague "we should think about" items

### `knowledge/definitions/`

**Content Type:** Terms, acronyms, glossary entries, concept explanations

**Route here when:**
- Defines a term or concept
- Explains what something means
- Expands an acronym
- Describes what a tool/system is

**File Organization:**
- One file per term: `<term>.md` (lowercase, hyphens)
- Example: `dag.md`, `data-mesh.md`, `etl.md`

**Do NOT route here:**
- Long explanatory articles (use wiki/)
- Process documentation
- How-to guides

### `knowledge/wiki/`

**Content Type:** Explanatory articles, how-tos, architecture docs, reference material

**Route here when:**
- Explains how something works
- Documents a process or workflow
- Provides reference information
- Contains tutorial or guide content
- Describes architecture or design

**File Organization:**
- Descriptive names: `<topic>.md`
- Examples: `deployment-process.md`, `api-authentication.md`

**Do NOT route here:**
- Simple term definitions (use definitions/)
- Task lists (use tasks/)
- Meeting summaries (use project-status/)

### `knowledge/project-status/`

**Content Type:** Status updates, sprint summaries, decision logs, progress reports

**Route here when:**
- Describes current state of a project
- Records decisions made
- Summarizes a time period (sprint, week, month)
- Tracks progress against goals
- Contains milestone updates

**File Organization:**
- Ongoing status: `<project>-status.md`
- Point-in-time: `<project>-YYYY-MM-DD.md`
- Decision logs: `<project>-decisions.md`

**Do NOT route here:**
- Generic reference documentation (use wiki/)
- Individual task tracking (use tasks/)

### `knowledge/people/`

**Content Type:** Person profiles, team information, contact details, roles

**Route here when:**
- Information about a specific person
- Role and responsibility descriptions
- Team membership
- Expertise areas
- Contact information

**File Organization:**
- One file per person: `<firstname>-<lastname>.md`
- Examples: `john-smith.md`, `jane-doe.md`

**Do NOT route here:**
- Task assignments (tasks reference people)
- Meeting attendee lists (stay in source docs)

### `knowledge/jira-drafts/`

**Content Type:** Draft JIRA tickets ready to be created

**Route here when:**
- Task is significant enough for formal ticket
- Needs tracking in JIRA/issue system
- Has clear scope and acceptance criteria
- Was identified as "JIRA candidate" during extraction

**File Organization:**
- Draft naming: `draft-<brief-title>.md`
- Examples: `draft-implement-auth.md`, `draft-fix-login-bug.md`

**Do NOT route here:**
- Small tasks that don't need formal tracking
- Already-existing JIRA tickets (just reference them)

## Decision Flow

Use this decision tree:

```
Start
  │
  ├── Is it about a specific person's info/role?
  │     YES → knowledge/people/
  │     NO ↓
  │
  ├── Is it a term/acronym definition (short)?
  │     YES → knowledge/definitions/
  │     NO ↓
  │
  ├── Is it an action item or task?
  │     YES → Is it significant enough for JIRA?
  │           YES → ALSO knowledge/jira-drafts/
  │           knowledge/tasks/ (primary)
  │     NO ↓
  │
  ├── Is it project progress/status/decisions?
  │     YES → knowledge/project-status/
  │     NO ↓
  │
  ├── Is it explanatory/reference content?
  │     YES → knowledge/wiki/
  │     NO ↓
  │
  └── Default: Review manually, may not need KB entry
```

## Handling Existing Entries

### Updates to Existing Files

When new info relates to existing KB entries:
1. Read the existing file
2. Determine if update needed
3. If minor update: append/modify in place
4. If major change: create proposed-update

### Merge vs New Entry

- **Merge** when: Same topic, complementary info
- **New entry** when: Different aspect, would make file too long
- **Link** when: Related but distinct topics

## Cross-Linking

When creating/updating entries, add links:

```markdown
## Related

- [[other-term]] - Related concept
- [[person-name]] - Key contact
- [[project-status]] - Current project state
```

## Quality Checks

Before creating an entry:
1. Does similar entry already exist?
2. Is this the right category?
3. Is there enough substance for a KB entry?
4. Would this be useful to find later?

## Entry Templates

Use the templates from `templates/` directory:
- `task-entry.md` for tasks
- `definition-entry.md` for definitions
- `person-profile.md` for people
- `project-status.md` for status
- `jira-draft.md` for JIRA drafts
