---
name: mindwork-analyze
description: Analyze therapy session transcripts or journal entries. Identifies cognitive patterns, emotional themes, and tracks progress over time. Automatically references recent analyses for context. Use for session analysis, journal reflection analysis, or pattern identification.
---

# Therapy & Journal Analyzer

Part of the **mindwork** suite. Analyzes transcripts and journal entries to identify patterns, themes, and track progress.

## What It Does

1. **Reads** the specified transcript or journal entry
2. **Loads context** from recent analyses (last 5 by default)
3. **Identifies** cognitive patterns and potential distortions
4. **Extracts** emotional themes and triggers
5. **Tracks progress** compared to previous sessions
6. **Saves** structured analysis to the configured output folder

## Prerequisites

- A `mindwork.yaml` config file (optional but recommended)
- Transcript or journal files to analyze

## Usage Examples

### Analyze a Session Transcript

> "Analyze my therapy session from transcriptions/2024-01-15-session.md"

### Analyze a Journal Entry

> "Analyze today's journal entry at journals/daily/2024-01-18.md"

### Analyze by Journal Type

> "Analyze my dream log from last night"
> "Analyze all gratitude entries from this week"
> "What patterns appear in my anxiety journal?"

### Analyze with Explicit Output Path

> "Analyze transcriptions/session-005.md and save to analysis/session-005-analysis.md"

### Analyze Multiple Entries

> "Analyze all journal entries from this week"

### Compare Sessions

> "Analyze my last 3 therapy sessions and compare the themes"

## How to Perform Analysis

When analyzing content, follow this structured approach:

### Step 1: Load Configuration

Check for `mindwork.yaml` in these locations (in order):
1. Current directory (`./mindwork.yaml`)
2. XDG config (`~/.config/mindwork/config.yaml`)
3. Home directory (`~/.mindwork.yaml`)

Extract:
- `outputs.analysis` - where to save analysis files
- `preferences.context_count` - how many recent analyses to load (default: 5)

### Step 2: Load Context

Read the most recent analysis files from the output directory for context. This enables progress tracking across sessions.

Look for files matching `*-analysis.md` in the analysis folder, sorted by date/name descending.

### Step 3: Read Input Content

Read the specified transcript or journal file completely.

### Step 4: Perform Analysis

Analyze the content using the frameworks below.

### Step 5: Generate Output

Create a structured markdown file following the output template.

### Step 6: Save and Summarize

Save to the configured analysis folder and provide a brief summary to the user.

---

## Analysis Framework

### Cognitive Patterns to Identify

When analyzing content, look for these cognitive patterns (often called "cognitive distortions" in CBT):

| Pattern | Description | Example |
|---------|-------------|---------|
| **All-or-Nothing Thinking** | Seeing things in black and white | "I'm a complete failure" |
| **Overgeneralization** | One event becomes a never-ending pattern | "This always happens to me" |
| **Mental Filter** | Focusing only on negatives | Dwelling on one criticism despite praise |
| **Disqualifying the Positive** | Rejecting positive experiences | "That doesn't count" |
| **Mind Reading** | Assuming you know what others think | "They must think I'm incompetent" |
| **Fortune Telling** | Predicting negative outcomes | "I know this will go wrong" |
| **Catastrophizing** | Expecting the worst-case scenario | "If I fail this, my life is over" |
| **Emotional Reasoning** | Feelings as evidence | "I feel stupid, so I must be stupid" |
| **Should Statements** | Rigid rules about how things should be | "I should be further along by now" |
| **Labeling** | Fixed negative labels on self/others | "I'm a loser" |
| **Personalization** | Taking excessive responsibility | "It's all my fault" |
| **Magnification/Minimization** | Blowing up negatives, shrinking positives | Obsessing over mistakes |

### Emotional Themes to Track

- **Primary emotions**: anxiety, sadness, anger, fear, joy, guilt, shame
- **Triggers**: situations, people, thoughts that provoke emotions
- **Coping strategies**: what the person does in response
- **Support systems**: people, activities that help

### Progress Indicators

When context is available, note:
- Recurring themes that appear across sessions
- Changes in how topics are discussed (more/less intensity)
- New coping strategies being tried
- Shifts in perspective or self-awareness
- Growth in emotional vocabulary
- Reduction in cognitive distortion frequency

### Therapeutic Techniques (for transcripts)

When analyzing therapy session transcripts, identify:
- Questions asked by the therapist
- Techniques used (CBT, mindfulness, reflection, etc.)
- Homework or exercises suggested
- Breakthroughs or insights achieved

---

## Output Format

Use this structured format for analysis output:

```markdown
# Analysis: {source_filename}

**Date**: {analysis_date}
**Source**: {source_path}
**Type**: {transcript|journal}
**Journal Type**: {description from config, if journal}

---

## Summary

{2-3 sentence overview of the content and its significance}

---

## Cognitive Patterns Observed

{For each pattern identified:}

### {Pattern Name}
- **Evidence**: "{quote or paraphrase from content}"
- **Context**: {situation in which this appeared}
- **Frequency**: {if recurring, note this}

---

## Emotional Themes

### Primary Emotions
- **{Emotion}**: {context and triggers}

### Triggers Identified
- {Trigger 1}: {description}
- {Trigger 2}: {description}

### Coping Strategies Noted
- {Strategy}: {how it was used, effectiveness}

---

## Key Insights

- {Insight 1}
- {Insight 2}
- {Insight 3}

---

## Progress Notes

{If previous analyses are available:}

### Compared to Previous Sessions
- {Notable change or pattern}
- {Theme that persists or evolved}

### Recurring Themes
- {Theme that appears across sessions}

### Growth Observed
- {Positive development noted}

---

## Suggested Focus Areas

{Areas that might benefit from attention in future sessions or reflection:}

1. {Area 1}: {why and potential approach}
2. {Area 2}: {why and potential approach}

---

## Therapist Techniques (if applicable)

{For therapy transcripts only:}

- **{Technique}**: {how it was applied, client response}

---

*Analysis generated by mindwork*
```

---

## Naming Convention

Save analysis files using this pattern:
```
{date}-{original-name}-analysis.md
```

Examples:
- `2024-01-15-session-001-analysis.md`
- `2024-01-18-morning-journal-analysis.md`

---

## Notes

### Privacy
Analysis files contain sensitive personal information. Store them securely.

### Context Handling
When loading previous analyses for context:
- Read the Summary and Progress Notes sections for quick context
- Look for Recurring Themes to track longitudinal patterns
- Note Suggested Focus Areas from previous analyses

### Journal vs Transcript Analysis
- **Transcripts**: Include therapist technique analysis, note the dialogue flow
- **Journals**: Focus more on self-reflection quality, internal processing

### Journal Type-Aware Analysis

When the config specifies journal types with descriptions, tailor the analysis:

| Journal Type | Analysis Focus |
|--------------|----------------|
| **Daily reflections** | Mood tracking, daily patterns, routine impacts |
| **Dream logs** | Symbolism, recurring imagery, emotional themes in dreams |
| **Gratitude entries** | Positive patterns, what brings joy, growth in appreciation |
| **Prompt card responses** | Depth of self-exploration, recurring themes across prompts |
| **Anxiety tracking** | Trigger identification, coping effectiveness, intensity patterns |

To determine journal type:
1. Check `mindwork.yaml` for `sources.journals.sources`
2. Match the file path to a configured source
3. Use the `description` field for context
4. Include the journal type in the analysis header

### Partial Analysis
If only partial content is available or readable, note this in the analysis and work with what's available.
