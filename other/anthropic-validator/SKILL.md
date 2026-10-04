---
name: anthropic-validator
description: Validates Claude Code assets (skills, hooks, agents, commands, MCP servers, plugins) against official Anthropic standards. Fetches latest docs dynamically and produces structured validation reports.
when_to_use: When validating Claude Code assets (skills, hooks, agents, commands, MCP servers, plugins) against official Anthropic standards before release, after creation, or when auditing for spec compliance.
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Glob
  - Read
  - Task
  - Write
version: 1.1.1
author: "Ashay Kubal @ Qball Inc."
---

# Anthropic Validator

Validates Claude Code assets against official Anthropic standards using dynamic documentation fetching and critical analysis.

---

## Overview

### The Problem

Claude Code evolves rapidly. Static checklists become outdated. Assets created months ago may violate current standards, and new features may not be reflected in embedded validation rules.

### The Solution

This skill provides **dynamic validation** by:

1. **Fetching latest standards** from official Claude Code documentation
2. **Critically analyzing** assets against those standards
3. **Producing actionable reports** with specific violations and remediation

### Design Pattern: Main Context Orchestration

This skill uses **Main Context Orchestration** — you (Claude) follow the instructions below to orchestrate sub-agents sequentially. This is required because sub-agents cannot spawn other sub-agents.

```
┌─────────────────────────────────────────────────────────────┐
│                   MAIN CONTEXT (You)                         │
│                                                             │
│  1. Load this skill (anthropic-validator)                   │
│  2. Determine asset type → load matching references file    │
│  3. Spawn claude-code-guide → fetch latest standards        │
│  4. Read output (direct response)                           │
│  5. Spawn bulwark-standards-reviewer → analyze asset        │
│  6. Read validation report from logs/validations/           │
│  7. Present summary to user                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Invocation

```bash
# Single asset validation
/anthropic-validator skills/my-skill/SKILL.md

# Batch validation (directory)
/anthropic-validator skills/

# Context inference (validates current file in context)
/anthropic-validator
```

---

## Validation Workflow

### Step 0: Resolve Target Asset

**IMPORTANT**: When this skill is invoked, first resolve what to validate:

```
IF $ARGUMENTS is provided (e.g., /anthropic-validator path/to/file):
    target_path = $1

    IF target_path ends with "/" OR is a directory:
        mode = "batch"
        → Skip to "Batch Validation" section below
    ELSE:
        mode = "single"
        → Continue with Step 1 for single-file validation

ELSE (no arguments, context inference):
    Look for Claude Code assets in recent conversation context
    IF found: validate that asset (single mode)
    ELSE: Ask user what to validate
```

**Argument Reference:**
- `$ARGUMENTS` — Full argument string passed to skill
- `$1` — First positional argument (the path)

**Workflow Routing:**
- Single file → Continue with Steps 1-4 below
- Directory (batch) → Jump to "Batch Validation" section

### Step 1: Determine Asset Type & Load Per-Type Reference

For the resolved `target_path`, match against these patterns and **load the corresponding `references/{type}-validation.md` file** for asset-specific workflow + validation points:

| Path Pattern | Asset Type | Reference File |
|--------------|------------|----------------|
| `skills/*/SKILL.md` | Skill | `references/skills-validation.md` |
| `hooks/hooks.json` or `*.hooks.json` | Hooks | `references/hooks-validation.md` |
| `agents/*.md` or `.claude/agents/*.md` | Agent | `references/agents-validation.md` |
| `commands/*.md` | Command | `references/commands-validation.md` |
| `mcp/` or `*-mcp-server*` | MCP Server | `references/mcp-validation.md` |
| `.claude-plugin/plugin.json` | Plugin | `references/plugins-validation.md` |

The loaded reference file provides:
- The official documentation URL for the asset type
- Asset-type-specific validation workflow steps
- Key validation points (frontmatter fields, required structure, etc.)
- Fallback checklist pointer (used if doc fetch fails — see Fallback Behavior section)

### Step 2: Fetch Latest Standards

Spawn `claude-code-guide` agent with the documentation URL from the loaded references file:

```
GOAL: Fetch current standards for {asset_type} from official Claude Code docs

CONSTRAINTS:
- Only use official Anthropic documentation
- Report what IS supported vs what is NOT
- Include any recent changes or deprecations

CONTEXT:
- Documentation URL: {URL from references/{type}-validation.md}
- Capability being validated: {asset_type}

OUTPUT:
- Current supported fields/features
- Required vs optional elements
- Common pitfalls or mistakes
- Any version-specific notes
```

### Step 2.5: Gather Supporting Files (Skills Only)

**Scope**: This step applies ONLY to `asset_type == "skill"`. Non-skill validations (agents, commands, MCP, plugins, hooks) MUST skip this step and proceed directly to Step 3 with `supporting_files = null` in the CONTEXT block.

For skills, check for supporting subdirectories and files:

```
IF asset_type == "skill":
    1. Check for references/ subdirectory
       - List all files if present
       - Note: references/ is OPTIONAL (not all skills have it)

    2. Check for other common subdirectories
       - examples/, scripts/, templates/, data/
       - List files if present

    3. Scan SKILL.md for file references
       - Look for patterns: `references/*.md`, `examples/*`, etc.
       - Verify referenced files exist

    4. Build supporting_files inventory:
       supporting_files = {
         references: [list of files or "none"],
         examples: [list of files or "none"],
         scripts: [list of files or "none"],
         referenced_but_missing: [any files mentioned but not found]
       }
```

### Step 3: Critical Analysis

Spawn `bulwark-standards-reviewer` agent (Task tool with `subagent_type: bulwark-standards-reviewer`):

```
GOAL: Critically analyze {asset_path} against fetched standards

CONSTRAINTS:
- Be thorough — check every requirement
- Rate findings by severity (Critical/High/Medium/Low)
- Provide specific remediation for each finding
- Do NOT modify the asset, only report
- Only flag missing references/ if the skill explicitly references files that don't exist
- Validate tools/fields against DOCUMENTATION, not by attempting to use them
  (The reviewer may not have access to all tools — don't conflate "I can't use this" with "this is invalid")
- Apply the three-tier frontmatter field classification (see "Bulwark-Adopted Fields
  Allowlist" section below) — adopted fields are informational notes, not violations;
  unknown fields remain HIGH-severity violations.

CONTEXT:
- Asset to validate: {asset_content}
- Current standards: {fetched_standards from Step 2}
- Asset type: {asset_type}
- Per-type reference: {contents of references/{type}-validation.md from Step 1}
- Supporting files inventory: {supporting_files from Step 2.5, if skill}
- Referenced files verified: {yes/no with details}
- Bulwark-Adopted Fields Allowlist (DO NOT flag as violations — emit informational notes):
  Three frontmatter fields are intentionally adopted by Bulwark as non-Anthropic-official
  but standardized conventions. The reviewer MUST classify these as
  `bulwark_adopted_fields` notes, not as violations:
  * `version` — semver string for skill/agent traceability across releases
  * `author` — attribution string (e.g., "Ashay Kubal @ Qball Inc.")
  * `skills` — applies ONLY to skill frontmatter (`SKILL.md`); for agent frontmatter
    (`.claude/agents/*.md`), `skills:` IS Anthropic-official and should be classified
    accordingly. The Bulwark adoption is the skill-frontmatter use case.
  Any other frontmatter field not in the official Anthropic spec for the asset type
  remains an `unknown` field and MUST be reported as a HIGH-severity violation.
- Known conventions (DO NOT flag as high/critical — classify as informational):
  The following patterns are intentional conventions backed by empirical testing.
  LLM agents reliably ignore behavioral-register instructions ("You always verify...")
  but comply with imperative-register instructions ("You MUST verify..."). These
  patterns have been validated across Opus and Sonnet models. Treat as informational
  only — note the divergence from pure Anthropic style but do NOT elevate severity:
  * Pre-Flight Gate sections with MUST/MUST NOT binding language
  * Imperative Protocol sections (step-by-step operational instructions)
  * Permissions Setup sections documenting settings.json configuration
  * Completion Checklists with checkbox items
  * DO/DO NOT mission sections
  * Tool Usage Constraints with Allowed/Forbidden per tool

OUTPUT:
Write structured YAML to logs/validations/{asset-name}-{timestamp}.yaml
Schema MUST include a top-level `bulwark_adopted_fields` array (separate from
`findings`) listing each adopted field detected with its value.
Schema MUST also include a top-level `reviewed_files: [...]` list (Stop-hook
contract — see Output Format section). Include any script/.sh files referenced
by the validated asset; empty list `[]` if the asset is .md/.json only.
```

### Step 4: Present Results

Summarize findings to user in human-readable format (see Output Format section).

---

## Bulwark-Adopted Fields Allowlist

Three frontmatter fields are non-Anthropic-official but intentionally standardized across Bulwark assets. The validator classifies them as **`bulwark-adopted`** — emitting informational notes in the report's `bulwark_adopted_fields` section, **not** counting them as violations against summary counters or verdict logic.

### Three-Tier Classification

| Tier | Definition | Validator Behavior |
|------|------------|--------------------|
| **`official`** | Field is in the canonical Anthropic spec for this asset type | Validate type/value per spec; flag mismatches as violations at appropriate severity |
| **`bulwark-adopted`** | Field is non-official but intentionally standardized in Bulwark | Emit info-level note in `bulwark_adopted_fields`; do **not** add to violation counters |
| **`unknown`** | Field is in neither category | Flag as **HIGH** violation — preserves the validator's drift-catching function |

### The Three Adopted Fields

| Field | Adoption Rationale | Asset Types |
|-------|--------------------|-------------|
| `version` | Semver traceability across skill/agent releases. Operationally required for downstream consumers to know which version they have installed. | Skills + Agents |
| `author` | Attribution. Uniform value `"Ashay Kubal @ Qball Inc."` across first-party Bulwark assets; user-prompted for skills generated externally via `create-skill`. | Skills + Agents |
| `skills` | Cross-skill dependency declaration. **Note**: `skills:` IS officially documented for *agent* frontmatter (`.claude/agents/*.md`); it is **not** documented for skill frontmatter (`SKILL.md`). The Bulwark adoption applies only to the skill-frontmatter use case — for agents, treat `skills` as official. | Skills (adopted) / Agents (official) |

### Promotion Path

If Anthropic publishes a spec update that formalizes any of these fields:

1. Move the field from the `bulwark-adopted` list to the appropriate `official` validation table.
2. Remove the adopted-field note logic for that field.
3. Update `references/{skills,agents,hooks,...}-validation.md` and matching `*-checklist.md` to reflect the change.
4. Update the "Last Verified" date stamps on the relevant tables.

This is intentionally a single-config change — the data-driven structure (a list of field names per tier) makes promotion trivial.

### Last Verified

- **2026-04-26 (Session 110, P10.3)** — verified against Anthropic skills spec at https://code.claude.com/docs/en/skills (none of `version`, `author`, `skills` documented for skill frontmatter); `skills` confirmed documented for agent frontmatter at https://docs.anthropic.com/en/docs/claude-code/sub-agents.

Sync this section whenever Anthropic publishes spec updates that affect frontmatter fields.

---

## Per-Asset-Type Validation Details

Asset-type-specific workflow + key validation points live in `references/`:

- **Skills**: `references/skills-validation.md`
- **Hooks**: `references/hooks-validation.md`
- **Agents**: `references/agents-validation.md`
- **Commands**: `references/commands-validation.md`
- **MCP**: `references/mcp-validation.md`
- **Plugins**: `references/plugins-validation.md`

Step 1 above routes to the correct file based on detected asset type. Each reference file contains the official documentation URL, the asset-specific validation workflow, the key validation points (fields, requirements, severities), and the fallback checklist pointer.

Fallback checklists (used when `claude-code-guide` doc fetch fails) live in the same directory: `references/{type}-checklist.md`.

---

## Batch Validation

When validating a directory:

1. **Glob** all matching files based on asset type patterns
2. **For each asset INDIVIDUALLY**:
   - Run the FULL single-asset validation workflow (Steps 1-4)
   - Spawn `bulwark-standards-reviewer` with ONLY that one asset
   - Write individual report to `logs/validations/`
   - **DO NOT** combine multiple assets into one reviewer context
3. **After all assets validated**, aggregate results into summary report

**CRITICAL**: Do NOT frontload all assets into a single reviewer context. This causes shallow analysis due to context overload. Each asset must be validated with full depth individually, then results aggregated.

### Batch Output

```
logs/validations/
├── batch-summary-{timestamp}.yaml    # Aggregate summary
├── skill-one-{timestamp}.yaml        # Individual reports
├── skill-two-{timestamp}.yaml
└── ...
```

### Batch Summary Format

```yaml
batch_validation:
  metadata:
    directory: "{path}"
    timestamp: "{ISO-8601}"
    total_assets: 5

  results:
    passed: 3
    failed: 2

  failures:
    - asset: "skills/broken-skill/SKILL.md"
      critical_count: 1
      report: "logs/validations/broken-skill-{timestamp}.yaml"
```

---

## Output Format

### YAML Report (logs/validations/)

```yaml
# Top-level — required for Stop-hook per-file pipeline-recursion suppression.
# List any script/.sh files referenced by the validated asset (asset itself
# is typically .md/.json which the accumulator excludes). Paths relative to
# ${CLAUDE_PROJECT_DIR}. Empty list `[]` is valid and common (asset-only
# validation). Missing field disables suppression for this log (strict mode).
reviewed_files:
  - scripts/hooks/enforce-quality.sh

validation_report:
  metadata:
    asset: "{file_path}"
    asset_type: skill | hook | agent | command | mcp | plugin
    timestamp: "{ISO-8601}"
    validator: "bulwark-standards-reviewer"
    standards_source: fetched | fallback

  findings:
    # Official-spec violations only — bulwark-adopted fields are NOT listed here.
    - severity: critical | high | medium | low
      rule: "{standard being checked}"
      violation: "{what is wrong}"
      location: "{line or field}"
      remediation: "{how to fix}"

  bulwark_adopted_fields:
    # Non-Anthropic-official fields detected that ARE intentionally adopted by Bulwark.
    # These are informational notes — they do NOT count against the verdict.
    - field: version
      value: "1.0.0"
      classification: bulwark-adopted
      note: "Bulwark-adopted convention for traceability across releases."
    - field: author
      value: "Ashay Kubal @ Qball Inc."
      classification: bulwark-adopted
      note: "Bulwark-adopted convention for attribution."
    - field: skills
      value: ["subagent-prompting"]
      classification: bulwark-adopted
      note: "Documentary cross-skill dependency declaration. Anthropic parser ignores unknown fields."

  summary:
    official_spec_violations: 0
    bulwark_adopted_fields_detected: 0
    critical: 0
    high: 0
    medium: 0
    low: 0
    verdict: pass | fail
    notes: "{any additional context}"
```

### Human-Readable Summary

```
Validation: skills/my-skill/SKILL.md
Standards: Fetched from official docs (2026-04-26)
Verdict: FAIL (2 critical, 1 high)

Official-Spec Violations:
  Critical:
    - Missing required 'description' field in frontmatter
    - SKILL.md exceeds 500 line limit (612 lines)
  High:
    - 'agent' field uses unsupported value 'gpt-4'

Bulwark-Adopted Fields Detected (informational, not violations):
  - version: "1.0.0"
  - author: "Ashay Kubal @ Qball Inc."

Full report: logs/validations/my-skill-2026-04-26T10-30-00.yaml
```

### Severity Definitions

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Blocks functionality, violates required standards | Missing required frontmatter, wrong file location |
| **High** | Significant issue, should fix before release | Deprecated field, exceeds limits |
| **Medium** | Quality improvement, recommended | Missing optional fields |
| **Low** | Style/naming suggestions | Naming conventions |

### Verdict Logic

```
# Field names align with the YAML summary schema above.
if summary.critical >= 1:
    verdict = "fail"
else:
    verdict = "pass"
# Always list ALL findings regardless of verdict.
# Bulwark-adopted field detections are NOT findings — they appear in
# the dedicated `bulwark_adopted_fields` section and do NOT affect verdict.
```

---

## Fallback Behavior

When `claude-code-guide` fetch fails:

1. **Log warning**: "Could not fetch latest standards, using embedded checklist"
2. **Set** `standards_source: fallback` in report
3. **Use** embedded checklist from `references/{type}-checklist.md` (the per-asset-type fallback file referenced in `references/{type}-validation.md`)
4. **Continue** validation
5. **Include note** in summary: "Validated against potentially outdated standards"

---

## Diagnostic Output

All validation runs write diagnostic data to:

```
logs/diagnostics/anthropic-validator-{ISO-8601-timestamp}.yaml
```

Use ISO-8601 with hyphens for filename safety, e.g. `2026-04-26T14-00-00`. Same convention applies to validation reports under `logs/validations/`.

### Diagnostic Schema

```yaml
# Top-level — required for Stop-hook per-file pipeline-recursion suppression.
# Diagnostic logs typically reference no scripts directly (the validation
# workflow operates on the asset itself). Empty list `[]` is the common case;
# include any script paths only if the diagnostic explicitly cites them.
reviewed_files: []

diagnostic:
  skill: anthropic-validator
  timestamp: "{ISO-8601}"

  invocation:
    asset_path: "{input}"
    asset_type: "{detected type}"
    batch_mode: true | false

  execution:
    standards_fetch:
      agent: claude-code-guide
      success: true | false
      fallback_used: true | false
    analysis:
      agent: bulwark-standards-reviewer
      findings_count: 0

  output:
    report_path: "logs/validations/{name}.yaml"
    verdict: pass | fail
```

---

## Related Skills

- `subagent-prompting` (P0.1) — 4-part template for agent invocation
- `subagent-output-templating` (P0.2) — Output format for logs

## Related Agents

- `bulwark-standards-reviewer` — Critical analysis agent (invoked by this skill)
- `claude-code-guide` — Built-in agent for documentation fetching
