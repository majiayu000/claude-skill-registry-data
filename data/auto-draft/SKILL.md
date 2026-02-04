---
name: auto-draft
description: Generate planning documents (기획서) automatically from mockups/MVP sites and project artifacts. This skill orchestrates the entire document generation workflow including crawling, analysis, section generation, validation, and final PPT creation.
---

# Auto-Draft Skill

## Overview

This skill is the main entry point for the Draftify auto-draft system. It coordinates the entire document generation workflow:

1. **Phase 1-3.5**: Invokes `auto-draft-orchestrator` agent for data collection, analysis, and section generation
2. **Phase 4**: Calls `/draftify-ppt` skill to generate the final PowerPoint document

## Usage

```bash
/auto-draft <URL> [options]
```

### Required Arguments

| Argument | Description |
|----------|-------------|
| `URL` | Target MVP/mockup site URL to analyze |

### Optional Arguments

| Option | Description | Default |
|--------|-------------|---------|
| `--prd <path>` | Path to PRD document | - |
| `--sdd <path>` | Path to SDD document | - |
| `--readme <path>` | Path to README file | - |
| `--screenshots <dir>` | Directory containing screenshots | - |
| `--source-dir <dir>` | Local source code directory | - |
| `--urls <file>` | Text file with additional URLs | - |
| `--output <dir>` | Output directory | `outputs/<project-name>/` |
| `--max-depth <n>` | Maximum crawling depth | `5` |
| `--max-pages <n>` | Maximum pages to crawl | `50` |
| `--record` | Enable Record mode for SPA | `false` |

## Workflow

```
/auto-draft invoked
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Argument Validation              │
│    - Validate URL format            │
│    - Check file paths exist         │
│    - Set default values             │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 2. Invoke Orchestrator (Phase 1-3.5)│
│    - Task tool call                 │
│    - auto-draft-orchestrator agent  │
│    - Timeout: 25 minutes            │
└─────────────────────────────────────┘
    │
    │ Orchestrator returns:
    │ - projectName
    │ - outputDir
    │ - validation result
    │
    ▼
┌─────────────────────────────────────┐
│ 3. Call /draftify-ppt (Phase 4)     │
│    - Skill tool call                │
│    - Generate <project>-draft-V{version}.pptx      │
│    - Timeout: 10 minutes            │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 4. Return Results                   │
│    - Output file path               │
│    - Success/failure status         │
│    - Validation summary             │
└─────────────────────────────────────┘
```

## Implementation

### Step 1: Argument Validation

```typescript
// Validate required URL
if (!url || !isValidUrl(url)) {
  throw new Error("Valid URL is required");
}

// Validate optional file paths
if (prd && !fileExists(prd)) {
  throw new Error(`PRD file not found: ${prd}`);
}

// Set defaults
const config = {
  url,
  prd: prd || null,
  sdd: sdd || null,
  readme: readme || null,
  screenshots: screenshots || null,
  sourceDir: sourceDir || null,
  urls: urls || null,
  output: output || null,
  maxDepth: maxDepth || 5,
  maxPages: maxPages || 50,
  record: record || false
};
```

### Step 2: Invoke Orchestrator

```typescript
const orchestratorResult = await Task({
  subagent_type: "general-purpose",
  description: "Execute auto-draft workflow Phase 1-3.5",
  prompt: `You are the auto-draft-orchestrator agent.

Read the orchestrator agent prompt from docs/design/agents/orchestrator.md.

**Configuration**:
${JSON.stringify(config, null, 2)}

Execute Phase 1-3.5 of the auto-draft workflow:
- Phase 1: Input collection (crawling + file reading)
- Phase 2: Analysis (input-analyzer)
- Phase 3-1: Prerequisite sections (policy + glossary, parallel)
- Phase 3-2: Dependent sections (screen → process, sequential)
- Phase 3.5: Quality validation

Return the project output directory path and validation result when complete.
  `,
  timeout: 1500000  // 25 minutes
});
```

### Step 3: Call /draftify-ppt (Phase 4)

```typescript
// Extract output directory from orchestrator result
const outputDir = orchestratorResult.outputDir;

// Call draftify-ppt skill for Phase 4
const pptResult = await Skill({
  skill: "draftify-ppt",
  args: outputDir
});
```

### Step 4: Return Results

```typescript
return {
  success: true,
  outputDir: outputDir,
  // Filename normalized from project metadata (spaces -> hyphens, lowercased)
  pptFile: `${outputDir}/${projectName}-draft-V${version}.pptx`,
  validation: orchestratorResult.validation
};
```

> Note: `projectName` and `version` should be read from analyzed-structure.json to match the draftify-ppt filename normalization.


## Error Handling

### Orchestrator Failure

If Phase 1-3.5 fails:
- Return partial results if any sections were generated
- Include error message in response
- Skip Phase 4 if no sections exist

### PPT Generation Failure

If Phase 4 fails:
- Return markdown sections as fallback
- Attempt HTML generation as alternative
- Include error message in response

## Output Structure

Upon successful completion:

```
outputs/<project-name>/
+-- screenshots/
|   +-- *.png
+-- analysis/
|   +-- crawling-result.json
|   +-- analyzed-structure.json
+-- sections/
|   +-- 01-cover.md
|   +-- 02-revision-history.md
|   +-- 03-table-of-contents.md
|   +-- 04-section-divider.md
|   +-- 05-glossary.md
|   +-- 06-policy-definition.md
|   +-- 07-process-flow.md
|   +-- 08-screen-definition.md
|   +-- 09-references.md (optional)
|   +-- 10-eod.md
+-- validation/
|   +-- validation-report.md
+-- <project>-draft-V{version}.pptx    // Generated by /draftify-ppt
```


## Timeout Budget

| Phase | Duration | Component |
|-------|----------|-----------|
| Phase 1-3.5 | 25 min | Orchestrator |
| Phase 4 | 10 min | /draftify-ppt |
| **Total** | **35 min** | |

## Examples

### Basic Usage

```bash
/auto-draft https://my-todo-app.com
```

### With PRD Document

```bash
/auto-draft https://my-todo-app.com --prd docs/prd.md
```

### With Screenshots Only (No Crawling)

```bash
/auto-draft https://my-todo-app.com --screenshots ./screens/
```

### Full Options

```bash
/auto-draft https://my-shop.com \
  --prd docs/prd.md \
  --sdd docs/sdd.md \
  --screenshots ./screens/ \
  --source-dir ./src/ \
  --max-pages 30
```

## Related Documents

- **Orchestrator**: [docs/design/agents/orchestrator.md](../../docs/design/agents/orchestrator.md)
- **Workflow**: [docs/design/workflow.md](../../docs/design/workflow.md)
- **PPT Generator**: [.claude/skills/draftify-ppt/SKILL.md](../draftify-ppt/SKILL.md)
