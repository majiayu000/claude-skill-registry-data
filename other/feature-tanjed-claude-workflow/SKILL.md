---
name: feature
description: >
  Implement a complete feature end-to-end: plan, scaffold structure, write all
  layers of code, and write tests. Auto-invoke when the user says "build the
  X feature", "implement the full flow for Y", "end-to-end implementation of Z",
  or "I need everything for the order cancellation feature".
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: <feature description>
---
 
# Feature Skill
 
Implement a complete feature end-to-end: `$ARGUMENTS`
 
This skill orchestrates the full development cycle — design → code → test — for a self-contained feature.
 
---
 
## Phase 1 — Understand and Plan
 
### 1.1 Read context
```bash
# Detect stack
ls package.json go.mod composer.json 2>/dev/null
 
# Understand existing patterns
find src app internal -name "*.ts" -o -name "*.go" -o -name "*.php" 2>/dev/null | head -20
```
 
Read 2–3 existing similar features/services to match the codebase's patterns exactly.
Read the relevant process file for the detected stack.
 
### 1.2 Present a Feature Plan
Before writing anything, output this plan and **wait for explicit approval**:
 
```
Feature: <name>
 
Layers affected:
  - Controller:   <endpoint(s) it will expose>
  - Service:      <business logic — what rules does it enforce?>
  - Repository:   <what data does it read/write?>
  - Events:       <does this emit any events? what?>
 
New files:
  - <file path> — <purpose>
  - ...
 
Modified files:
  - <file path> — <what changes>
 
Interfaces / contracts to define:
  - <IXxxRepository> — methods: ...
  - <IXxxService> — methods: ...
 
DTOs:
  - <XxxRequestDTO> — fields: ...
  - <XxxResponseDTO> — fields: ...
 
Error classes:
  - <XxxNotFoundError>, <XxxAlreadyExistsError>, etc.
 
Tests to write:
  - Unit: <service> — <N> test cases
  - Integration: <repository> — <N> test cases
 
Open questions (if any):
  - <question> — assumption I'll use if you don't answer
```
 
---
 
## Phase 2 — Implement (after approval)
 
Write files in this strict order — each layer depends on the one above:
 
### 2.1 Contracts First (no dependencies)
- Interfaces for the service and repository
- DTOs (input and output shapes)
- Custom error/exception classes
- Enums if new domain constants are needed
 
### 2.2 Repository Layer
- Implement the repository interface against the ORM/DB
- All DB access lives here — no raw queries in services
- Match the DB naming conventions from `~/.claude/process/db_process.md`
 
### 2.3 Service Layer
- Inject repository via its interface
- Enforce business rules here — validation, domain logic, event emission
- No DB knowledge — only calls repository methods
- Use early returns for guard clauses
 
### 2.4 Controller / Handler Layer
- Inject service via its interface
- Parse and validate request input (Form Request / Zod / binding)
- Call exactly one service method per endpoint
- Map service output to HTTP response via DTO/Resource
- Zero business logic here
 
### 2.5 Route / DI Wiring
- Register the route pointing to the new controller
- Bind interfaces to implementations in the DI container / service provider
- Never skip this — untested wiring is a common failure point
 
---
 
## Phase 3 — Tests (spawn test-writer agent)
 
Spawn the `test-writer` agent to write in parallel:
 
**Unit tests (service layer):**
- Mock the repository
- Cover: happy path, each error condition, each business rule branch
- Format: `it should <behaviour> when <condition>`
 
**Integration tests (repository layer):**
- Use real test database
- Cover: create, read, update, delete — verify data actually persists
- Cover: constraints and edge cases (duplicate, not found, cascade)
 
**Feature / HTTP tests (where applicable):**
- Test the full request → response cycle
- Cover: valid input returns correct response, invalid input returns correct error code
 
---
 
## Phase 4 — Self-Verify
 
```bash
# Node.js
npx tsc --noEmit && npx jest --testPathPattern="<feature>"
 
# Go
go build ./... && go test ./... -run "TestOrder"
 
# PHP
./vendor/bin/pint && ./vendor/bin/phpstan analyse && ./vendor/bin/pest --filter="order"
```
 
Fix any type errors, linting failures, or test failures before finishing.
 
---
 
## Output Summary
 
After completing all phases, print:
 
```
Feature: <name> — COMPLETE
 
Files written:
  Interfaces:    <list>
  DTOs:          <list>
  Errors:        <list>
  Repository:    <list>
  Service:       <list>
  Controller:    <list>
  Routes/DI:     <list>
  Tests:         <list> (<N> unit, <N> integration, <N> feature)
 
Patterns applied: <list with one-line explanation each>
Build: PASS | FAIL (details)
Tests: <N> passing | <N> failing (details)
 
Next steps:
  - <anything that needs a follow-up decision or human action>
```
