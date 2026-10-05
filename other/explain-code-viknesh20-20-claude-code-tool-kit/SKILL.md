---
name: explain-code
description: "Explains code with multiple levels of detail — high-level purpose, line-by-line walkthrough, data flow diagrams, and design rationale. Use when onboarding to unfamiliar code or trying to understand complex logic."
argument-hint: "[file, function, or module to explain]"
allowed-tools: Read, Grep, Glob, Bash(git log*), Bash(git blame*)
---

# Code Explanation

## Instructions

### Step 1: Identify the Target
Read the specified file, function, or module completely. Also read:
- Any imports/dependencies it uses
- Any files that import/call it (to understand usage context)
- Recent git history for the file: `git log --oneline -10 <file>`

### Step 2: Provide Multi-Level Explanation

#### Level 1 — One-Sentence Summary
What does this code do in plain English? A non-technical person should understand this.

#### Level 2 — High-Level Overview
- **Purpose**: What problem does it solve?
- **Inputs**: What goes in? (parameters, config, env vars, external data)
- **Outputs**: What comes out? (return values, side effects, events emitted)
- **Dependencies**: What does it rely on?
- **Callers**: Who uses this? In what context?

#### Level 3 — Detailed Walkthrough
Walk through the code section by section:
- Explain the logic flow with numbered steps
- Highlight non-obvious decisions ("this uses X instead of Y because...")
- Note any error handling and what triggers each path
- Explain any performance-sensitive sections

#### Level 4 — Data Flow Diagram
Create an ASCII diagram showing:
```
[Input] → [Processing Step 1] → [Processing Step 2] → [Output]
                ↓                       ↓
         [Side Effect 1]         [Side Effect 2]
```

### Step 3: Highlight Key Details
- **Tricky Parts**: Code that might confuse a new reader
- **Assumptions**: Implicit assumptions the code makes
- **Edge Cases**: How are boundary conditions handled?
- **History**: Why was it written this way? (use `git blame` for context)

### Step 4: Related Code
List the most important related files/functions that someone exploring this code should read next.

---

## Output Style
- Use clear section headers
- Include code snippets with line references
- Use analogies where helpful
- Adjust technical depth based on the complexity of the code
