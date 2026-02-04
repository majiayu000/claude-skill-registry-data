---
name: prompt-clarifier
description: |
  WHEN: Ambiguous prompts, vague requirements, missing context, unclear instructions
  WHAT: Ambiguity detection + AskUserQuestion clarification + Interactive option selection
  WHEN NOT: Clear detailed instructions → proceed directly
---

# Prompt Clarifier Skill

## Purpose
Detects ambiguous prompts and asks clarification questions using AskUserQuestion with interactive selections.

## When to Use
Activate when:
1. Prompt seems ambiguous or lacks necessary details
2. User wants to create/build something without specifying technical details
3. Vague instructions like "fix this", "optimize", or "improve" without context
4. Excessive pronouns ("this", "that", "it") without clear references

## Detection Criteria
Consider prompt ambiguous if it:
- Is very short (< 5 words) and lacks context
- Mentions project type without specifying:
  - Technology stack
  - Main features
  - Project scope
- Contains optimization requests without specifying aspect:
  - Performance/speed
  - Memory usage
  - Code readability
  - Bundle size
- References code/files without paths
- Uses vague verbs without specifying target

## Workflow

### Step 1: Acknowledge
Briefly acknowledge what the user is asking for.

### Step 2: Use AskUserQuestion
Present targeted questions with multiple-choice options.

**Example Question Patterns:**

For missing tech stack:
```
AskUserQuestion: "Which tech stack would you like to use?"
Options:
- React + TypeScript + Node.js
- Vue + JavaScript + Express
- Vanilla JS + Python + FastAPI
- I'll specify manually
```

For missing features:
```
AskUserQuestion: "Select main features (multiple selection)"
Options:
- User auth/login
- Database CRUD
- File upload
- Real-time (WebSocket)
- Payment system
- Admin dashboard
multiSelect: true
```

For vague optimization:
```
AskUserQuestion: "What type of optimization do you need?"
Options:
- Execution speed/performance
- Memory usage reduction
- Bundle size reduction
- Code readability
```

For project scope:
```
AskUserQuestion: "What's the project scale?"
Options:
- Simple prototype/MVP
- Medium-scale project
- Large enterprise-level
- Not sure (recommend for me)
```

### Step 3: Provide Guidance
After receiving answers, proceed with enhanced context.

## Response Template

When detecting ambiguity:

1. **Acknowledge**: "Got it. I'll help you with [request]."
2. **Explain**: "To provide better results, I have a few questions."
3. **Ask**: Use AskUserQuestion with relevant options
4. **Proceed**: Start implementation with full context

## Examples

### Example 1: Vague Web Project
**User**: "Build me a website"

**Response**:
```
Got it. I'll help you build a website.
For better results, I have a few questions.

[Use AskUserQuestion]
1. Tech stack selection
2. Main features selection
3. Project scope

[After answers, proceed with implementation]
```

### Example 2: Vague Optimization
**User**: "Optimize this code"

**Response**:
```
I'll help optimize your code.
First, let me understand what type of optimization you need.

[Use AskUserQuestion for optimization type]
[Ask for file path if not specified]

[Proceed with targeted optimization]
```

## Best Practices
1. **Keep questions focused**: Ask only what's necessary
2. **Provide sensible defaults**: Include common choices
3. **Allow custom input**: Include "Other" option
4. **Be conversational**: Don't make it feel like a form
5. **Group related questions**: Ask related questions together
6. **Proceed efficiently**: Once you have enough context, start working

## Integration with Hook
Works with UserPromptSubmit hook. When you see:

```
<!-- VIBE CODING ASSISTANT: PROMPT CLARIFICATION NEEDED -->
```

Automatically activate this skill and use AskUserQuestion.

## Notes
- Enhances vibe coding by ensuring sufficient context
- Interactive selections make it easy to provide details
- Don't ask unnecessary questions if prompt is clear
