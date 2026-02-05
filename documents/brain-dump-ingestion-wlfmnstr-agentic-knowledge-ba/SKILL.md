---
name: "brain-dump-ingestion"
description: "Process unstructured brain dumps, transcripts, and stream-of-consciousness notes into structured knowledge base content. Use when converting raw ideas, meeting notes, or recorded thoughts into organized documentation."
---

# Brain Dump Ingestion & Processing

Process unstructured brain dumps—transcribed audio, stream-of-consciousness writing, rambling thoughts—into structured, valuable knowledge base content while preserving the original context.

## Core Philosophy

**Principle 1: Preserve the Original**
Never discard the raw brain dump. It contains context, emotion, and connections that structured notes may lose.

**Principle 2: Isolate Before Integrating**
Use a landing zone workflow to prevent pollution of the mature knowledge base. Content must be reviewed and refined before integration.

**Principle 3: Extract Atomic Ideas**
Break large dumps into focused, single-topic pieces that can be independently valuable and linked together.

**Principle 4: Maintain Traceability**
Always link processed content back to its source brain dump for future reference.

---

## Landing Zone Architecture

### Three-Tier Content Structure

```
src/content/
├── brain-dumps/       # Raw, unprocessed dumps (preserved forever)
│   └── {date}-{slug}.mdx
├── staging/           # Processed but not yet integrated content
│   └── {topic}-{slug}.mdx
└── docs/              # Production knowledge base (mature content)
    └── {category}/{slug}.mdx
```

### Content Flow

```
1. Brain Dump → brain-dumps/     (raw input, timestamped)
2. Processing → staging/          (structured, tagged, ready for review)
3. Integration → docs/            (refined, linked, published)
```

### Schema Design

**brain-dumps collection:**
```typescript
{
  title: string           // Brief description of the dump
  date: Date              // When it was captured
  source: string          // 'audio' | 'text' | 'transcript' | 'conversation'
  duration?: string       // For audio/video sources
  tags?: string[]         // Rough categorization
  processed: boolean      // Whether staging content exists
  stagedItems?: string[]  // Links to staging entries created from this
}
```

**staging collection:**
```typescript
{
  title: string           // Extracted topic/concept
  description: string     // Clear summary of content
  sourceFile: string      // Reference back to brain dump
  extractedDate: Date     // When this was extracted
  targetCategory?: string // Suggested docs category
  status: 'new' | 'reviewed' | 'ready' | 'integrated'
  tags: string[]          // Refined tags
  relatedTopics?: string[] // Connections to other content
  integrationNotes?: string // Notes for integration
}
```

---

## Processing Workflow

### Step 1: Analyze the Brain Dump

When presented with a brain dump, first understand its characteristics:

**Content Type:**
- Stream of consciousness (free-flowing thoughts)
- Narrative (story-like explanation)
- Problem-solving (working through an issue)
- Knowledge capture (explaining something you know)
- Ideation (brainstorming and exploring)
- Meeting notes (conversation transcript)

**Density Indicators:**
- How many distinct topics are covered?
- What's the primary focus vs. tangential thoughts?
- Are there clear pivots or topic changes?
- What's the signal-to-noise ratio?

**Extraction Potential:**
- What could become standalone documentation?
- What are the key insights or decisions?
- What should be cross-referenced?
- What's contextual fluff vs. valuable content?

### Step 2: Save the Raw Dump

Always start by preserving the original in `brain-dumps/`:

```markdown
---
title: "Quick thoughts on authentication patterns"
date: 2025-11-05T14:30:00Z
source: "audio"
duration: "20 minutes"
tags: ["authentication", "security", "ideas"]
processed: false
---

[Raw content exactly as provided, no editing]
```

**File naming:** `YYYY-MM-DD-brief-slug.mdx`

### Step 3: Extract Atomic Topics

Identify distinct concepts that could become independent documentation:

**Extraction Criteria:**
- ✅ Concept can stand alone without full context
- ✅ Topic is focused on a single idea
- ✅ Content provides value independent of other extracts
- ✅ Clear title can be written without "context dump"

**Example Extraction:**
From a 20-minute ramble about auth, you might extract:
1. "JWT vs Session Tokens - Decision Matrix"
2. "Password Reset Flow Security Concerns"
3. "OAuth Integration Gotchas"
4. "User Session Management Best Practices"

### Step 4: Create Staging Entries

For each extracted topic, create a structured entry in `staging/`:

```markdown
---
title: "JWT vs Session Tokens - Decision Matrix"
description: "Comparison of JWT and session-based authentication with decision criteria for choosing between them"
sourceFile: "brain-dumps/2025-11-05-auth-thoughts.mdx"
extractedDate: 2025-11-05T15:00:00Z
targetCategory: "security"
status: "new"
tags: ["authentication", "jwt", "sessions", "security"]
relatedTopics: ["oauth-integration", "session-management"]
---

## Overview

[Extracted and structured content]

## Key Considerations

[Organized insights from the brain dump]

## Decision Criteria

[Structured decision matrix]

## Source Context

This content was extracted from a brain dump recorded on 2025-11-05.
See the [original brain dump](/brain-dumps/2025-11-05-auth-thoughts) for full context.
```

**File naming:** `{topic-slug}.mdx` (no date prefix, describes the content)

### Step 5: Update Source References

Update the original brain dump to track what was extracted:

```markdown
---
processed: true
stagedItems:
  - "staging/jwt-vs-sessions.mdx"
  - "staging/password-reset-security.mdx"
  - "staging/oauth-gotchas.mdx"
---
```

---

## Content Structuring Techniques

### From Stream to Structure

**Identify Patterns:**
- Repeated phrases → key concepts
- "So basically..." → summary moments
- "The problem is..." → problem statements
- "What we should do..." → action items/recommendations
- "I learned that..." → key insights
- Questions asked → important considerations

**Extract Hierarchies:**
- Main topic: What's the overarching theme?
- Subtopics: What distinct areas are covered?
- Details: What specific examples or explanations support each subtopic?

**Clean Up Narrative Artifacts:**
- Remove: "um", "like", "you know", filler words
- Convert: First person narrative → clear documentation
- Preserve: Unique phrasing that adds clarity or insight
- Keep: Examples and analogies that illustrate concepts

### Structure Templates

**For Conceptual Content:**
```markdown
## Overview
[What is this concept?]

## Key Characteristics
[What makes this important/unique?]

## Use Cases
[When should this be used?]

## Considerations
[What should you keep in mind?]

## Related Concepts
[What connects to this?]
```

**For Decision/Problem Content:**
```markdown
## Problem Statement
[What problem are we solving?]

## Context
[Why does this matter?]

## Options Considered
[What are the alternatives?]

## Decision Criteria
[How do we choose?]

## Recommendation
[What's the suggested approach?]

## Trade-offs
[What are we accepting/rejecting?]
```

**For How-To/Process Content:**
```markdown
## What This Does
[Clear outcome description]

## When to Use This
[Applicability]

## Prerequisites
[What you need first]

## Steps
[Ordered process]

## Common Issues
[Troubleshooting]

## Related Processes
[Connected workflows]
```

---

## Integration Readiness

### Staging Review Checklist

Before content can move from `staging/` to `docs/`, verify:

**Content Quality:**
- [ ] Title is clear and descriptive
- [ ] Description accurately summarizes content
- [ ] Content is well-structured with appropriate headings
- [ ] Grammar and clarity are good (not perfect, but readable)
- [ ] Examples are included where helpful
- [ ] Technical accuracy is verified

**Categorization:**
- [ ] Target category is identified
- [ ] Tags are relevant and consistent with existing taxonomy
- [ ] Related topics are identified and can be linked

**Integration Planning:**
- [ ] No duplicate content exists in docs
- [ ] If merging with existing doc, plan is clear
- [ ] If new doc, navigation placement is identified
- [ ] Cross-links to related content are identified

**Traceability:**
- [ ] Source brain dump is referenced
- [ ] Extraction date is recorded
- [ ] Context is preserved if needed

### Status Progression

```
new → reviewed → ready → integrated
```

- **new**: Just extracted, needs initial review
- **reviewed**: Content quality verified, needs categorization
- **ready**: Integration plan complete, ready to move
- **integrated**: Successfully moved to docs, can be archived

---

## Best Practices

### Do's

- ✅ **Save everything**: Even if a brain dump seems useless now, context may matter later
- ✅ **Extract generously**: Better to have multiple small staged pieces than one large dump
- ✅ **Link bidirectionally**: Brain dump → staging → docs, and back
- ✅ **Use timestamps**: Helps understand evolution of thinking
- ✅ **Tag broadly in dumps**: Narrow down tags during staging
- ✅ **Keep voice where valuable**: If the narrative style adds clarity, preserve it
- ✅ **Note uncertainties**: Mark areas that need verification or expansion
- ✅ **Cross-reference**: Identify connections to existing content

### Don'ts

- ❌ **Don't edit brain dumps**: They're raw archives, keep them authentic
- ❌ **Don't rush to docs**: Let content mature in staging
- ❌ **Don't lose context**: Always maintain traceability
- ❌ **Don't over-structure**: If narrative flow helps, keep it
- ❌ **Don't delete tangents**: They might matter later, just don't extract them
- ❌ **Don't force atomicity**: Some concepts need more context
- ❌ **Don't ignore duplicates**: Check for existing content before creating new

---

## Common Patterns

### Pattern 1: Exploratory Ramble

**Characteristics:** Stream of consciousness, multiple topic pivots, thinking out loud

**Approach:**
- Extract 3-5 distinct mini-topics
- Create one "exploration notes" staging entry with multiple sections
- Link to related existing docs for context
- Mark areas that need deeper exploration

### Pattern 2: Deep Dive

**Characteristics:** Sustained focus on one topic, thorough coverage, examples included

**Approach:**
- Extract as comprehensive single document
- Structure carefully with clear hierarchy
- May become primary doc for that topic
- Verify technical accuracy before marking ready

### Pattern 3: Meeting Notes

**Characteristics:** Conversational, decisions made, action items, multiple participants

**Approach:**
- Save full transcript in brain-dumps
- Extract decisions as separate staging entries
- Pull out action items with owners
- Create context document linking all pieces

### Pattern 4: Problem Solving

**Characteristics:** Working through a specific issue,試行錯誤, eventual resolution

**Approach:**
- Extract the problem statement
- Extract the solution/approach
- Consider extracting "what didn't work" as gotchas
- Link to related troubleshooting docs

### Pattern 5: Knowledge Transfer

**Characteristics:** Explaining something you know, teaching narrative, examples rich

**Approach:**
- Structure as tutorial or guide
- Extract conceptual overview separately from how-to
- Pull out examples as separate entries if reusable
- Consider creating a series of linked docs

---

## Tools & Commands

### Expected Supporting Commands

**`/ingest [source]`** - Complete ingestion workflow
- Prompts for brain dump content
- Saves to brain-dumps/
- Analyzes and suggests extractions
- Creates staging entries
- Updates references

**`/review-staging [file]`** - Review staged content
- Validates content quality
- Checks for duplicates
- Suggests categorization
- Identifies integration opportunities
- Updates status

**`/integrate-content [staging-file]`** - Move from staging to docs
- Checks integration readiness
- Handles placement in docs/
- Creates cross-links
- Updates all references
- Marks as integrated

---

## Quick Reference

### File Naming Conventions

```
brain-dumps:  YYYY-MM-DD-brief-description.mdx
staging:      topic-focused-slug.mdx
docs:         category/descriptive-slug.mdx
```

### Frontmatter Quick Copy

```yaml
# Brain Dump
---
title: "Brief description of dump"
date: 2025-11-05T14:30:00Z
source: "audio" | "text" | "transcript"
tags: ["broad", "tags"]
processed: false
---

# Staging
---
title: "Focused topic title"
description: "Clear one-sentence summary"
sourceFile: "brain-dumps/YYYY-MM-DD-slug.mdx"
extractedDate: 2025-11-05T15:00:00Z
targetCategory: "suggested-category"
status: "new"
tags: ["specific", "tags"]
relatedTopics: ["other-topic-slugs"]
---
```

### Processing Checklist

1. [ ] Save raw dump to brain-dumps/
2. [ ] Analyze content type and density
3. [ ] Identify atomic topics (3-7 typical)
4. [ ] Create staging entry for each topic
5. [ ] Structure content appropriately
6. [ ] Add source references
7. [ ] Update brain dump with processed: true
8. [ ] Review and refine staging entries
9. [ ] Plan integration approach
10. [ ] Move to docs when ready

---

## Success Metrics

You're doing this well when:

- ✅ No valuable thoughts are lost
- ✅ Original context is always accessible
- ✅ Staged content is focused and atomic
- ✅ Integration path is clear for each piece
- ✅ No pollution of main docs with half-baked ideas
- ✅ Connections between concepts are identified
- ✅ Content evolves from raw → refined naturally
- ✅ You can find the source of any extracted content

---

*Brain dumps are the raw material of knowledge. This skill transforms chaos into clarity while honoring the messiness of creative thinking.*
