---
name: doc-indexer
description: Use this skill at the beginning of any session or when needing to understand available project documentation. Provides just-in-time context by scanning YAML frontmatter from all markdown files in the docs/ directory without loading full content.
---

# Document Indexer Skill

## Purpose

Provide just-in-time context about available project documentation without loading full file content into the context window. The doc-indexer scans all markdown files in the `docs/` directory, extracts their YAML frontmatter metadata, and returns a structured map of available documentation. This enables efficient discovery of specs, plans, retrospectives, and other documentation while minimizing token usage.

## When to Use

Use this skill in the following situations:

- At the beginning of any work session to understand the current state of documentation
- When starting work on a new issue to identify relevant specs and context
- Before proposing changes to understand existing specifications
- When planning a sprint to review available approved specs
- Anytime you need an overview of project documentation without reading full files

## Prerequisites

- The project must have a `docs/` directory
- Documentation files should follow the convention of including YAML frontmatter
- The `jq` tool is NOT required (script works without it)

## Workflow

### Step 1: Run the Documentation Scanner

Execute the helper script to scan all markdown files in the docs/ directory:

```bash
bash scripts/scan-docs.sh
```

This will output a human-readable summary showing each document's frontmatter metadata.

For machine-readable JSON output (useful for programmatic processing):

```bash
bash scripts/scan-docs.sh -j
```

### Step 2: Review the Documentation Map

The scanner returns information about all markdown files found in `docs/`, including:

- **File path**: Location of the documentation file
- **Frontmatter metadata**: Key-value pairs from YAML frontmatter (title, status, type, etc.)
- **Compliance warnings**: Files missing YAML frontmatter are flagged

**Example human-readable output**:
```
---
file: docs/specs/001-synthesis-flow.md
title: AgenticDev Methodology
status: approved
type: spec
---
file: docs/changes/my-feature/proposal.md
title: My Feature Proposal
status: in-review
type: proposal
[WARNING] Non-compliant file (no frontmatter): docs/README.md
```

**Example JSON output**:
```json
[
  {
    "file": "docs/specs/001-synthesis-flow.md",
    "compliant": true,
    "frontmatter": {
      "title": "AgenticDev Methodology",
      "status": "approved",
      "type": "spec"
    }
  },
  {
    "file": "docs/README.md",
    "compliant": false,
    "frontmatter": null
  }
]
```

### Step 3: Use the Map to Identify Relevant Documentation

Based on the documentation map, identify which specific files to read for your current task:

- **For implementation work**: Look for approved specs related to your issue
- **For spec proposals**: Review existing specs to understand the current state
- **For sprint planning**: Identify approved specs ready for implementation
- **For learning context**: Find retrospectives and design docs

### Step 4: Read Specific Documentation Files

Once you've identified relevant files from the map, use the Read tool to load their full content:

```bash
# Example: Read a specific spec identified from the map
Read docs/specs/001-synthesis-flow.md
```

This two-step approach (scan first, then read selectively) minimizes token usage while ensuring you have access to all necessary context.

## Error Handling

### No docs/ Directory

**Symptom**: Script reports "No such file or directory"

**Solution**:
- Verify you're in the project root directory
- Check if the project has been initialized with `project-init` skill
- Create `docs/` directory structure if needed

### Files Missing Frontmatter

**Symptom**: Script outputs "[WARNING] Non-compliant file (no frontmatter): ..."

**Impact**: These files won't have structured metadata in the output

**Solution**:
- Add YAML frontmatter to documentation files for better discoverability
- Frontmatter should be at the top of the file between `---` markers
- Example format:
  ```markdown
  ---
  title: My Document
  status: draft
  type: design
  ---

  # Document content starts here
  ```

### Script Permission Errors

**Symptom**: "Permission denied" when running the script

**Solution**:
```bash
chmod +x scripts/scan-docs.sh
```

## Output Interpretation Guide

### Frontmatter Fields

Common frontmatter fields you'll encounter:

- **title**: Human-readable document title
- **status**: Document state (draft, in-review, approved, archived)
- **type**: Document category (spec, proposal, design, retrospective, plan)
- **epic**: Associated epic issue number
- **sprint**: Sprint identifier
- **author**: Document author
- **created**: Creation date
- **updated**: Last update date

### Using JSON Output Programmatically

The JSON output mode is particularly useful when:

- Filtering documents by specific criteria (e.g., only approved specs)
- Counting documents by type or status
- Building automated workflows
- Integrating with other tools

Example using `jq` to filter approved specs:
```bash
bash scripts/scan-docs.sh -j | jq '.[] | select(.frontmatter.status == "approved")'
```

## Notes

- The scanner is non-invasive and read-only - it never modifies files
- Large projects with many docs benefit most from this just-in-time approach
- The script scans recursively through all subdirectories in `docs/`
- Empty frontmatter sections are treated as non-compliant
- The scan is fast and can be run frequently without performance concerns
- Consider running this at the start of each work session to stay current with documentation changes
