---
name: output-dev-folder-structure
description: Workflow folder structure conventions for Output SDK. Use when creating new workflows, organizing workflow files, or understanding the standard project layout.
allowed-tools: [Read, Glob]
---

# Workflow Folder Structure Conventions

## Overview

This skill documents the standard folder structure for Output SDK workflows. Following these conventions ensures consistency across the codebase and enables proper tooling support.

## When to Use This Skill

- Creating a new workflow from scratch
- Reorganizing an existing workflow
- Understanding where to place different file types
- Reviewing workflow structure for compliance

## Standard Workflow Folder Structure

```
src/workflows/{category}/{workflow-name}/
├── workflow.ts          # Main workflow definition (default export)
├── steps.ts             # Step function definitions (all I/O operations)
├── types.ts             # Zod schemas and TypeScript types
├── utils.ts             # Helper functions (optional)
├── prompts/             # LLM prompt files (optional)
│   └── {promptName}@v1.prompt
└── scenarios/           # Test input scenarios (optional)
    └── {scenario_name}.json
```

## File Purposes

### workflow.ts (Required)
- Contains the main `workflow()` function definition
- Default exports the workflow
- Must be deterministic - no direct I/O operations
- Orchestrates step calls

**Related Skill**: `output-dev-workflow-function`

### steps.ts (Required)
- Contains all `step()` function definitions
- Handles all I/O operations (HTTP, LLM, file system, etc.)
- Named exports for each step function
- Includes error handling with FatalError and ValidationError

**Related Skill**: `output-dev-step-function`

### types.ts (Required)
- Contains Zod schemas for input/output validation
- Exports TypeScript types derived from schemas
- Imports `z` from `@output.ai/core` (never from `zod`)

**Related Skill**: `output-dev-types-file`

### utils.ts (Optional)
- Contains pure helper functions
- No I/O operations - those belong in steps
- Shared utility logic for the workflow

### prompts/ folder (Optional)
- Contains `.prompt` files for LLM operations
- File naming: `{promptName}@v1.prompt`
- Uses YAML frontmatter and Liquid.js templating

**Related Skill**: `output-dev-prompt-file`

### scenarios/ folder (Optional)
- Contains JSON test input files
- File naming: `{scenario_name}.json`
- Matches workflow inputSchema structure

**Related Skill**: `output-dev-scenario-file`

## Workflow Categories

Workflows are organized into category folders:

```
src/workflows/
├── content_utils/       # Content processing workflows
├── data_processing/     # Data transformation workflows
├── integrations/        # External service integrations
└── {custom_category}/   # Project-specific categories
```

## Naming Conventions

### Folder Names
- Use `snake_case` for workflow folder names
- Example: `image_infographic_nano`, `resume_parser`

### File Names
- Use `camelCase` for `.ts` files (except `workflow.ts`, `steps.ts`, `types.ts`)
- Use `camelCase@v{n}` for `.prompt` files
- Use `snake_case` for `.json` scenario files

### Workflow Names
- The `name` property in `workflow()` should be camelCase
- Example: `contentUtilsImageInfographicNano`

## Example: Complete Workflow Structure

```
src/workflows/content_utils/image_infographic_nano/
├── workflow.ts              # workflow({ name: 'contentUtilsImageInfographicNano', ... })
├── steps.ts                 # generateImageIdeas, generateImages, validateReferenceImages
├── types.ts                 # WorkflowInputSchema, WorkflowOutput, step schemas
├── utils.ts                 # normalizeReferenceImageUrls, buildS3Url, etc.
├── prompts/
│   └── generateImageIdeas@v1.prompt
└── scenarios/
    ├── test_input_complex.json
    └── test_input_solar_panels.json
```

## Shared Resources

### HTTP Clients
HTTP clients are shared across workflows and live in a central location:

```
src/clients/
├── gemini_client.ts     # Google Gemini API client
├── jina_client.ts       # Jina AI client
└── perplexity_client.ts # Perplexity API client
```

Import pattern in workflows:
```typescript
import { GeminiImageService } from '#clients/gemini_client.js';
```

**Related Skill**: `output-dev-http-client-create`

## Verification Checklist

When reviewing workflow structure, verify:

- [ ] `workflow.ts` exists with default export
- [ ] `steps.ts` exists with all step definitions
- [ ] `types.ts` exists with Zod schemas
- [ ] All `.ts` imports use `.js` extension
- [ ] `prompts/` folder exists if LLM operations are used
- [ ] `scenarios/` folder exists with at least one test input
- [ ] Folder naming follows `snake_case` convention
- [ ] Workflow name in code follows `camelCase` convention

## Related Skills

- `output-dev-workflow-function` - Writing workflow.ts files
- `output-dev-step-function` - Writing step functions
- `output-dev-types-file` - Creating Zod schemas
- `output-dev-prompt-file` - Creating prompt files
- `output-dev-scenario-file` - Creating test scenarios
- `output-dev-http-client-create` - Creating shared HTTP clients
