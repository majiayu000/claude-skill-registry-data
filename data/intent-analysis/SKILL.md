---
name: intent-analysis
description: Analyze and explain the intent behind AI tool calls. Use when you need to understand what an action will do, verify your interpretation is correct, or explain your reasoning to the user.
---

# Intent Analysis Skill

This skill helps analyze and explain the intent behind tool calls, making the AI's interpretation visible and verifiable.

> **Acknowledgement**: This skill implements concepts from the YouTube video ["The AI Failure Mode Nobody Warned You About"](https://www.youtube.com/watch?v=T74uZgfu6mU&t=11s) - making AI interpretation visible before action.

## When to Use This Skill

Use this skill when:
- You want to verify your understanding of what a tool call will do
- The user asks "what will this do?" or "explain what you're about to do"
- You're about to take a significant action and want to document your reasoning
- You need to generate a structured intent document for audit purposes

## Intent Document Structure

When analyzing intent, produce a structured document with these 7 fields:

### 1. Task
One sentence describing EXACTLY what will happen. Be specific about files, paths, counts, sizes.

### 2. Who/What
- **Affected**: What will be changed (specific files, resources, with counts/sizes)
- **Excluded**: What will NOT be changed (to catch scope misunderstandings)

### 3. Boundaries
3-5 concrete statements about what this action will NOT do. Focus on adjacent actions that might be confused with the intended action.

### 4. If Uncertain
What should happen if the action encounters ambiguity or problems. Prefer "stop and ask" for destructive actions.

### 5. Reversibility
- **Can Undo**: true / false / "partial"
- **Method**: How to undo
- **Effort**: "trivial" / "moderate" / "significant" / "impossible"

### 6. Alternatives
1-2 other valid interpretations that were considered, with reasoning for why they weren't chosen.

### 7. Confidence Breakdown
Your confidence in this interpretation, broken down by:
- Ambiguity Analysis (how many valid interpretations exist)
- Intent-to-Action Distance (semantic gap between request and action)
- Historical Patterns (similarity to past successful actions)
- Uncertainty Markers (hedging language in the request)

## Example Usage

**User request**: "Clean up old docs"

**Intent Analysis**:

```
TASK: Delete all files in ~/docs/ not modified in the last 180 days

WHO/WHAT:
  Affected: ~/docs/**/* (47 files, 2.3GB estimated)
  Excluded: Files modified in last 180 days, subdirectories themselves

BOUNDARIES:
  - Will not delete files outside ~/docs/
  - Will not delete directories themselves
  - Will not delete files matching 'keep' in name
  - Will not proceed if any file is open

IF UNCERTAIN: Stop and ask for clarification. Do not delete partially.

REVERSIBILITY:
  Can Undo: NO
  Method: Restore from backup
  Effort: Impossible (permanent CLI deletion)

ALTERNATIVES:
  1. "Archive instead of delete"
     Outcome: Move files to ~/archive/docs/
     Not chosen: "clean up" typically implies deletion for space

  2. "Delete ALL files, not just old ones"
     Outcome: Remove all 50+ files
     Not chosen: User said "old" specifically

CONFIDENCE: 0.62
  Ambiguity: 0.55 - "clean up" has multiple meanings
  Distance: 0.70 - Direct mapping with reasonable defaults
  Historical: 0.60 - Similar patterns approved before
  Uncertainty: 0.65 - No hedging, but "old" is subjective
```

## Integration with ICR

This skill works with the ICR plugin to:
- Generate intent documents for tool calls
- Provide explanations when users select "Explain" during review
- Support the `/icr:simulate` command for dry-run analysis
- Help debug confidence calculations via `/icr:debug`

## Best Practices

1. **Be Specific**: Never say "delete files" when you can say "delete 47 .tar.gz files older than 30 days in /tmp/builds/"

2. **Expose Inferences**: If you're assuming defaults (like "30 days" for "old"), say so explicitly

3. **Think Adversarially**: What could go wrong? What might the user NOT want?

4. **Honest Reversibility**: Most CLI operations are permanent. Don't sugarcoat.

5. **Consider Scope Creep**: The biggest risks come from affecting more than intended
