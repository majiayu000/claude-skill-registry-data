---
name: sync-docs
layer: method
description: Analyze code changes and update relevant documentation to stay in sync. Runs automatically before /commit. Assumes docs are outdated — only updates what this change touches, never over-reaches.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write
---

# Sync Docs Skill

Ensures documentation reflects the current code changes. **Conservative for existing docs, proactive for new features** — updates what changed, creates what's missing.

## Core Philosophy

1. **Assume docs are outdated** — don't trust them, verify against source code
2. **Only update what this change touches** — if you changed a composable, update its entry in CLAUDE.md. Don't rewrite the whole file.
3. **Create CLAUDE.md for new packages/apps** — if a package or app directory lacks a CLAUDE.md and this change adds significant functionality, create one following the standard template.
4. **New features need documentation** — when a feature is added (new MCP tools, new API endpoints, new composables, new integrations), it MUST be documented somewhere. This is the exception to "never add sections" — new capabilities require new entries.
5. **Additions over rewrites** — prefer adding a line to a table or list over restructuring
6. **Skip if nothing to update** — config tweaks, bug fixes to internal logic, formatting changes rarely need doc changes.

## When NOT to Update Docs

- Pure bug fixes with no API/behavior change
- Internal refactors that don't change any public interface
- Dependency bumps
- Test-only changes
- Formatting/linting changes
- Changes to files that have no documentation coverage (and shouldn't)

## What to Check

### 0. Missing CLAUDE.md (CREATE if needed)

**When to create a new CLAUDE.md:**
- A new package was added to `packages/*/` and has no CLAUDE.md
- An app in `apps/*/` gained significant new functionality (MCP tools, integrations, custom server APIs) and has no CLAUDE.md
- A new layer was added with its own composables, components, or API endpoints

**Template for new CLAUDE.md:**
```markdown
# CLAUDE.md - {package-or-app-name}

## Purpose
{One paragraph describing what this does}

## Key Files
| File | Purpose |
|------|---------|
| ... | ... |

## API Endpoints (if applicable)
| Path | Method | Purpose |
|------|--------|---------|

## Common Tasks
{How to use, test, develop}
```

Don't over-document — start minimal, cover what an AI agent needs to use this package effectively.

### 1. Package & App CLAUDE.md Files

Each package in `packages/*/CLAUDE.md` and app in `apps/*/CLAUDE.md` documents its components, composables, server utils, types, and patterns.

**When to update:**
- Added/removed/renamed a component → update "Key Components" or similar section
- Added/removed/renamed a composable → update "Key Composables" section
- Changed a composable's return value or parameters → update its documentation
- Added/removed/renamed an API endpoint → update "API Endpoints" section
- Changed a component's props/emits significantly → update component docs
- Added a new export → add it to the relevant section
- **Added new MCP tools** → update or create MCP section with tool names, inputs, descriptions
- **Added new integrations** (CLI, external services) → add integration section
- **Added new server API routes** → add to API endpoints table

**How to update:**
- Read the existing CLAUDE.md for the package/app
- Find the relevant section (components, composables, API, etc.)
- Add/update/remove the specific entry
- Match the existing format exactly — don't restructure
- If the section doesn't exist and the new feature warrants it, add a new section at the appropriate location

### 2. Root CLAUDE.md

Only update if:
- A new package was added (add to scopes list)
- A critical gotcha was discovered (add to gotchas section)
- A dev command changed (update commands section)
- Architecture changed fundamentally
- A new skill/agent was added (add to artifacts table)

### 3. Docs App Content (`docs/content/`)

**When to update existing pages:**
- The change directly contradicts what a docs page says
- A documented API endpoint changed its contract
- A documented component changed its usage pattern
- A field type was added/removed from the generator

**When to create new pages:**
- A major feature was added that users need to know about (e.g., MCP integration, new dispatch service, new CLI command)
- A new package was released that needs user-facing documentation
- Use existing pages as templates — match the structure and tone

**How to find relevant docs pages:**
- Search `docs/content/` for the name of the changed component/composable/endpoint
- If a docs page references it, check if the reference is still accurate
- Only fix inaccuracies in existing pages — don't expand or improve unrelated sections

### 4. Skills and Commands (`.claude/skills/`, `.claude/commands/`)

Only update if:
- The change affects a workflow that a skill describes
- A CLI command changed that a skill references
- A file path changed that a skill uses
- A new feature was added that an existing skill should know about

**Added / changed / removed a skill** (anything under `.claude/skills/`) → regenerate the
skills overview HTML: `node scripts/gen-skills-doc.mjs`. For a brand-new skill, also add it
to that script's `META` map (group + trigger) or it lands under "Uncategorised". CI
(`skills-doc.yml`) fails if the HTML is stale.

## Workflow

### Step 1: Identify What Changed

Run in parallel:
- `git diff --name-only` — list changed files
- `git diff --cached --name-only` — list staged files
- `git diff --stat` — summary of changes

### Step 2: Categorize Changes

For each changed file, determine:
- **Package**: which `packages/*/` does it belong to?
- **Type**: component, composable, server util, type, config, other?
- **Impact**: public API change, internal change, or cosmetic?

Only proceed with files that have **public API impact**.

### Step 3: Check Relevant Docs

For each package with public API changes:

1. **Read the package's CLAUDE.md** (if it exists)
2. **Search for references** in `docs/content/` using the changed item's name
3. **Compare** the docs against what the code now says

### Step 4: Make Targeted Updates

For each doc that needs updating:
1. Show what's changing: `Updating packages/crouton-foo/CLAUDE.md — adding useNewComposable to Key Composables`
2. Use the Edit tool to make the minimum change
3. Match existing formatting

### Step 5: Report

Summarize what was updated:

```
Docs synced:
- packages/crouton-core/CLAUDE.md: added useTeamRoles to composables list
- docs/content/8.api-reference/composables.md: updated useTeamRoles signature

No updates needed:
- 3 internal files changed (no public API impact)
```

Or if nothing needs updating:

```
No doc updates needed — changes are internal/cosmetic only.
```

## Mapping: File Change → Doc Location

| Changed File Pattern | Check This Doc |
|---------------------|----------------|
| `packages/*/app/components/*.vue` | `packages/*/CLAUDE.md` (components section) |
| `packages/*/app/composables/use*.ts` | `packages/*/CLAUDE.md` (composables section) |
| `packages/*/server/api/**` | `packages/*/CLAUDE.md` (API section) |
| `packages/*/server/utils/**` | `packages/*/CLAUDE.md` (server utils section) |
| `packages/*/types*.ts` | `packages/*/CLAUDE.md` (types section) |
| `packages/crouton-cli/**` | `.claude/skills/crouton.md`, `packages/crouton-cli/CLAUDE.md` |
| `packages/crouton-mcp*/**` | `packages/crouton-mcp*/CLAUDE.md` |
| `docs/content/**` | N/A (it IS the docs) |
| `*.nuxt.config.ts` | Package CLAUDE.md (config section, if exists) |

## Examples

### Example 1: Added a composable

Changed: `packages/crouton-core/app/composables/useTeamRoles.ts`

Action:
1. Read `packages/crouton-core/CLAUDE.md`
2. Find composables section
3. Add `useTeamRoles` entry matching existing format
4. Search `docs/content/` for "team roles" — if found, verify accuracy

### Example 2: Renamed a component

Changed: `packages/crouton-editor/app/components/EditorToolbar.vue` → `EditorActions.vue`

Action:
1. Read `packages/crouton-editor/CLAUDE.md`
2. Replace `EditorToolbar` with `EditorActions`
3. Search docs for `EditorToolbar` references and update

### Example 3: Internal bug fix

Changed: `packages/crouton-auth/server/utils/session.ts` (fixed a null check)

Action: No doc update needed — internal fix, no API change.

## Rules

1. **NEVER restructure docs** — add/edit/remove specific entries only
2. **NEVER add new sections** unless the change introduces an entirely new category
3. **NEVER update docs for internal changes** — only public API
4. **ALWAYS match existing format** — if the list uses `- `, keep using `- `
5. **ALWAYS show what you're updating** before doing it
6. **ALWAYS read the doc first** before editing it
7. **Prefer skipping over guessing** — if you're unsure whether a doc needs updating, skip it
