---
name: import
description: >-
  Import existing skills from .claude/skills/ into the Engine workspace for validation,
  packaging, and publishing. Auto-detects type, creates .meta.yaml, runs MCS-1 check.
  Use when: 'import', 'bring in', 'add existing skill', or to scan inventory.
argument-hint: "[skill-slug | --scan]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Importer

Bring existing skills into the Studio Engine pipeline for validation, packaging, and publishing.

**When to use:** You have skills in `.claude/skills/` that you want to publish via the marketplace.

**When NOT to use:** For creating new products from scratch (use `/create`). For marketplace-installed products that are already published.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Parse arguments: `$ARGUMENTS` is either a skill slug or `--scan`
2. If `--scan`: run inventory scan mode
3. If slug: run single import mode
4. Read `creator.yaml` — if missing, suggest `/onboard`
5. **Maintain creator persona**: Adapt language and depth to `profile.type` and `technical_level` throughout this skill's execution.
6. Verify `workspace/` exists
7. **Load voice identity:** Load `references/quality/engine-voice-core.md`. Every user-facing line in this skill honors the ✦ signature, three tones, and six anti-patterns.

---

## Core Instructions

### MODE 1: Single Import (`/import {slug}`)

**Step 1 — Locate source**

Check if `.claude/skills/{slug}/` exists. If not:
- "Skill `{slug}` not found in .claude/skills/. Check the name and try again."

**Step 2 — Detect product type**

Scan the directory for primary files and structural signatures. Detection is
ordered from most specific to least specific — the first match wins.

| Signature | Detected Type |
|-----------|---------------|
| CLAUDE.md + STATE.yaml + config/routing.yaml + (agents/ OR squads/ OR skills/) | **system** |
| SQUAD.md + routing.yaml + agents/*.md | **squad** |
| AGENT.md + references/cognitive-core.md (or 5-layer cognitive references) | **minds** (cognitive) |
| AGENT.md | agent |
| SKILL.md with frontmatter `context: fork` | skill (fork-bridge) |
| SKILL.md | skill |
| WORKFLOW.md | workflow |
| hooks.json + scripts/ | hooks |
| OUTPUT-STYLE.md OR file in output-styles/ | output-style |
| DESIGN-SYSTEM.md + tokens/ | design-system |
| APPLICATION.md | application |
| statusline.sh + settings-fragment.json | statusline |
| vault.yaml (and no primary file) | bundle |
| CLAUDE.md (and NOT other primary files, and NOT STATE.yaml) | claude-md |

**Detection rules:**
- The `system` signature is the most specific: requires CLAUDE.md AND STATE.yaml
  AND config/routing.yaml. A plain CLAUDE.md alone is a claude-md product.
- The `squad` signature requires BOTH routing.yaml AND an agents/ subdirectory
  with at least one .md file. A lone SQUAD.md without routing.yaml is incomplete
  and should be reported as an error, not auto-converted to agent.
- `minds` detection looks for cognitive depth references. If the agent ships
  only AGENT.md + README.md, it is a regular agent.

If multiple signatures match ambiguously, ask which type to use.
If no signature matches: "Cannot detect product type. What type is this? (skill/agent/squad/system/minds/workflow/hooks/claude-md/output-style/design-system/application/statusline/bundle)"

**Step 3 — Check for duplicates**

If `workspace/{slug}/` already exists:
- "Product `{slug}` already exists in workspace. Use `/fill` to continue or `/create --force` to reset."
- Do NOT overwrite — BLOCKING. Return immediately without copying any files.
- If `--force` flag is provided: require explicit confirmation via AskUserQuestion before overwriting. Show file count diff between source and target.

**Step 4 — Copy to workspace**

Copy the ENTIRE directory from `.claude/skills/{slug}/` to `workspace/{slug}/`.
- Preserve all subdirectories (references/, examples/, agents/, etc.)
- Do NOT modify the originals in `.claude/skills/`

**Step 5 — Create .meta.yaml**

```yaml
product:
  slug: "{slug}"
  type: "{detected-type}"
  created: "{today YYYY-MM-DD}"
  mcs_target: "{from creator.yaml quality_target or MCS-2}"

state:
  phase: "{auto-detected phase}"
  last_validated: null
  last_validation_score: null
  dna_compliance:
    tier1: null
    tier2: null
    tier3: null
  overall_score: null

history:
  created_at: "{today YYYY-MM-DD}"
  validated_at: []
  packaged_at: null
  published_at: null
  version: "1.0.0"
```

**Step 6 — Auto-detect phase**

Analyze the imported content to determine current phase:

| Condition | Phase |
|-----------|-------|
| Primary file < 50 lines OR > 50% placeholder patterns (TODO, PLACEHOLDER, etc.) | scaffold |
| Real content + at least 1 reference file | content |
| Passes MCS-1 structural check + README.md with 4 required sections | validated |

**Step 7 — Quick MCS-1 check**

Run a lightweight structural validation (Stage 1 only):
- Required files exist for the product type?
- README.md present with what/install/usage/requirements?
- Primary file has frontmatter with name + description?

Report the result but do NOT block import on failure.

**Step 8 — Report**

```
Imported: {slug}
  Type:    {detected-type}
  Phase:   {auto-detected phase}
  Files:   {N} files copied
  MCS-1:   {PASS|FAIL} ({details})

  Next: /validate for full quality check
        /package when ready to publish
```

---

### MODE 2: Inventory Scan (`/import --scan`)

**Step 1 — Scan .claude/skills/**

List ALL directories in `.claude/skills/`. For each:
1. Detect product type (same logic as single import)
2. Check if already in `workspace/` (skip if yes)
3. Check file count and primary file line count
4. Flag marketplace-installed products (if detectable — e.g., has marketplace_url in frontmatter)

**Step 2 — Present inventory**

```
Inventory Scan: .claude/skills/

  IMPORTABLE ({N}):
  | Slug | Type | Files | Lines | Status |
  |------|------|-------|-------|--------|
  | aegis | skill | 10 | 368 | ready |
  | kairo-skill | skill | 8 | 89 | ready |
  | premium-lp | skill | 4 | 305 | ready |
  ...

  ALREADY IN WORKSPACE ({N}):
  | aegis | skill | workspace/aegis/ exists |
  ...

  MARKETPLACE PRODUCTS ({N}):
  | pdf | skill | marketplace_url detected |
  ...

  Import all {N} importable? [Y/n/select]
```

**Step 3 — Handle response**

- "Y" or "yes": import all importable skills sequentially
- "n" or "no": cancel
- "select": present numbered list, accept comma-separated numbers
- For batch import: run single import for each, collect results, report summary

**Step 4 — Batch report**

```
Import complete: {imported}/{total} skills

  Imported:
  ✓ aegis (skill, content, MCS-1 PASS)
  ✓ kairo-skill (skill, content, MCS-1 PASS)
  ✗ some-skill (skill, scaffold, MCS-1 FAIL: no README)

  Skipped: {N} (already in workspace or marketplace products)

  Next: /validate --batch to check all imported products
```

---

## Anti-Patterns

1. **Modifying originals** — NEVER touch files in .claude/skills/. Copy only.
2. **Overwriting workspace** — If workspace/{slug}/ exists, do NOT overwrite without --force.
3. **Importing marketplace products** — Products installed from myclaude.sh should not be re-imported for publishing (they belong to another author).
4. **Skipping .meta.yaml** — Every imported product MUST have .meta.yaml for the state machine to work.
5. **Assuming MCS-1 pass** — Report the check result honestly. Many existing skills will fail structural checks.

---

## Quality Gate

Before completing any import:
- [ ] Original files in .claude/skills/ are UNTOUCHED
- [ ] workspace/{slug}/ contains all copied files
- [ ] .meta.yaml exists with correct type and auto-detected phase
- [ ] MCS-1 structural check was run and result reported
- [ ] No duplicate imports (workspace/{slug}/ didn't already exist)
