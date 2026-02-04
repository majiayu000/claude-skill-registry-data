---
name: writing-kit-assembler
description: |
  Looplia writer skill for assembling final writing kits.
  Combines content analysis and ideas into structured output with suggested outlines.
  Creates comprehensive WritingKit JSON with all components.
tools: Read, Write
---

# Writing Kit Assembler Skill

Assemble comprehensive writing kits from analysis and ideas.

## Purpose

Combine outputs from earlier workflow steps into a final, actionable writing kit:
- Content summary and metadata
- Generated ideas (hooks, angles, questions)
- Suggested outline with sections
- Supporting quotes and references

## Process

### Step 1: Read Analysis

Read content analysis JSON (first input):
- contentId
- source metadata
- summary (headline, tldr, bullets)
- keyThemes
- importantQuotes
- coreIdeas

### Step 2: Read Ideas

Read idea synthesis JSON (second input):
- hooks
- angles
- questions
- personalization context

### Step 3: Create Suggested Outline

Design a structured outline:

```
Introduction
├── Hook (from ideas)
├── Context/Background
└── Thesis/Main Point

Body Sections (3-5)
├── Section 1: {Theme from analysis}
│   ├── Key point
│   ├── Supporting quote
│   └── Transition
├── Section 2: {Theme from analysis}
│   └── ...
└── Section N: {Theme from analysis}

Conclusion
├── Summary of key points
├── Call to action (from angles)
└── Closing thought
```

### Step 4: Map Content to Sections

For each body section:
1. Choose a key theme from analysis
2. Identify supporting quotes
3. Connect to relevant ideas/angles
4. Write section summary

### Step 5: Assemble WritingKit

Combine all components into final structure.

### Step 6: Write Output

Output complete WritingKit JSON.

## Input

Two input files:
1. Analysis JSON from media-reviewer
2. Ideas JSON from idea-synthesis

## Output Schema

```json
{
  "contentId": "string",
  "source": {
    "type": "video|audio|article|transcript",
    "title": "Original content title",
    "url": "Source URL if available",
    "creator": "Author/creator name"
  },
  "summary": {
    "headline": "One compelling sentence",
    "tldr": "3-5 sentence summary",
    "bullets": ["Key point 1", "Key point 2", "Key point 3"],
    "keyThemes": ["theme1", "theme2"],
    "importantQuotes": [
      {
        "text": "Exact quote from source",
        "timestamp": "12:34",
        "context": "What was being discussed"
      }
    ]
  },
  "ideas": {
    "hooks": [
      { "text": "Hook text", "type": "question" }
    ],
    "angles": [
      { "perspective": "...", "approach": "..." }
    ],
    "questions": [
      { "text": "...", "depth": "medium" }
    ]
  },
  "suggestedOutline": {
    "title": "Suggested article title",
    "sections": [
      {
        "heading": "Introduction",
        "type": "intro",
        "points": ["Hook with question", "Establish context", "Preview main argument"],
        "suggestedHook": "What if...?"
      },
      {
        "heading": "Section title based on theme",
        "type": "body",
        "points": ["Main point", "Evidence/quote", "Analysis"],
        "supportingQuote": {
          "text": "Quote from source",
          "timestamp": "5:23"
        },
        "theme": "Related theme from analysis"
      },
      {
        "heading": "Conclusion",
        "type": "conclusion",
        "points": ["Summarize key insights", "Call to action", "Final thought"],
        "suggestedAngle": "Skeptic's view"
      }
    ]
  },
  "meta": {
    "generatedAt": "2025-01-15T10:30:00Z",
    "workflowVersion": "2.0.0",
    "stepsCompleted": ["analyze-content", "generate-ideas", "build-writing-kit"]
  }
}
```

## Outline Design Guidelines

### Introduction Section
- Start with a hook from ideas
- Establish why this matters
- Preview the structure

### Body Sections (3-5)
- One theme per section
- Include supporting quote when available
- Build logical progression
- Connect to angles where relevant

### Conclusion Section
- Summarize (don't repeat)
- Include call to action
- End with memorable thought

## Section Mapping

| Analysis Component | Outline Usage |
|--------------------|---------------|
| keyThemes | Body section headings |
| importantQuotes | Section supporting quotes |
| coreIdeas | Section key points |
| hooks | Introduction opener |
| angles | Body perspectives, conclusion CTA |
| questions | Section discussion points |

## Quality Checklist

Before outputting:
- [ ] All required fields present
- [ ] contentId matches across inputs
- [ ] At least 3 body sections
- [ ] Each body section has heading and points
- [ ] Quotes are properly attributed
- [ ] Meta includes timestamp
- [ ] JSON is valid

## Important Rules

1. **Include all components** - Don't omit summary, ideas, or outline
2. **Preserve quotes exactly** - Never paraphrase
3. **Keep timestamps** - If input has them, output has them
4. **Match contentId** - Same ID across all components
5. **Design actionable outlines** - Writer should be able to start immediately
6. **Use sonnet model** - This requires synthesis and organization
