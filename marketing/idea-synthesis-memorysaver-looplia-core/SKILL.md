---
name: idea-synthesis
description: |
  Looplia writer skill for generating content ideas with personalization.
  Reads user profile for context. Generates hooks, angles, and thought-provoking questions.
  Use after media-reviewer to transform analysis into creative content ideas.
tools: Read, Skill
---

# Idea Synthesis Skill

Generate creative content ideas from analyzed content, personalized for the user.

## Purpose

Transform content analysis into actionable writing ideas:
- Attention-grabbing hooks
- Unique angles/perspectives
- Thought-provoking questions

## Process

### Step 1: Read User Profile

Use the user-profile-reader skill to get user context:
- Topics of interest and expertise levels
- Preferred writing style
- Target audience

```
Skill("user-profile-reader")
```

### Step 2: Read Content Analysis

Read the input file containing content analysis from media-reviewer:
- Key themes
- Important quotes
- Narrative structure
- Core ideas

### Step 3: Generate Hooks

Create 3-5 attention-grabbing openers:

| Hook Type | Description | Example |
|-----------|-------------|---------|
| Question | Opens with a compelling question | "What if everything you knew about X was wrong?" |
| Statistic | Leads with surprising data | "90% of writers miss this critical step..." |
| Story | Starts with a brief narrative | "When I first discovered X, I was skeptical..." |
| Contrast | Highlights a surprising contradiction | "Most experts say X, but the data shows Y..." |
| Bold Statement | Makes a provocative claim | "X is dead. Here's what's replacing it..." |

### Step 4: Generate Angles

Create 3-5 unique perspectives on the content:

For each angle:
- **Perspective**: What viewpoint does this take?
- **Approach**: How would you develop this angle?
- **Target**: Who would this appeal to?

### Step 5: Generate Questions

Create 5-7 discussion starters:

| Depth | Description |
|-------|-------------|
| Surface | Basic comprehension questions |
| Medium | Application and analysis questions |
| Deep | Synthesis and evaluation questions |

### Step 6: Personalize

Apply user profile:
- Emphasize topics matching user interests
- Adjust complexity to user's expertise level
- Align with user's writing style

### Step 7: Write Output

Output JSON with all generated ideas.

## Input

Content analysis JSON from media-reviewer containing:
- `contentId`
- `keyThemes`
- `importantQuotes`
- `coreIdeas`

## Output Schema

```json
{
  "contentId": "string",
  "hooks": [
    {
      "text": "What if the key to X isn't Y, but Z?",
      "type": "question"
    },
    {
      "text": "According to new research, 80% of...",
      "type": "statistic"
    }
  ],
  "angles": [
    {
      "perspective": "Skeptic's view",
      "approach": "Challenge the main premise with counterexamples",
      "target": "Readers who question conventional wisdom"
    },
    {
      "perspective": "Beginner's guide",
      "approach": "Break down complex concepts for newcomers",
      "target": "People new to this topic"
    }
  ],
  "questions": [
    {
      "text": "What would happen if we applied this to everyday life?",
      "depth": "medium"
    },
    {
      "text": "How does this change our understanding of X?",
      "depth": "deep"
    }
  ],
  "personalization": {
    "matchedTopics": ["ai", "productivity"],
    "adjustedFor": "intermediate expertise"
  }
}
```

## Quality Guidelines

### Good Hooks
- Specific, not generic
- Create curiosity
- Promise value
- Match content tone

### Good Angles
- Unique perspective
- Actionable approach
- Clear target audience
- Connected to content themes

### Good Questions
- Open-ended (not yes/no)
- Thought-provoking
- Multiple valid answers
- Encourage discussion

## Important Rules

1. **Always read user profile first** - Personalization is key
2. **Include all hook types** - Variety in approaches
3. **Cover all depth levels** - Questions for different readers
4. **Stay true to content** - Ideas must derive from source
5. **Be specific** - Avoid generic, cookie-cutter ideas
