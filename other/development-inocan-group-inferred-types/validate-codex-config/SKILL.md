---
name: validate-codex-config
description: >
  Validate afi-config codex and governance configuration for structural consistency,
  broken references, and schema alignment, without changing protocol semantics.
  This skill performs read-only validation and produces a human-readable report
  of issues found, without attempting automatic fixes.
---

# Skill: validate-codex-config (afi-config)

## Purpose

Use this skill when you need to **validate the structural integrity and consistency of afi-config's codex, governance artifacts, and schema definitions**.

This skill ensures:

- **Codex files are structurally valid** (JSON/YAML syntax, required fields)
- **File references are not broken** (paths point to existing files)
- **Schemas are valid** (JSON Schema Draft 2020-12 compliance)
- **Validation commands pass** (`npm run validate`, `npm test`)
- **`.afi-codex.json` metadata is accurate** (reflects actual capabilities)

This skill is primarily used by `config-keeper-droid` and can be called when:

- We want to validate codex structure before making changes
- We want to catch broken references in governance docs
- We want to ensure schemas are valid before publishing
- We want to verify that validation tests pass
- We want to audit configuration drift or inconsistencies

---

## Preconditions

Before using this skill, the droid must:

1. Read:
   - `afi-config/AGENTS.md`
   - AFI Droid Charter v0.1 (`afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md`)
   - AFI Droid Playbook v0.1 (`afi-config/codex/governance/droids/AFI_DROID_PLAYBOOK.v0.1.md`)

2. Confirm:
   - The request is about **validation only**, not modification
   - You have access to `afi-config` repo
   - Node.js and npm are installed (`node --version`, `npm --version`)
   - Dependencies are installed (`npm install` if needed)

3. Understand afi-config structure:
   - **codex/** — Codex metadata and governance artifacts
   - **codex/governance/droids/** — AFI Droid Charter, Playbook, Glossary
   - **schemas/** — JSON Schema definitions for AFI Protocol
   - **templates/** — Configuration templates
   - **tests/** — Schema validation tests (Vitest)
   - **.afi-codex.json** — Repo metadata (provides, consumers, entrypoints)

4. Understand validation commands:
   - `npm run validate` — Run schema validation tests
   - `npm test` — Run all tests (Vitest)
   - `npm run typecheck` — Validate TypeScript types
   - `npm run build` — Compile TypeScript

If any requirement is unclear or appears to violate AGENTS.md or Charter, STOP and ask for human clarification.

---

## Inputs Expected

The caller should provide, in natural language or structured form:

- **scope**: Which files or directories to validate (default: full validation)
  - `full` — Validate all codex, schemas, and governance files
  - `codex` — Validate only codex files
  - `schemas` — Validate only schema files
  - `governance` — Validate only governance artifacts
  - `metadata` — Validate only `.afi-codex.json`
- **checks**: Which validation checks to run (default: all)
  - `syntax` — JSON/YAML syntax validation
  - `references` — File reference validation
  - `schema-compliance` — JSON Schema compliance validation
  - `tests` — Run validation commands (`npm run validate`, `npm test`)
  - `all` — Run all checks

Optional:
- **filters**: Specific files or patterns to validate (e.g., `schemas/pipeline.schema.json`)
- **report_format**: Output format (`summary`, `detailed`, `json`)

If no inputs are provided, use conservative defaults:
- **scope**: `full`
- **checks**: `all`
- **report_format**: `summary`

---

## Step-by-Step Instructions

When this skill is invoked, follow this sequence:

### 1. Restate the request

In your own words, summarize:

- Which files or directories will be validated
- Which validation checks will be run
- What the expected outcome is (validation report)
- Confirm this is read-only validation and won't modify files

This summary should be short and precise, so humans can quickly confirm the intent.

---

### 2. Enumerate files in scope

Navigate to `afi-config/` and list files based on scope:

**Full validation** (default):
- Codex files: `find codex -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" \)`
- Schema files: `find schemas -type f -name "*.json"`
- Governance files: `find codex/governance -type f -name "*.md"`
- Metadata: `.afi-codex.json`

**Codex only**:
- `find codex -type f \( -name "*.md" -o -name "*.json" -o -name "*.yaml" \)`

**Schemas only**:
- `find schemas -type f -name "*.json"`

**Governance only**:
- `find codex/governance -type f -name "*.md"`

**Metadata only**:
- `.afi-codex.json`

**Filtered**:
- Use provided file patterns or paths

---

### 3. Run validation checks

Based on the `checks` input, run the following:

#### Check 1: JSON/YAML Syntax Validation

For each JSON file:
```bash
# Validate JSON syntax
node -e "JSON.parse(require('fs').readFileSync('path/to/file.json', 'utf8'))"
```

For each YAML file (if any):
```bash
# Validate YAML syntax (requires js-yaml or similar)
# Or use a simple parser check
```

**Capture**:
- Files with syntax errors
- Error messages and line numbers

#### Check 2: File Reference Validation

For each codex file and governance doc:

1. **Extract file references**:
   - Look for markdown links: `[text](path/to/file.md)`
   - Look for JSON/YAML path fields: `"path": "schemas/pipeline.schema.json"`
   - Look for relative paths in documentation

2. **Validate each reference**:
   - Check if file exists: `test -f path/to/file`
   - If file doesn't exist, record as broken reference

**Capture**:
- Broken file references (file path, source file, line number)
- Missing files

#### Check 3: JSON Schema Compliance Validation

For each schema file in `schemas/`:

1. **Parse as JSON** (already done in Check 1)
2. **Validate against JSON Schema meta-schema**:
   - Check that `$schema` field is present
   - Validate against Draft 2020-12 meta-schema (if tooling available)
   - Check for required fields: `type`, `properties`, etc.

3. **Check schema structure**:
   - Ensure `$id` is present and unique
   - Validate that `$ref` references are resolvable
   - Check for circular references

**Capture**:
- Invalid schemas (file path, error message)
- Missing required fields
- Unresolvable references

#### Check 4: Run Validation Commands

Execute validation commands defined in `package.json`:

**npm run validate**:
```bash
cd afi-config
npm run validate
```

**Capture**:
- Exit code (0 = pass, non-zero = fail)
- stdout and stderr output
- Number of tests passed/failed

**npm test**:
```bash
cd afi-config
npm test
```

**Capture**:
- Exit code (0 = pass, non-zero = fail)
- Test results (passed/failed/total)
- Error messages for failed tests

**npm run typecheck** (optional):
```bash
cd afi-config
npm run typecheck
```

**Capture**:
- Exit code (0 = pass, non-zero = fail)
- TypeScript errors (if any)

---

### 4. Validate `.afi-codex.json` metadata

Read `.afi-codex.json` and validate:

1. **Required fields**:
   - `codexVersion` (should be "2.0.0")
   - `module.name` (should be "afi-config")
   - `module.role` (should be "config-schema-library")
   - `provides` (array of capabilities)
   - `consumers` (array of consuming repos)
   - `entrypoints` (array of entry points)

2. **Consistency checks**:
   - **provides**: Check that each capability corresponds to actual files
     - `configSchemas` → `schemas/` directory exists
     - `droidCharter` → `codex/governance/droids/AFI_DROID_CHARTER.v0.1.md` exists
   - **entrypoints**: Check that each path exists
     - `schemas/` → directory exists
     - `templates/` → directory exists
     - `codex/` → directory exists
   - **consumers**: Check that each repo is a valid AFI repo name
     - Valid: `afi-core`, `afi-reactor`, `afi-skills`, `afi-ops`, `afi-token`, etc.

**Capture**:
- Missing required fields
- Inconsistencies between metadata and actual files
- Invalid consumer names

---

### 5. Collect findings

Organize findings by severity:

**ERRORS** (must fix):
- JSON/YAML syntax errors
- Broken file references in critical paths
- Invalid schemas (fail JSON Schema meta-schema validation)
- Failed validation commands (`npm run validate`, `npm test`)
- Missing required fields in `.afi-codex.json`

**WARNINGS** (should fix):
- Broken file references in documentation
- Missing optional fields in schemas
- Inconsistencies in `.afi-codex.json` metadata
- TypeScript type errors (if not critical)

**INFO** (nice to have):
- Formatting inconsistencies
- Typos in comments
- Outdated documentation

---

### 6. Produce validation report

Generate a concise, human-readable report:

**Summary format** (default):

```markdown
## Codex Validation Report

**Scope**: Full validation (codex/, schemas/, governance/, metadata)
**Timestamp**: 2025-11-28 14:30:00 UTC

**Files Scanned**:
- Codex files: 4 (codex/governance/droids/*.md, codex/governance/README.md)
- Schema files: 7 (schemas/*.json, schemas/usignal/v1/*.json)
- Governance files: 3 (codex/governance/droids/*.md)
- Metadata: 1 (.afi-codex.json)

**Validation Results**:
- ✅ JSON/YAML syntax: PASS (12/12 files valid)
- ✅ File references: PASS (0 broken references)
- ✅ Schema compliance: PASS (7/7 schemas valid)
- ✅ `npm run validate`: PASS (20/20 tests)
- ✅ `npm test`: PASS (20/20 tests)
- ✅ `.afi-codex.json`: PASS (all required fields present)

**Issues Found**: None

**Overall Status**: ✅ CLEAN
```

**Detailed format** (if requested):

Include full list of files scanned, detailed error messages, and suggested fixes.

**JSON format** (if requested):

```json
{
  "timestamp": "2025-11-28T14:30:00Z",
  "scope": "full",
  "files_scanned": {
    "codex": 4,
    "schemas": 7,
    "governance": 3,
    "metadata": 1
  },
  "checks": {
    "syntax": { "status": "PASS", "errors": [] },
    "references": { "status": "PASS", "errors": [] },
    "schema_compliance": { "status": "PASS", "errors": [] },
    "validation_commands": { "status": "PASS", "errors": [] },
    "metadata": { "status": "PASS", "errors": [] }
  },
  "overall_status": "CLEAN"
}
```

---

### 7. Escalate if needed

If validation reveals critical issues, escalate:

**Schema breaking changes**:
- Tag @afi-core-team for cross-repo coordination
- Explain which schemas are affected and which repos consume them

**Governance inconsistencies**:
- Tag @afi-governance-team for review
- Explain which governance artifacts are affected

**Systemic validation failures**:
- Tag @afi-core-team for architecture review
- Provide full validation output and error messages

**Unclear requirements**:
- Ask for clarification on validation scope or expected behavior

---

## Hard Boundaries

When using this skill, you MUST NOT:

- **Modify any files**:
  - Do NOT fix syntax errors automatically
  - Do NOT update file references
  - Do NOT change schema definitions
  - Do NOT modify `.afi-codex.json`
  - This skill is **read-only validation only**

- **Modify governance artifacts**:
  - Do NOT change AFI Droid Charter v0.1
  - Do NOT change AFI Droid Playbook v0.1
  - Do NOT modify governance rules or policies

- **Change protocol semantics**:
  - Do NOT modify schema field types or semantics
  - Do NOT remove schema fields
  - Do NOT change validation logic

- **Touch other repos**:
  - Do NOT validate or modify files in afi-core, afi-reactor, afi-skills, afi-ops, afi-token, etc.
  - Do NOT run validation commands in other repos

If a request forces you towards any of the above, STOP and escalate.

---

## Output / Summary Format

At the end of a successful `validate-codex-config` operation, produce a summary that includes:

**Validation Scope**:
- Which files or directories were validated
- Which validation checks were run

**Files Scanned**:
- Number of codex files
- Number of schema files
- Number of governance files
- Number of metadata files

**Validation Results**:
- JSON/YAML syntax: PASS/FAIL (number of files with errors)
- File references: PASS/FAIL (number of broken references)
- Schema compliance: PASS/FAIL (number of invalid schemas)
- Validation commands: PASS/FAIL (test results)
- Metadata: PASS/FAIL (consistency check results)

**Issues Found**:
- List of errors (critical issues)
- List of warnings (should fix)
- List of info items (nice to have)

**Overall Status**:
- ✅ CLEAN — No issues found
- ⚠️ WARNINGS — Some warnings, no errors
- ❌ ERRORS — Critical issues found

**Next Steps**:
- Action items (e.g., "Fix broken reference in codex/governance/README.md")
- Escalation recommendations (if needed)

---

## Example Usage Patterns

### Example A: Full Validation

**Request**:
> "Validate the entire afi-config codex to make sure there are no broken references or invalid schemas."

**Inputs**:
- **scope**: `full`
- **checks**: `all`
- **report_format**: `summary`

**Implementation**:

1. Restate: "Running full validation on all codex, schemas, and governance files."
2. Enumerate files:
   - Codex: 4 files
   - Schemas: 7 files
   - Governance: 3 files
   - Metadata: 1 file
3. Run checks:
   - JSON syntax: Parse all JSON files → All valid
   - File references: Check all markdown links → No broken references
   - Schema compliance: Validate all schemas → All valid
   - Validation commands: Run `npm run validate` and `npm test` → All pass
   - Metadata: Validate `.afi-codex.json` → All required fields present
4. Collect findings: No errors, no warnings
5. Produce report:

```markdown
## Codex Validation Report

**Scope**: Full validation (codex/, schemas/, governance/, metadata)

**Files Scanned**: 15 total
- Codex files: 4
- Schema files: 7
- Governance files: 3
- Metadata: 1

**Validation Results**:
- ✅ JSON/YAML syntax: PASS (15/15 files valid)
- ✅ File references: PASS (0 broken references)
- ✅ Schema compliance: PASS (7/7 schemas valid)
- ✅ `npm run validate`: PASS (20/20 tests)
- ✅ `npm test`: PASS (20/20 tests)
- ✅ `.afi-codex.json`: PASS (all required fields present)

**Issues Found**: None

**Overall Status**: ✅ CLEAN

**Next Steps**: No action required. All validation checks passed.
```

---

### Example B: Schema-Only Validation

**Request**:
> "Check that all schemas in `schemas/` are valid JSON Schema Draft 2020-12."

**Inputs**:
- **scope**: `schemas`
- **checks**: `schema-compliance`
- **report_format**: `summary`

**Implementation**:

1. Restate: "Validating all schema files in `schemas/` for JSON Schema Draft 2020-12 compliance."
2. Enumerate files:
   - Schemas: 7 files (blueprint.schema.json, character.schema.json, pipeline.schema.json, etc.)
3. Run checks:
   - Schema compliance: Validate each schema against meta-schema → All valid
4. Collect findings: No errors
5. Produce report:

```markdown
## Schema Validation Report

**Scope**: Schema validation only (schemas/)

**Files Scanned**: 7 schemas
- blueprint.schema.json
- character.schema.json
- pipeline.schema.json
- plugin-manifest.schema.json
- repo-metadata.schema.json
- vault.schema.json
- usignal/v1/*.json

**Validation Results**:
- ✅ Schema compliance: PASS (7/7 schemas valid JSON Schema Draft 2020-12)

**Issues Found**: None

**Overall Status**: ✅ CLEAN

**Next Steps**: No action required. All schemas are valid.
```

---

### Example C: Validation with Errors

**Request**:
> "Validate codex and report any broken file references."

**Inputs**:
- **scope**: `codex`
- **checks**: `references`
- **report_format**: `detailed`

**Implementation**:

1. Restate: "Validating codex files for broken file references."
2. Enumerate files:
   - Codex: 4 files
3. Run checks:
   - File references: Check all markdown links
     - Found broken reference in `codex/governance/README.md` line 15: `[Charter](droids/AFI_DROID_CHARTER.v0.2.md)` → File does not exist
4. Collect findings:
   - **ERRORS**: 1 broken reference
5. Produce report:

```markdown
## Codex Validation Report

**Scope**: Codex validation (codex/)

**Files Scanned**: 4 codex files

**Validation Results**:
- ❌ File references: FAIL (1 broken reference)

**Issues Found**:

### ERRORS (1)

1. **Broken file reference** in `codex/governance/README.md` (line 15):
   - Reference: `[Charter](droids/AFI_DROID_CHARTER.v0.2.md)`
   - Expected file: `codex/governance/droids/AFI_DROID_CHARTER.v0.2.md`
   - Status: File does not exist
   - **Suggested fix**: Change to `[Charter](droids/AFI_DROID_CHARTER.v0.1.md)` (actual file)

**Overall Status**: ❌ ERRORS

**Next Steps**:
1. Fix broken reference in `codex/governance/README.md` line 15
2. Re-run validation to confirm fix
```

6. Escalate: "Found broken reference in governance README. Please review and fix."

---

## Notes for Humans

### When to Use This Skill

Use this skill when:

- **Before making changes** to codex or schemas (validate current state)
- **After making changes** to codex or schemas (validate new state)
- **Before publishing** schemas or governance artifacts (ensure validity)
- **Periodic audits** to catch drift or inconsistencies
- **CI/CD integration** to validate on every commit

### Expected Outcomes

- **Validation report**: Clear summary of validation results
- **Issue list**: Errors, warnings, and info items (if any)
- **No modifications**: This skill is read-only and does not fix issues
- **Escalation**: Critical issues are escalated to appropriate teams

### Limitations

This skill is **read-only validation only**:

- Does NOT fix syntax errors (escalate to human or config-keeper-droid)
- Does NOT update file references (escalate to human)
- Does NOT modify schemas (escalate to human for schema changes)
- Does NOT change governance artifacts (escalate to @afi-governance-team)

### Integration with CI/CD

This skill can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/validate-config.yml
name: Validate Config
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm install
      - run: npm run validate
      - run: npm test
```

---

**Last Updated**: 2025-11-28
**Maintainers**: AFI Core Team
**Charter**: `afi-config/codex/governance/droids/AFI_DROID_CHARTER.v0.1.md`
**Workflow**: `afi-config/AGENTS.md`
**Consumers**: afi-core, afi-reactor, afi-skills, afi-ops, afi-token, afi-infra, afi-plugins
