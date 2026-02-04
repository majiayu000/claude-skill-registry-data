---
name: content-documenter
description: |
  Generate structured ContentSummary JSON from analyzed content.
  Use after media-reviewer to produce final output with all 16 fields.
tools: Read, Write
---

# Content Documenter Skill

Transforms media-reviewer analysis into structured JSON documentation.

## What This Skill Does

Takes your media-reviewer analysis and produces ContentSummary JSON
with all 16 required fields.

## Input

You should have already used media-reviewer skill which provides:
- Deep understanding of content structure
- Core ideas and their connections
- Narrative flow analysis
- Key moments and quotes with timestamps
- Thematic patterns

## Output Fields

### Core Fields (7)

1. **contentId** (string)
   - Copy from input file frontmatter id field

2. **headline** (string, 10-200 chars)
   - One compelling sentence capturing the essence
   - Should make someone want to read more
   - Focus on the unique value or insight

3. **tldr** (string, 20-500 chars)
   - 3-5 sentence summary
   - Cover the main points concisely
   - Answer: "What is this about and why does it matter?"

4. **bullets** (string[], 1-10 items)
   - Key points as bullet list
   - Each bullet = one distinct insight
   - Ordered by importance or logical flow

5. **tags** (string[], 1-20 items)
   - Topic tags for categorization
   - Include broad tags (e.g., "AI") and specific (e.g., "Constitutional AI")
   - Lowercase, no special characters

6. **sentiment** ("positive" | "neutral" | "negative")
   - Overall tone of content
   - Based on language and framing, not topic

7. **category** (string)
   - Content type: article, video, podcast, tutorial, interview, etc.

8. **score.relevanceToUser** (number, 0-1)
   - Based on user-profile.json topics
   - 1.0 = perfectly matches user interests
   - 0.0 = no relevance to user interests
   - Calculate: sum(matched topic weights) / sum(all topic weights)

### Documentary Fields (8)

9. **overview** (string, min 50 chars)
   - 2-3 rich paragraphs introducing the material
   - Write for someone unfamiliar with the content
   - Cover: what it is, who it's for, why it matters
   - Set the stage for detailed analysis

10. **keyThemes** (string[], 3-7 items)
    - Main topics/themes identified
    - Broader than tags, more conceptual
    - Examples: "The tension between safety and capability"

11. **detailedAnalysis** (string, min 100 chars)
    - Documentary-style breakdown
    - Follow the content's structure
    - Explain each major section/segment
    - Include specific details and examples

12. **narrativeFlow** (string, min 50 chars)
    - How the content progresses
    - Explain the arc and transitions
    - Show how ideas build on each other
    - Note pacing and structure choices

13. **coreIdeas** (CoreIdea[], 1-10 items)
    Each item has:
    - concept: string - the idea name
    - explanation: string (min 10 chars) - what it means in this context
    - examples?: string[] - specific examples from content

14. **importantQuotes** (Quote[], 0-20 items)
    Each item has:
    - text: string - EXACT verbatim quote (never paraphrase!)
    - timestamp?: string - HH:MM:SS or MM:SS format (for video/audio)
    - context?: string - what was being discussed when this was said

15. **context** (string, min 20 chars)
    - Background needed to understand the content
    - Prerequisites or prior knowledge assumed
    - Historical or situational context
    - Related work or references mentioned

16. **relatedConcepts** (string[], 0-15 items)
    - Related topics mentioned or implied
    - Connections to other ideas or fields
    - What someone might want to learn next

## Timestamp Format

For video/audio content:
- `0:30` - 30 seconds
- `2:45` - 2 minutes 45 seconds
- `1:30:00` - 1 hour 30 minutes
- Always use the format from the source (don't normalize)

## JSON Output Example

```json
{
  "contentId": "abc123",
  "headline": "Constitutional AI introduces a novel approach to aligning language models through self-critique",
  "tldr": "This video explains Constitutional AI, Anthropic's method for training helpful and harmless AI assistants. The approach uses a set of principles (a 'constitution') to guide the model's self-improvement, reducing the need for human feedback while maintaining safety.",
  "bullets": [
    "Constitutional AI uses self-critique guided by explicit principles",
    "The method reduces reliance on human feedback for safety training",
    "Models learn to identify and correct their own harmful outputs"
  ],
  "tags": ["ai", "safety", "alignment", "constitutional-ai", "anthropic", "rlhf"],
  "sentiment": "positive",
  "category": "video",
  "score": { "relevanceToUser": 0.85 },
  "overview": "This comprehensive video from Anthropic introduces Constitutional AI...",
  "keyThemes": [
    "AI Safety and Alignment",
    "Self-supervised learning for safety",
    "Reducing human feedback requirements",
    "Explicit principles for AI behavior"
  ],
  "detailedAnalysis": "The video opens with a clear problem statement...",
  "narrativeFlow": "The presentation follows a classic problem-solution structure...",
  "coreIdeas": [
    {
      "concept": "Constitutional AI",
      "explanation": "An alignment approach where AI models critique and revise their own outputs based on explicit principles",
      "examples": ["A model generating a harmful response, then self-critiquing"]
    }
  ],
  "importantQuotes": [
    {
      "text": "The key insight is that we can use AI to supervise AI",
      "timestamp": "12:34",
      "context": "Explaining the core mechanism that makes Constitutional AI scalable"
    }
  ],
  "context": "This video builds on prior work in RLHF...",
  "relatedConcepts": ["RLHF", "red teaming", "scalable oversight", "AI alignment"]
}
```

## Quality Checklist

Before outputting, verify:
- All 16 fields are present
- All minimum lengths are met
- Quotes are exact (verbatim)
- Timestamps are included for video/audio
- contentId matches input file
- relevanceToUser is calculated from user profile
- JSON is valid

## Important Rules

- Include ALL 16 fields - never omit any
- Use exact verbatim quotes - never paraphrase
- Include timestamps when source has them
- Meet all minimum character requirements
- Follow the JSON schema exactly
- Base relevanceToUser on actual user profile
- Never paraphrase quotes
- Never add interpretation beyond source
- Never omit required fields
- Never guess timestamps - only include if known
