---
name: code-analyst
description: >
  Use this skill whenever the user wants to understand, document, or analyze a piece of code.
  Triggers include: "analyze this code", "explain what this does", "document this function",
  "what does this code do", "review this snippet", "help me understand this", or any time the
  user pastes or uploads code and expects a structured breakdown. Even if the user just pastes
  code with no explanation, use this skill. Also triggers when the user asks about parameters,
  return values, edge cases, or test coverage for a given function or module.
---

# Code Analyst Skill

Produces a structured Markdown analysis document for a given piece of code. Covers purpose, parameters, return values, and test case behavior — all within a strict 2-minute time budget.

---

## Workflow

### 0. Start the clock

Note the start time mentally (or use `Date.now()` in a script context). You have **120 seconds** total. Budget roughly:
- 0–30s: Read and understand the code
- 30–90s: Write the Markdown document
- 90–120s: Test case analysis

Every ~10 seconds of elapsed wall-clock time, emit a brief inline status line to the user, e.g.:
> ⏱ *[~10s] Reading the code structure and identifying entry points...*

These should be short (one line), natural, and informative — not robotic. Keep writing; don't pause for a response unless asking the continuation question (see §4).

---

### 1. Read and Understand

Scan the code for:
- **Language and paradigm** (procedural, OO, functional, async, etc.)
- **Entry points**: top-level functions, classes, exported symbols
- **Dependencies**: imports, external calls, side effects
- **Control flow**: branches, loops, recursion, error handling
- **Data flow**: what goes in, what gets transformed, what comes out

Don't guess — if something is ambiguous, note it as "unclear" rather than inventing behavior.

---

### 2. Write the Markdown Document

Produce a document with this structure:

```markdown
# Code Analysis: `<filename or inferred name>`

## Overview
One paragraph: what this code does at a high level, in plain language.

## Function / Class Breakdown

### `functionName(param1, param2, ...)`
- **Purpose**: What it does.
- **Parameters**:
  | Name | Type | Description |
  |------|------|-------------|
  | param1 | string | ... |
- **Returns**: Type and description of return value. `void` if nothing.
- **Side effects**: Any mutations, I/O, or external calls. "None" if clean.
- **Throws / Errors**: Conditions under which it throws or returns an error state.

_(Repeat for each significant function, class, or exported symbol.)_

## Data Flow
Short description or ASCII diagram of how data moves through the code.

## Dependencies
List of imports/modules used and why.

## Notes & Ambiguities
Anything unclear, potentially buggy, or worth flagging for the reader.
```

Adapt the structure if the code is a single function, a class, a module, a script, etc. Don't force sections that don't apply.

---

### 3. Test Case Analysis

Add a `## Test Cases` section to the document:

```markdown
## Test Cases

### ✅ Cases that should PASS
| Input | Expected Output | Reason |
|-------|----------------|--------|
| ...   | ...            | ...    |

### ❌ Cases that will FAIL (or are unhandled)
| Input | Observed/Expected Behavior | Reason |
|-------|---------------------------|--------|
| ...   | ...                       | ...    |

### ⚠️ Edge Cases to Watch
- List any boundary conditions, nulls, empty inputs, overflow, type mismatches, etc.
```

Base this on static analysis — you are **not** running the code. Reason through the logic carefully. If you genuinely can't determine behavior, mark it `Unknown — runtime-dependent`.

---

### 4. Time Limit Handling

If you reach **120 seconds** before completing the document:

1. Stop writing mid-section (don't rush to finish poorly).
2. Emit a clear message:

> ⏱ **2-minute limit reached.** I've covered [what's done so far]. Should I **continue** and finish the analysis, or **stop here**?

Wait for the user's response before proceeding. If they say continue, pick up exactly where you left off. If they say stop, summarize what's left in 2–3 bullet points so they know what's missing.

---

## Output Format

- Always output the document as a **Markdown code block** or, if file creation tools are available, save it as `<filename>_analysis.md` and present it.
- Keep language plain and readable — write for a developer who didn't write this code.
- Avoid filler phrases like "As we can see..." or "It's worth noting that...". Be direct.

---

## Status Line Examples

Use natural, varied status lines. Some examples:
- ⏱ *[~10s] Identified 3 functions — mapping parameters now...*
- ⏱ *[~20s] Writing the overview section...*
- ⏱ *[~40s] Documenting return values and side effects...*
- ⏱ *[~60s] Moving on to test case analysis...*
- ⏱ *[~80s] Analyzing edge cases and failure modes...*
- ⏱ *[~100s] Almost done — finalizing the document...*

Emit one roughly every 10 seconds of work. Don't emit them all at once.
