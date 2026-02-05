---
name: skill-professor
description: Creates comprehensive tutorials to teach users any skill from the skills library. Use when users want to learn a skill, need a tutorial, ask for guidance on using a skill, or want to apply a skill to their project. Guides users from understanding to practical implementation through hands-on exercises.
---

# Skill Professor

## Overview

Transform any skill into a comprehensive, interactive tutorial that guides users from zero to practical mastery. This skill creates personalized learning experiences that help users understand, practice, and apply skills to their own projects.

## Tutorial Creation Workflow

Follow these steps to create an effective tutorial:

### 1. Discover & Analyze the Target Skill

**First, identify what skill to teach:**
- If user specifies a skill name (e.g., "teach me the pdf skill"), use that skill
- If user describes a need (e.g., "I want to create documents"), identify the relevant skill

**Then, analyze the skill:**
- Read the skill's SKILL.md to understand its purpose, capabilities, and structure
- Review any reference files or examples in the skill directory
- Identify the core concepts, common use cases, and key workflows
- Note any prerequisites, dependencies, or setup requirements

### 2. Understand the User's Context

**Gather essential information:**
- What project are they working on?
- What do they want to accomplish with this skill?
- What's their experience level with related tools/concepts?
- What's their learning preference (hands-on vs. overview-first)?

**Keep it conversational - Don't interrogate:**
- Ask 1-2 questions at a time
- Infer what you can from context
- Offer sensible defaults they can accept

### 3. Design the Tutorial Structure

**Choose the appropriate tutorial type:**

**Quick Start Tutorial (15-20 min)**
- For simple skills or experienced users
- One complete example start-to-finish
- Focus on getting results fast
- Good for: pdf, theme-factory, simple utilities

**Standard Tutorial (30-45 min)**
- For most skills and users
- Foundation → Core concepts → Practical application
- Multiple examples with increasing complexity
- Good for: frontend-design, canvas-design, webapp-testing

**Comprehensive Tutorial (60+ min)**
- For complex skills or career-critical learning
- Multiple phases with deep dives
- Several project implementations
- Troubleshooting and advanced features
- Good for: skill-creator, complex integrated systems

### 4. Deliver the Tutorial

**Use a phased approach:**

**Phase 1: Foundation**
1. Explain what the skill does and when to use it
2. Show the simplest possible working example
3. Verify user's environment/prerequisites
4. Achieve one quick success to build confidence

**Phase 2: Core Concepts**
1. Introduce essential features and workflows
2. Provide hands-on exercises for each concept
3. Apply concepts to a simple version of their project goal
4. Include checkpoints to verify understanding

**Phase 3: Practical Application**
1. Guide user to implement a real feature for their project
2. Build iteratively - start simple, add complexity
3. Troubleshoot issues together
4. Refine until they have working code they can build on

**Phase 4: Mastery Path**
1. Show what's possible with advanced features
2. Provide resources for continued learning
3. Suggest natural next projects or explorations
4. Ensure they know how to get help

### 5. Ensure Successful Learning

**Throughout the tutorial:**
- ✅ Provide complete, working code examples (not pseudocode)
- ✅ Explain the "why" behind each step, not just the "how"
- ✅ Pause for user verification at key checkpoints
- ✅ Proactively address common mistakes and gotchas
- ✅ Encourage experimentation and customization
- ✅ Build real artifacts they can use going forward

**Success criteria:**
- User has working implementation in their project
- User understands core concepts, not just memorized steps
- User can troubleshoot common issues independently
- User feels confident to explore the skill further

## Tutorial Design Patterns

For detailed guidance on creating effective tutorials, see [references/tutorial-patterns.md](references/tutorial-patterns.md).

Key patterns include:
- **Progressive complexity**: Start simple, build up gradually
- **Learning by doing**: Every concept gets immediately applied
- **Real-world context**: Use their actual project, not toy examples
- **Scaffolding**: Provide support early, reduce as confidence grows
- **Checkpoint verification**: Regular opportunities to confirm understanding

## Adaptation Guidelines

### For Technical Skills (pdf, webapp-testing)
- Emphasize working code and testing
- Include debugging strategies
- Show error handling patterns
- Provide reference-style quick lookups

### For Creative Skills (canvas-design, frontend-design)
- Encourage exploration and iteration
- Show multiple valid approaches
- Focus on developing judgment and taste
- Balance structure with creative freedom

### For Workflow Skills (skill-creator)
- Use decision trees for complex choices
- Provide templates and examples
- Walk through complete end-to-end scenarios
- Emphasize best practices and common patterns

### For Integration Skills (theme-factory, brand-guidelines)
- Show how pieces fit together
- Demonstrate on complete examples
- Explain when to use which features
- Provide quick reference guides

## Working with Skill Resources

**When the target skill has bundled resources:**

**Scripts:**
- Show how to use them, don't just list them
- Demonstrate with actual execution
- Explain when to use vs. writing custom code

**References:**
- Load and reference as needed during tutorial
- Don't dump all reference content at once
- Point users to specific sections for specific tasks

**Assets:**
- Use them in examples to show realistic usage
- Explain how to customize or adapt them
- Show where they fit in workflows

## Anti-Patterns to Avoid

❌ **Don't create info dumps** - Overwhelming users with everything at once
✅ **Do reveal progressively** - Introduce concepts as they're needed

❌ **Don't use toy examples** - "Imagine you want to process a document..."
✅ **Do use their project** - "Let's process your actual resume data..."

❌ **Don't just explain theory** - Long descriptions without practice
✅ **Do emphasize doing** - Brief explanation → immediate application

❌ **Don't skip error handling** - Showing only the happy path
✅ **Do show troubleshooting** - "If you see X error, here's why and how to fix..."

❌ **Don't leave them dependent** - They need you for next steps
✅ **Do build independence** - They can continue without you

## Tutorial Tone

- **Encouraging**: Celebrate small wins, normalize struggles
- **Conversational**: "Let's try..." not "One should attempt..."
- **Practical**: Focus on getting things done
- **Confident**: Be direct about best approaches
- **Patient**: Allow time for understanding and experimentation
