---
name: user-profile-reader
description: |
  Read user profile from workspace and calculate content relevance.
  Use to personalize output based on user interests.
tools: Read
---

# User Profile Reader Skill

Read and interpret user preferences for content personalization.

## What This Skill Does

- Reads `user-profile.json` from workspace root
- Provides user context to other processing
- Calculates relevance scores for content

## User Profile Location

`~/.looplia/user-profile.json`

## User Profile Schema

```json
{
  "userId": "string",
  "topics": [
    { "topic": "string", "interestLevel": 1-5 }
  ],
  "style": {
    "tone": "beginner" | "intermediate" | "expert" | "mixed",
    "targetWordCount": 100-10000,
    "voice": "first-person" | "third-person" | "instructional"
  }
}
```

## Relevance Scoring Algorithm

Calculate `score.relevanceToUser` (0-1):

```
1. For each user topic:
   - weight = interestLevel / 5
   - matched = content tags/themes contain topic (case-insensitive)

2. Calculate score:
   - matchedWeight = sum of weights for matched topics
   - totalWeight = sum of all topic weights
   - score = matchedWeight / totalWeight

3. If no user topics defined:
   - score = 0.5 (neutral)
```

## Example Calculation

User profile:
```json
{
  "topics": [
    { "topic": "AI", "interestLevel": 5 },
    { "topic": "productivity", "interestLevel": 3 },
    { "topic": "cooking", "interestLevel": 2 }
  ]
}
```

Content tags: ["AI", "safety", "alignment"]

Calculation:
- AI: matched, weight = 5/5 = 1.0 (contributes to matchedWeight)
- productivity: not matched, weight = 3/5 = 0.6 (contributes to totalWeight only)
- cooking: not matched, weight = 2/5 = 0.4 (contributes to totalWeight only)
- matchedWeight = 1.0
- totalWeight = 1.0 + 0.6 + 0.4 = 2.0
- score = 1.0 / 2.0 = 0.5

## Usage in Other Skills

When content-documenter needs relevance score:
1. Read user-profile.json
2. Compare content tags/themes to user topics
3. Apply algorithm above
4. Return score in `score.relevanceToUser` field

## Handling Edge Cases

- **No user profile file:** Use score = 0.5
- **Empty topics array:** Use score = 0.5
- **Invalid JSON:** Use score = 0.5, log warning
- **All topics matched:** score = 1.0
- **No topics matched:** score = 0.0
