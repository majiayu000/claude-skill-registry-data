---
name: knowledge-capture
description: >
  Use when converting completed work into durable knowledge. This skill provides
  a systematic process for extracting lessons learned, patterns, and insights from
  completed work and storing them in memory systems (PARA, Gigabrain, OpenStinger)
  for future reuse.
---

# Knowledge Capture

## Overview
This skill defines how to extract and store knowledge from completed work. Without deliberate capture, valuable insights are lost when sessions end or contexts are compacted. Use this skill after significant work is completed to ensure learning persists.

## When to Use
- After completing a non-trivial task or solving a difficult problem
- When discovering a pattern, workaround, or technique worth sharing
- Before a session ends that involved significant learning
- After resolving a bug, issue, or failure with a non-obvious solution
- **Don't use when:** Work was routine with no new insights learned

## Core Procedures

### Step 1: Identify Capturable Knowledge
Ask these questions about your completed work:
- What was the hardest part of this task?
- What took longer than expected and why?
- What assumption turned out to be wrong?
- What pattern or approach would be useful for similar future work?
- What mistake was almost made (or was made)?

### Step 2: Structure the Knowledge
Package findings using this structure:

```
KNOWLEDGE CAPTURE
================
Topic: [what domain this applies to]
Context: [project, company, or system this relates to]
Date: [when this was learned]
Captured by: [agent name]

FINDING:
[clear statement of the knowledge - 1-3 sentences]

EVIDENCE:
[what happened, what proves this is true]

APPLICABILITY:
- Applies when: [conditions where this knowledge is relevant]
- Does NOT apply when: [conditions where this knowledge is misleading]

ACTION:
[what should be done differently based on this knowledge]

TAGS:
[gigabrain tags for discoverability: domain, topic, type]

RELATED:
[existing PARA entries, skills, or knowledge this connects to]
```

### Step 3: Store in Appropriate Systems
Route knowledge to the right storage layer:

| Knowledge Type | Primary Storage | Secondary |
|---------------|----------------|-----------|
| Technical patterns | PARA/resources | Gigabrain |
| Process improvements | PARA/areas | Gigabrain |
| Bug root causes | PARA/resources | OpenStinger |
| Domain insights | Discipline-specific para | Gigabrain |
| Cross-company learnings | Cross-company para | OpenStinger |
| One-time lessons | Daily memory file | LCM |

### Step 4: Update Relevant Resources
- Add new entries to discipline knowledge bases
- Update existing skill files if the knowledge changes procedures
- Tag with appropriate gigabrain tags for automatic surfacing
- Notify relevant team leads if the knowledge affects their domain

## Quality Checklist
- [ ] Finding is clearly stated and actionable
- [ ] Evidence supports the finding (not just opinion)
- [ ] Applicability boundaries are explicit
- [ ] Storage location is appropriate for the knowledge type
- [ ] Tags enable future discoverability
- [ ] Related knowledge is cross-referenced

## Error Handling
- **Error:** Knowledge conflicts with existing stored knowledge
  **Response:** Document both findings, flag for review by domain specialist or team lead
- **Error:** Knowledge is too sensitive to store (security, credentials)
  **Response:** Store only the sanitized pattern without sensitive context
- **Error:** Knowledge is too specific to be broadly useful
  **Response:** Store in daily memory file only, with note to promote if pattern recurs
- **Error:** No obvious storage location
  **Response:** Store in PARA/resources as draft, flag for taxonomy review

## Cross-Team Integration
**Related Skills:** knowledge-retrieval, lessons-learned-synthesis, taxonomy-standards, knowledge-transfer
**Used By:** ALL agents after significant work completion