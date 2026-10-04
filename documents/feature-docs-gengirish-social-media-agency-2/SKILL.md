---
name: feature-docs
description: Maintain ever-evolving feature documentation that stays in sync with the codebase. Use after adding, changing, or removing features — API endpoints, database models, services, UI pages, integrations, or workers. Also use when the user mentions "update feature docs," "document this feature," "sync docs with code," "feature documentation," "what features exist," or "changelog."
---

# Feature Documentation — Living Codebase Docs

Keep `docs/features/` in sync with the actual codebase so documentation never drifts from reality.

## When to Run

Trigger this skill whenever code changes touch:
- API routers/endpoints (`backend/src/agency/routers/`)
- Database models or migrations (`backend/src/agency/models/`, `backend/alembic/`)
- Services (`backend/src/agency/services/`)
- Celery workers (`backend/src/agency/workers/`)
- Platform integrations (`backend/src/agency/integrations/`)
- WebSocket handlers (`backend/src/agency/websocket/`)
- Frontend pages (`frontend/src/app/`)
- Frontend components (`frontend/src/components/`)
- Environment variables (`.env.example`, `backend/src/agency/config.py`)
- Middleware (`backend/src/agency/middleware/`)

## Workflow

### Step 1: Detect What Changed

Scan the areas that were modified. Use git diff when available:

```bash
git diff --name-only HEAD~1
```

Or compare against the documented state in `docs/features/`.

### Step 2: Read Current Feature Docs

Read the relevant section(s) in `docs/features/`:

```
docs/features/
├── README.md              # Feature index with status overview
├── api-endpoints.md       # All REST API endpoints
├── database-schema.md     # Tables, columns, relationships
├── services.md            # Business logic services
├── workers.md             # Background jobs (Celery)
├── integrations.md        # Platform connectors
├── websocket.md           # Real-time features
├── frontend-pages.md      # UI pages and routes
├── frontend-components.md # Reusable UI components
├── auth-and-rbac.md       # Authentication & roles
├── billing.md             # Stripe billing features
└── changelog.md           # Chronological change log
```

### Step 3: Update the Docs

For each changed area, update the matching doc file. Follow the format in [templates.md](templates.md).

**Rules:**
- Scan the actual source code, don't guess
- Include function signatures, route paths, model fields from real code
- Mark features as `[PLANNED]`, `[IN PROGRESS]`, `[LIVE]`, or `[DEPRECATED]`
- Add date of last verification: `<!-- verified: 260324 -->`
- Keep entries atomic — one feature per section, easy to update individually

### Step 4: Update the Index

Update `docs/features/README.md` with:
- New features added
- Changed feature statuses
- Removed/deprecated features
- Last-updated date

### Step 5: Update the Changelog

Append to `docs/features/changelog.md`:

```markdown
## YYMMDD — Brief Description

- **Added**: [feature] — short explanation
- **Changed**: [feature] — what changed and why
- **Deprecated**: [feature] — replacement or removal plan
- **Fixed**: [feature] — what was broken
```

## Scan Targets Reference

For detailed scan patterns per area, see [scan-targets.md](scan-targets.md).

## Feature Doc Format

Each feature doc follows this pattern:

```markdown
## Feature Name
<!-- verified: YYMMDD -->
**Status**: [LIVE] | [PLANNED] | [IN PROGRESS] | [DEPRECATED]

### Purpose
One-line description of what this feature does.

### Implementation
- **File(s)**: `path/to/file.py`
- **Route**: `POST /api/v1/content` (API only)
- **Model**: `Content` table (DB only)

### Key Details
Bullet list of important behaviors, constraints, or config.

### Dependencies
What this feature depends on (other services, env vars, etc.)
```

## Verification Protocol

When asked to verify docs are current:

1. **Glob** for all source files in scan targets
2. **Grep** for route decorators, model classes, page exports, service methods
3. Compare against documented features
4. Flag any **undocumented features** or **stale docs**
5. Output a diff report:

```
SYNC REPORT — YYMMDD
━━━━━━━━━━━━━━━━━━━
✅ In sync:      12 features
⚠️  Undocumented:  2 features (list them)
🗑️  Stale docs:    1 feature  (list them)
━━━━━━━━━━━━━━━━━━━
```

## Integration with Other Workflows

- After running this skill, update `agency-project` SKILL.md if the project structure changed
- Notify `docs-manager` agent if marketing-facing features changed (pricing, billing, analytics)
- If new env vars were added, update `.env.example` and `docs/features/README.md`
