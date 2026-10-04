---
name: plan
description: Explore the codebase and produce an implementation plan. Use when the user runs /plan or wants a plan before building.
---

# /plan — Explore + Create Implementation Plan

Explores the codebase and produces a structured implementation plan. Optionally materializes Beads tasks.

## Usage
```
/plan add user settings page
/plan T-42                     # Plan for an existing task
/plan refactor auth module --tasks   # Also create Beads tasks from the plan
```

---

## Step 1 — Load Knowledge (mandatory)

Before any code exploration, load the relevant knowledge files:

```bash
cat knowledge/_shared.yaml
cat knowledge/repos/<repo>.yaml      # For each affected repo
```

If knowledge files are missing or stale (>50 commits behind HEAD):
- Warn: "knowledge/<repo>.yaml may be stale — consider running /sync-knowledge <repo>"
- Proceed anyway with a note that exploration results may supersede stale knowledge

---

## Step 1b — Planner mode *(short or vague prompts)*

If the user input is **only one to four sentences** with **no** Beads task id and **no** detailed spec:

1. Read `.claude/agents/planner.md` and adopt the **Planner** role **before** deep exploration.
2. Expand the prompt into a **product spec** (overview, numbered features / user stories, **non-goals**, testable signals). Save to `plans/drafts/<slug>-product-spec.md`.
3. Use that spec as the source of truth for exploration in Step 3 and the implementation plan in Step 4.

If the user already provided a detailed spec or `bd show` task context, skip this step.

---

## Step 2 — Reuse Verification

Search for existing implementations before planning anything new:

```bash
# Hooks
grep -rE "^export function use" src/ --include="*.ts" --include="*.tsx" -l

# Types and interfaces
grep -rE "^export (interface|type)" src/ --include="*.ts" -l

# Components
grep -rE "^export (default|function|const)" src/components/ --include="*.tsx" -l

# Utilities
grep -rE "^export (function|const|class)" src/utils/ --include="*.ts" -l
```

Note any existing implementations relevant to the plan.

---

## Step 3 — Explore

Use an Explore subagent (or explore directly) to map the codebase:

For small scope (single feature area):
- Read 5-10 key files relevant to the task
- Trace the data flow from entry point to the affected code

For large scope (cross-cutting concern):
- Spawn an Explore agent: "Explore <repo> and map all files related to <topic>. Focus on: <areas>. Report file paths, key functions, and integration points."
- Read the agent's findings, then read the specific files it identifies

**Goal**: understand the codebase well enough to write a complete, accurate plan with real file paths and function names.

---

## Step 4 — Write Plan

Write to `plans/drafts/<TASK-ID>.md` (create `plans/drafts/` if needed).
If no task ID: use a slug from the description.

### Plan format:

```markdown
# Plan: <TASK-ID> — <title>
Generated: <date>
Repo: <repo>

## Summary
<~100 tokens: what is being built, why, and the approach in plain language>

## Existing Code to Reuse
- `src/hooks/useAuth.ts` — auth state hook, extend it for settings
- `src/types/user.ts` — UserProfile type already has the needed fields

## Implementation Steps
1. Add settings schema to `src/types/user.ts`
   - Extend `UserProfile` with `settings: UserSettings`
   - Define `UserSettings` interface

2. Create `src/api/settings.ts`
   - `getSettings(userId: string): Promise<UserSettings>`
   - `updateSettings(userId: string, patch: Partial<UserSettings>): Promise<void>`

3. Create `src/hooks/useUserSettings.ts`
   - Wraps `getSettings` / `updateSettings`
   - Returns `{ settings, loading, error, update }`

4. Create `src/components/UserSettingsPage.tsx`
   - Form bound to `useUserSettings`
   - Save/cancel buttons, loading state, error display

5. Add route in `src/App.tsx`
   - `/settings` → `<UserSettingsPage />`

## Files to Modify
| File | Change |
|------|--------|
| `src/types/user.ts` | Add UserSettings interface |
| `src/App.tsx` | Add /settings route |

## Files to Create
| File | Purpose |
|------|---------|
| `src/api/settings.ts` | Settings API calls |
| `src/hooks/useUserSettings.ts` | Settings state hook |
| `src/components/UserSettingsPage.tsx` | Settings UI |
| `src/api/settings.test.ts` | API unit tests |
| `src/hooks/useUserSettings.test.ts` | Hook unit tests |

## Test Strategy
- Unit: `useUserSettings` — loading state, error state, successful update
- Unit: `settings.ts` API — mock fetch, verify request format
- Integration: settings page saves and persists across page refresh
- Edge: empty settings object, network error, validation failure

## Validation Commands
\`\`\`bash
bun run typecheck
bun test src/api/settings.test.ts
bun test src/hooks/useUserSettings.test.ts
\`\`\`

## Estimated Scope
- Files: 5 new, 2 modified
- Complexity: Medium
- Estimated time: 90 minutes

## Interfaces (if this plan produces shared APIs)
\`\`\`typescript
export function useUserSettings(userId: string): {
  settings: UserSettings | null;
  loading: boolean;
  error: Error | null;
  update: (patch: Partial<UserSettings>) => Promise<void>;
}
\`\`\`
```

---

## Step 5 — Present Plan

Output a summary to the user:
```
Plan ready: plans/drafts/<TASK-ID>.md

Summary: <2-sentence description>
Scope: <n> files (<n> new, <n> modified), ~<n> minutes
Complexity: Low | Medium | High

Key decisions:
- <decision 1 and why>
- <decision 2 and why>
```

---

## Step 6 — Materialize Beads *(with `--tasks` flag only)*

If `--tasks` was passed:

For each implementation step in the plan:
```bash
bd create \
  --type task \
  --title "<step description>" \
  --repo <repo> \
  --priority <value> \
  --acceptance "<acceptance criterion from the step>"
```

Pick **`<value>`** with `.claude/skills/beads-priority-assignment/SKILL.md` (critical-path or high-risk steps → **high** / **critical**; later optional steps → **medium** / **low**).

Add sequential dependencies (step 2 requires step 1):
```bash
bd dep add <step-2-id> --requires <step-1-id>
```

If there are 4+ tasks: create a parent feature:
```bash
bd create --type feature --title "<overall feature title>" --priority <value>
# then add parent relationship to each task
```

Use the same skill for the parent feature priority (often **medium** unless the plan is release-blocking).

Report: "Created N Beads tasks. Run /go to start work."

---

## Staleness Warning

After loading knowledge files, check commit distance:
```bash
git log --oneline knowledge/repos/<repo>.yaml -- | head -1
git rev-list --count HEAD   # compare against knowledge file's last commit
```

If >50 commits behind: `⚠ knowledge/<repo>.yaml is stale (>50 commits). Run /sync-knowledge <repo>.`
