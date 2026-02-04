---
name: adhd-friendly-documentation
description: Create documentation optimized for ADHD and neurodivergent readers with short scannable content, clear hierarchy, progressive disclosure, actionable steps, and reduced cognitive load. Use when creating or improving any technical documentation (README files, API docs, tutorials, guides, onboarding materials) or when users request accessible, easy-to-scan, or beginner-friendly documentation.
---

# ADHD-Friendly Documentation

## Overview

This skill transforms technical documentation into accessible, scannable content optimized for ADHD and neurodivergent readers. Apply ADHD-friendly principles to create documentation that reduces cognitive load, improves information retention, and enables quick scanning while maintaining technical accuracy.

**Core principles:**
- Short, scannable content with clear visual hierarchy
- Progressive disclosure of complexity
- Actionable steps with concrete examples
- Visual aids and consistent formatting
- Quick reference sections for rapid lookup

## When to Use This Skill

Use this skill when:
- Creating new documentation (READMEs, guides, tutorials, API docs)
- Improving existing documentation for accessibility
- Users request "easy to understand," "beginner-friendly," or "scannable" docs
- Writing onboarding materials or getting-started guides
- Documenting complex systems that need clear explanation
- Creating internal documentation or knowledge bases

**Always apply** these principles to documentation unless the user explicitly requests a different style.

## Creating ADHD-Friendly Documentation

### Step 1: Choose the Right Template

Select the appropriate template from `assets/` based on documentation type:

**Quick Start / README** → `assets/template-quick-start.md`
- Project introductions
- Getting started guides
- Repository README files
- Installation instructions

**API Documentation** → `assets/template-api-docs.md`
- Method/function reference
- Library documentation
- REST/GraphQL API docs
- SDK documentation

**Tutorials** → `assets/template-tutorial.md`
- Step-by-step guides
- Learning paths
- Hands-on workshops
- Feature walkthroughs

### Step 2: Apply Core Patterns

Reference `references/adhd-patterns.md` for detailed guidance on:

**Visual Hierarchy:**
- Use clear H1/H2/H3 structure (max 3-4 levels deep)
- Add generous whitespace between sections
- Keep header nesting shallow for easy scanning

**Scannable Content:**
- Lead with key information (what/why in first 2-3 lines)
- Use bullet points over paragraphs
- Limit paragraphs to 2-3 sentences maximum
- **Bold** important terms and actions
- Use `code formatting` for technical terms

**Progressive Disclosure:**
- Start with TL;DR or Quick Start section
- Provide quick wins before deep explanations
- Link to details rather than including inline
- Separate basic from advanced content

**Action-Oriented:**
- Start instructions with verbs (Install, Run, Create, Configure)
- Number sequential steps clearly
- Include expected outcomes after each step
- Provide complete, runnable code examples

**Cognitive Load Reduction:**
- One concept per section
- Use consistent terminology throughout
- Define jargon on first use
- Include time estimates for tutorials
- Explain "why" for non-obvious steps

### Step 3: Add Visual Elements

Enhance scannability with:

**Tables** for comparisons and structured data:
```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Speed   | Fast     | Slow     |
```

**Callouts** for important information:
```markdown
> ⚠️ **Warning:** Critical information
> 💡 **Tip:** Helpful suggestion
> ℹ️ **Note:** Additional context
> ✅ **Success:** Expected outcome
```

**Code blocks** with syntax highlighting:
````markdown
```language
// Complete, runnable example
// Comments for non-obvious parts
```
````

**Checklists** for learning objectives:
```markdown
- [ ] Objective 1
- [ ] Objective 2
```

### Step 4: Structure for Scanning

Organize information for quick navigation:

**Information hierarchy:**
1. Title + one-line summary
2. Quick start (< 2 minutes)
3. Core concepts (5-10 min)
4. Tutorials/guides (hands-on)
5. API reference (lookup)
6. Advanced topics (deep dives)

**Section format:**
- Lead with the most important info
- Keep sections focused (one topic each)
- Use consistent formatting patterns
- Provide clear navigation (table of contents, next steps)

### Step 5: Validate with Checklist

Use `references/checklist.md` to validate documentation quality:

**Quick validation checks:**
- ✅ Clear headers and structure
- ✅ Paragraphs under 3 sentences
- ✅ Sequential steps numbered
- ✅ Code examples complete and runnable
- ✅ Key terms bolded
- ✅ One concept per section

**Priority fixes** if time is limited:
1. Add clear headers
2. Break up long paragraphs
3. Add quick start section
4. Number sequential steps
5. Bold key terms

See the complete checklist in `references/checklist.md` for comprehensive validation.

## Anti-Patterns to Avoid

Reference `references/adhd-patterns.md` for detailed anti-patterns. Key ones:

**❌ Walls of text** - No paragraphs over 5 sentences
- Instead: Break into bullet points or shorter paragraphs

**❌ Hidden action steps** - Don't bury commands in prose
- Instead: Use numbered lists with explicit actions

**❌ Ambiguous language** - Avoid "might," "could," "sometimes"
- Instead: Provide clear guidance on when to use what

**❌ Missing expected outcomes** - Always show what should happen
- Instead: Add "You should see:" after steps

**❌ Undefined jargon** - Define technical terms on first use
- Instead: Explain or link to definitions

## Working with Existing Documentation

When improving existing docs:

1. **Assess current state** - Identify walls of text, missing structure, buried actions
2. **Add quick wins first** - Quick start section, clear headers, numbered steps
3. **Break up content** - Convert paragraphs to bullets, add whitespace
4. **Add visual hierarchy** - Ensure proper header levels and structure
5. **Validate** - Use checklist from `references/checklist.md`

**Preserve technical accuracy** while improving accessibility.

## Resources

### references/adhd-patterns.md
Comprehensive guide to ADHD-friendly documentation patterns including:
- Core principles and detailed explanations
- Specific patterns for different doc types (Quick Start, API, Tutorial, Troubleshooting)
- Visual aids guidelines (tables, callouts, diagrams)
- Anti-patterns with before/after examples
- Formatting conventions
- Content organization strategies
- Writing style guidelines
- Accessibility considerations

**Use this as the primary reference** for detailed pattern guidance.

### references/checklist.md
Quick validation checklist with:
- Structure & hierarchy checks
- Scannability criteria
- Progressive disclosure validation
- Action steps quality
- Cognitive load assessment
- Visual elements checklist
- Common anti-patterns to avoid
- Quick validation tests (Skim Test, 30-Second Test)
- Scoring system

**Use this to validate** documentation before publishing.

### assets/template-quick-start.md
Template for README files and getting-started guides with:
- Quick start section (60 seconds)
- What this does explanation
- Common use cases
- Next steps navigation
- Quick reference
- Troubleshooting section

**Use when creating** project READMEs or quick-start guides.

### assets/template-api-docs.md
Template for API and library documentation with:
- Method documentation format
- Parameter tables
- Common examples
- Error handling
- Rate limiting and pagination
- Complete working examples

**Use when documenting** APIs, libraries, or SDKs.

### assets/template-tutorial.md
Template for step-by-step tutorials with:
- Learning objectives
- Step-by-step instructions with checkpoints
- Common issues sections
- "You're done" celebration
- Next steps and extensions
- Complete code sections

**Use when creating** hands-on tutorials or walkthroughs.

## Best Practices

**Start simple:**
- Begin with template that matches doc type
- Focus on quick wins (headers, bullets, quick start)
- Add complexity progressively

**Be consistent:**
- Use same formatting patterns throughout
- Maintain consistent terminology
- Follow established conventions in templates

**Test scannability:**
- Can readers find what they need in 30 seconds?
- Are headers descriptive and hierarchical?
- Can someone skim bullets and understand the content?

**Prioritize action:**
- Make it easy to get started quickly
- Provide working examples early
- Show expected results

**Reduce friction:**
- Remove barriers to understanding
- Explain non-obvious steps
- Provide multiple entry points (quick start, deep dive, reference)

## Writing Style

Use imperative/infinitive form throughout:
- ✅ "Install the package using npm"
- ✅ "To configure authentication, create a config file"
- ❌ "You should install the package"
- ❌ "If you want to configure authentication, you can create..."

**Voice:**
- Present tense, active voice
- Direct and conversational but precise
- Command form for instructions

**Sentence structure:**
- Lead with action or key point
- Keep under 20 words
- One idea per sentence

## Examples

### Example 1: README Documentation

User asks: "Create a README for my authentication library"

**Approach:**
1. Start with `assets/template-quick-start.md`
2. Add one-line description of auth library
3. Create 60-second quick start (install, configure, use)
4. Show 2-3 common use cases with code
5. Add API reference links
6. Include troubleshooting for common auth issues
7. Validate with `references/checklist.md`

### Example 2: API Documentation

User asks: "Document my REST API endpoints"

**Approach:**
1. Use `assets/template-api-docs.md` structure
2. For each endpoint: What it does, when to use, quick example
3. Add parameter tables with types and descriptions
4. Include authentication section
5. Show error responses and handling
6. Add rate limiting information
7. Provide complete working examples

### Example 3: Tutorial

User asks: "Write a getting started guide for building a todo app"

**Approach:**
1. Start with `assets/template-tutorial.md`
2. Define learning objectives and time estimate
3. Break into clear steps (Setup → Add todos → Display → Complete)
4. Each step: Goal, instructions, checkpoint, expected result
5. Add "What you learned" summaries
6. Include troubleshooting section
7. Suggest next steps and extensions

### Example 4: Improving Existing Docs

User asks: "Make this documentation easier to understand"

**Approach:**
1. Read existing documentation
2. Identify issues (walls of text, missing structure, unclear actions)
3. Add quick start section if missing
4. Break paragraphs into bullets
5. Add clear headers and hierarchy
6. Make action steps explicit and numbered
7. Add expected outcomes
8. Validate with `references/checklist.md`

## Summary

Create documentation that is:
- **Scannable** - Headers, bullets, whitespace
- **Actionable** - Clear steps, working examples
- **Progressive** - Quick start → concepts → advanced
- **Accessible** - Low cognitive load, clear language
- **Consistent** - Same patterns throughout

**Always reference** `references/adhd-patterns.md` for detailed guidance and `references/checklist.md` for validation. **Use templates** from `assets/` as starting points for common documentation types.
