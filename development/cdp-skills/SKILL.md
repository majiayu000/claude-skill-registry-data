---
name: cdp-skills
description: Claude Developer Platform Skills feature. Custom knowledge packages for agents, curated playbooks, and versioned expertise domains.
---

# Skills Feature Skill

## When to Use
- Questions about packaging custom knowledge
- "How do I give Claude domain expertise?"
- Building agents with specialized knowledge
- RAG vs Skills comparison
- Knowledge management for AI agents

## Key Feature: Skills

Skills let you package organizational knowledge as curated, versioned playbooks that Claude can use.

### Core Capabilities
1. **Curated knowledge**: Human-verified, policy-safe content
2. **Version control**: Track changes, roll back if needed
3. **Dynamic attachment**: Attach skills based on conversation context
4. **Progressive disclosure**: Claude loads skill content as needed

### Skills vs RAG

| Aspect | RAG | Skills |
|--------|-----|--------|
| Content | Retrieved chunks | Curated playbooks |
| Verification | Raw documents | Human-reviewed |
| Policy | Not built-in | Built-in guardrails |
| Versioning | Document-level | Skill-level |
| Use case | Document search | Expert behavior |

### Skill Structure

```
skills/
├── customer_success/
│   ├── SKILL.md          # When to use, guidelines
│   └── references/
│       ├── objections.md # Common objections
│       └── case_studies.md
└── technical/
    ├── SKILL.md
    └── references/
        └── architecture.md
```

## Response Guidelines

1. **Explain the value**: Verified knowledge, not just retrieval
2. **Use RAG analogy**: "Like RAG, but with policy and versioning"
3. **Show structure**: SKILL.md + references pattern
4. **Emphasize curation**: Human-in-the-loop for quality
