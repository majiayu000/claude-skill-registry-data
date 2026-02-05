---
name: gemini-review
description: This skill orchestrates code review and plan validation using Google Gemini CLI. It should be used when users want to validate implementation plans, review completed code, or discuss architecture decisions with Gemini as a second opinion. Supports FastAPI, Next.js, and general tech stacks with specialized checklists. Uses gemini-3-pro-preview model with free tier (60 req/min, 1000 req/day).
---

# Gemini Review Skill

## Overview

This skill enables a dual-AI review workflow where Claude prepares context and Gemini provides independent validation. The output always includes both Gemini's raw feedback and Claude's synthesized action plan.

**Model**: `gemini-3-pro-preview` (fixed)
**Cost**: Free tier (60 requests/min, 1000 requests/day)

## When to Use

- Validating implementation plans before coding
- Reviewing completed code for bugs, security, and best practices
- Discussing architecture decisions with a second AI perspective
- Getting specialized feedback for FastAPI or Next.js projects

## Workflow Types

| Type | Purpose | When to Use |
|------|---------|-------------|
| **plan** | Validate implementation plan | Before starting development |
| **code** | Review completed code | After implementing features |
| **architecture** | Discuss system design | During design phase or refactoring |

## Execution Process

### Step 1: Gather Context from User

Before executing, collect:
1. **Review type**: `plan`, `code`, or `architecture`
2. **Tech stack** (optional): `fastapi`, `nextjs`, or `general`
3. **Content to review**: The actual plan, code, or architecture description

### Step 2: Load Appropriate Checklist

Based on tech stack, load the corresponding checklist from `references/checklists.md`:
- FastAPI: API design, Pydantic models, async patterns, security
- Next.js: SSR/SSG, routing, state management, performance
- General: Universal best practices

### Step 3: Build and Execute Gemini Command

Load the appropriate prompt template from `references/prompt-templates.md` and execute:

**For inline prompts:**
```bash
gemini -m gemini-3-pro-preview -p "{constructed_prompt}" --output-format json
```

**For file content review:**
```bash
cat {file_path} | gemini -m gemini-3-pro-preview -p "{review_instructions}" --output-format json
```

**For multi-line prompts (heredoc):**
```bash
gemini -m gemini-3-pro-preview --output-format json -p "$(cat << 'EOF'
{constructed_prompt}
EOF
)"
```

### Step 4: Parse JSON Response

Gemini returns JSON with this structure:
```json
{
  "response": "The actual review content",
  "stats": {
    "models": { ... },
    "tools": { ... }
  }
}
```

Extract the review content from the `response` field. Use `jq` for parsing:
```bash
result=$(gemini -m gemini-3-pro-preview -p "..." --output-format json)
echo "$result" | jq -r '.response'
```

### Step 5: Present Results in Two Sections

**CRITICAL**: Always present results in two clearly separated sections:

#### Section A: Gemini Raw Response
Present Gemini's complete response without modification. This shows the user exactly what Gemini found.

#### Section B: Claude's Analysis & Action Plan
Based on Gemini's feedback, Claude provides:

1. **Summary** (2-3 sentences)
   - Key findings
   - Overall assessment

2. **Action Items** (prioritized list)
   - 🔴 Critical: Must fix before proceeding
   - 🟡 Important: Should address soon
   - 🟢 Minor: Nice to have improvements

3. **Ready-to-Apply Code** (when applicable)
   - Provide actual code fixes for each issue
   - Include before/after comparison when helpful

## Output Format Template

```markdown
---
## 📋 Gemini Review Results

### A. Gemini Response (Raw)

{gemini_response_verbatim}

---

### B. Claude's Analysis

#### Summary
{2-3 sentence overview}

#### Action Items

🔴 **Critical**
- Issue: {description}
- Fix: {solution}

🟡 **Important**  
- Issue: {description}
- Fix: {solution}

🟢 **Minor**
- Issue: {description}
- Fix: {solution}

#### Ready-to-Apply Code

**{issue_name}**
```{language}
{fixed_code}
```

---
```

## Command Examples

### Plan Review
```bash
gemini -m gemini-3-pro-preview --output-format json -p "$(cat << 'EOF'
[PLAN REVIEW REQUEST]
Review this implementation plan for completeness and potential issues:

{plan_content}

Check for: Logic errors, missing edge cases, architecture flaws, security concerns.
Provide specific, actionable feedback.
EOF
)"
```

### Code Review (piping file)
```bash
cat src/api/auth.py | gemini -m gemini-3-pro-preview -p "Review this FastAPI authentication code for security issues, bugs, and best practices. Provide specific line-by-line feedback." --output-format json
```

### Architecture Review
```bash
gemini -m gemini-3-pro-preview --output-format json -p "$(cat << 'EOF'
[ARCHITECTURE REVIEW]
System: {system_name}
Tech Stack: FastAPI + Next.js + AWS

{architecture_description}

Evaluate: Scalability, reliability, maintainability, security, cost efficiency.
Suggest improvements with trade-off analysis.
EOF
)"
```

## Environment Compatibility

| Environment | Execution Method |
|-------------|------------------|
| Claude Code | Direct bash execution |
| Claude (Web/Desktop) | Use `bash_tool` |

Command syntax remains identical across environments.

## Error Handling

If Gemini returns an error:
1. Display the error message to user
2. Check for common issues:
   - Quota exceeded (60/min or 1000/day limit)
   - Network connectivity
   - Invalid prompt format
3. Suggest retry or alternative approach

## Quota Management

Free tier limits:
- 60 requests per minute
- 1000 requests per day

To conserve quota:
- Combine related reviews into single prompts
- Use specific, focused review requests
- Avoid redundant re-reviews

## References

- `references/checklists.md`: Tech stack-specific review checklists
- `references/prompt-templates.md`: Prompt templates for each review type
