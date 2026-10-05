---
name: design-review
description: >
  Review code for SOLID violations, design pattern misuse, tight coupling,
  and architectural boundary violations. Auto-invoke when the user says
  "review this", "check my design", "is this well-structured", or shares a
  class/service for feedback.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: [file-or-directory]
---
 
# Design Review Skill
 
Perform a structured design and architecture review of the specified file(s) or directory.
 
## Input
`$ARGUMENTS` — file path, directory, or empty (review recently modified files via `git diff --name-only`)
 
## Review Protocol
 
### Step 1 — Understand the Code
- Read all files in scope
- Identify: what layer is this? (controller / service / repository / domain / utility)
- Identify: what are the dependencies? What does it instantiate directly?
 
### Step 2 — Run the SOLID Checklist
For each class or module:
 
| Principle | Question to answer |
|---|---|
| **S** — Single Responsibility | Does this class have more than one reason to change? |
| **O** — Open/Closed | Would adding a new variant require modifying this class? |
| **L** — Liskov Substitution | Can subtypes be swapped without breaking callers? |
| **I** — Interface Segregation | Are interfaces too fat? Do implementors have unused methods? |
| **D** — Dependency Inversion | Does this class depend on concrete implementations instead of interfaces? |
 
### Step 3 — Check Design Patterns
- Identify patterns in use — name them explicitly
- Flag misapplied patterns (e.g. Singleton used where DI would suffice)
- Suggest patterns where they would improve the design — explain why
 
### Step 4 — Check Coupling & Layer Boundaries
- Is business logic leaking into controllers?
- Are DB queries in services instead of repositories?
- Are there direct instantiations (`new ConcreteClass()`) inside classes?
- Are there cross-layer imports that break the dependency rule?
 
### Step 5 — Check for Code Smells
- God class / God method
- Long parameter lists (consider a DTO or options object)
- Feature envy (a method that uses another class's data more than its own)
- Dead code or unreachable branches
- Missing early returns (deeply nested conditionals)
 
## Output Format
 
Structure your output exactly like this:
 
---
 
### 🔴 Critical (must fix — breaks design integrity)
- [Issue]: [file:line] — [explanation] — [suggested fix]
 
### 🟡 Warning (should fix — degrades maintainability)
- [Issue]: [file:line] — [explanation] — [suggested fix]
 
### 🟢 Suggestion (nice to have — improves clarity)
- [Issue]: [file:line] — [explanation] — [suggested fix]
 
### ✅ What's done well
- [Specific callout] — be precise, not generic
 
---
 
## Rules
- Be specific — cite file and line number for every issue
- Never say "consider following best practices" — name the specific principle or pattern
- Distinguish between a SOLID violation and a code smell — they are not the same
- If no issues are found in a category, say so explicitly — don't skip the section
- End with: **Refactoring priority** — which single change would have the highest impact
 
