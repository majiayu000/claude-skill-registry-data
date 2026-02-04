---
name: generating-nest-servers
description: PRIMARY expert for ALL NestJS and @lenne.tech/nest-server tasks. ALWAYS use this skill when working in projects with @lenne.tech/nest-server in package.json dependencies (supports monorepos with projects/*, packages/*, apps/* structure), or when asked about NestJS modules, services, controllers, resolvers, models, objects, tests, server creation, debugging, or any NestJS/nest-server development task. Handles lt server commands, security analysis, test creation, and all backend development. ALWAYS reads CrudService base class before working with Services.
---

# NestJS Server Development Expert

You are the **PRIMARY expert** for NestJS backend development and the @lenne.tech/nest-server framework. This skill handles **ALL NestJS-related tasks**, from analysis to creation to debugging:

## When to Use This Skill

**ALWAYS use this skill for:**

### Analysis & Understanding
- Analyzing existing NestJS code structure
- Understanding how modules, services, controllers work
- Reviewing project architecture
- Mapping relationships between modules
- Reading and explaining NestJS code
- Finding specific implementations (controllers, services, etc.)

### Running & Debugging
- Starting the NestJS server (`npm start`, `npm run dev`)
- Debugging server issues and errors
- Running tests (`npm test`)
- Checking server logs and output
- Configuring environment variables
- Troubleshooting build/compile errors

### Creation & Modification
- Creating new modules with `lt server module`
- Creating new objects with `lt server object`
- Adding properties with `lt server addProp`
- Creating a new server with `lt server create`
- Modifying existing code (services, controllers, resolvers)
- Adding relationships between modules
- Managing dependencies and imports

### Testing & Validation
- Creating API tests for controllers/resolvers
- Running and fixing failing tests
- Testing endpoints manually
- Validating data models and schemas
- Testing authentication and permissions

### General NestJS Tasks
- Answering NestJS/nest-server questions
- Explaining framework concepts
- Discussing architecture decisions
- Recommending best practices
- Refactoring existing code

**Rule: If it involves NestJS or @lenne.tech/nest-server in ANY way, use this skill!**

## Recommended: Test-Driven Development (TDD)

**Use TDD for robust, maintainable code:**

```
1. Write API tests FIRST (REST/GraphQL endpoint tests)
2. Implement backend code until tests pass
3. Iterate until all tests green
4. Then proceed to frontend (E2E tests first)
```

**Why TDD?**
- Catches bugs early
- Documents expected behavior
- Enables safe refactoring
- Ensures security requirements are tested

**For TDD workflow, use `building-stories-with-tdd` skill** - it coordinates backend and frontend test-first development.

### Test Cleanup (CRITICAL)

```typescript
afterAll(async () => {
  // Clean up test-created entities
  await db.collection('entities').deleteMany({ createdBy: testUserId });
  await db.collection('users').deleteMany({ email: /@test\.com$/ });
});
```

**Use separate test database:** `app-test` instead of `app-dev`

## Related Skills

**Works closely with:**
- `developing-lt-frontend` skill - For ALL Nuxt/Vue frontend development (projects/app/)
- `building-stories-with-tdd` skill - For building user stories with Test-Driven Development
- `using-lt-cli` skill - For Git operations and Fullstack initialization
- `nest-server-updating` skill - For updating @lenne.tech/nest-server to latest version

**When to use which:**
- Nuxt/Vue frontend work? Use `developing-lt-frontend` skill
- Building features with TDD workflow? Use `building-stories-with-tdd` skill (it will use this skill for implementation)
- Need Git operations? Use `using-lt-cli` skill
- Updating @lenne.tech/nest-server? Use `nest-server-updating` skill

**In monorepo projects:**
- `projects/api/` or `packages/api/` → This skill (generating-nest-servers)
- `projects/app/` or `packages/app/` → `developing-lt-frontend` skill
- Direct NestJS work? Use this skill

## TypeScript Language Server (Recommended)

**Use the LSP tool when available** for better code intelligence in TypeScript/NestJS projects:

| Operation | Use Case |
|-----------|----------|
| `goToDefinition` | Find where a class, function, or type is defined |
| `findReferences` | Find all usages of a symbol across the codebase |
| `hover` | Get type information and documentation for a symbol |
| `documentSymbol` | List all classes, functions, and variables in a file |
| `workspaceSymbol` | Search for symbols across the entire project |
| `goToImplementation` | Find implementations of interfaces or abstract methods |
| `incomingCalls` | Find all callers of a function/method |
| `outgoingCalls` | Find all functions called by a function/method |

**When to use LSP:**
- Navigating unfamiliar code → `goToDefinition`, `findReferences`
- Understanding inheritance → `goToImplementation`
- Analyzing dependencies → `incomingCalls`, `outgoingCalls`
- Exploring file structure → `documentSymbol`
- Finding symbols by name → `workspaceSymbol`

**Installation (if LSP not available):**
```bash
claude plugins install typescript-lsp --marketplace claude-plugins-official
```

---

## CRITICAL SECURITY RULES - READ FIRST

**Before you start ANY work, understand these NON-NEGOTIABLE rules:**

### NEVER Do This:
1. **NEVER remove or weaken `@Restricted()` decorators**
2. **NEVER change `@Roles()` decorators** to more permissive roles
3. **NEVER modify `securityCheck()` logic** to bypass security
4. **NEVER remove class-level `@Restricted(RoleEnum.ADMIN)`**

### ALWAYS Do This:
1. **ALWAYS analyze permissions BEFORE writing tests**
2. **ALWAYS test with the LEAST privileged user** who is authorized
3. **ALWAYS adapt tests to security requirements**, never vice versa
4. **ALWAYS ask developer for approval** before changing ANY security decorator

**Complete security rules with all details, examples, and testing strategies: `security-rules.md`**
**Comprehensive OWASP Secure Coding Practices checklist: `owasp-checklist.md`**

## CRITICAL: NEVER USE `declare` KEYWORD FOR PROPERTIES

**DO NOT use the `declare` keyword when defining properties in classes!**

```typescript
// WRONG
declare name: string;  // Decorator won't work!

// CORRECT
@UnifiedField({ description: 'Product name' })
name: string;  // Decorator works properly
```

**Why**: `declare` prevents decorators from being applied, breaking the decorator system.

**Complete explanation and correct patterns: `declare-keyword-warning.md`**

## CRITICAL: DESCRIPTION MANAGEMENT

**Descriptions must be applied consistently to EVERY component.**

**Quick 3-Step Process:**
1. Extract descriptions from user's `// comments`
2. Format: `'English text'` or `'English (Deutsch)'` for German input
3. Apply EVERYWHERE: Model, CreateInput, UpdateInput, Objects, Class-level decorators

**Complete formatting rules, examples, and verification checklist: `description-management.md`**

---

## Core Responsibilities

This skill handles **ALL** NestJS server development tasks, including:

### Simple Tasks (Single Commands)
- Creating a single module with `lt server module`
- Creating a single object with `lt server object`
- Adding properties with `lt server addProp`
- Creating a new server with `lt server create`
- Starting the server with `npm start` or `npm run dev`
- Running tests with `npm test`

### Complex Tasks (Multiple Components)
When you receive a complete structure specification, you will:

1. **Parse and analyze** the complete structure (modules, models, objects, properties, relationships)
2. **Create a comprehensive todo list** breaking down all tasks
3. **Generate all components** in the correct order (objects first, then modules)
4. **Handle inheritance** properly (Core and custom parent classes)
5. **Manage descriptions** (translate German to English, add originals in parentheses)
6. **Create API tests** for all controllers and resolvers
7. **Verify functionality** and provide a summary with observations

### Analysis Tasks
When analyzing existing code:

1. **Explore the project structure** to understand the architecture
2. **Read relevant files** (modules, services, controllers, models)
3. **Identify patterns** and conventions used in the project
4. **Explain findings** clearly and concisely
5. **Suggest improvements** when appropriate

### Debugging Tasks
When debugging issues:

1. **Read error messages and logs** carefully
2. **Identify the root cause** by analyzing relevant code
3. **Check configuration** (environment variables, config files)
4. **Test hypotheses** by examining related files
5. **Provide solutions** with code examples

**Remember:** For ANY task involving NestJS or @lenne.tech/nest-server, use this skill!

## Understanding the Framework

**Complete framework guide: `framework-guide.md`**

**Critical Rules:**
- [ ] Read CrudService before modifying any Service (`node_modules/@lenne.tech/nest-server/src/core/common/services/crud.service.ts`)
- [ ] NEVER blindly pass all serviceOptions to other Services (only pass `currentUser`)
- [ ] Check if CrudService already provides needed functionality (create, find, findOne, update, delete, pagination)

## Configuration File & Commands

**Complete guide: `configuration.md`**

**Quick Command Reference:**
```bash
# Create complete module (REST is default!)
lt server module --name Product --controller Rest

# Create SubObject
lt server object --name Address

# Add properties
lt server addProp --type Module --element User

# New project
lt server create <server-name>
```

**API Style: REST is the default!**
- **REST** (default): Use `--controller Rest` - Standard for all modules unless explicitly requested otherwise
- **GraphQL**: Use `--controller GraphQL` - ONLY when user explicitly requests GraphQL
- **Both**: Use `--controller Both` - ONLY when user explicitly wants both REST and GraphQL

**Essential Property Flags:**
- `--prop-name-X / --prop-type-X` - Name and type (string|number|boolean|ObjectId|Json|Date|bigint)
- `--prop-nullable-X` / `--prop-array-X` - Modifiers
- `--prop-enum-X / --prop-schema-X / --prop-reference-X` - Complex types

## Service Health Check (MANDATORY)

**Before starting ANY backend work, check if services are running:**

```bash
# Check if API is running (Port 3000)
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api

# Check if port is in use (alternative)
lsof -i :3000
```

**Workflow:**

```
┌────────────────────────────────────────────────────────────────┐
│  BEFORE starting backend work:                                 │
│                                                                │
│  1. CHECK if Port 3000 is in use:                              │
│     lsof -i :3000                                              │
│     - If port in use: API already running, proceed             │
│     - If port free: Start API                                  │
│                                                                │
│  2. START API (if not running):                                │
│     cd projects/api && npm run start:dev &                     │
│     - Wait until API responds (max 30s)                        │
│     - Verify: curl -s http://localhost:3000/api                │
│                                                                │
│  3. FOR FULLSTACK WORK (API + Frontend):                       │
│     Also check Port 3001 for frontend                          │
│     cd projects/app && npm run dev &                           │
│                                                                │
│  4. ONLY THEN proceed with development                         │
└────────────────────────────────────────────────────────────────┘
```

**Starting Services (if not running):**

```bash
# Start API in background (from monorepo root)
cd projects/api && npm run start:dev &

# Optional: Start Frontend too (Port 3001)
cd projects/app && npm run dev &
```

**Important:**
- Always check with `lsof -i :3000` BEFORE starting to avoid duplicate processes
- If port is in use but service not responding, kill the process first: `kill $(lsof -t -i :3000)`
- For tests that require running server, ensure API is started first

## Prerequisites Check

**Setup:**
```bash
lt --version  # Check CLI installation
npm install -g @lenne.tech/cli  # If needed
ls src/server/modules  # Verify project structure
```

**Creating New Server:**
```bash
lt server create <server-name>
```

**Post-creation verification:** Check `src/config.env.ts` for replaced secrets and correct database URIs.

## Understanding the Specification Format

**Complete reference and examples: `reference.md` and `examples.md`**

**Quick Type Reference:**
- Basic: `string`, `number`, `boolean`, `Date`, `bigint`, `Json`
- Arrays: `type[]` -> add `--prop-array-X true`
- Optional: `property?: type` -> add `--prop-nullable-X true`
- References: `User` -> use `--prop-type-X ObjectId --prop-reference-X User`
- Embedded: `Address` -> use `--prop-schema-X Address`
- Enums: `ENUM (VAL1, VAL2)` -> use `--prop-enum-X PropertyNameEnum`

## Workflow Process

**Complete details: `workflow-process.md`**

**7-Phase Workflow:**
1. Analysis & Planning - Parse spec, create todo list
2. SubObject Creation - Create in dependency order
3. Module Creation - Create with all properties
4. Inheritance Handling - Update extends, CreateInput must include parent fields
5. **Description Management** (CRITICAL) - Extract from comments, format as "ENGLISH (DEUTSCH)", apply everywhere
6. Enum File Creation - Manual creation in `src/server/common/enums/`
7. API Test Creation - **MANDATORY:** Analyze permissions first, use least privileged user, test failures

**Critical Testing Rules:**
- Test via REST/GraphQL using TestHelper (NEVER direct Service tests)
- Analyze @Roles decorators BEFORE writing tests
- Use appropriate user role (not admin when S_USER works)
- Test unauthorized access failures (401/403)

## Property Ordering

**ALL properties must be in alphabetical order** in Model, Input, and Output files. Verify and reorder after generating.

## Verification Checklist

**Complete checklist: `verification-checklist.md`**

**Essential Checks:**
- [ ] All components created with descriptions (Model + CreateInput + UpdateInput)
- [ ] Properties in alphabetical order
- [ ] Permission analysis BEFORE writing tests
- [ ] Least privileged user used in tests
- [ ] Security validation tests (401/403 failures)
- [ ] All tests pass

## Error Handling

**Common Issues:**
- **TypeScript errors** -> Add missing imports manually
- **CreateInput validation fails** -> Check parent's CreateInput for required fields
- **Tests fail with 403** -> Check @Roles decorator, use appropriate user role (not admin when S_USER works)
- **Security tests not failing** -> Verify @Roles and securityCheck() logic, fix model/controller if needed

## Phase 8: Pre-Report Quality Review

**Complete process: `quality-review.md`**

**7 Steps:**
1. Identify all changes (git)
2. Test management (analyze existing tests, create new, follow patterns)
3. Compare with existing code (consistency)
4. Critical analysis (style, structure, quality)
5. Automated optimizations (imports, properties, formatting)
6. Pre-report testing (build, lint, all tests must pass)
7. Final verification (complete checklist)

**Critical:** Understand TestHelper, analyze existing tests first, use appropriate user roles, all tests must pass.

## Final Report

After completing all tasks, provide:
1. Summary of created components (SubObjects, Objects, Modules, enums, tests)
2. Observations about data structure
3. Test results (all passing)
4. Next steps

## Best Practices

1. Create dependencies first (SubObjects before Modules)
2. Check for circular dependencies
3. Test incrementally, commit after major components
4. **Use REST controller by default** - Only use GraphQL when explicitly requested
5. Validate required fields in tests
6. Document complex relationships

## Working with This Skill

When receiving a specification:
1. Parse completely, ask clarifying questions
2. Create detailed todo list
3. Execute systematically following workflow
4. Verify each step, report progress
5. Provide comprehensive summary
