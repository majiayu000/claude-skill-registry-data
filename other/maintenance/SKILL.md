---
name: maintenance
description: Documentation self-maintenance rules. Auto-applied after any code change to ensure docs, skills, and feature lists stay in sync with the codebase.
user-invocable: false
---

# Documentation Self-Maintenance

After EVERY code change, check and update affected documentation. Treat documentation as code — it ships with the commit.

## Documentation Registry

These are the living documents that must stay in sync with the codebase:

| File | Purpose | When to Update |
|------|---------|----------------|
| `CLAUDE.md` | Project overview, structure map, skills reference | New directories, new skills, tech stack changes |
| `docs/feature-list.md` | Master list of all user-facing features (currently 160) | Any new feature added or existing feature removed |
| `docs/tabs.md` | Tab groups, sub-tabs, panel organization | Any tab added, removed, renamed, or reorganized |
| `docs/PROGRESS.md` | Session progress and pending items | Features completed, bugs fixed, new pending items |
| `.claude/skills/*/SKILL.md` | Skill-specific workflows | Referenced files moved/renamed, APIs changed, new steps added |
| `.claude/skills/architecture/SKILL.md` | Project architecture | New directories, new architectural patterns, tech stack changes |
| `.claude/skills/patterns/SKILL.md` | Coding conventions | New patterns adopted, naming conventions changed |
| `docs/codebase/*.md` | Per-section API reference (functions, stores, components) | Any function/store/component/hook added, removed, or renamed |

## Update Rules by Change Type

### 1. New Feature Added
```
docs/feature-list.md    → Add numbered entry (increment count in header)
docs/tabs.md            → Add tab entry if feature has a panel
CLAUDE.md               → Update Project Structure if new directory created
Relevant skill SKILL.md → Update Key Files or Steps if skill covers this area
```

### 2. New Panel/Tab Created
```
docs/tabs.md            → Add to correct group with id, label, icon, description
docs/feature-list.md    → Add feature entry if not already listed
```

### 3. New Store/Service/Component Created
```
CLAUDE.md               → Only if it creates a new directory pattern
Architecture SKILL.md   → If it introduces a new architectural concept
Patterns SKILL.md       → If it establishes a new coding pattern
```

### 4. Feature Modified or Refactored
```
Relevant skill SKILL.md → Update steps, file paths, function names
docs/feature-list.md    → Update description if behavior changed
```

### 5. File Moved or Renamed
```
ALL skills that reference the old path → Update file paths
CLAUDE.md               → Update Project Structure if directory changed
```

### 6. Bug Fixed
```
docs/PROGRESS.md        → Add to completed section with fix description
```

### 7. New Skill Created
```
CLAUDE.md               → Add to Skills Reference table in correct category
```

### 8. Tab Reorganized
```
docs/tabs.md            → Reflect new group structure
```

## How to Update `docs/feature-list.md`

- Entries are numbered: `1. **Feature Name** — One-line description`
- Keep the count in the header accurate: `160 user-facing features.`
- Group by area (characters, rigging, audio, AI, canvas, export, etc.)
- One line per feature, bold name, em-dash, description

## How to Update `docs/tabs.md`

- Format: `- \`tab-id\` — Label — Description`
- Grouped under numbered sections matching `tabGroups.ts` group IDs
- Include sub-tab count per group in the heading

## Stale Reference Detection (MANDATORY)

After ANY code change — even small ones — run a stale reference scan before committing. This catches renamed functions, moved files, changed parameters, and modified store interfaces that docs still reference by the old name.

### Step 1: Identify what changed

Look at the files you modified. Extract the key identifiers: file names, exported function names, store names, type names, interface properties, API endpoints.

### Step 2: Grep docs for stale references

For each changed/renamed/removed identifier, search ALL documentation:

```bash
# Search all skills and docs for references to a changed file or function
rg "oldFunctionName\|oldFileName\|oldStoreName" .claude/skills/ docs/ CLAUDE.md
```

Run this for:
- **Renamed files**: `rg "oldFileName" .claude/skills/ docs/ CLAUDE.md`
- **Renamed functions/exports**: `rg "oldFunctionName" .claude/skills/ docs/`
- **Changed store interfaces** (added/removed/renamed fields): `rg "useXxxStore" .claude/skills/`
- **Changed API endpoints**: `rg "/api/old-endpoint" .claude/skills/ docs/`
- **Renamed types/interfaces**: `rg "OldTypeName" .claude/skills/`

### Step 3: Update every hit

Every grep result is a stale reference that MUST be updated. No exceptions.

### Examples of small changes that need doc updates

| Change | What goes stale |
|--------|----------------|
| Rename `silenceDetection.ts` → `silenceDetector.ts` | `smart-cut/SKILL.md` references old filename |
| Rename `processAlignment()` → `convertAlignment()` | `generate-voice/SKILL.md` references old function |
| Add `threshold` param to `detectSilence()` | `smart-cut/SKILL.md` missing new parameter |
| Change store field `items` → `elements` | Any skill referencing `store.items` |
| Move `src/services/foo.ts` → `src/services/audio/foo.ts` | All skills referencing old path |
| Remove an export from a service | Skills that tell Claude to use that export |
| Change API route `/api/whisper` → `/api/transcribe` | `transcript-edit/SKILL.md`, architecture skill |
| Rename tab ID `voice-clone` → `clone-voice` | `docs/tabs.md`, `add-panel/SKILL.md` |

### When NOT to scan

Skip the scan only if your change is:
- Purely internal logic (no renamed exports, files, types, or interfaces)
- CSS/styling only
- Console.log additions/removals
- Comment changes

If in doubt, scan. It takes 2 seconds and catches real problems.

## Commit Pattern

Always include doc updates in the SAME commit as the code change:
```bash
git add src/services/newFeature.ts src/stores/useNewFeatureStore.ts docs/feature-list.md docs/tabs.md
git commit -m "Add new feature X with panel and store"
```

Never make a separate "update docs" commit after a code change.

## Verification Checklist

Before committing, run through:
- [ ] **Stale reference scan done?** → `rg "changedIdentifier" .claude/skills/ docs/ CLAUDE.md`
- [ ] Did I add a new feature? → `docs/feature-list.md` updated?
- [ ] Did I add a new panel/tab? → `docs/tabs.md` updated?
- [ ] Did I change files referenced by a skill? → Skill SKILL.md updated?
- [ ] Did I fix a bug or complete a pending item? → `docs/PROGRESS.md` updated?
- [ ] Did I create a new skill? → `CLAUDE.md` Skills Reference updated?
- [ ] Did I change project structure? → `CLAUDE.md` Project Structure updated?
