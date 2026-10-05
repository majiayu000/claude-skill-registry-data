---
name: research-team
description: Spawn a research agent team for multi-source investigation. Use when researching topics requiring multiple URL fetches, cross-referencing, and synthesis.
user-invocable: true
argument-hint: <topic-to-research>
context: fork
agent: researcher
---

# Research Team Spawn Recipe

## Team Composition

| Role | Model | Tools | Purpose |
|------|-------|-------|---------|
| **Lead** (you) | inherit | All | Decompose task, assign sources, synthesize results |
| **Researcher(s)** | Haiku | Read, Glob, Grep, Bash, Write, Edit + agent-fetch | Fetch + analyze + write findings |
| **Reviewer** | Sonnet | Read, Glob, Grep | Cross-reference, identify contradictions, quality check |

## Spawn Protocol

1. **Decompose** the research topic into 2-4 independent source groups
2. **Spawn researchers** (one per source group) as background agents:
   ```
   For each source group, spawn a researcher agent with:
   - Specific URLs or search terms to investigate
   - Target output file: docs/research/trail/deep-reviews/<topic>.md
   - Provenance records: docs/research/trail/findings/finding-<slug>.yaml
   ```
3. **Spawn reviewer** after researchers complete:
   - Cross-reference all findings for contradictions
   - Identify gaps requiring follow-up
   - Quality-check source citations
4. **Synthesize** results into a summary

## File Ownership (No Conflicts)

| Owner | Writes To | Cannot Touch |
|-------|-----------|-------------|
| Researcher A | findings/finding-<topic>-a-*.yaml | Other researchers' files |
| Researcher B | findings/finding-<topic>-b-*.yaml | Other researchers' files |
| Reviewer | (read-only) | Everything |
| Lead | deep-reviews/<topic>.md, source-catalog.md | findings/ |

## Quality Gate
- Every URL fetched must be logged in source-catalog.md
- Every finding must have a YAML provenance record
- Contradictions between sources must be flagged
- Final synthesis must cite specific findings

## Source Discovery Protocol
- Log EVERY URL encountered (HIGH/MEDIUM/LOW/SKIP classification)
- Never silently discard a URL
- Use `npx agent-fetch "<url>" --json` for full content (never WebFetch)
