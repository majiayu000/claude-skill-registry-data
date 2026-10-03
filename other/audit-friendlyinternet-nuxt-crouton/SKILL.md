---
name: audit
layer: method
description: Audit packages for documentation completeness, detect drift between code and docs, and maintain documentation quality across the monorepo. Use when checking package docs, running audits, or reviewing documentation health.
argument-hint: "[package-name | --all | --docs-health | --docs-verify [section]]"
allowed-tools: Bash, Read, Grep, Glob
---

# Package Audit Skill

Audit packages for documentation completeness, detect drift, and maintain docs quality.

## Critical Principle: Defensive & Human-First

**AI makes mistakes. Human choices always win.**

### Trust Hierarchy

```
1. Human-written content     → PRESERVE, never auto-overwrite
2. Human-approved AI content → Trust, but flag if conflicts
3. AI-generated suggestions  → SUSPECT, always require confirmation
```

### Rules for This Skill

1. **Never auto-overwrite** - Always show what will change, ask for confirmation
2. **Flag, don't fix** - When docs differ from code, present BOTH options
3. **Assume AI mistakes** - Your analysis might be wrong, offer "skip" always
4. **Preserve human content** - Even if it seems outdated, ask before changing
5. **Show diffs** - Never just say "I updated X", show exactly what changed

### When in Doubt

```
I found a potential issue, but I might be wrong:

CLAUDE.md says: "CroutonEditor accepts 5 props"
I found in source: 7 props defined

This could mean:
- Docs are outdated (likely)
- 2 props are internal/undocumented (intentional)
- I misread the source code (possible)

What would you like to do?
1. Show me the details so I can decide
2. Update docs to show all 7 props
3. Skip - the docs are correct as-is
4. Add a TODO comment for later review
```

## Prerequisites

The `@fyit/crouton-ci` package must be built and available. If not, fall back to manual analysis.

## Commands

### Single Package Audit

```bash
/audit <package-name>
```

Example: `/audit crouton-editor`

### Full Monorepo Audit

```bash
/audit --all
```

### Docs Folder Health Check

```bash
/audit --docs-health
```

### Docs Verification (verify docs claims against source code)

```bash
/audit --docs-verify              # Verify all docs sections
/audit --docs-verify features     # Verify only features section
/audit --docs-verify api          # Verify only API reference section
```

## Workflow: Single Package

### Step 1: Run Analysis

```bash
pnpm crouton-ci audit <package> --json
```

If crouton-ci is not available, manually analyze:
1. Read all files in `packages/<package>/`
2. Extract components from `app/components/`
3. Extract composables from `app/composables/`
4. Extract server utils from `server/`
5. Read existing CLAUDE.md and README.md

### Step 2: Present Findings

Format results clearly:

```
## Audit: crouton-editor

**Package Info**
- Type: addon (Nuxt Layer)
- Files: 12
- Maturity: stable

**Exports Found**
- Components: 5
- Composables: 1
- Server Utils: 0
- Types: 2

**Documentation Status**
- CLAUDE.md: 95% coverage
- README.md: exists
- apps/docs: may need update

**Issues**
1. CroutonEditorToolbar not documented in CLAUDE.md
2. Package reference "@friendlyinternet/..." is outdated
```

### Step 3: Offer Fixes

Ask the user:
> Would you like me to fix these issues?
> 1. Add missing exports to CLAUDE.md
> 2. Update outdated package references
> 3. Both

### Step 4: Execute Fixes

If user approves:

1. **For missing documentation:**
   - Read the source file
   - Extract props/emits for components
   - Extract return values for composables
   - Add section to CLAUDE.md following existing format

2. **For outdated references:**
   - Find and replace old package names with current ones

### Step 5: Verify

```bash
npx nuxt typecheck
```

### Step 6: Suggest Commit

```
docs(<package>): update documentation

- Add missing exports to CLAUDE.md
- Update package references to @fyit scope
- Coverage: X% → Y%
```

## Workflow: Full Audit

### Step 1: Run Full Analysis

```bash
pnpm crouton-ci audit --all --json
```

### Step 2: Summarize

```
## Monorepo Audit Summary

**Packages Analyzed**: 21

**By Coverage**
- 90%+: 8 packages
- 70-89%: 10 packages
- <70%: 3 packages

**Packages Needing Attention**
1. crouton-maps (45%) - missing 3 components
2. crouton-admin (62%) - missing 5 composables
3. crouton-collab (68%) - missing README

Would you like to audit a specific package?
```

### Step 3: Iterate

Let user pick packages to fix one by one.

## Workflow: Docs Health

### Step 1: Analyze /docs

```bash
pnpm crouton-ci docs-health --json
```

Or manually check:
- `docs/upcoming/` - Plans in progress
- `docs/briefings/` - Feature briefs
- `docs/projects/` - Larger initiatives
- `docs/completed/` - Archived items

### Step 2: Detect Status

For each file, check:
1. **Likely done**: Feature mentioned exists in code
2. **Active**: Recent modifications, clear "in progress" markers
3. **Stale**: No updates in 60+ days, no related commits
4. **Unknown**: Can't determine status

### Step 3: Present Findings

```
## /docs Health Check

**upcoming/** (6 files)
- PLAN-package-rename-fyit.md — Active
- PLAN-keyboard-shortcuts.md — Likely done
  → useCroutonShortcuts exists
- PLAN-playground.md — Unknown

**Suggestions**
- Move 2 files to completed/
- Triage 3 files with unknown status

Would you like me to help triage the unknown files?
```

### Step 4: Triage Unknown Files

For each unknown file:
1. Read the file content
2. Search codebase for related features
3. Ask user: "Is this complete, in progress, or abandoned?"
4. Move to appropriate folder or add status marker

## Manual Analysis Fallback

If crouton-ci is not available, use these patterns:

### Extract Components

```bash
# Find all Vue components
find packages/<pkg>/app/components -name "*.vue" 2>/dev/null
```

### Extract Composables

```bash
# Find all composables
find packages/<pkg>/app/composables -name "use*.ts" 2>/dev/null
```

### Check Documentation

```bash
# Check if CLAUDE.md exists and search for component names
grep -l "ComponentName" packages/<pkg>/CLAUDE.md
```

## Workflow: Docs Verification (`--docs-verify`)

Verifies that claims in `apps/docs/content/` are still accurate by checking them against actual source code. This is the main tool for catching silently outdated documentation.

### Philosophy

- **Docs make claims. Code is truth.** Every component name, prop, composable signature, config key, and API endpoint in a docs page is a testable assertion.
- **Flag, don't fix.** Produce a report. Let the user decide what to fix, delete, or leave.
- **False positives are OK.** Better to flag something that's fine than miss something that's wrong. The user filters.

### Sections

Docs are organized under `apps/docs/content/`:

| Section | Path | Approx pages |
|---------|------|-------------|
| features | `6.features/*.md` | ~15 |
| api | `8.api-reference/**/*.md` | ~15 |
| generation | `3.generation/*.md` | ~5 |
| patterns | `4.patterns/*.md` | ~5 |
| customization | `5.customization/*.md` | ~3 |
| advanced | `7.advanced/*.md` | ~3 |
| getting-started | `1.getting-started/*.md` | ~3 |
| fundamentals | `2.fundamentals/*.md` | ~3 |
| guides | `10.guides/*.md` | ~3 |

### Step 1: Discover docs pages

List all `.md` files in the target section (or all sections if `--docs-verify` with no argument).

Group pages into batches of 2-3 for parallel agent processing.

### Step 2: Launch parallel verification agents

**CRITICAL**: Launch ALL agents in a single message. Each agent gets 2-3 docs pages.

Each agent receives this prompt (adapt file paths):

```
Verify these documentation pages against the actual source code.

For EACH page, read the docs page first, then verify every claim against source code.

## What to verify

### Component Claims
For each component mentioned (e.g., `CroutonEditorSimple`):
1. Search `packages/*/app/components/` — does it exist?
2. If yes, check: are the documented props still correct? (read the component's `defineProps`)
3. Are documented events/emits still correct? (check `defineEmits`)
4. Are documented slots still there?

### Composable Claims
For each composable mentioned (e.g., `useEntityTranslations()`):
1. Search `packages/*/app/composables/` — does it exist?
2. If yes, check: does the signature match? (read the function parameters)
3. Does the return value match what docs describe?

### API Endpoint Claims
For each endpoint mentioned (e.g., `POST /api/upload-image`):
1. Search `packages/*/server/api/` — does the route file exist?
2. If yes, check: does it accept the documented params/body?
3. Is the HTTP method correct?

### Config Claims
For each config option (e.g., `hub: { blob: true }`):
1. Search for where it's consumed in `nuxt.config.ts` or module setup
2. Is the key name correct? Are the documented values valid?

### Code Examples
For each code example in the docs:
1. Do the imports reference real exports?
2. Do the component/composable names match what exists?
3. Are the props/options used in examples still valid?

### Package Claims
For package names, versions, install commands:
1. Check `package.json` — is the package name correct?
2. Is the install command using the right scope (@fyit)?

## Output format (use exactly this structure)

## [Page Title] (`path/to/file.md`)

### Verified ✅
- Component `CroutonFoo` exists with documented props
- Composable `useFoo()` signature matches
- ...

### Broken ❌
- Component `CroutonBar` — RENAMED to `CroutonBaz` (found at packages/x/app/components/Baz.vue)
- Prop `toolbar` on CroutonEditor — REMOVED, now called `tools`
- Endpoint `POST /api/upload-image` — MOVED to `POST /api/teams/[id]/assets`
- Composable `useFoo()` — parameter `options` removed, now takes 2 positional args
- ...

### Suspicious ⚠️ (couldn't fully verify)
- Config key `retentionDays` — couldn't find where it's consumed
- Code example imports `@fyit/crouton-editor/utils` — path not found but might be auto-imported
- ...

### Missing from docs (exists in code but not documented)
- Component `CroutonEditorActions` exists but not mentioned
- Composable `useEditorState()` exported but not documented
- ...
```

### Step 3: Compile verification report

After ALL agents complete, compile into a single report.

Save to: `docs/reports/docs-verification-{YYYYMMDD}.md`

Report structure:

```markdown
# Documentation Verification Report
Date: {date}
Pages verified: X
Scope: {section or "all"}

## Summary

| Status | Count |
|--------|-------|
| ✅ Verified claims | X |
| ❌ Broken claims | Y |
| ⚠️ Suspicious | Z |
| 📝 Missing from docs | W |

## Pages by Health

### 🔴 Needs Rewrite (>50% broken claims)
- 6.features/7.rich-text.md — 8/15 claims broken

### 🟡 Needs Fixes (1-50% broken)
- 6.features/9.assets.md — 3/20 claims broken

### 🟢 Healthy (<5% issues)
- 6.features/1.i18n.md — 1 suspicious, 0 broken

## Detailed Findings

### 6.features/7.rich-text.md
[full agent output here]

### 6.features/9.assets.md
[full agent output here]
...

## Recommended Actions

### Delete (page describes feature that no longer exists)
- ...

### Rewrite (too many broken claims to patch)
- ...

### Fix (specific claims to update)
- 6.features/9.assets.md: update 3 endpoint paths
- ...

### Leave (healthy or cosmetic issues only)
- ...
```

### Step 4: Present to user

Show the summary table and the "Recommended Actions" section inline. Tell the user the full report was saved and offer to fix specific pages.

**Do NOT auto-fix.** This is a verification tool, not a fixer. The user decides what to do with each finding.

### Step 5 (optional): Fix a specific page

If user says "fix X", then:
1. Read the full findings for that page from the report
2. Read the source docs page
3. For each broken claim, find the correct current value from source code
4. Show a diff of proposed changes
5. Apply only after user confirms

### Agent Batching Guide

For `--docs-verify` (all sections), group into ~6 agents:

| Agent | Pages |
|-------|-------|
| A | `6.features/1.i18n.md`, `6.features/6.rich-text.md`, `6.features/7.assets.md` |
| B | `6.features/9.events.md`, `6.features/10.maps.md`, `6.features/11.devtools.md` |
| C | `6.features/12.flow.md`, `6.features/13.ai.md`, `6.features/14.admin.md` |
| D | `6.features/15.export.md`, `6.features/16.email.md`, `6.features/17.pages.md`, `6.features/18.bookings.md`, `6.features/19.sales.md`, `6.features/20.collaboration.md` |
| E | `8.api-reference/**` (all API ref pages) |
| F | `3.generation/*.md`, `4.patterns/*.md`, `5.customization/*.md` |

Adjust based on actual files found. Each agent should handle no more than 5 pages.

For single-section verify (e.g., `--docs-verify features`), use 2-3 agents covering just that section.

## Related Files

- Plan: `docs/active/PLAN-crouton-ci.md`
- CLI Package: `packages/crouton-ci/` (when built)
- Existing sync-check: `.claude/commands/sync-check.md`
- Sync docs skill: `.claude/skills/sync-docs/SKILL.md`