---
name: project-index
description: "Generate PROJECT_INDEX.yaml for a repository to enable fast file lookup. Use when setting up a new repo, updating project index, or when user mentions 'generate index', 'project index', 'update index'."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Project Index Generator

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Generate `PROJECT_INDEX.yaml` files for repositories to provide instant file lookup for agents.

## Commands

- `/project-index generate {repo} {team}` - Generate index for a repo
- `/project-index update {repo} {team}` - Regenerate/update existing index

## Purpose

PROJECT_INDEX.yaml eliminates Glob overhead by pre-computing file paths. Instead of:
```
Glob(pattern="**/Controllers/*.php")  # 50+ files scanned
```

Agents can:
```
Read: {repo}/PROJECT_INDEX.yaml  # Instant lookup
```

## Process

### `/project-index generate {repo} {team}`

#### Step 1: Run Generator Script

```bash
cd .
./scripts/generate-project-index.sh {repo} {team}
```

The script:
1. Detects project type (Laravel, Flutter, Nuxt, Go)
2. Scans entry points
3. Extracts model information
4. Generates structured YAML

#### Step 2: Review Generated File

```
Read: {teams_dir}/{team}/repos/{repo}/PROJECT_INDEX.yaml
```

#### Step 3: Complete TODOs

The generated file includes TODOs for manual completion:
- Module descriptions
- Model relationships
- Critical file annotations

## Supported Project Types

| Type | Detection | Entry Points |
|------|-----------|--------------|
| Laravel | `artisan` file | Routes, Controllers, Models, Migrations |
| Flutter | `pubspec.yaml` | lib/, screens/, widgets/, services/ |
| Nuxt | `nuxt.config.ts` | pages/, components/, composables/ |
| Go | `go.mod` | cmd/, internal/, pkg/ |

## Index File Structure

```yaml
# PROJECT_INDEX.yaml
project: "{repo_name}"
type: laravel
version: "1.0"
generated_at: "2026-01-12T10:00:00Z"

entry_points:
  routes: "routes/api.php"
  web_routes: "routes/web.php"
  models: "app/Models/"
  controllers: "app/Http/Controllers/"
  migrations: "database/migrations/"
  config: "config/"
  views: "resources/views/"

modules:
  events:
    description: "Event management" # TODO: Add description
    model: "app/Models/Event.php"
    controller: "app/Http/Controllers/EventController.php"
    migration: "database/migrations/2024_01_01_create_events_table.php"
    views: "resources/views/events/"
    tests: "tests/Feature/EventTest.php"

models:
  Event:
    path: "app/Models/Event.php"
    table: "events"
    traits: ["HasFactory", "SoftDeletes"]
    relationships: ["belongsTo:User", "hasMany:Ticket"]

  Ticket:
    path: "app/Models/Ticket.php"
    table: "tickets"
    relationships: ["belongsTo:Event"]

task_contexts:
  bug_fix:
    priority_files:
      - "routes/api.php"
      - "app/Http/Controllers/"
    search_pattern: "function {method}"

  new_endpoint:
    steps:
      - "Add route to routes/api.php"
      - "Create/update controller"
      - "Add tests"

anti_patterns:
  - "Don't add business logic to controllers"
  - "Don't skip migrations"
  - "Don't hardcode IDs"
```

## Examples

```bash
# Generate index for a project
/project-index generate my-app-core my-project

# Update an existing index
/project-index update my-saas-v2 my-project

# Generate index for a personal project
/project-index generate personal-site personal
```

## Manual Index Creation

If the script doesn't support your project type, create manually:

1. Create `PROJECT_INDEX.yaml` in repo root
2. Add entry_points for quick navigation
3. Add modules for feature organization
4. Add models for data structure reference
5. Add task_contexts for common workflows

## Notes

- Re-run when adding major features
- Keep descriptions updated
- Include test file locations
- Document anti-patterns

Script location: `scripts/generate-project-index.sh`
SOP: `docs/system/sops/project-index-workflow.md`

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
