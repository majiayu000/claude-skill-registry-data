---
name: delegation-validator
description: |
  Use when educators need to validate if their lesson plan covers all 3 Delegation subcategories (Problem/Platform/Task Awareness).
  Analyzes lesson plans and provides objective scores (0-10) with actionable feedback.
  Works in Claude.ai, Claude Code, and API for maximum portability.
---

# Delegation Validator

Validates lesson plans to ensure complete coverage of Delegation competency from the AI Fluency Framework.

## When to Use This Skill

Use this skill when:
- Educator created a lesson plan about AI planning/Delegation
- Need objective validation of 3 subcategories coverage
- Want specific, actionable feedback on gaps
- Preparing for pilot test with students
- Want to self-assess before using delegation-coach agent

## How It Works

### Input
Lesson plan text (markdown, PDF, or plain text)

### Output
1. **Score (0-10)** for each subcategory:
   - Problem Awareness (0-10)
   - Platform Awareness (0-10)
   - Task Delegation (0-10)
2. **Overall Delegation Score** (average)
3. **Gap Analysis** (what's missing)
4. **Actionable Recommendations** (specific improvements)

### Process

1. Read lesson plan file or text
2. Execute validation script: `python scripts/validate_plan.py --input <file>`
3. Script analyzes against criteria from `references/delegation_criteria.md`
4. Return structured report with scores and recommendations

## Validation Criteria

### Problem Awareness (0-10)
- **0-3:** No mention of defining objectives before using AI
- **4-6:** Mentions objectives but doesn't teach students to question IF they should use AI
- **7-9:** Teaches when to use AI vs when not to
- **10:** Includes exercises for identifying appropriate AI interaction modes (Automation/Augmentation/Agency)

### Platform Awareness (0-10)
- **0-3:** Assumes one AI tool (usually ChatGPT)
- **4-6:** Mentions multiple tools but doesn't compare
- **7-9:** Teaches comparison of capabilities AND limitations
- **10:** Includes ethical/privacy considerations in tool selection

### Task Delegation (0-10)
- **0-3:** No guidance on dividing work
- **4-6:** Generic advice on "use AI for X"
- **7-9:** Specific strategies for human-AI collaboration
- **10:** Includes examples of good vs bad delegation + justifications

## Example Usage

### Via Script (Claude Code)
```bash
# Validate lesson plan
python scripts/validate_plan.py --input lesson_plan.md --format json

# Output:
{
  "scores": {
    "problem_awareness": 8,
    "platform_awareness": 6,
    "task_delegation": 9,
    "overall": 7.7
  },
  "gaps": [
    "Platform Awareness: Lesson doesn't teach students to compare tool limitations"
  ],
  "recommendations": [
    "Add exercise: Students compare ChatGPT vs Claude vs Copilot for same task",
    "Include discussion on privacy considerations when choosing AI tools"
  ]
}
```

### Via Skill (Claude.ai or Code)
```
"Use delegation-validator to analyze this lesson plan: [paste plan text]"
```

## Integration with delegation-coach Agent

The `delegation-coach` agent invokes this skill when:
- Educator shares a written lesson plan
- Coach wants objective validation to supplement Socratic questioning
- Coach needs concrete data to guide deeper questions

### Workflow:
1. **Coach asks:** "Can you share your written lesson plan?"
2. **Educator provides** file/text
3. **Coach runs:** `python scripts/validate_plan.py --input plan.md`
4. **Coach uses score** to guide Socratic questions:
   - "Your Platform Awareness scored 6/10. What do you think might be missing?"
   - "You scored 9/10 on Task Delegation - excellent! What made that part strong?"
   - "The validator suggests adding X. Does that align with your teaching goals?"

## Analogies

**This Skill = Recipe for Quality Control**
- Clear rubric (ingredients)
- Objective scoring steps
- Same input = same output (deterministic)
- Anyone can use to validate

**delegation-coach Agent = Master Teacher Using Recipe**
- Uses validation scores to guide teaching
- Adapts questions based on results
- Combines objective data with subjective coaching

**Together = Restaurant with Quality Standards**
- Recipe ensures consistency (skill validation)
- Chef uses standards to improve dishes (coach uses scores to guide)

## References

For detailed criteria and examples:
- `references/delegation_criteria.md` - Complete rubric with examples
- `references/example_plans.md` - Annotated lesson plans (good vs weak)

Both files available on-demand when you need more detail.

## Portability

✅ **Works in Claude.ai** (browser - paste lesson text)
✅ **Works in Claude Code** (CLI - file or text)
✅ **Works via Claude API** (integrations)
✅ **Can be shared** with other educators via plugin

## Token Efficiency

- Skill body: ~1.5k tokens
- References loaded only when needed
- Script executes without loading into context
- Optimal for repeated use
