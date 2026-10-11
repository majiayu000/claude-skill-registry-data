---
name: review-router
description: Routes PR review by diff — delegates to backend/frontend specialist.
---

# Review Router

Classify the changeset and route to the correct specialist reviewer(s). Run this logic before any review work begins.

---

## Step 1 — Classify the Diff

Run the following command to get the list of changed files:

```bash
git diff main...HEAD --name-only 2>/dev/null || git diff HEAD~1 --name-only
```

If reviewing a specific ref or PR branch, adapt the command accordingly. For an override, check whether the user passed an explicit argument (`/review backend`, `/review frontend`, `/review both`) — if so, skip classification and go directly to Step 2.

### Classification Heuristics

Score each changed file against the two path sets below. A file matches **backend** or **frontend** (or both) based on its extension and directory.

#### Backend signals

| Pattern | Examples |
|---------|----------|
| Server-side extensions | `*.go`, `*.py`, `*.rb`, `*.php`, `*.java`, `*.kt`, `*.rs`, `*.ex`, `*.exs`, `*.cs` |
| Server directories | `app/Http/`, `app/Models/`, `app/Services/`, `app/Repositories/`, `app/Jobs/`, `app/Events/`, `app/Listeners/`, `app/Console/` |
| Database | `database/migrations/`, `database/seeders/`, `db/migrate/`, `alembic/`, `prisma/migrations/` |
| API/config | `routes/api.*`, `config/`, `src/routes/`, `src/controllers/`, `src/services/`, `src/repositories/` |
| Infrastructure | `docker-compose.yml`, `Dockerfile`, `*.tf`, `.env.example` |

#### Frontend signals

| Pattern | Examples |
|---------|----------|
| Component extensions | `*.tsx`, `*.jsx`, `*.vue`, `*.svelte` |
| Style files | `*.css`, `*.scss`, `*.sass`, `*.less`, `*.module.css` |
| Frontend directories | `src/components/`, `src/pages/`, `src/views/`, `src/app/` (Next.js), `src/hooks/`, `src/context/`, `src/store/`, `resources/js/`, `resources/css/`, `resources/views/` |
| Assets | `public/`, `assets/`, `static/` |
| Frontend config | `vite.config.*`, `next.config.*`, `nuxt.config.*`, `tailwind.config.*` |

#### Shared / ambiguous files

Files like `*.ts` (non-React), `package.json`, `tsconfig.json`, or `*.json` alone do not determine the type. Count only if paired with other signals on the same side.

### Classification Result

| Condition | Result |
|-----------|--------|
| Only backend signals | `BACKEND` |
| Only frontend signals | `FRONTEND` |
| Both signals present | `BOTH` |
| No clear signal | `BOTH` (safer default — include all reviewers) |

---

## Step 2 — Route

### Result: `BACKEND`

Proceed as `backend-reviewer`. Apply all categories from `agents/backend-reviewer.md` without invoking a separate agent. State at the start of the review:

> **Review type: Backend** (classified from diff — N backend files, 0 frontend files)

### Result: `FRONTEND`

Proceed as `frontend-reviewer`. Apply all categories from `agents/frontend-reviewer.md` without invoking a separate agent. State at the start of the review:

> **Review type: Frontend** (classified from diff — 0 backend files, N frontend files)

### Result: `BOTH`

Do **not** attempt a full review alone. Output the following routing message and stop:

---

> **Review type: Full-stack** (N backend files + M frontend files detected)
>
> This PR has both backend and frontend changes. For the most thorough review, invoke the two specialist agents **in parallel** by sending both prompts in a single message:
>
> **Prompt A → backend-reviewer:**
> "Review the backend changes in this PR. Focus on: API contracts, database transactions, N+1 queries, auth/authz, background jobs, race conditions, SOLID, and security."
>
> **Prompt B → frontend-reviewer:**
> "Review the frontend changes in this PR. Focus on: component design, re-renders, accessibility, bundle size, state management, XSS, loading/error states, and type safety."
>
> Send both prompts simultaneously — they are independent and can run in parallel.

---

## Manual Override

Users can bypass classification by passing an explicit argument:

| Command | Behavior |
|---------|----------|
| `/review backend` | Skip classification → route as `BACKEND` |
| `/review frontend` | Skip classification → route as `FRONTEND` |
| `/review both` | Skip classification → output routing message for `BOTH` |

---

## Project-Specific Path Overrides

Projects with non-standard directory structures can define custom path mappings in `docs/development/code-standards.md` or `CLAUDE.md` under a `## Review Router` section:

```yaml
review-router:
  backend-paths:
    - "server/"
    - "lambda/"
  frontend-paths:
    - "web/src/"
    - "mobile/src/"
```

When this block is present, use it **instead of** the default heuristics above.
