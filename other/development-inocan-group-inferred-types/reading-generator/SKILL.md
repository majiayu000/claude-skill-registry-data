---
name: reading-generator
description: "Create chapter readings for CSC-113 with proper structure, voice, and pedagogy"
allowed-tools: "Read,Write,Glob,Grep"
---

# Reading Generator

Create chapter readings that teach concepts while maintaining engagement and accessibility.

## When to Use This Skill

- Creating new module readings
- Adapting external content into reading format
- Reviewing/revising existing readings
- When asked to "write a reading about X"

## Reading Specifications

### Length & Scope
- **Target**: 1,500-2,500 words
- **Reading time**: 10-15 minutes
- **Scope**: One major concept or 2-3 tightly related ideas
- **Depth**: Enough to understand and apply, not exhaustive reference

### Required Sections

Every reading must include these sections in order:

```markdown
---
title: "Reading Title"
module: M0X
reading_number: X
estimated_time: "XX minutes"
prerequisites: ["previous-reading"] or "None"
---

# [Title]

## Learning Objectives
[3-5 specific, measurable objectives]

## Why This Matters
[1-2 paragraphs connecting to real world]

## The Core Concept
[Main content - multiple subsections as needed]

## Putting It Together
[Synthesis and connections]

## Common Questions
[FAQ format, 3-5 questions]

## Reflection Questions
[3-4 questions for personal consideration]

## Next Steps
[What to do after finishing this reading]
```

## Section-by-Section Guidance

### Learning Objectives
Use action verbs from Bloom's Taxonomy:
- **Remember**: Define, list, identify
- **Understand**: Explain, describe, summarize
- **Apply**: Use, demonstrate, implement
- **Analyze**: Compare, contrast, differentiate
- **Evaluate**: Assess, judge, critique
- **Create**: Design, construct, develop

**Good**: "By the end of this reading, you'll be able to explain how AI systems learn from examples."
**Bad**: "Understand machine learning."

### Why This Matters
Connect to:
- Career relevance
- Daily life impact
- Course project (SAGE)
- Skills employers value

**Example**:
> Whether you're aiming to build AI applications or just want to be an informed citizen in an AI-powered world, understanding how these systems learn is foundational. In CSC-113, you'll apply these concepts when building SAGE, your personal study assistant. More broadly, this knowledge helps you evaluate AI claims critically—a skill increasingly valuable in any career.

### The Core Concept
Structure for learning:

1. **Hook**: Start with a concrete, relatable example
2. **Define**: Clear definition without jargon
3. **Expand**: Build complexity gradually
4. **Illustrate**: Multiple examples at different levels
5. **Connect**: Link to prior knowledge and future learning

Use these patterns:
- **Analogy**: "Think of it like..." (then explain limits of analogy)
- **Contrast**: "Unlike X, which does Y, this approach..."
- **Progression**: "Let's start simple and build up..."

### Putting It Together
Synthesize, don't just summarize:
- How do the pieces connect?
- What's the big picture?
- How does this change how you think about X?

### Common Questions
Answer questions students actually ask:
- "But what if...?"
- "How is this different from...?"
- "Do I need to memorize...?"
- "When would I actually use this?"

### Reflection Questions
Prompt genuine thinking, not regurgitation:
- ✅ "How might this apply to a field you're interested in?"
- ❌ "What are the three types of machine learning?"

### Next Steps
Specific, actionable:
- Which reading/lab comes next
- Optional deeper dives
- Practice suggestions

## Formatting Guidelines

### Headers
```markdown
# Main Title (only one)
## Major Sections
### Subsections
#### Detail sections (use sparingly)
```

### Emphasis
- **Bold** for key terms on first use
- *Italic* for emphasis in prose
- `Code formatting` for technical terms, file names, commands

### Lists
- Use for 3+ parallel items
- Prefer prose for 2 items
- Don't nest more than 2 levels

### Code Examples
- Always explain what code does
- Use comments liberally
- Keep examples under 20 lines
- Show output where helpful

### Callouts
```markdown
> **💡 Pro Tip**: [Helpful insight]

> **⚠️ Common Pitfall**: [What to avoid]

> **🔗 Connection**: [Link to other content]
```

## Quality Checklist

Before completing a reading:

- [ ] Frontmatter complete (title, module, time estimate, prereqs)
- [ ] 3-5 specific learning objectives
- [ ] "Why This Matters" connects to real world
- [ ] Core content uses concrete-before-abstract pattern
- [ ] At least one analogy or relatable example
- [ ] Technical terms defined on first use
- [ ] Common Questions section addresses real student concerns
- [ ] Reflection questions prompt genuine thinking
- [ ] Next Steps are specific and actionable
- [ ] Word count: 1,500-2,500
- [ ] Voice consistent with course-content-writer skill

## Example Opening

Here's how a reading on "What is AI?" might begin:

```markdown
---
title: "What is AI? Separating Hype from Reality"
module: M01
reading_number: 1
estimated_time: "12 minutes"
prerequisites: "None"
---

# What is AI? Separating Hype from Reality

## Learning Objectives

By the end of this reading, you'll be able to:
- Define artificial intelligence in practical terms
- Distinguish between AI capabilities and AI hype
- Identify three categories of AI systems
- Explain how AI already affects your daily life

## Why This Matters

You've probably heard AI will either save humanity or destroy it, 
depending on which headline you read last. The reality is less 
dramatic but more relevant to your life and career. AI systems 
already influence what shows Netflix recommends, whether your 
loan gets approved, and how your email filters spam.

In this course, you'll build your own AI assistant (SAGE) and learn 
to collaborate with AI tools professionally. But first, we need to 
establish what AI actually is—and isn't. This foundation helps you 
think critically about AI claims and use these tools effectively.

## The Core Concept

### Let's Start With What AI Isn't

Picture the robots from science fiction movies...
```

## Anti-Patterns to Avoid

**Wall of text**: Break up every 3-4 paragraphs with headers, examples, or visuals
**Definition dump**: Don't list definitions; weave them into narrative
**Passive voice overuse**: "The model is trained" → "We train the model"
**Assumed knowledge**: Define everything, even "obvious" terms
**Ending abruptly**: Always provide clear next steps
