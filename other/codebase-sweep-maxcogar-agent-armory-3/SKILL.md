---
name: codebase-sweep
description: Systematically discover quality issues in an existing codebase through a single broad sweep, then organize findings into an actionable document. Use when the user wants to clean up a vibe-coded app, audit codebase quality, find technical debt, survey an app for problems, or prepare an existing codebase for improvement. Triggers on "sweep my codebase", "clean up this app", "audit code quality", "find issues in this project", "this app is a mess", "technical debt", "vibe coded", "what's wrong with this code", "review my project", or any request to assess or inventory problems in an existing codebase before fixing things. Use this skill even if the user doesn't explicitly say "sweep" — any request to find or catalog problems in a codebase qualifies.
---

# Codebase Sweep

Discover every quality issue in a codebase through a single broad sweep, then organize findings into a prioritized document.

This skill covers **discovery and triage only**. Do not fix anything. Do not prescribe architecture. Do not run linters or static analysis. You are reading code and reasoning about quality.

---

## Step 1: Map the Codebase

Before reading any code, get the lay of the land.

1. List the project's top-level directory structure (2 levels deep).
2. Count total source files (exclude `node_modules`, `.git`, `dist`, `build`, lock files).
3. Identify the project type: framework, language, entry points, config files present.
4. Note any existing documentation (`README`, `ARCHITECTURE.md`, `docs/`, etc.) — skim it for stated intentions. The gap between stated intentions and actual code is itself a finding.

This step should take one tool call (directory listing) and a quick scan of config/README files. The goal is to know what you're looking at before diving in, so you can make informed decisions about reading order.

---

## Step 2: Read Every Source File

Read through every source file in the project. For each file, note anything that's wrong — any quality issue, any code smell, any bug, any inconsistency.

### File reading strategy

**Small projects (under 30 source files):** Read every file, in full.

**Medium projects (30–80 files):** Read every file. For files over 300 lines, read the first 100 lines, last 50 lines, and scan the middle for function signatures and structure. If something looks wrong in the scan, read the full section.

**Large projects (80+ files):** Read all files in core directories (routes, controllers, services, models, main components). For remaining directories, read a representative sample — at minimum 3 files per directory. If a directory shows problems in the sample, read the rest of it.

Regardless of project size: always read entry points, configuration files, and anything that other files heavily import.

### What to look for

Read with the mindset of a senior engineer doing a code review where the only goal is to find problems. You are not scanning for specific categories in sequence — you are reading code and writing down what's wrong. Here are the kinds of things that should catch your eye (this is calibration, not a sequential checklist):

- **Inconsistent patterns.** Three different ways to fetch data across the app. Error handling done differently in every file. This is the #1 signal in vibe-coded apps — each feature was built with whatever approach the AI or developer reached for at the time.
- **Silent failure.** Empty catch blocks, `.catch(() => {})`, functions that return null on error with no logging.
- **Coupling hotspots.** Files that import everything or are imported by everything. Utility files that became dumping grounds.
- **Functions doing too many things.** Data fetching + transformation + validation + rendering in one function. Business logic inside event handlers.
- **Stale comments.** Comments describing behavior the code no longer performs. `// TODO` items that have clearly been abandoned.
- **Uncoordinated state.** Global variables modified from multiple places. Multiple sources of truth for the same data.
- **Pattern decay.** First few files follow a clean structure (from a tutorial or template), later files get progressively sloppier.
- **Dead code.** Unused imports, unreachable branches, commented-out blocks, exported functions nothing calls.
- **Hardcoded values.** API URLs, credentials, magic numbers, environment-specific paths baked into source.
- **Missing boundaries.** Database queries in route handlers. Business logic in UI components.

### How to write findings as you go

As you read each file, write your findings immediately. For each finding:

1. **State what's wrong** — not what to do about it. Fixes come later.
2. **Reference specific files and line numbers.**
3. **Note when the same problem appears across multiple files** — this is one finding (a pattern), not five separate findings.

**Good finding:**
> `src/api/users.js:34`, `src/api/projects.js:67`, `src/api/auth.js:12` — All have empty catch blocks (`.catch(() => {})`). Errors in API calls are silently swallowed with no logging or user feedback.

**Bad finding:**
> "Error handling needs improvement."

**Good finding:**
> `Dashboard.jsx:142` — `fetchData()` is 89 lines. It calls 3 different API endpoints, parses each response differently, updates local state, and triggers 2 side effects. At least 5 distinct responsibilities in one function.

**Bad finding:**
> "Dashboard component is too complex."

### Severity

Assign each finding a severity as you write it:

- **critical** — Will cause data loss, security vulnerabilities, or crashes during normal use. (SQL injection, credentials in source, race conditions that corrupt data, unhandled rejections that kill the process.)
- **high** — Breaks functionality in edge cases, or blocks other improvements. (Error handling that hides failures, tight coupling that makes isolated changes impossible, missing input validation on external inputs.)
- **medium** — Makes the codebase harder to work with but doesn't break user-facing functionality. (Duplicated logic, inconsistent patterns, overloaded functions, poor naming.)
- **low** — Readability and style. (Formatting, minor duplication, naming conventions.)

---

## Step 3: Compile the Findings Document

After reading all files, organize your raw findings into the deliverable document. Write it to `docs/sweep/YYYY-MM-DD-findings.md` in the target project (create the directory if needed).

### Document structure

```markdown
# Codebase Sweep — [date]

**Project:** [name/path]
**Source files scanned:** [count]
**Total findings:** [count]
**Severity breakdown:** [N critical, N high, N medium, N low]

---

## Critical & High Priority

### [Group name — describe the pattern, not the fix]

**Severity:** critical | high
**Files:** `path/file.js`, `path/other.js`, ...
**Depends on:** [other group name, if this must be addressed first]

[2-4 sentences describing the problem pattern. What's wrong, where it appears, why it matters. Key line numbers.]

### [Next group]
...

## Medium Priority

### [Group name]
...

## Low Priority

### [Group name]
...

---

## Raw Findings by File

### src/api/users.js
- **high** — No input validation on route parameters. User IDs from URL params passed directly to DB queries without sanitization.
- **medium** — Error responses use three different formats: `{error: msg}`, `{message: msg}`, and raw strings.

### src/components/Dashboard.jsx
- **medium** — `fetchData()` (line 142) is 89 lines. Fetches from 3 endpoints, parses responses, updates state, triggers side effects.
- **low** — 4 unused imports.

[... every file with findings ...]
```

### Grouping and triage rules

The top section (Critical & High, Medium, Low) groups related findings into patterns. The bottom section (Raw Findings by File) preserves every individual finding for reference. Both sections are important — the groups give the big picture, the raw list ensures nothing is lost.

To build the groups:

1. **Merge findings that describe the same problem across files.** "Empty catch blocks in 4 API files" is one group, not four.
2. **Name each group after the problem**, not the solution. "Silent error swallowing in API layer" not "Add error handling middleware."
3. **Mark dependencies between groups.** If group A must be addressed before group B can be safely changed, note `Depends on: [group A]`. Example: "Separate business logic from UI components" should happen before "Add unit tests for business logic."
4. **Order by severity first, then by how many other groups depend on it.** A group that blocks 3 other groups outranks one that blocks none, even at the same severity.

---

## Step 4: Present to User

After writing the findings document, present it. Summarize:
- Total findings and severity breakdown
- The 2-3 most important groups and why they matter
- Any dependency chains that suggest a natural fix order

Ask the user if priorities look right before anyone moves to fixing things.
