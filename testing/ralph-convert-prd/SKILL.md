---
name: ralph-convert-prd
description: Converts Product Requirements Documents into prd.json format for the Ralph autonomous agent system. Use when preparing PRDs for Ralph execution, breaking down features into atomic user stories, or when the user mentions Ralph, prd.json, or autonomous agent workflows.
model: claude-opus-4-5
context: fork
---

<objective>
Transform existing Product Requirements Documents into the structured `prd.json` format used by the Ralph autonomous agent system. Each story must be completable in one LLM context window to prevent broken code from context overflow. Each story must include real runtime verification commands.
</objective>

<quick_start>
1. Read the user's PRD or feature requirements
2. Read SPEC.md if available (for verification environment info)
3. Break down into atomic user stories (one context window each)
4. Classify each story with `storyType`
5. Generate `verificationCommands` with real runtime checks
6. Set `blockedBy` dependencies
7. Order stories by dependency (schema → backend → UI → dashboard)
8. Output valid `tasks/prd.json`
</quick_start>

<essential_principles>
<principle name="story_size">
**Critical Rule**: Each story must be completable in ONE Ralph iteration (one context window).

Stories that are too large cause the LLM to run out of context before completion, resulting in broken code.

**Right-sized stories**:
- Add a database column
- Create a UI component
- Update server actions
- Implement a filter

**Too large (split these)**:
- Build entire dashboards
- Add authentication systems
- Refactor entire APIs
</principle>

<principle name="story_ordering">
Stories must execute sequentially without forward dependencies:

1. Schema/database changes
2. Server actions and backend logic
3. UI components
4. Dashboard/summary views

Never reference something that doesn't exist yet.
</principle>

<principle name="acceptance_criteria">
Each criterion must be verifiable and specific. Avoid vague language.

**Good criteria**:
- "Add status column with values: 'pending' | 'in_progress' | 'done'"
- "Filter dropdown includes: All, Active, Completed"
- "Clicking delete shows confirmation dialog"

**Bad criteria** (too vague):
- "Works correctly"
- "Good UX"
- "Handles edge cases"
</principle>

<principle name="mandatory_criteria">
Every story MUST include: `"Typecheck passes"`

UI-focused stories MUST also include: `"Verify in browser using Playwright e2e test"`
</principle>

<principle name="real_verification">
Every story MUST include `verificationCommands` with real runtime checks — not just static analysis.

**By storyType:**

| storyType | Required verification | Example |
|-----------|----------------------|---------|
| `database` | Run migration + query DB to confirm schema | `prisma migrate deploy`, SQL query for new column |
| `backend` | Run tests + curl endpoint with real data | `curl -s http://localhost:3000/api/...` |
| `api` | curl endpoint, check status code and response body | `curl -s -w '%{http_code}' ...` |
| `frontend` | Playwright e2e test that interacts with real UI | `npx playwright test tests/e2e/...` |
| `infra` | Health check, config validation, service startup | `curl -s http://localhost:3000/health` |
| `test` | Run the test suite | `npm test` / `pytest` |

Static checks (typecheck) are always included as baseline. Runtime validation is **additionally required**.
</principle>
</essential_principles>

<output_format>
```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name-kebab-case]",
  "description": "[Feature description]",
  "testCommands": {
    "unit": "npm test",
    "integration": "npm run test:integration",
    "e2e": "npx playwright test",
    "typecheck": "npm run typecheck"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "storyType": "database",
      "acceptanceCriteria": [
        "Specific criterion 1",
        "Specific criterion 2",
        "Typecheck passes"
      ],
      "verificationCommands": [
        { "command": "npm run typecheck", "expect": "exit_code:0" },
        { "command": "curl -s http://localhost:3000/api/tasks | jq length", "expect": "not_empty" }
      ],
      "status": "pending",
      "priority": 1,
      "attempts": 0,
      "maxAttempts": 3,
      "notes": "",
      "blockedBy": [],
      "docsToUpdate": ["README.md"],
      "completedAt": null,
      "lastAttemptLog": ""
    }
  ]
}
```

**Field requirements**:
- `id`: Sequential US-001, US-002, etc.
- `title`: Short, descriptive action
- `description`: User story format (As a... I want... so that...)
- `storyType`: One of `"backend"` | `"frontend"` | `"database"` | `"api"` | `"infra"` | `"test"`
- `acceptanceCriteria`: Array of specific, verifiable criteria
- `verificationCommands`: Array of `{command, expect}` with real runtime checks
- `status`: Always `"pending"` initially
- `priority`: Execution order (1 = first)
- `attempts`: Always `0` initially
- `maxAttempts`: Default `3` (increase for complex stories)
- `notes`: Empty string initially
- `blockedBy`: Array of story IDs that must be `"done"` first
- `docsToUpdate`: Array of file paths to documentation that must be updated when story is done (e.g., `"README.md"`, `"docs/api.md"`, `"CHANGELOG.md"`)
- `completedAt`: Always `null` initially
- `lastAttemptLog`: Empty string initially

**Expect matchers for verificationCommands:**
- `exit_code:0` — command exits with code 0
- `exit_code:N` — command exits with specific code N
- `contains:STRING` — stdout contains STRING
- `not_empty` — stdout is non-empty
- `matches:REGEX` — stdout matches regex pattern
</output_format>

<workflow>
1. **Understand the PRD**: Read the full requirements document or feature request
2. **Read SPEC.md**: If available, extract verification environment info (dev server URL, DB type, test runners, commands). Use this to populate the root-level `testCommands` object
3. **Identify components**: List all database changes, backend logic, UI elements
4. **Decompose into stories**: Break each component into atomic, one-iteration tasks
5. **Classify storyType**: Assign `database`, `backend`, `api`, `frontend`, `infra`, or `test` to each story
6. **Order by dependency**: Schema first, then backend, then UI, then dashboards
7. **Set blockedBy**: Each story should list IDs of stories it depends on
8. **Write acceptance criteria**: Make each criterion specific and verifiable
9. **Generate verificationCommands**: Add real runtime checks per storyType (curl, Playwright, DB queries)
10. **Add mandatory criteria**: Ensure every story has "Typecheck passes"
11. **Generate tasks/prd.json**: Output the complete JSON structure to `tasks/prd.json`
12. **Run pre-save checklist**: Verify all requirements before finalizing
</workflow>

<pre_save_checklist>
Before outputting the final prd.json, verify:

- [ ] Previous runs archived (if applicable)
- [ ] Each story completable in one iteration
- [ ] Each story has a `storyType` assigned
- [ ] Stories ordered by dependency (no forward references)
- [ ] `blockedBy` dependencies are set correctly
- [ ] All stories include "Typecheck passes" in acceptanceCriteria
- [ ] UI stories include Playwright verification
- [ ] Every story has `verificationCommands` with at least one runtime check
- [ ] Acceptance criteria are verifiable, not vague
- [ ] No story depends on later stories
- [ ] `docsToUpdate` lists relevant docs for each story
- [ ] `status` is `"pending"`, `attempts` is `0`, `maxAttempts` is set
</pre_save_checklist>

<examples>
<example name="database_story">
```json
{
  "id": "US-001",
  "title": "Add task status column to database",
  "description": "As a developer, I want a status column on tasks so that we can track task progress",
  "storyType": "database",
  "acceptanceCriteria": [
    "Add status column to tasks table with type enum('pending', 'in_progress', 'done')",
    "Default value is 'pending'",
    "Migration runs without errors",
    "Typecheck passes"
  ],
  "verificationCommands": [
    { "command": "npx prisma migrate deploy", "expect": "exit_code:0" },
    { "command": "npx prisma db execute --stdin <<< \"SELECT column_name FROM information_schema.columns WHERE table_name='tasks' AND column_name='status'\"", "expect": "contains:status" },
    { "command": "npm run typecheck", "expect": "exit_code:0" }
  ],
  "status": "pending",
  "priority": 1,
  "attempts": 0,
  "maxAttempts": 3,
  "notes": "",
  "blockedBy": [],
  "docsToUpdate": ["README.md"],
  "completedAt": null,
  "lastAttemptLog": ""
}
```
</example>

<example name="api_story">
```json
{
  "id": "US-002",
  "title": "Create task CRUD API endpoints",
  "description": "As a developer, I want REST endpoints for tasks so that the frontend can manage tasks",
  "storyType": "api",
  "acceptanceCriteria": [
    "GET /api/tasks returns array of tasks",
    "POST /api/tasks creates a new task and returns 201",
    "PATCH /api/tasks/:id updates task and returns 200",
    "DELETE /api/tasks/:id removes task and returns 204",
    "Typecheck passes"
  ],
  "verificationCommands": [
    { "command": "npm run typecheck", "expect": "exit_code:0" },
    { "command": "npm test -- --grep 'tasks API'", "expect": "exit_code:0" },
    { "command": "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/api/tasks", "expect": "contains:200" },
    { "command": "curl -s -X POST http://localhost:3000/api/tasks -H 'Content-Type: application/json' -d '{\"title\":\"test task\"}' -o /dev/null -w '%{http_code}'", "expect": "contains:201" }
  ],
  "status": "pending",
  "priority": 2,
  "attempts": 0,
  "maxAttempts": 3,
  "notes": "",
  "blockedBy": ["US-001"],
  "docsToUpdate": ["README.md", "docs/api.md"],
  "completedAt": null,
  "lastAttemptLog": ""
}
```
</example>

<example name="ui_story">
```json
{
  "id": "US-003",
  "title": "Add status filter dropdown to task list",
  "description": "As a user, I want to filter tasks by status so that I can focus on relevant tasks",
  "storyType": "frontend",
  "acceptanceCriteria": [
    "Filter dropdown appears above task list",
    "Options: All, Pending, In Progress, Done",
    "Selecting option filters displayed tasks",
    "Filter persists on page refresh",
    "Typecheck passes",
    "Verify in browser using Playwright e2e test"
  ],
  "verificationCommands": [
    { "command": "npm run typecheck", "expect": "exit_code:0" },
    { "command": "npx playwright test tests/e2e/task-filter.spec.ts", "expect": "exit_code:0" }
  ],
  "status": "pending",
  "priority": 3,
  "attempts": 0,
  "maxAttempts": 3,
  "notes": "",
  "blockedBy": ["US-002"],
  "docsToUpdate": ["README.md"],
  "completedAt": null,
  "lastAttemptLog": ""
}
```
</example>
</examples>

<success_criteria>
Conversion is complete when:

- [ ] All features from PRD are captured as user stories
- [ ] Each story is atomic (one context window)
- [ ] Each story has a `storyType` assigned
- [ ] Stories are properly ordered by dependency with `blockedBy` set
- [ ] All acceptance criteria are specific and verifiable
- [ ] Mandatory criteria ("Typecheck passes") present on all stories
- [ ] Every story has `verificationCommands` with real runtime checks
- [ ] UI stories include Playwright verification
- [ ] Valid JSON structure with all required fields
- [ ] Pre-save checklist passes
</success_criteria>
