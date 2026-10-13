---
name: packaging-skills
description: >
  Packages Claude skills into production-ready zip files with full March 2026
  Anthropic spec compliance, including structure validation, YAML
  verification, gerund naming enforcement, path reference validation (all
  SKILL.md subdirectory paths must exist in the zip), version sync checks,
  and exclusion of .DS_Store and .mcpb-cache artifacts. Activates when creating
  distributable skill packages for Cowork, Claude Desktop, Claude Code, or
  skill marketplaces. Also triggers on: zip this skill, package this up,
  validate my skill, is this spec compliant, skill zip broken, prepare for
  install, make this installable, or distribute this skill.
version: "3.0.0"
---

# Packaging Skills — March 2026 Spec

Validates, packages, and distributes Claude skills as zip files compliant with the March 2026 Anthropic specification. Knows every rule the spec defines and enforces them before a zip is created.

## Quick-Start Decision Tree

```
What are you packaging?
  ├─ Single skill directory ─── Standard package (this guide)
  ├─ Plugin with multiple skills ─── Plugin package (wrap in plugin.json manifest)
  ├─ Existing zip to validate ─── Validation-only mode (skip to Step 3)
  └─ Batch of skills ─── Batch mode (loop through directories)
```

---

## Usage Examples

**Example 1 — Package a single skill**
User: "Package the automating-workflows skill for distribution."
→ Locate directory. Validate frontmatter. Check gerund name. Exclude .DS_Store and .mcpb-cache. Create zip with single top-level folder. Verify. Report.

**Example 2 — Validate an existing zip**
User: "Check if this skill zip meets the March 2026 spec."
→ Extract to temp. Run all 15 validation checks. Report findings with PASS/WARN/FAIL per check. Suggest fixes for any failures.

**Example 3 — Package for a plugin**
User: "Package these 3 skills into a Cowork plugin."
→ Validate each skill independently. Check version sync between SKILL.md frontmatter and plugin.json. Create plugin zip with manifest. Verify.

---

## March 2026 Specification Rules

### Directory Structure (Required)

```
skill-name.zip
└── skill-name/              # Single top-level folder, matches skill name
    ├── SKILL.md             # Required — under 500 lines
    ├── references/          # Optional progressive disclosure
    ├── examples/            # Optional
    ├── resources/           # Optional
    ├── scripts/             # Optional
    ├── templates/           # Optional
    ├── workflows/           # Optional
    └── assets/              # Optional
```

### YAML Frontmatter (Required Fields)

```yaml
---
name: gerund-name-here        # Must match directory name exactly
description: >                # Third-person, what + when, max 1024 chars
  Performs X and produces Y. Activates when user mentions Z.
version: "1.0.0"             # Semver — must match plugin.json if in a plugin
---
```

### The 15 Validation Checks

| # | Check | Level | Rule |
|---|-------|-------|------|
| 1 | SKILL.md exists | FAIL | Must be at root of skill directory |
| 2 | Line count | FAIL | SKILL.md must be 500 lines or fewer |
| 3 | Gerund name | WARN | First segment must end in "-ing" (e.g., packaging-skills) |
| 4 | Name format | WARN | Lowercase, hyphens only, max 64 chars |
| 5 | Reserved words | FAIL | Name must not contain "anthropic" or "claude" |
| 6 | Description format | WARN | Third-person voice, no first-person patterns |
| 7 | Progressive disclosure | FAIL | If SKILL.md >100 lines, must have a valid subdirectory |
| 8 | No nested refs | FAIL | Reference files must not link to sibling reference files |
| 9 | Version sync | WARN | SKILL.md version must match plugin.json version (if in plugin) |
| 10 | .DS_Store exclusion | WARN | Must not be included in zip |
| 11 | .mcpb-cache exclusion | WARN | Must not be included in zip |
| 12 | No secrets | FAIL | No API keys, tokens, or passwords in any file |
| 13 | Single top-level folder | FAIL | Zip must contain exactly one root directory |
| 14 | Package size | WARN | Recommended under 10MB |
| 15 | Path reference validation | FAIL | Every subdirectory path referenced in SKILL.md must exist at that path inside the zip (no FLAT_EXISTS, no MISSING) |

### Gerund Naming Rules

The first hyphen-separated segment of the skill name must be a present participle (ending in "-ing"). This is a WARN, not a FAIL — legacy skills may retain non-gerund names.

**Valid:** packaging-skills, creating-hooks, engineering-staff-workflows, producing-ai-newsletter
**Invalid:** skill-packager, create-hooks, staff-engineer-v4, the-prompt-newsletter

### Legacy Detection

If the skill directory contains a `commands/` folder with `.md` files using the old slash-command format (YAML frontmatter with `allowed-tools:` plus a prompt body), flag it: "This skill uses the legacy commands/ format. Cowork plugins use a different command structure — see the plugin specification."

---

## Packaging Process

### Step 1 — Locate and Read

Read the skill directory. Confirm SKILL.md exists. Extract YAML frontmatter. Inventory all files and subdirectories.

### Step 2 — Validate

Run all 15 checks from the table above. For each check, record PASS, WARN, or FAIL with a specific message. Stop on any FAIL and report — do not create a zip with known failures.

### Step 3 — Exclusion Filter

Before creating the zip, exclude these files and directories:

```python
EXCLUSIONS = {
    '.DS_Store',          # macOS metadata
    '.mcpb-cache/',       # Cowork plugin build cache
    '__pycache__/',       # Python bytecode
    '.git/',              # Version control
    '.env',               # Environment secrets
    'node_modules/',      # Dependencies
    '.vscode/',           # Editor config
    '*.pyc',              # Compiled Python
    '.gitignore',         # Git config
    'Thumbs.db',          # Windows metadata
}
```

### Step 4 — Create Zip

```python
import zipfile
from pathlib import Path

def create_skill_zip(skill_dir: Path, output_dir: Path) -> Path:
    skill_name = skill_dir.name
    zip_path = output_dir / f"{skill_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_dir.rglob('*'):
            if file_path.is_file() and not should_exclude(file_path, skill_dir):
                arcname = f"{skill_name}/{file_path.relative_to(skill_dir)}"
                zf.write(file_path, arcname)

    return zip_path
```

### Step 5 — Verify

Extract the zip to a temp directory. Re-run all 15 validation checks on the extracted content. Confirm the round-trip is clean.

### Step 6 — Report

Output a packaging report with: skill name, version, file count, package size, validation results (14 checks), installation instructions, and output path.

---

## Version Sync Check (Plugin Context)

When a skill is part of a Cowork plugin, the version in SKILL.md frontmatter must match the version in plugin.json. If they differ:

```
WARN: Version mismatch
  SKILL.md version: 1.2.0
  plugin.json version: 1.1.0
  Action: Update one to match the other before packaging
```

---

## Batch Packaging

```bash
for skill_dir in /path/to/skills/*/; do
    if [ -f "$skill_dir/SKILL.md" ]; then
        python3 package_skill.py "$skill_dir" --output /path/to/output/
    fi
done
```

---

## Edge Cases

**Skill over 500 lines with no subdirectory:** FAIL. The packager must not create a zip. Recommend splitting content into references/ before re-running.

**Skill with nested references:** FAIL. If `references/a.md` links to `references/b.md`, the packager flags it. Fix by inlining the referenced content or removing the cross-link.

**Plugin with multiple skills at different versions:** Each skill's SKILL.md version must match plugin.json. If any skill diverges, WARN on the specific mismatch.

**Path references in SKILL.md point to wrong locations:** FAIL (Check 15). Two sub-cases:
- FLAT_EXISTS: files are at zip root but SKILL.md references them via `references/X.md` path.
  Fix: create subdirectory inside the zip, move files, re-package.
- MISSING: SKILL.md references files that aren't in the zip at all.
  Fix: either add the missing files before packaging, or remove the dead reference from SKILL.md.

Run `python3 diagnose.py <skill-dir>` to enumerate all Mode 6 findings before packaging.

**Empty subdirectories:** Exclude from zip. An empty references/ folder provides no progressive disclosure value and inflates the package.

---

## Self-Verification Checklist

Before delivering a packaged zip:
1. All 15 validation checks pass (0 FAIL, 0 WARN preferred)
2. No .DS_Store or .mcpb-cache in the zip contents
3. Single top-level folder matching skill name
4. Gerund naming verified on skill name
5. Version sync confirmed (if in plugin context)
6. Zip extracts cleanly and re-validates
7. Package report generated and delivered to user
8. Path reference validation (Check 15) passes — diagnose.py Mode 6 clean on source before zip

---

## CLAIMS
- The 15-check validation suite covers all March 2026 Anthropic spec requirements for skill packaging
- Gerund naming is a WARN-level convention, not a hard spec requirement — legacy skills may retain old names

## COUNTEREXAMPLE
- A skill could pass all 14 checks and still be low quality if the SKILL.md content is shallow or the reference files are placeholder shells

## CONTRADICTIONS
- The spec recommends 500-line max for SKILL.md but some domain-dense skills (security, compliance) genuinely need more — progressive disclosure into references/ is the escape hatch but adds navigation cost
