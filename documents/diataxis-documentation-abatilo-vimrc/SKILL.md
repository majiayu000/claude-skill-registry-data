---
name: diataxis-documentation
description: Write comprehensive, user-focused documentation following the Diataxis framework. Use this skill when creating or improving tutorials, how-to guides, reference documentation, or explanatory content. Helps identify the right documentation type and apply best practices for each.
allowed-tools:
  - Read
  - Write
  - Edit
---

# Diataxis Documentation Skill

This skill helps you create high-quality, user-focused documentation following the Diataxis framework, which organizes documentation into four distinct types based on user needs.

## When to Use This Skill

Use this skill when:
- Creating new documentation of any kind
- Improving existing documentation
- Organizing documentation for a project or codebase
- Writing tutorials, how-to guides, reference material, or explanations
- Unsure which type of documentation is needed
- Documentation feels unclear or serves multiple purposes poorly

## The Diataxis Framework Overview

Diataxis organizes documentation along two dimensions:

**User Context:**
- **Study** (Skill Acquisition): User is learning
- **Work** (Skill Application): User is doing

**Content Nature:**
- **Action** (Practical Steps): How to do things
- **Cognition** (Theoretical Knowledge): Understanding concepts

This creates four distinct documentation types:

```
                Study          |          Work
           (Learning)          |         (Doing)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━
                                |
    TUTORIALS                   |    HOW-TO GUIDES
    Learning-oriented           |    Goal-oriented
    Guided lessons              |    Practical directions
    "Learn by doing"            |    "Achieve a goal"
                                |
Action ━━━━━━━━━━━━━━━━━━━━━━━━┼━━━━━━━━━━━━━━━━━━━━━━━━━━ Action
                                |
    EXPLANATION                 |    REFERENCE
    Understanding-oriented      |    Information-oriented
    Background & context        |    Technical description
    "Why & how it works"        |    "Facts about machinery"
                                |
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cognition                       |                    Cognition
```

## How to Use This Skill

### 1. Identify the Documentation Type Needed

**Ask these two questions:**
1. **Action or Cognition?** Does the user need to DO something or UNDERSTAND something?
2. **Study or Work?** Is the user learning something new or applying existing knowledge?

**Decision Tree:**
- Action + Study = **Tutorial** (learning by doing)
- Action + Work = **How-to Guide** (solving a problem)
- Cognition + Work = **Reference** (looking up facts)
- Cognition + Study = **Explanation** (understanding concepts)

### 2. Load the Appropriate Reference File

Based on the documentation type identified, load the relevant reference for detailed guidance:

**For Tutorials:**
Load [Tutorials Reference](./references/tutorials.md) when you need to:
- Guide a learner through a complete, practical lesson
- Teach basic skills and concepts through hands-on experience
- Create a learning-oriented "first steps" experience
- Help someone gain confidence with a new tool or technology

**For How-to Guides:**
Load [How-to Guides Reference](./references/how-to-guides.md) when you need to:
- Provide step-by-step instructions to achieve a specific goal
- Help solve a particular real-world problem
- Write task-oriented documentation for competent users
- Address a "How do I..." question

**For Reference Documentation:**
Load [Reference Documentation Reference](./references/reference.md) when you need to:
- Document APIs, functions, classes, or configuration options
- Provide accurate technical descriptions
- Create lookup material for factual information
- Write information-oriented content structured like the product

**For Explanations:**
Load [Explanations Reference](./references/explanation.md) when you need to:
- Explain concepts, design decisions, or architectural choices
- Provide background and context
- Discuss alternatives and trade-offs
- Answer "why" questions about how things work

**For Framework Overview:**
Load [Framework Overview Reference](./references/framework-overview.md) when you need:
- Detailed understanding of Diataxis principles
- Guidance on maintaining distinctness between types
- Common mistakes to avoid
- The iterative improvement workflow

### 3. Follow the Iterative Improvement Process

Diataxis emphasizes continuous, incremental improvement:

1. **Choose**: Select a small piece of documentation (page, paragraph, or sentence)
2. **Assess**: Evaluate it against Diataxis standards:
   - What user need does it serve?
   - How well does it serve that need?
   - Does it belong in the right documentation type?
   - Is it using the right style and approach?
3. **Decide**: Determine one specific improvement that aligns with Diataxis
4. **Do**: Complete that single improvement and publish immediately

**Important:** Focus on small, immediate improvements rather than large restructuring efforts.

## Key Principles

### Maintain Distinctness
- Each documentation type has a specific purpose - don't blur them
- Tutorials teach through doing, not explaining
- How-to guides solve problems, not teach concepts
- Reference describes facts, not guide users through tasks
- Explanations provide context, not instructions

### User-Centered Approach
- Always consider: What does the user need right now?
- Match the documentation type to the user's context (study vs. work)
- Match the content to the user's need (action vs. cognition)

### Organic Structure
- Don't create empty documentation structures upfront
- Let structure emerge from content improvements
- Create documentation types only when content demands it

### Link Between Types
- Tutorials can link to explanations for deeper understanding
- How-to guides can reference relevant reference material
- Keep each type focused; use links for cross-cutting needs

## Quick Documentation Type Selector

**User says "How do I..."**
- If they're learning → Tutorial
- If they're working → How-to Guide

**User needs facts about something**
→ Reference

**User asks "Why..." or "What is..."**
→ Explanation

**User is frustrated or stuck**
- Check recent tasks → How-to Guide
- Check understanding → Explanation
- Check syntax/parameters → Reference

**Creating first-time user content**
→ Tutorial

## Common Patterns

### Tutorial Example Scenarios
- "Build your first web app"
- "Getting started with X"
- "Introduction to Y"
- "Your first Z project"

### How-to Guide Example Scenarios
- "How to deploy to production"
- "Implementing authentication"
- "Optimizing database queries"
- "Troubleshooting connection errors"

### Reference Example Scenarios
- API documentation
- Configuration file reference
- Command-line options
- Class/function documentation

### Explanation Example Scenarios
- "Understanding the architecture"
- "Why we chose X over Y"
- "How the authentication system works"
- "Database design decisions"

## Important Notes

- Load specific reference files only when needed to keep context manageable
- Each documentation type requires different writing styles and structures
- Avoid mixing purposes - if documentation tries to do multiple things, split it
- The framework is descriptive, not prescriptive - adapt to your project's needs
- Iterate continuously rather than attempting complete restructuring
- Quality comes from alignment with user needs, not from following rigid templates

---

**Remember:** The goal is to serve user needs effectively. Use the Diataxis compass to identify what users need, then load the appropriate reference file for detailed guidance on creating that documentation type.
