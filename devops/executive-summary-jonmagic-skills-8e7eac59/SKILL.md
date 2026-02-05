---
name: executive-summary
description: Create formal executive summaries from GitHub conversations or meeting transcripts. Use when generating leadership-ready summaries that distill key decisions, alternatives, outcomes, and next steps from complex conversations or meetings. Supports GitHub issues/PRs and transcript URIs (Zoom, Teams, etc.). Outputs are saved to Executive Summaries/ with date-organized structure.
---

# Executive Summary Skill

Create formal, narrative-driven executive summaries for leadership and stakeholders. This skill handles two primary workflows: synthesizing GitHub conversations (issues, pull requests, discussions) and distilling meeting transcripts (Zoom, Teams, etc.) into concise, decision-focused summaries.

## Related Skills

**Use `brain-operating-system` skill** for:
- Output directory structure and naming conventions (`Executive Summaries/YYYY-MM-DD/`)
- Date folder creation patterns and file numbering

**Use `voice-and-tone` skill** for:
- Narrative construction and paragraph patterns
- First-person framing when appropriate
- Crediting collaborators and showing impact

**Use `github-interaction` skill** for:
- Fetching complete GitHub conversations (issues, PRs, discussions)
- Comment and review retrieval patterns
- Pagination handling

## Core Principles

All executive summaries follow these unifying principles, regardless of source:

### Narrative-Driven Prose

- Structure content as **dense, logically-connected paragraphs** in formal, authoritative tone
- Avoid bullet points, subheaders, or lists
- Each paragraph builds on the previous, conveying a cohesive narrative of evolution from initial topic through decisions and next steps
- Limit length to **3–5 structured paragraphs** (GitHub summaries may run longer for complex decisions)

### Impact & Decision Focus

- Include **only details that significantly influenced direction, decisions, or outcomes**
- Omit administrative commentary, routine pleasantries, subscription messages, procedural remarks, superficial technical minutiae (code diffs, exact timestamps), or automation events
- Center on **key debates, decisions, constraints, resolutions, and business/user impact**
- Clearly articulate **alternatives explored, current status, next steps, and individual responsibilities**

### Contextual Linking

- Every piece of cited information must link to its source
- Attribute statements to individuals by name (no @ symbol on names themselves)
- Links follow the statement or are integrated into sentences
- Ensure readers can drill into source material for deeper context

### Formal Tone & Authority

- Use complete, well-structured sentences
- Integrate all references and links seamlessly without extraneous formatting
- Write for educated, time-constrained readers

## Workflow: GitHub Conversations

For GitHub issues, pull requests, and discussions:

1. **Fetch the complete conversation** using the [`github-interaction` skill](../github-interaction/SKILL.md). This ensures you capture all comments, reviews, and state changes necessary for context.

2. **Identify the narrative arc**: What was the initial problem/request? How did the conversation evolve? What decisions were made?

3. **Apply the rules from [references/github-conversations.md](references/github-conversations.md)**, which details:
   - How to structure GitHub-specific summaries
   - Linking patterns for comments, events, and status changes
   - Handling alternative solutions and partial resolutions
   - Ignoring bot-generated events

4. **Save the summary** to the correct location (see "Output Location & Naming" section below)

## Workflow: Meeting Transcripts

For Zoom, Teams, or other meeting transcripts:

1. **Fetch the transcript** from the provided URI using HTTP or platform-specific tools

2. **Parse and prepare the transcript**: Extract speaker attributions, timestamps, and key discussion points

3. **Apply the rules from [references/transcript-summaries.md](references/transcript-summaries.md)**, which details:
   - Attribution patterns for named participants
   - How to reference shared documents or screens
   - Handling decisions and action items
   - Appropriate scope and constraints for transcript summaries

4. **Save the summary** to `Executive Summaries/YYYY-MM-DD/##.md` (use today's date; sequential numbering within each date folder)

## Quick Reference: Which Workflow?

| Source | Use This Workflow | Notes |
| --- | --- | --- |
| GitHub issue, PR, discussion URL | GitHub Conversations | Fetch using `github-interaction` skill; apply GitHub-specific rules |
| Zoom/Teams transcript or recording URI | Meeting Transcripts | Fetch transcript; parse for speakers; apply transcript-specific rules |
| Email thread, Slack conversation | GitHub Conversations (adapted) | If available as a GitHub discussion or converted to one, use GitHub workflow; otherwise, treat as narrative text input |

## Tips for Quality Summaries

- **Start by understanding the arc**: Skim the conversation or transcript to understand the trajectory before drafting
- **Prioritize decision impact**: What changed as a result of this conversation? Lead with that
- **Use participant names strategically**: Name decision-makers and key contributors; anonymize or skip minor commenters
- **Link judiciously but comprehensively**: Every claim should be traceable; avoid standalone links
- **Edit for density**: Remove connecting words, tighten sentences, but preserve clarity
