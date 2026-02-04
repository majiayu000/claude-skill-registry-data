---
name: ontology-phase-1-ingest
description: |
  Phase 1 of Ontology Builder Pipeline. Ingests and catalogs all input materials 
  from _input/ folder. Use when starting ontology building process or when 
  processing new input documents for domain analysis.
---

# Phase 1: Ingest

Read and catalog all input materials to prepare for analysis.

## Trigger

Execute when:
- Starting Ontology Builder Pipeline
- New documents added to `_input/`
- Re-processing requested

## Process

### Step 1: Validate Input Structure

Check `_input/` folder:

```
Required:
✓ project-context.md (MUST exist)

Optional but valuable:
○ domain-hints.md
○ requirements/*.md
○ interviews/*.md
○ existing-docs/*
○ references/*
```

If `project-context.md` missing:
→ STOP and request from user

### Step 2: Read Project Context

Extract from `project-context.md`:
- Project name, module, domain
- Region (for regulatory context)
- Current state and pain points
- Stakeholders
- Constraints

Store as `context_vars` for later phases.

### Step 3: Catalog All Files

For each file in `_input/`:

```yaml
file_entry:
  path: [relative path]
  type: [user-story | interview | existing-doc | reference | other]
  format: [md | pdf | docx | txt | image]
  size: [file size]
  summary: [2-3 sentence summary of content]
  key_topics: [list of main topics]
  entities_mentioned: [list of nouns that might be entities]
  workflows_mentioned: [list of processes/actions mentioned]
```

### Step 4: Identify File Relationships

Map relationships between files:
- Which files reference each other?
- Which files cover same topics?
- Which files contradict each other?

### Step 5: Assess Input Quality

Rate input completeness:

| Aspect | Score | Notes |
|--------|-------|-------|
| Requirements coverage | [1-5] | [notes] |
| Domain context | [1-5] | [notes] |
| Stakeholder input | [1-5] | [notes] |
| Examples/scenarios | [1-5] | [notes] |

### Step 6: Generate Ingestion Report

Output: `_output/_logs/ingestion-report.md`

```markdown
# Ingestion Report

**Generated**: [timestamp]
**Project**: [from context]
**Module**: [from context]

## Input Summary

| Category | Files | Status |
|----------|-------|--------|
| Project Context | 1 | ✓ Valid |
| Requirements | [N] | [status] |
| Interviews | [N] | [status] |
| Existing Docs | [N] | [status] |
| References | [N] | [status] |

## File Catalog

[List all files with summaries]

## Preliminary Extraction

### Potential Entities (Raw)
[List all nouns that appear to be domain entities]

### Potential Workflows (Raw)
[List all processes/actions mentioned]

### Potential Business Rules (Raw)
[List any rules or constraints mentioned]

## Quality Assessment

[Quality scores and notes]

## Gaps Identified

[List what seems to be missing]

## Recommendations

[Suggestions for Phase 2]
```

## Output

- `_output/_logs/ingestion-report.md`
- `_output/_logs/gate-1-manifest.yaml` (verification manifest)
- Ready for Phase 2: Analyze

## Gate 1: Self-Verification

Before completing Phase 1, generate verification manifest:

```yaml
# _output/_logs/gate-1-manifest.yaml
gate: 1
name: "Post-Ingest Verification"
timestamp: "[ISO timestamp]"

structural_checks:
  - check: "ingestion-report.md exists"
    status: PASS
  - check: "All input files cataloged"
    status: PASS | FAIL
    details:
      input_files_count: [N]
      cataloged_count: [N]
      missing: []
  - check: "project-context.md processed"
    status: PASS | FAIL

consistency_checks:
  - check: "No duplicate entries"
    status: PASS | FAIL
  - check: "All file paths valid"
    status: PASS | FAIL

traceability_checks:
  - check: "Each file has summary"
    status: PASS | FAIL
    files_without_summary: []

result:
  status: PASS | FAIL | WARN
  blocking_failures: []
  warnings: []
  proceed_to_next_phase: true | false
```

**Verification Rule**: Only proceed to Phase 2 if `status: PASS` or `status: WARN`

## Error Handling

| Issue | Action |
|-------|--------|
| No project-context.md | STOP, request from user |
| Empty _input/ folder | STOP, request input files |
| Unreadable file | Log warning, skip file |
| Very large file (>100KB) | Summarize first 10K, note truncation |

## Next Phase

After completing ingestion:
→ Load `phase-2-analyze/SKILL.md`
→ Pass ingestion-report.md as input
