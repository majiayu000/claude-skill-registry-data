---
name: mindwork-insights
description: Build and maintain a personal profile from therapy sessions and journal entries. Creates a living document that accumulates self-knowledge about patterns, strengths, coping strategies, and growth over time. Unlike other skills, insights updates an existing profile rather than creating new files.
---

# Personal Profile Builder

Part of the **mindwork** suite. Creates and maintains a living profile document that accumulates self-knowledge over time.

## What It Does

1. **Reads** analysis files to extract patterns and insights
2. **Builds** a comprehensive personal profile
3. **Updates** the profile as new sessions are analyzed
4. **Preserves** existing insights while adding new ones

## Key Difference from Other Skills

| Skill | Focus | Output Behavior |
|-------|-------|-----------------|
| `analyze` | What's in THIS session | Creates new file per session |
| `progress` | How things CHANGE | Creates reports for periods |
| `insights` | What's CONSISTENT | Updates single living document |

**Unique behavior:** The `insights` skill **updates** `profile.md` rather than replacing it. Each invocation enriches the existing profile with new knowledge.

---

## Modes of Operation

### 1. Initial Build

Create a profile from scratch based on all available analysis files.

**Example prompts:**
> "Build my profile from all analyses"
> "Create my initial profile"
> "Start my personal profile"

**Workflow:**
1. Read all files in analysis/ folder
2. Identify recurring patterns across sessions
3. Extract strengths, coping strategies, triggers
4. Create profile.md with all sections populated
5. Save to vault root

### 2. Update

Add new insights from recent sessions to existing profile.

**Example prompts:**
> "Update my profile with recent sessions"
> "Add today's session to my profile"
> "Refresh my profile"

**Workflow:**
1. Read existing profile.md
2. Note the "Last updated" date
3. Read analysis files created after that date
4. Extract new patterns, realizations, strategies
5. Merge into existing sections (don't duplicate)
6. Update metadata
7. Save updated profile.md

### 3. Query

Answer questions about the profile without modifying it.

**Example prompts:**
> "What does my profile say about my coping strategies?"
> "What are my main triggers according to my profile?"
> "Summarize my growth journey"

**Journal type queries:**
> "What patterns appear in my dream logs?"
> "What themes recur in my gratitude entries?"
> "What do my anxiety journal entries reveal about my triggers?"

**Workflow:**
1. Read profile.md
2. Answer the question based on profile content
3. No modifications

---

## Profile Structure

Save as `profile.md` in the vault root.

```markdown
# My Profile

*Last updated: {date}*
*Based on: {N} therapy sessions, {M} journal entries*
*Journal breakdown: {X} daily, {Y} dreams, {Z} gratitude, ...*

---

## Core Patterns

### Thinking Patterns
{Cognitive tendencies that appear consistently}
- **{Pattern}**: {context when it appears}

### Emotional Patterns
{Recurring emotional responses and their contexts}
- {Emotion}: {triggers or situations}

### Triggers
{Situations, people, or thoughts that consistently provoke reactions}
- {Trigger description}

### Patterns by Journal Type
{Insights specific to each journal type}
- **Dream logs**: {recurring themes, symbols, emotions in dreams}
- **Gratitude entries**: {what you're grateful for, patterns in appreciation}
- **Daily reflections**: {mood patterns, daily triggers}
- **{Other types}**: {patterns specific to that journal type}

---

## Strengths

{Positive qualities and capabilities observed across sessions}
- {Strength with brief evidence}

---

## Coping Strategies That Work

{Techniques and approaches that have proven effective}
1. **{Strategy name}** - {when/how it helps}

---

## Relationship Dynamics

### With Authority
{Patterns in relationships with bosses, parents, therapists}

### With Peers
{Patterns with friends, colleagues, siblings}

### With Self
{Self-relationship patterns, inner dialogue tendencies}

---

## Growth Journey

### Major Realizations
{Significant insights and breakthroughs, with dates}
- {Date}: {Realization}

### Skills Developing
{Capabilities that are emerging or improving}
- {Skill in development}

---

## Areas of Focus

{Current therapeutic work and attention areas}
1. {Focus area}

---

*This profile evolves as new insights emerge from sessions and journals.*
```

---

## Extraction Guide

### What to Look For in Analysis Files

**For Core Patterns:**
- Cognitive patterns section: patterns that appear in multiple analyses
- Anything marked as "recurring" or "consistent"
- Patterns noted in Progress Notes as "continues" or "persists"

**For Strengths:**
- Positive observations about the person
- Coping strategies that worked
- Growth markers and improvements
- Self-awareness demonstrations

**For Triggers:**
- Emotional triggers identified
- Situations that provoke strong reactions
- Contexts where patterns emerge

**For Growth Journey:**
- Items from "Key Insights" sections
- Breakthroughs mentioned in analyses
- First-time achievements ("First time...")
- Realizations and connections made

---

## Update Logic

### Merging Strategy

When updating an existing profile:

**DO:**
- Add new patterns not already listed
- Add new entries to Growth Journey with dates
- Update "Skills Developing" if progress is noted
- Add new coping strategies discovered
- Update metadata (date, session count)

**DON'T:**
- Duplicate existing patterns (check before adding)
- Remove patterns that may still be relevant
- Contradict earlier insights without explicit evidence
- Lose historical growth journey entries

### Detecting New vs Existing

Before adding a pattern:
1. Read the relevant section in existing profile
2. Check if a similar pattern is already listed
3. If similar: consider enriching the existing entry
4. If new: add as new bullet point

### Conflict Resolution

If new insights seem to contradict existing profile:
- Note the evolution rather than replacing
- Example: "Harsh inner critic → softening with practice"
- Preserve the growth narrative

---

## Usage Examples

### Building Initial Profile

User: "Build my profile from all my analyses"

Claude will:
1. List all files in analysis/ folder
2. Read each analysis file
3. Extract patterns that appear in 2+ sessions
4. Compile strengths mentioned across sessions
5. Identify effective coping strategies
6. Build growth journey from insights and breakthroughs
7. Create comprehensive profile.md
8. Save to vault root

### Updating After New Sessions

User: "Update my profile with this week's sessions"

Claude will:
1. Read existing profile.md, note last update date
2. Find analysis files newer than that date
3. Read the new analysis files
4. Identify new patterns or reinforced existing ones
5. Add any new realizations to Growth Journey
6. Update session count in metadata
7. Save updated profile.md

### Querying the Profile

User: "What coping strategies work best for me?"

Claude will:
1. Read profile.md
2. Find "Coping Strategies That Work" section
3. Summarize the strategies listed
4. Optionally reference specific sessions where they helped

---

## Notes

### Privacy

The profile.md contains deeply personal information. Store alongside other mindwork files in a secure location.

### Profile Evolution

The profile should reflect growth over time. Early patterns may soften or resolve - this is part of the journey. The Growth Journey section captures this evolution.

### When to Rebuild

Consider rebuilding the profile from scratch if:
- The existing profile feels outdated
- Many sessions have accumulated since last update
- You want a fresh perspective on patterns

Use: "Rebuild my profile from scratch"

### Session Count Tracking

The metadata tracks:
- Total therapy sessions analyzed
- Total journal entries analyzed
- Last update date

This helps you and your therapist understand the basis of the profile.
