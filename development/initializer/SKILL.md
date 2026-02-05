---
name: initializer
description: Initialize long-running agent projects with environment setup, feature list generation, and progress tracking. Use when starting a new implementation project or setting up an existing codebase for Claude-assisted development. Creates init.sh (dev server script), claude-progress.txt (work log), and docs/features.json (feature list with status tracking).
---

# Initializer

Set up a project for long-running Claude agent implementation with environment scripts, feature tracking, and progress logging.

## When to Use

- Starting a new implementation project
- Setting up an existing codebase for Claude-assisted development
- After spec2impl generates the implementation harness
- Beginning a feature implementation sprint

## Input Modes

The Initializer works with three types of input:

### 1. Specification Documents
```
Input: docs/ directory with Markdown specs
Output: Feature list extracted from specifications
```

### 2. Existing Codebase
```
Input: Project with package.json, src/, etc.
Output: Feature list inferred from code structure
```

### 3. High-Level Prompt
```
Input: User description (e.g., "E-commerce site with user auth")
Output: Feature list generated from requirements
```

## Workflow

### Step 1: Analyze Input

Determine input mode and gather information:

```typescript
// Check for specification docs
const hasSpecs = await Glob("docs/**/*.md")

// Check for existing project
const hasProject = await Glob("{package.json,requirements.txt,go.mod,Cargo.toml}")

// Determine tech stack
const techStack = detectTechStack(hasProject)
```

### Step 2: Generate Feature List

Create `docs/features.json` with comprehensive feature tracking:

```typescript
// See references/feature-list-format.md for schema
const features = {
  project: { name: projectName, generatedAt: new Date() },
  features: extractOrGenerateFeatures(input),
  summary: { total: N, pending: N, ... }
}

Write("docs/features.json", JSON.stringify(features, null, 2))
```

**Feature Granularity Guidelines:**
- Small projects (< 10 features): Fine-grained, one feature per endpoint/component
- Medium projects (10-50 features): Group related functionality
- Large projects (50+ features): High-level feature groups, use subtasks for details

### Step 3: Create Environment Files

Generate `init.sh` based on detected tech stack:

```bash
# Run the initialization script
python3 .claude/skills/spec2impl/initializer/scripts/init_project.py \
  --tech-stack "${techStack}" \
  --project-name "${projectName}"
```

See `references/init-templates.md` for tech-stack-specific templates.

### Step 4: Initialize Progress Log

Create `claude-progress.txt` for session tracking:

```
# Claude Progress Log
# Project: {project-name}
# Generated: {date}

## Current Session
- Started:
- Current Task:

## Completed Tasks
(none yet)

## Notes

```

## Output Files

| File | Purpose |
|------|---------|
| `docs/features.json` | Feature list with status tracking (pending/in_progress/completed/failed) |
| `init.sh` | Development server startup script (chmod +x) |
| `claude-progress.txt` | Work log for Claude sessions |

## Resources

### scripts/
- `init_project.py` - Generates init.sh and claude-progress.txt based on tech stack

### references/
- `feature-list-format.md` - Schema and examples for features.json
- `init-templates.md` - Tech-stack-specific templates for init.sh
