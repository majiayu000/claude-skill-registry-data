---
name: meeting-analyzer
description: "Analyze and restructure meeting transcripts into actionable notes. Use when processing raw meeting transcripts, identifying action items, extracting takeaways, or when user mentions 'analyze meeting', 'meeting notes', 'process transcript', or 'meeting summary'."
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Meeting Analyzer

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Transform raw meeting transcripts into structured, actionable notes.

## Commands

- `/meeting analyze {file}` - Analyze a single transcript
- `/meeting analyze-all {folder}` - Process all transcripts in a folder
- `/meeting summary {file}` - Quick summary without full restructuring

## Process

### Step 1: Read & Extract Metadata
- **Date:** from filename or content
- **Attendees:** speakers identified
- **Type:** 1:1, standup, planning, review, external
- **Context:** which context this meeting belongs to

### Step 2: Content Analysis
1. **Topics:** Identify main discussion points, group related items
2. **Decisions:** Look for "We decided...", "Let's go with...", "Agreed that..."
3. **Action Items:** "I will...", "You should...", "[Name] to...", "By [date]..."
4. **Project References:** Cross-reference `contexts/{context}/projects/`
5. **Key Takeaways:** Strategic decisions, risks, opportunities, feedback
6. **Sentiment:** Positive / Neutral / Concerning / Urgent

### Step 3: Generate Output

## Output Format

```markdown
# Meeting: {Title}

**Date:** YYYY-MM-DD | **Type:** {type} | **Context:** {context}
**Participants:** {names}

## Executive Summary
{2-3 sentences} | **Sentiment:** {assessment}

## Key Takeaways
1. **{Takeaway}** - {explanation}

## Discussion Topics
### {Topic}
{Summary} | **Outcome:** {conclusion}

## Decisions Made
| # | Decision | Owner | Impact | Deadline |
|---|----------|-------|--------|----------|

## Action Items
| # | Action | Owner | Due Date | Priority |
|---|--------|-------|----------|----------|

## Risks & Concerns
| Risk | Raised By | Mitigation | Priority |
|------|-----------|------------|----------|

## Follow-up Required
- [ ] {items}
```

## File Naming Convention

```
YYYY-MM-DD-{meeting-type}-{topic}.md
```

## Batch Processing (`/meeting analyze-all {folder}`)

Process all files, generate structured output per file, then aggregate:
- Action items by owner
- Projects referenced
- Recurring topics

## Quality Checks

- [ ] All action items have owners and due dates
- [ ] Key decisions captured
- [ ] Project references linked
- [ ] File naming follows convention

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
