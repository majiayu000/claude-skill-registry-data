---
name: knowledge-retrieval
description: >
  Use before starting any new work to check for existing knowledge. This skill provides
  a systematic search and retrieval process for finding relevant knowledge from memory
  systems (PARA, Gigabrain, OpenStinger, existing skills) before starting work,
  preventing redundant effort and leveraging prior learning.
---

# Knowledge Retrieval

## Overview
This skill defines how to find and use existing knowledge before starting work. The enterprise has accumulated knowledge across many sessions and agents - this skill ensures you find and use it instead of rediscovering solutions. Always run this skill as the first step in any non-trivial task.

## When to Use
- Before starting any new task or project
- When encountering a problem that seems familiar
- When asked to solve something another agent may have tackled
- When working in a domain outside your primary expertise
- **Don't use when:** Task is trivial, routine, or clearly has no prior knowledge available

## Core Procedures

### Step 1: Define the Search
Before searching, clarify what you're looking for:
- **Topic:** What domain or subject area?
- **Problem type:** What kind of problem (bug, design, process, analysis)?
- **Keywords:** What terms would relevant knowledge be tagged with?
- **Scope:** Which company, team, or system might have relevant knowledge?

### Step 2: Search Strategy (in order)

#### Level 1: Direct Knowledge Check (always do)
- Check your own PARA resources and knowledge base
- Check relevant skill files for procedures
- Look for similar completed tasks in your history

#### Level 2: Cross-Agent Check (for non-trivial work)
- Search Gigabrain for tagged insights matching your keywords
- Check OpenStinger for cross-session patterns
- Look for relevant daily memory files from other agents

#### Level 3: Cross-Company Check (for novel or complex work)
- Check other companies' knowledge bases in same domain
- Search discipline-specific PARA entries across all companies
- Look for cross-company collaboration records

### Step 3: Evaluate Retrieved Knowledge
For each piece of knowledge found:
1. **Relevance:** Does this actually apply to my current problem?
2. **Currency:** Is this still valid, or has something changed?
3. **Authority:** Was this from a reliable source (tested, validated, expert agent)?
4. **Completeness:** Is this the full solution or just a partial insight?

### Step 4: Apply and Adapt
- Use retrieved knowledge as starting point, not final answer
- Adapt solutions to current context (don't copy blindly)
- Note any gaps between retrieved knowledge and current needs
- Document modifications for future knowledge capture

### Step 5: Document the Search
If you searched and found nothing:
- Record that a search was performed and returned empty
- This is itself valuable knowledge (prevents redundant future searches)
- Capture any near-misses (similar but not quite applicable)

## Quality Checklist
- [ ] Search was performed at appropriate depth for task complexity
- [ ] Retrieved knowledge was evaluated for relevance and currency
- [ ] Applied knowledge was adapted to current context
- [ ] Search results (including "nothing found") are documented
- [ ] Any knowledge gaps identified for future capture

## Error Handling
- **Error:** Found knowledge but it's contradictory
  **Response:** Use most recent/authoritative source, flag contradiction for resolution
- **Error:** Found partial knowledge that doesn't fully solve the problem
  **Response:** Use what's available, fill gaps with best judgment, capture complete solution when done
- **Error:** Found outdated knowledge that no longer applies
  **Response:** Note the obsolescence, update or archive the old entry with current knowledge
- **Error:** Search returns overwhelming number of results
  **Response:** Narrow search scope, focus on most relevant tags, escalate to knowledge manager if pattern persists

## Cross-Team Integration
**Related Skills:** knowledge-capture, taxonomy-standards, source-verification, lessons-learned-synthesis
**Used By:** ALL agents as first step in non-trivial work