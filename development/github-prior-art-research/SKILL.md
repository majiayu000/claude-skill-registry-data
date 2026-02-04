---
name: GitHub Prior Art Research
description:
  When asked implementation questions or tool selection questions like "how do
  I implement", "what's the best way to", "how should I", "which library",
  "what tool should I use", or "how might we", search GitHub for prior art,
  code examples, and proven approaches before proposing solutions
---

# GitHub Prior Art Research

## Purpose

This skill activates when you ask questions about implementation approaches or
tool selection. It guides Claude to research GitHub for proven solutions,
popular libraries, real-world examples, and community discussions before
formulating an answer.

## When This Skill Activates

This skill automatically engages when your questions include patterns like:

- "How do I [implement/build/create/add] X?"
- "What's the best way to [solve/approach/handle] X?"
- "How should I structure/organize/design X?"
- "Which library/tool/framework should I use for X?"
- "What are people using for X?"
- "How might we [implement/architect] X?"

## Research Process

### 1. Identify the Core Problem

Extract the key concept or task from your question. What's the actual problem you're solving?

### 2. Search Multiple Sources on GitHub

Use the WebSearch tool to find relevant information on GitHub:

**Code Examples**: Search for implementation patterns

- Example: `site:github.com "how to implement [X]" language:[relevant]`
- Look for well-maintained repos with multiple stars

**Popular Repos**: Find established solutions

- Search for repos that solve your problem
- Review their approach, architecture, and design decisions

**Issues & Discussions**: Learn from community problem-solving

- Search GitHub issues for discussions about similar challenges
- See what problems others encountered and how they solved them

**Documentation**: Find best practices and patterns

- Check README files and docs in relevant repos
- Look for architectural decisions and trade-offs explained

### 3. Synthesize Findings

Analyze what you discovered:

- What approaches are most common?
- What patterns do successful projects use?
- What trade-offs exist between different approaches?
- What mistakes do people make (from issues/discussions)?

### 4. Present Evidence-Based Answer

Propose solutions grounded in your research:

- Cite specific repos or discussions
- Explain why certain approaches work
- Mention alternatives and their trade-offs
- Point to real examples the user can study

## Key Principles

- **Always search before proposing**: GitHub research informs every recommendation
- **Cite sources**: Include repo links or discussion references
- **Show alternatives**: Discuss different approaches and their trade-offs
- **Learn from mistakes**: Include common pitfalls found in issues/discussions
- **Respect complexity**: Acknowledge when multiple valid approaches exist

## Example Usage

**User asks**: "How do I implement real-time updates in a React app?"

**Skill activates because**: The question matches "How do I implement [X]"

**Claude's process**:

1. Searches GitHub for popular React real-time solutions (Firebase, Socket.io, etc.)
2. Examines top repos and their architectural approaches
3. Reviews issues discussing real-time update challenges
4. Reads documentation explaining different patterns
5. Proposes solution citing specific repos: "Based on popular approaches like [RepoA] and [RepoB], here are two main patterns..."
