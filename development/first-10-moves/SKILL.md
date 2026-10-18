---
name: First 10 Moves
description: The exact operational recon sequence for an unfamiliar codebase or unfamiliar area. Replaces "ask the human to clarify" with "read the code first." Most clarification questions are answered by 5 minutes in the relevant file - this skill enforces reading before asking.
---

# First 10 Moves

When dropped into an unfamiliar codebase or asked to fix something in code you don't know — run this sequence before doing anything else. The principle: **most "clarification" questions are answered by 5 minutes in the relevant file.** If the answer is in the code, the docs, or the file tree — find it there before asking.

## When to use

- Fresh in an unfamiliar codebase
- Asked to fix or change code in an area you haven't worked in
- Tempted to ask "where does X live?" or "how does Y work?"
- Triggered by Caddy on prompts like: "fix the X", "investigate", "trace this bug", "how does X work", "unfamiliar codebase", "where is X defined", "what calls Y", "navigate the code", "find the bug in"

## The sequence (run top-to-bottom)

### 1. Re-read the user's request
Look for clues. "Fix" implies a bug. "The headline generator" implies a named module. Note any screenshots, errors, or examples included. **The exact phrasing embeds most of the diagnosis** — don't abstract it away.

### 2. Get the lay of the land (~30 seconds)
- List project root
- Identify main source directory
- Read `package.json` / `pyproject.toml` / `Cargo.toml` (whatever the manifest is)
- Read README if short

This rules out a lot. You learn the language, framework, build system, and entry point in 30 seconds.

### 3. Search for the keyword across the project
One ripgrep, filtered to relevant extensions. The matches will cluster around the real module.

### 4. Pick the most likely 2-3 matched files
**Filenames are huge signal.** `aiHeadlineGenerator.ts` beats `headlineUtils.test.ts`. Production code beats test code. Implementation beats type definitions.

### 5. Read the public surface of the top candidate
**Imports + exports, not bodies.** Shape first. What does this module take in and put out? What does it depend on?

### 6. Find the entry point — who calls this?
Search for the main exported function name. Call sites tell you how the module fits into the larger pipeline.

### 7. Read one upstream call site fully
Concrete example of "what inputs does this receive in real use?" That constrains everything downstream. Don't read 5 call sites — one is usually enough.

### 8. Read the main function body, focused on the symptom
- **Specific symptom** ("headlines are repeating") → find the path that produces it (the loop, the dedup logic, the source list)
- **General "fix it"** → top-to-bottom, alert for obvious issues (off-by-one, null guards, stale comparators, hardcoded values)

### 9. Query the data the function works with
A few DB rows, the actual config file, the recent log lines. **Reality often disagrees with code's assumptions.** This catches it fast.

### 10. Form a hypothesis, verify with one targeted read or query
"I think X because Y, confirm by checking Z."
- Confirmed → fix.
- Not confirmed → loop back to step 8 with the new hypothesis.

**Hit rate at step 10: ~80% land a correct hypothesis.** The remaining 20% loop back with what was learned.

## What NOT to do in the first 10 moves

- ❌ Read every file in the directory
- ❌ Read tests before reading the code under test
- ❌ Ask a clarifying question (unless genuinely too vague)
- ❌ Start writing fix code (first fix attempt comes AFTER move 10)
- ❌ Run the code to "see what happens" — understand it statically first
- ❌ Open the IDE outline / class hierarchy explorer — too noisy
- ❌ Ask the user "where is X defined?" — grep is faster than asking

## Most of the work is reading, not writing

A typical non-trivial change is **~80% reading, 20% writing.** The edit is the *result* of the engineering, not the engineering itself. Agents that flip this ratio produce code that doesn't fit the surrounding system.

## Output format

When you complete the recon, before writing any fix code, output:

```
**Recon complete:**
- Module: {path/to/file.ts}
- Entry point: {function name + caller path}
- Hypothesis: {what I think is wrong, in plain English}
- Verified by: {what I read/queried that confirms the hypothesis}
- Plan: {smallest change that solves it}
```

Then execute the fix.
