---
name: obsidian-knowledge-capture
description: Transforms conversations and discussions into structured documentation notes in Obsidian. Captures insights, decisions, and knowledge from chat context, formats with appropriate templates and frontmatter, and saves to vault with proper tagging, linking, and organization for easy discovery.
---

# Knowledge Capture

Transforms conversations, discussions, and insights into structured documentation within your Obsidian vault. Captures knowledge from chat context, formats it appropriately, and saves it with proper organization, tags, and links.

## Quick Start

When asked to save information to Obsidian:

1. **Extract content**: Identify key information from conversation
2. **Determine content type**: Classify knowledge (concept, how-to, decision, FAQ, etc.)
3. **Structure information**: Apply appropriate template and frontmatter
4. **Choose location**: Determine optimal folder and organization
5. **Create note**: Generate markdown file with structured content
6. **Make discoverable**: Add tags, links, and MOC entries

## Knowledge Capture Workflow

### Step 1: Identify content to capture

From conversation context, extract:
- Key concepts and definitions
- Decisions made and rationale
- How-to information and procedures
- Important insights or learnings
- Q&A pairs and explanations
- Examples and use cases
- Best practices and patterns

### Step 2: Determine content type

Classify the knowledge for appropriate structuring:

**Concept/Definition**: Explaining what something is
**How-To Guide**: Step-by-step instructions
**Decision Record**: Important decisions and context
**FAQ Entry**: Common questions and answers
**Meeting Summary**: Meeting notes and outcomes
**Learning/Post-Mortem**: Lessons from experience
**Reference Documentation**: Technical or factual reference
**Pattern**: Reusable solution or approach

See [reference/content-types.md](reference/content-types.md) for detailed templates.

### Step 3: Structure the content

Apply appropriate template based on content type:

**Frontmatter structure:**
```yaml
---
type: [concept|how-to|decision|faq|meeting|learning|reference|pattern]
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - knowledge
  - TOPIC
  - DOMAIN
status: draft|published|archived
related:
  - "[[related-note-1]]"
  - "[[related-note-2]]"
---
```

**Content structure**: Use section headings, bullet points, examples, and links as appropriate for the content type.

See [reference/content-types.md](reference/content-types.md) for complete templates.

### Step 4: Choose vault location

Determine where to save based on content and context:

**General knowledge base:**
```
vault/
└── knowledge/
    ├── concepts/
    ├── how-to/
    ├── decisions/
    └── reference/
```

**Project-specific knowledge:**
```
vault/
└── projects/
    └── project-name/
        └── docs/
```

**Team wiki structure:**
```
vault/
└── team/
    ├── onboarding/
    ├── processes/
    └── decisions/
```

**Domain-organized:**
```
vault/
└── domains/
    ├── engineering/
    ├── product/
    └── design/
```

### Step 5: Create the note

```bash
# Create note file
touch /path/to/vault/knowledge/how-to/topic-name.md
```

Write structured content using template:
- Clear, searchable title
- Complete frontmatter with metadata
- Well-organized sections with headings
- Examples and context where helpful
- Links to related notes
- Tags for discoverability

### Step 6: Make content discoverable

**Add to MOC (Map of Content):**
```markdown
# Knowledge Base MOC

## How-To Guides
- [[how-to/deploy-to-production]]
- [[how-to/debug-performance-issues]]
- [[how-to/write-technical-specs]]  ← New entry
```

**Link from related notes:**
Update notes that reference this topic to link to the new note.

**Use consistent tags:**
- Domain tags: `#engineering`, `#product`, `#design`
- Type tags: `#how-to`, `#concept`, `#decision`
- Topic tags: `#deployment`, `#database`, `#api`

**Create backlinks:**
Reference related concepts within the note to generate natural backlinks.

## Content Type Templates

### Concept Note
```markdown
---
type: concept
tags: [concept, DOMAIN]
---

# Concept: [Name]

## Overview
Brief definition and purpose.

## Definition
Detailed explanation of what this is.

## Key Characteristics
- Characteristic 1
- Characteristic 2

## Examples
Concrete examples demonstrating the concept.

## When to Use
Situations where this concept applies.

## Related Concepts
- [[related-concept-1]]
- [[related-concept-2]]
```

### How-To Guide
```markdown
---
type: how-to
tags: [how-to, DOMAIN]
difficulty: beginner|intermediate|advanced
estimated-time: X minutes
---

# How to [Task]

## Overview
What you'll learn and why it matters.

## Prerequisites
- Requirement 1
- Requirement 2

## Steps

### Step 1: [Action]
Detailed instructions with code examples if needed.

### Step 2: [Action]
Continue with clear, actionable steps.

## Verification
How to confirm it worked.

## Troubleshooting
Common issues and solutions.

## Related Guides
- [[related-guide-1]]
- [[related-guide-2]]
```

### Decision Record
```markdown
---
type: decision
tags: [decision, DOMAIN]
date: YYYY-MM-DD
status: proposed|accepted|rejected|deprecated
deciders: [[person-1]], [[person-2]]
---

# Decision: [Title]

## Context
What situation led to this decision?

## Decision
What was decided?

## Rationale
Why was this the best choice?

## Options Considered

### Option 1: [Name]
- Pros:
- Cons:

### Option 2: [Name]
- Pros:
- Cons:

## Consequences
What are the implications?

## Implementation
How to implement this decision.

## Related Decisions
- [[previous-decision]]
- [[related-decision]]
```

See [reference/content-types.md](reference/content-types.md) for all templates.

## Extraction Patterns

### From Chat Discussion
Extract:
- Key points and conclusions
- Important resources and links
- Action items
- Q&A exchanges
- Decisions made

### From Problem-Solving
Capture:
- Problem statement
- Approaches tried
- Solution that worked
- Why it worked
- Future considerations

### From Knowledge Sharing
Document:
- Concept explained
- Examples provided
- Best practices mentioned
- Common pitfalls warned about
- Resources referenced

## Formatting Best Practices

**Headings**: Use `#` for title, `##` for sections, `###` for subsections

**Lists**: Use `-` for unordered, `1.` for ordered, `- [ ]` for task lists

**Links**: Use `[[note-name]]` for internal, `[text](url)` for external

**Code**: Use ` `code` ` for inline, ` ```language ` for blocks

**Emphasis**: `*italic*` for emphasis, `**bold**` for strong emphasis

**Callouts**: Use Obsidian callouts for important information:
```markdown
> [!note]
> Additional context or information

> [!warning]
> Important caution or warning

> [!tip]
> Helpful tip or best practice
```

## Tagging Strategy

**Domain tags**: `#engineering`, `#product`, `#design`, `#ops`

**Type tags**: `#concept`, `#how-to`, `#decision`, `#reference`

**Topic tags**: `#api`, `#database`, `#deployment`, `#testing`

**Status tags**: `#draft`, `#published`, `#needs-review`

**Audience tags**: `#beginner`, `#advanced`, `#team-specific`

## Linking Strategy

**Bidirectional links**: Link related concepts in both directions

**Hierarchical structure**: Link to parent concepts and child details

**Related topics**: Link to complementary information

**Examples**: Link to real-world examples or case studies

**Sources**: Link to original sources or references

## MOC (Map of Content) Integration

Create and maintain MOC notes for major topics:

```markdown
# Engineering Knowledge MOC

## Concepts
- [[concepts/microservices-architecture]]
- [[concepts/event-driven-design]]

## How-To Guides
- [[how-to/deploy-to-production]]
- [[how-to/rollback-deployment]]

## Decisions
- [[decisions/choose-database-system]]
- [[decisions/api-versioning-strategy]]

## Patterns
- [[patterns/retry-with-backoff]]
- [[patterns/circuit-breaker]]

## Reference
- [[reference/api-conventions]]
- [[reference/coding-standards]]
```

## Update Management

**Create new note when:**
- Content is substantive (>3 paragraphs)
- Will be referenced multiple times
- Part of knowledge base
- Needs independent discovery

**Update existing note when:**
- Adding to existing topic
- Correcting information
- Expanding on concept
- Updating for changes

**Version tracking:**
```markdown
## Revision History

### 2025-10-20
- Added new section on advanced techniques
- Updated examples for v2 API

### 2025-09-15
- Initial creation
```

## Dataview Queries

**Recent knowledge captures:**
```dataview
TABLE created, type, tags
FROM "knowledge"
WHERE type != null
SORT created DESC
LIMIT 10
```

**How-to guides by topic:**
```dataview
LIST
FROM "knowledge"
WHERE type = "how-to"
GROUP BY file.folder
SORT file.name
```

**Decisions by status:**
```dataview
TABLE date, deciders, status
FROM "knowledge"
WHERE type = "decision"
SORT date DESC
```

## Best Practices

1. **Capture promptly**: Document while context is fresh
2. **Structure consistently**: Use templates for similar content
3. **Link extensively**: Connect related knowledge
4. **Write for discovery**: Use clear titles and tags
5. **Include context**: Why this matters, when to use
6. **Add examples**: Concrete examples aid understanding
7. **Maintain**: Review and update periodically
8. **Make it scannable**: Use headings, lists, callouts

## Common Issues

**"Not sure where to save"**: Default to general knowledge base, can reorganize later

**"Content is fragmentary"**: Group related fragments into cohesive note

**"Already exists"**: Search first using tags or content, update existing if found

**"Too informal"**: Clean up language while preserving insights

**"Missing context"**: Add background section explaining why this matters

## Scripts

`scripts/create_note.py`: Generate note from template
`scripts/add_to_moc.py`: Automatically add note to relevant MOC
`scripts/tag_suggestion.py`: Suggest tags based on content
`scripts/find_related.py`: Find related notes for linking

## Examples

See [examples/](examples/) for complete workflows:
- [examples/conversation-to-how-to.md](examples/conversation-to-how-to.md)
- [examples/decision-capture.md](examples/decision-capture.md)
- [examples/concept-extraction.md](examples/concept-extraction.md)
