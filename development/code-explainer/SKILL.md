---
name: code-explainer
description: "Explains code, functions, files, or programming concepts in plain English for a non-programmer. Triggers when the user asks what code does, asks for an explanation, says they do not understand something, or asks about a programming concept."
---

# Code Explainer

## Goal

Make any piece of code understandable to someone who has never programmed, without oversimplifying or being condescending.

## Instructions

### Determine the Scope

What is being explained?
- **A single line or expression** → give a one-sentence explanation
- **A function or method** → use the Function Explanation format
- **A file or module** → use the File Explanation format
- **A concept or pattern** → use the Concept Explanation format
- **An architecture or system** → use the Architecture Explanation format

### Function Explanation Format

1. **What it does** (one sentence, no jargon)
2. **Inputs**: What goes in? What does each input mean?
3. **Output**: What comes out? What format is it in?
4. **Step-by-step**: Walk through the logic, explaining each block
5. **Why it exists**: What problem does it solve?
6. **Analogy**: Compare to something in the physical world
7. **What could go wrong**: What errors could occur and how they are handled

### File Explanation Format

1. **Purpose** (one sentence: "This file handles [what]")
2. **What it contains**: List the main functions/classes and what each does
3. **What depends on it**: Other files that use this file
4. **What it depends on**: Libraries and other files this file needs
5. **How it fits in the project**: Where it sits in the overall architecture

### Concept Explanation Format

1. **Analogy first**: Explain the concept using a physical-world comparison
2. **Simple example**: Show the concept in 3-5 lines of code with comments
3. **Where it appears**: Point to where this concept is used in THIS project
4. **Why it is used**: What problem it solves here specifically
5. **Update glossary**: Add to `.agent/knowledge/glossary.md` if not already there
6. **Update learning journal**: Add to `docs/learning-journal.md`

### Architecture Explanation Format

1. **The big picture**: What does the whole system do? (2-3 sentences)
2. **The parts**: List each major component and what it handles
3. **How they connect**: Describe how data flows between components
4. **A diagram**: Use simple text-based diagram (boxes and arrows)
5. **Entry points**: Where does a user request start? Where does it end?

## Quality Assessment (Include When Relevant)

When explaining existing code, assess its quality:

| Aspect | Rating | Why |
|--------|--------|-----|
| Error handling | Good/Needs work | Does it handle failures gracefully? |
| Readability | Good/Needs work | Is it easy to follow? |
| Security | Safe/Concern | Any obvious vulnerabilities? |
| Naming | Clear/Confusing | Are variable/function names descriptive? |

## Constraints

- Never say "it's simple" or "it's obvious" — if it were, they would not be asking
- Always provide at least one analogy for abstract concepts
- Use "you" language: "When you call this function..." not "When one invokes..."
- If the code is genuinely bad, say so diplomatically: "This works, but a more robust approach would be..."
