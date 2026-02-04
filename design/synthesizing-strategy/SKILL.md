---
name: synthesizing-strategy
description: Transforms raw research findings into opinionated, actionable brand strategy documents. A strategist's perspective on synthesizing insights into strategic guidance.
---

# Strategy Synthesis

Knowledge base for synthesizing research findings into polished, actionable strategy documents that guide brand decisions and content creation.

## Core Philosophy

**Research = Unopinionated Analysis** (What exists, what was said, what was found)
**Strategy = Opinionated Synthesis** (What it means, what to do, how to position)

This skill embodies the strategist's role: taking raw insights and transforming them into clear, prescriptive guidance.

## Synthesis vs Research

| Aspect | Research | Strategy Synthesis |
|--------|----------|-------------------|
| **Perspective** | Analyst (objective) | Strategist (opinionated) |
| **Purpose** | Gather insights | Prescribe action |
| **Input** | External sources | Research RESEARCH.md files |
| **Output** | RESEARCH.md (findings) | STRATEGY.md (guidance) |
| **Tone** | "We found that..." | "We should..." |
| **Location** | `/research/{domain}/` | `/strategy/{domain}/` |
| **Temporal** | Date-stamped executions | Git versioned (current truth) |

## Strategy Domains

Each domain addresses a distinct strategic question:

1. **brand-fundamentals** - Who are we? Why do we exist?
2. **positioning** - Where do we fit? What makes us different?
3. **messaging** - What do we say? What are our key messages?
4. **voice** - How do we sound? What's our personality?
5. **audience** - Who are we talking to?

## Synthesis Workflows

Each workflow follows a **plan-implement** pattern using the orchestration skill:

### Planning Phase
- Check research prerequisites (RESEARCH.md files exist and are current)
- Verify research is newer than existing strategy (via frontmatter dates)
- Create execution plan

### Implementation Phase
- Load research findings by path (progressive disclosure)
- Synthesize into strategic recommendations
- Write/update STRATEGY.md with frontmatter
- Update CHANGELOG.md
- Create cross-references to research (audit trail)

## Standard Strategy File Structure

```
/strategy/{domain}/
├── STRATEGY.md           # Current strategy (git versioned)
└── CHANGELOG.md          # Evolution tracking
```

### STRATEGY.md Frontmatter

```yaml
---
domain: {domain-name}
last_updated: YYYY-MM-DD
research_sources:
  - /research/{domain}/RESEARCH.md
  - /research/{other-domain}/RESEARCH.md
---
```

## Workflows Available

- [brand-fundamentals](workflows/brand-fundamentals/WORKFLOW.md)
- [positioning](workflows/positioning/WORKFLOW.md)
- [messaging](workflows/messaging/WORKFLOW.md)
- [voice](workflows/voice/WORKFLOW.md)
- [audience](workflows/audience/WORKFLOW.md)

## Invocation

Synthesis workflows are triggered via slash commands:

```
/strategy:brand-fundamentals
/strategy:positioning
/strategy:messaging
/strategy:voice
/strategy:audience
```

## Update Logic

Strategy synthesis only runs when:
1. Required research files exist
2. Research `last_updated` (frontmatter) is newer than strategy `last_updated`
3. User explicitly requests update

This ensures strategy stays current with research while avoiding unnecessary re-synthesis.

## Progressive Disclosure

Strategy files reference research by path, not content:

```markdown
Our customers struggle with [complex tools that overwhelm them](/research/customer-insights/RESEARCH.md).
```

This enables:
- Human navigation (clickable links)
- AI progressive disclosure (load when needed)
- Audit trails (claim → evidence)
