---
name: program-ideation
description: Research existing libraries and tools before building from scratch. Use when the user describes a program, feature, or capability they want — especially before writing any implementation code. Searches the web in parallel to find existing solutions.
argument-hint: <description of what you want to build or the problem you want to solve>
---

# Program Ideation

Before writing code, search for existing libraries, tools, and frameworks that already solve the problem. AI tools have a bias toward reimplementing things from scratch — this skill counteracts that by front-loading research.

## Process

1. **Parse the user's requirements** into 3-5 distinct search angles. Each angle should target a different facet of what the user wants:
   - The core capability (e.g., "Python library for PDF table extraction")
   - The domain/ecosystem (e.g., "data pipeline tools for converting PDF to CSV")
   - Alternative framings (e.g., "OCR library with table detection")
   - Known adjacent tools (e.g., "Tabula alternatives 2025")
   - The "awesome list" angle (e.g., "awesome-pdf-parsing GitHub")

2. **Launch parallel web search agents** — one per search angle. Each agent should:
   - Perform 2-3 web searches with different query phrasings
   - For each promising result, fetch the project page or README to get: name, what it does, how mature it is (stars, last commit, maintenance status), and how it compares to alternatives
   - Return a structured summary: library name, URL, one-line description, maturity signals, and how well it fits the stated requirements

3. **Synthesize and present results** on the main thread:
   - Group findings by approach/category
   - For each candidate, list: name, what it does, fit to requirements, maturity
   - Flag any gaps — requirements that no existing tool covers
   - Recommend a shortlist (1-3 options) with reasoning

4. **Iterate with the user** — the first search may not match what they actually want. Ask clarifying questions. Re-search with refined angles if needed.

## Agent Prompt Template

Use this template when spawning each search agent:

```
You are researching existing tools/libraries for the following need:

**User's requirement:** {requirement_summary}
**Search angle:** {specific_angle}

Do 2-3 web searches with different phrasings. For each promising project you find:
1. Fetch its homepage or GitHub README
2. Note: name, URL, one-line description, stars/maintenance status, key features
3. Assess: how well does it fit the stated requirement? What does it cover vs. miss?

Return a structured summary of your findings. Prefer recent, actively maintained projects.
```

## When Applying This Skill

1. Do NOT write any implementation code until research is complete and the user has chosen an approach
2. Spawn at least 3 parallel search agents with genuinely different search angles — not minor query variations
3. If the user's description is vague, ask one round of clarifying questions before searching
4. After presenting results, explicitly ask: "Does this match what you're looking for, or should I search from a different angle?"
5. If nothing good exists, say so — then the user can make an informed decision to build from scratch
