---
name: write-issue
description: Create or update project issues following the Epic specification format with Behaviors (Rules + Examples), Technical Specifications (Action/Hook/Component/Service), and task lists. Use when user asks to create/update an issue, document requirements, or write specifications for a new feature.
---

# Write Issue

## Overview

This skill creates issues that combine behavioral specifications with technical implementation details. Issues follow the Epic specification format where **Behavior is the bridge** between functional and technical specs.

## Issue Structure

```markdown
# [Issue title]

Brief overview of what this issue accomplishes.

# Functional Specification

## Behavior: [Name]

[One paragraph describing the behavior in user-facing terms.]
Directory: `app/[role]/[page]/behaviors/[behavior-name]/`

### Rules

#### [Rule Name]
- When:
  - [Condition]
- Then:
  - [Outcome]

### Examples

#### [Primary Use Case]

##### PreDB
[table-name]:
col_a, col_b, col_c
1, foo, bar

##### Steps
* Act: [User or system performs an action]
* Act: [Another action]
* Check: [Observable result in UI / API response]
* Check: [Observable result in database]

##### PostDB
[table-name]:
col_a, col_b, col_c
1, foo, bar
2, new, row

# Technical Specification

## createProject(input: CreateProjectInput): Promise<Project>

Creates a new project for the authenticated user.

- Given: project name and authenticated user with "client" role
- Returns: the newly created project
- Calls: ProjectModel.findByNameAndUser, ProjectModel.create

### Example: Create project successfully

#### PreDB
users:
id, email, role
1, user@example.com, client

projects:
id, user_id, name, status
1, 1, Existing Project, active

#### PostDB
projects:
id, user_id, name, status, created_at
1, 1, Existing Project, active, <timestamp>
2, 1, New Project, draft, <timestamp>

---

## useCreateProject(options?: Options)

Manages form state and submission logic for creating a new project.

### Parameters
- options.onSuccess: (project: Project) => void - callback after successful creation

### State
- name: string
- errors: ValidationErrors
- isPending: boolean

### Returns
- name: string - current name value
- errors: ValidationErrors - field-level errors
- isPending: boolean - submission in progress
- setName: (value: string) => void - update name field
- submit: () => Promise<void> - submit the form
- reset: () => void - reset to initial state

### Dependencies
- useProjects - for optimistic updates to project list

---

## Component: [ComponentName]
File: `[page-path]/components/[component-name].tsx`
Props: `{ prop1: Type, prop2?: Type }`

[Single sentence describing what this component renders]

### [Primary Use Case]

* Uses `use-[hook-name]` for [behavior]
* Renders [UI elements]
* Handles [user interactions]

# Tasks

* [ ] Backend implementation
* [ ] Frontend components
* [ ] Testing

# Notes

Additional implementation considerations
```

## Workflow for Creating Issues

### 1. Check Current Implementation

**Before writing the issue, analyze what already exists:**

1. **Search for related files:**
   - Check if behavior files exist (e.g., `app/client/projects/behaviors/create-project/`)
   - Look for existing tests (e.g., `behaviors/*/tests/*.spec.ts`)
   - Review database schema (`db/schema.ts`)

2. **Review existing code:**
   - Read any existing implementation files
   - Note patterns and conventions used in the codebase
   - Identify dependencies

3. **Align with current state:**
   - Match existing naming conventions
   - Follow established patterns
   - Identify gaps between spec and current implementation

### 2. Gather Context

Determine:
- **Issue Title**: Clear description of the feature
- **Behavior Name**: kebab-case name for the behavior
- **Directory**: `app/[role]/[page]/behaviors/[behavior-name]/`
- **File Path**: `docs/issues/[prefix]-[number]-[slug].md`

If information is missing, ask the user before proceeding.

### 3. Write Functional Specification

Define **what** the system should do behaviorally.

#### Behavior Structure

```markdown
## Behavior: [Name]

[One paragraph describing the behavior in user-facing terms.]
Directory: `app/[role]/[page]/behaviors/[behavior-name]/`
```

#### Rules (When/Then)

Rules are **declarative constraints** with conditions and outcomes:

```markdown
### Rules

#### Authentication Required
- When:
  - User is not authenticated
- Then:
  - Reject with "Unauthorized"

#### Name Required
- When:
  - Project name is empty
- Then:
  - Reject with "Name is required"
  - Form field "name" shows error

#### Unique Name Per User
- When:
  - Project name already exists for user
- Then:
  - Reject with "Project name already exists"
```

**Rule guidelines:**
- Each rule has a descriptive name
- Multiple conditions under When are implicitly AND
- For OR logic, create separate rules
- Then describes observable outcomes

#### Examples (Act/Check)

Examples demonstrate how behavior plays out in concrete scenarios:

```markdown
### Examples

#### User creates project successfully

##### PreDB
users:
id, email, role, status
1, user@example.com, client, active

projects:
id, user_id, name, status
1, 1, Existing Project, active

##### Steps
* Act: User logs in as "client"
* Act: User navigates to the projects page
* Act: User submits the create project form with name "New Project"
* Check: New project appears in the list
* Check: Project status is "draft"

##### PostDB
projects:
id, user_id, name, status
1, 1, Existing Project, active
2, 1, New Project, draft
```

**Step keywords:**
- `Act:` - User or system performs an action (changes state)
- `Check:` - Verification that something is true (asserts state)

**Key points:**
- Use CSV-like format for database tables (headers, then data rows)
- Use placeholders: `<uuid>`, `<timestamp>`, `<vector>`
- PostDB include both pre-existing and new rows
- **Keep it simple**: 2-3 examples maximum (primary use case + key edge cases)

### 4. Write Technical Specification

Define **how** to implement the feature. Each unit type has its own format.

#### Function Specification (for Actions)

Actions use the **Function specification format** with optional examples for state changes:

```markdown
## functionName(input: InputType): ReturnType

[Short description of what the function does]

- Given: [input parameters and assumptions]
- Returns: [value or outcome returned]
- Calls: [direct dependencies - models, integrations]

### Example: [Scenario name]

#### PreDB
[table_name]:
column1, column2, column3
value1, value2, value3

#### PostDB
[table_name]:
column1, column2, column3
value1, value2, value3
new_id, new_val, new_val
```

**Example:**
```markdown
## createProject(input: CreateProjectInput): Promise<Project>

Creates a new project for the authenticated user.

- Given: project name and authenticated user with "client" role
- Returns: the newly created project
- Calls: ProjectModel.findByNameAndUser, ProjectModel.create

### Example: Create project successfully

#### PreDB
users:
id, email, role
1, user@example.com, client

projects:
id, user_id, name, status
1, 1, Existing Project, active

#### PostDB
projects:
id, user_id, name, status, created_at
1, 1, Existing Project, active, <timestamp>
2, 1, New Project, draft, <timestamp>

### Example: Reject duplicate name

#### PreDB
projects:
id, user_id, name
1, 1, My Project

#### PostDB
(no changes - operation rejected)
```

**Guidelines:**
- Signature as heading: `## functionName(input: Type): ReturnType`
- Description is one sentence
- Given describes input parameters and assumptions
- Returns describes the return value
- Calls lists direct dependencies (optional)
- Examples show database state transitions (for functions that modify state)
- Use placeholders: `<uuid>`, `<timestamp>` for generated values

#### Hook Specification

Hooks use structured sections for parameters, state, returns, and dependencies:

```markdown
## useHookName(params?: ParamType)

[Short description of what stateful logic this hook encapsulates]

### Parameters
- paramName: Type - description

### State
- stateName: Type
- anotherState: Type

### Returns
- value: Type - description
- action: () => void - description

### Dependencies
- useOtherHook - why it's needed
```

**Example:**
```markdown
## useCreateProject(options?: Options)

Manages form state and submission logic for creating a new project.

### Parameters
- options.onSuccess: (project: Project) => void - callback after successful creation

### State
- name: string
- errors: ValidationErrors
- isPending: boolean

### Returns
- name: string - current name value
- errors: ValidationErrors - field-level errors
- isPending: boolean - submission in progress
- setName: (value: string) => void - update name field
- submit: () => Promise<void> - submit the form
- reset: () => void - reset to initial state

### Dependencies
- useProjects - for optimistic updates to project list
```

**Guidelines:**
- Use hook signature as the heading
- Parameters section lists what the hook accepts
- State section lists internal state it manages
- Returns section lists all exposed values and functions
- Dependencies section lists other hooks it calls (optional)

#### Component Specification

```markdown
## Component: [ComponentName]
File: `[page-path]/components/[component-name].tsx`
Props: `{ prop1: Type, prop2?: Type }`

[Single sentence describing what this component renders and its purpose]

### [Primary Use Case]

* Uses `use-[hook-name]` for [behavior]
* Renders [UI elements]
* Handles [user interactions]
```

#### Service Specification

```markdown
## Service: [ServiceName]
File: `shared/services/[service-name]/[service-name].service.ts`

[Single sentence describing what external system this integrates with]

### [Primary Use Case]

* Integrates with [external API/service]
* Handles [authentication/rate limiting/retries]
* Transforms external data to internal format
* Returns typed responses

### [Error Handling]

* Retries on network failures (max 3 attempts)
* Throws typed errors for API failures
```

### 5. Write Tasks

Break down implementation into trackable tasks:

```markdown
# Tasks

* [ ] Backend implementation
  * [ ] Create action file with validation
  * [ ] Add model methods if needed
* [ ] Frontend components
  * [ ] Create hook with optimistic updates
  * [ ] Create/update component
* [ ] Testing
  * [ ] Write behavior tests for examples
  * [ ] Write action tests
```

**Task guidelines:**
- Make tasks specific and actionable
- Use verbs: Create, Implement, Add, Set up
- Order by dependency
- Each example should have a corresponding test task

### 6. Create or Update File

**For new issues:**
Use Write tool with path `docs/issues/[prefix]-[number]-[slug].md`

**For updating existing issues:**
1. Read the existing file first
2. Use Edit tool for targeted changes

### 7. Validate

Check:
- [ ] Behavior has clear Rules with When/Then format
- [ ] 2-3 Examples maximum covering primary use case + key edge cases
- [ ] Each Example has PreDB/Steps/PostDB
- [ ] Steps use Act: and Check: prefixes
- [ ] Technical specs follow Action/Hook/Component/Service formats
- [ ] Tasks are specific and ordered by dependency

## Usage with Other Skills

**write-unit-test skill:**
Examples can be directly used with write-unit-test to generate behavioral tests. The PreDB/Steps/PostDB format maps to PreDB/Execute/PostDB pattern.

## Reference

See `docs/templates/issue.md` for the complete issue template.
See `docs/Epic.md` for the full Epic specification format documentation.

### Examples

- `references/implement-issue.md` - Example of implementing a new behavior from scratch (new feature with database changes)
- `references/change-issue.md` - Example of changing existing behaviors (refactoring, moving code, updating modules)
