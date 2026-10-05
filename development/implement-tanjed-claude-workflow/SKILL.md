---
name: implement
description: >
  Write production code for a specific class, method, function, or unit of logic.
  Auto-invoke when the user says "implement this", "write the code for",
  "build the X class", "code the Y method", or "make this work".
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: <what to implement> [file-path]
---
 
# Implement Skill
 
Write production-quality code for: `$ARGUMENTS`
 
## Step 1 — Gather Context
Before writing a single line, read:
- The target file if it exists (interfaces, existing patterns, imports)
- Adjacent files in the same layer (how does a similar class look in this project?)
- The relevant process file based on detected stack:
  - `@~/.claude/process/node_process.md`
  - `@~/.claude/process/go_process.md`
  - `@~/.claude/process/php_process.md`
  - `@~/.claude/process/frontend_process.md`
- Any interface or DTO this implementation must satisfy
 
Run these to understand the project shape:
```bash
# Detect stack
ls package.json go.mod composer.json 2>/dev/null
 
# Find existing similar implementations to match patterns
grep -r "class.*Service\|class.*Repository\|type.*Service\|interface.*Repository" src/ --include="*.ts" -l 2>/dev/null | head -5
```
 
## Step 2 — State Assumptions Explicitly
Before writing code, list:
- What interface/contract this implements
- What dependencies will be injected
- What the method signatures will be
- Any design pattern being applied (name it)
 
If anything is genuinely ambiguous, ask ONE question. Otherwise proceed.
 
## Step 3 — Write the Code
 
### Universal Rules
- Constructor injection only — never `new ConcreteClass()` inside a class
- Dependencies typed as interfaces, not concrete classes
- Early return over nested conditionals — always
- No `any` in TypeScript, no ignored errors in Go, no missing `strict_types` in PHP
- Custom error classes for domain errors — never throw raw strings
- Method names describe behaviour, not implementation (`getActiveOrders` not `queryOrdersWhereDeletedAtNull`)
- Keep methods small — if a method needs more than ~20 lines, extract named private methods
 
## Step 4 — Self-Review Before Finishing
After writing, check each file against:
- [ ] Does it depend on an interface, not a concrete class?
- [ ] Are all dependencies injected via constructor?
- [ ] Are there any nested conditionals that could be early returns?
- [ ] Does every error case throw a typed exception / return a wrapped error?
- [ ] Is every method name self-documenting?
- [ ] Would this be easy to unit test (all dependencies are injectable mocks)?
 
Fix any failures before presenting the code.
 
## Step 5 — Output
- Write the file(s)
- Print: what was implemented, what pattern was applied (if any), what the caller needs to inject, what tests should be written next (offer to run `/tdd`)
 
