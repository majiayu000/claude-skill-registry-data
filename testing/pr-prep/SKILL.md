---
name: pr-prep
description: >
  Prepare code for a pull request: run design review, check test coverage,
  verify layer boundaries, and generate a PR description. Auto-invoke when
  the user says "prepare PR", "ready to merge", "PR checklist", or "review
  before I push".
allowed-tools: Read, Bash, Glob, Grep
---
 
# PR Prep Skill
 
Run the full pre-PR checklist on changed files, then generate a PR description.
 
## Step 1 — Identify Changed Files
```bash
git diff --name-only main  # or master / develop — detect the base branch
git diff --stat main
```
 
## Step 2 — Run Automated Checks
```bash
# Node.js
npx tsc --noEmit          # type check
npx eslint .              # lint
npx jest --passWithNoTests # tests
 
# Go
go vet ./...
golangci-lint run
go test ./... -race
 
# PHP
./vendor/bin/pint          # formatting (Laravel)
./vendor/bin/phpstan analyse
./vendor/bin/pest
```
 
Report results — list failures clearly. Do not proceed with the PR description if there are type errors or test failures.
 
## Step 3 — Design Checklist (for changed files only)
 
Check each changed file against:
 
- [ ] No business logic in controllers
- [ ] No direct DB access in services
- [ ] No `new ConcreteClass()` inside classes — dependencies are injected
- [ ] No `any` type (TypeScript) / unhandled errors (Go) / missing strict_types (PHP)
- [ ] Early returns used — no deeply nested conditionals
- [ ] New code has corresponding tests
- [ ] New public methods have clear names that describe their behaviour
 
Flag any failures with file:line reference.
 
## Step 4 — Generate PR Description
 
```markdown
## What
<1–2 sentence summary of what this PR does>
 
## Why
<business or technical reason — what problem does it solve?>
 
## Changes
- <specific change 1>
- <specific change 2>
- ...
 
## Design Decisions
<any trade-offs made, patterns applied, or notable architectural choices>
 
## Testing
- Unit tests: <what is covered>
- Integration tests: <what is covered>
- Manual testing: <steps to verify if needed>
 
## Checklist
- [ ] Tests pass
- [ ] No linting errors
- [ ] No type errors
- [ ] Layer boundaries respected
- [ ] No secrets or debug code committed
```
 
## Output
- Print the checklist results first (pass/fail per item)
- Then print the PR description, ready to copy
- Flag any items that need manual attention before the PR is opened
 
