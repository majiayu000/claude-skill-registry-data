---
name: Prompt Brevity Review
description: Review AI prompts and instructions for conciseness and clarity. Use when reviewing skills, CLAUDE.md, slash commands, or any LLM prompt content.
---

# Prompt Brevity Review

## Overview

AI prompts (skills, CLAUDE.md files, slash commands) are consumed by language models with token limits. Verbose prompts waste context window space and reduce comprehension. This skill identifies unnecessary verbosity and suggests concise alternatives while preserving essential information and clarity.

## When to Use

- Reviewing new or updated skill files (.claude/skills/)
- Evaluating CLAUDE.md project instructions
- Assessing slash command prompts (.claude/commands/)
- Auditing system prompts or agent instructions
- Optimizing prompt performance and token usage

## Process

### 1. Identify Core Information

Extract the essential message:
- **What**: What is the instruction or knowledge?
- **When**: When should it be applied?
- **How**: How should it be executed?
- **Why**: Why does this matter? (optional, only if critical)

### 2. Detect Verbosity Patterns

Common bloat indicators:

**Redundancy**
- Restating the same point multiple times
- Overlapping examples that demonstrate the same concept
- Repetitive phrasing across sections

**Fluff Words**
- "It's important to note that..."
- "You should definitely make sure to..."
- "Please be aware that..."
- "Keep in mind that..."

**Over-Explanation**
- Explaining obvious concepts
- Excessive background context
- Unnecessary justifications

**Ceremonial Language**
- "In order to" → "To"
- "Due to the fact that" → "Because"
- "At this point in time" → "Now"

### 3. Apply Brevity Techniques

**Use Active Voice**
- ❌ "The file should be read by the agent"
- ✅ "Read the file"

**Remove Hedge Words**
- ❌ "Generally, you might want to consider using..."
- ✅ "Use..."

**Use Direct Commands**
- ❌ "You should try to validate the input"
- ✅ "Validate the input"

**Eliminate Redundant Qualifiers**
- ❌ "Completely eliminate all unnecessary words"
- ✅ "Eliminate unnecessary words"

**Convert Prose to Lists**
- ❌ Paragraph explaining multiple steps
- ✅ Numbered or bulleted list

**Use Concrete Examples Over Abstract Explanation**
- ❌ "When dealing with situations where authentication might be compromised..."
- ✅ "Example: SQL injection in login form"

### 4. Preserve Critical Information

Don't remove:
- **Specificity**: Exact file paths, commands, patterns
- **Disambiguation**: Clarifications that prevent misinterpretation
- **Context boundaries**: When/when not to apply the skill
- **Edge cases**: Important exceptions or caveats
- **Examples**: Concrete demonstrations (if not redundant)

### 5. Measure Impact

Calculate improvement:
- **Token reduction**: Count before/after tokens (rough: 4 chars = 1 token)
- **Clarity gain**: Is the message clearer or more ambiguous?
- **Information loss**: Did we remove anything essential?
- **Target**: 30-50% token reduction without information loss

## Examples

### Example 1: Verbose Skill Introduction

**Before** (92 tokens):
```markdown
## Overview

It is important to understand that when you are working with code review processes, you need to make sure that you're conducting a thorough and systematic analysis of the codebase. This skill will help you learn how to effectively review code by providing you with a structured approach that you can follow in order to ensure that you don't miss any important issues or concerns that might exist in the code being reviewed.
```

**After** (28 tokens):
```markdown
## Overview

Conduct systematic code reviews using a structured approach to catch issues and improve code quality.
```

**Improvement**: 70% token reduction, message is clearer and more actionable

### Example 2: Over-Explained Process Step

**Before** (68 tokens):
```markdown
1. First, you should make sure to carefully read through the pull request description so that you can get a good understanding of what the developer was trying to accomplish with their changes. It's really important that you take the time to understand the context before you start looking at the actual code changes themselves.
```

**After** (15 tokens):
```markdown
1. Read PR description to understand change goals and context
```

**Improvement**: 78% token reduction, action is clear

### Example 3: Redundant Examples

**Before** (145 tokens):
```markdown
## Examples

Here are some examples of how to use this skill:

- Example 1: You can use this when reviewing a pull request that adds new features
- Example 2: You might want to use this when examining code that fixes bugs
- Example 3: This is useful when looking at refactoring changes
- Example 4: You could apply this when checking security updates
- Example 5: This works well for performance optimization reviews
```

**After** (31 tokens):
```markdown
## Examples

Use when reviewing:
- New features
- Bug fixes
- Refactoring
- Security updates
- Performance optimizations
```

**Improvement**: 79% token reduction, same information preserved

### Example 4: Fluff-Heavy Instruction

**Before** (47 tokens):
```markdown
You should definitely make sure to validate all user input in order to prevent security vulnerabilities due to the fact that malicious users might try to inject harmful code.
```

**After** (13 tokens):
```markdown
Validate all user input to prevent injection attacks.
```

**Improvement**: 72% token reduction, more direct

## Anti-patterns

- ❌ **Don't**: Remove necessary context that prevents misinterpretation
  - ✅ **Do**: Remove only redundant or obvious information

- ❌ **Don't**: Make prose cryptic by over-abbreviating
  - ✅ **Do**: Use clear, direct language that's still readable

- ❌ **Don't**: Cut concrete examples that demonstrate concepts
  - ✅ **Do**: Cut redundant examples that show the same pattern

- ❌ **Don't**: Remove edge cases and important exceptions
  - ✅ **Do**: State exceptions concisely (e.g., "Except when X, then Y")

- ❌ **Don't**: Strip personality from prompts entirely
  - ✅ **Do**: Keep minimal tone/personality that aids comprehension

## Brevity Checklist

Use this checklist when reviewing prompts:

- [ ] Remove "it's important to note", "please be aware", "keep in mind"
- [ ] Convert passive voice to active voice
- [ ] Replace "in order to" with "to"
- [ ] Remove hedge words ("generally", "typically", "usually")
- [ ] Eliminate redundant qualifiers ("completely", "totally", "very")
- [ ] Convert paragraph explanations to lists
- [ ] Combine overlapping examples
- [ ] Remove obvious explanations
- [ ] Replace verbose phrases with concise alternatives
- [ ] Verify all specific details (paths, commands) are preserved

## Testing This Skill

### Test Scenario 1: Skill File Review

1. Read an existing skill file from .claude/skills/
2. Apply brevity techniques to each section
3. Calculate token reduction percentage
4. Success: 30%+ reduction with no information loss

### Test Scenario 2: CLAUDE.md Optimization

1. Review project CLAUDE.md instructions
2. Identify verbose sections
3. Suggest concise alternatives
4. Success: Clearer instructions in fewer tokens

### Test Scenario 3: Command Prompt Review

1. Examine a slash command prompt
2. Apply brevity checklist
3. Verify command still functions correctly
4. Success: Faster execution with maintained accuracy

## Common Verbose → Concise Patterns

| Verbose | Concise | Savings |
|---------|---------|---------|
| "in order to" | "to" | 66% |
| "due to the fact that" | "because" | 80% |
| "at this point in time" | "now" | 75% |
| "it is important to note that" | [remove] | 100% |
| "you should make sure to" | [imperative verb] | 100% |
| "take into consideration" | "consider" | 67% |
| "in the event that" | "if" | 75% |
| "for the purpose of" | "to" | 75% |

## Related Skills

- `creating-skills` - Creating well-structured skills from the start
- `code-review` - Reviewing code for similar clarity issues
- `writing-commit-messages` - Concise, information-dense writing

---

**Remember**: Every token counts. Clear and concise beats verbose and redundant.
