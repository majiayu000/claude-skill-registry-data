---
name: adr
description: Create a new Architecture Decision Record (ADR) for a proposed feature or design change.
argument-hint: "<title>"
allowed-tools: Read, Glob, Grep, Bash(ls *), Write
---

# Create ADR

Create a new ADR document for: $ARGUMENTS

## Process

1. **Determine next ADR number**: List `docs/ai/adr/` to find the highest existing number, then increment by 1.

2. **Research the topic**: Before writing, explore the codebase to understand the current state of the relevant area. Read related files, check existing ADR documents for context, and identify what currently exists vs what's missing.

3. **Write the ADR** at `docs/ai/adr/{NNN}-{slug}.md` using this format:

```markdown
# ADR {NNN}: {Title}

## Status: Proposed

## Context

{Why is this needed? What's the current situation? What problems exist?}

## Decision

{The proposed design. Include:}
- Architecture / structure
- UI layout (ASCII diagrams if helpful)
- State management approach
- Implementation details
- Mobile considerations

## Considerations

{Trade-offs, open questions, alternative approaches considered}

## Future Extensions

{What could be built on top of this later}
```

## Guidelines

- Write in English (per CLAUDE.md conventions). Discussion in Japanese is fine, but the ADR document itself should be in English
- Include ASCII layout diagrams for UI-related ADRs
- Reference specific files and line numbers for current code
- Break complex features into phased implementation steps
- Keep it concise but thorough enough to guide implementation
