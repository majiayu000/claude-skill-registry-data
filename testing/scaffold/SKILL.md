---
name: scaffold
description: >
  Scaffold a new service, module, or feature with full layered architecture.
  Auto-invoke when the user says "create a new service", "add a module for X",
  "scaffold a feature", or "set up the structure for Y".
allowed-tools: Read, Write, Bash, Glob
argument-hint: <domain> <stack>
---
 
# Scaffold Skill
 
Generate a fully layered module/service for the given domain and stack.
 
## Arguments
- `$ARGUMENTS` — e.g. `order nodejs`, `payment laravel`, `user golang`
 
## Step 1 — Parse Arguments
Identify:
- **Domain name** (e.g. `order`, `user`, `payment`)
- **Stack** (`nodejs` | `laravel` | `golang`) — if not provided, detect from the project (check for `package.json`, `go.mod`, `composer.json`)
 
## Step 2 — Read the Relevant Process File
Before generating anything, read the matching process file:
- Node.js → `@~/.claude/process/node_process.md`
- Golang → `@~/.claude/process/go_process.md`
- Laravel → `@~/.claude/process/php_process.md`
 
## Step 3 — Confirm Structure Before Generating
Present the proposed file tree and the interface/contract list to the user.
Wait for explicit approval before writing any files.
 
Example for `order nodejs`:
```
src/
  interfaces/
    IOrderRepository.ts
    IOrderService.ts
  dtos/
    CreateOrderDTO.ts
    OrderResponseDTO.ts
  repositories/
    OrderRepository.ts
  services/
    OrderService.ts
  controllers/
    OrderController.ts
  errors/
    OrderNotFoundError.ts
tests/
  unit/
    services/OrderService.test.ts
  integration/
    repositories/OrderRepository.test.ts
```
 
## Step 4 — Generate Files in This Order
1. Interface / contract files first
2. DTOs
3. Custom error classes
4. Repository (implementing the interface)
5. Service (injecting the repository interface)
6. Controller (injecting the service interface)
7. Unit test for the service (mock the repository)
8. Integration test stub for the repository
 
## Rules
- Every class receives its dependencies via constructor injection — no `new ConcreteClass()` inside classes
- Service depends on the **interface**, never the concrete repository
- Controller must not contain business logic
- Every file starts with the file path as a comment on line 1
- Use the naming conventions from `~/.claude/CLAUDE.md`
- Generated tests must follow the `it should <behaviour> when <condition>` naming format
- After generating, print a summary of: files created, interfaces defined, what still needs wiring (DI binding, routes, etc.)
