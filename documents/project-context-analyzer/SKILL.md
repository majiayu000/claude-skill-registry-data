---
name: Project Context Analyzer
description: Analyzes project structure, dependencies, and patterns to generate comprehensive context documentation. Uses parallel agent execution for faster analysis. Helps understand unfamiliar codebases quickly.
trigger: both
allowed-tools:
  - Read
  - Glob
  - Bash
  - Write
  - Task
  - TaskOutput
---

# Purpose

Analyze a project's structure, dependencies, framework, and patterns to generate comprehensive context documentation. Uses parallel agent swarm execution for blazing-fast analysis. Helps with onboarding, understanding unfamiliar codebases, and providing context to other AI agents. Uses specialized analysis tools for deep project understanding.

## Variables

ENABLE_JAVASCRIPT: true           # Enable JavaScript/TypeScript project analysis
ENABLE_PYTHON: true               # Enable Python project analysis
ENABLE_GO: false                  # Enable Go project analysis (not yet implemented)
ENABLE_PARALLEL_EXECUTION: true   # Use parallel agent swarm for faster analysis
OUTPUT_MODE: display              # Options: display (show results), save (write to file)
OUTPUT_FILE: .project-context.md  # Where to save report if OUTPUT_MODE is save
SUPPORTED_PROJECT_TYPES: javascript, typescript, python # Currently supported project types

## Workflow

1. **Parse User Request**

   - Determine intent: analyze, generate, show project context
   - Determine output mode: display or save
   - Display mode triggers: "analyze project", "show me project context", "what is this project"
   - Save mode triggers: "generate project context and save", "save project context"
   - Example: "analyze this project" → Intent: analyze, Mode: display

2. **Detect Project Type**

   - Tool: Run `tools/detect_framework.py`
   - Checks for: package.json (JS/TS), requirements.txt/pyproject.toml (Python), go.mod (Go)
   - Returns: {type, framework, language, confidence}
   - Example: package.json found → {type: "nodejs", framework: "react-vite", language: "typescript", confidence: "high"}

3. **Route to Cookbook**

   - Based on detected type and ENABLE flags
   - JavaScript/TypeScript: IF package.json AND ENABLE_JAVASCRIPT → javascript.md
   - Python: IF requirements.txt/pyproject.toml AND ENABLE_PYTHON → python.md
   - Unknown: IF no match → Basic analysis with Glob/Read
   - Example: TypeScript project detected + ENABLE_JAVASCRIPT=true → Route to cookbook/javascript.md

4. **Execute Analysis Tools**

   - IF: ENABLE_PARALLEL_EXECUTION is true → Launch parallel agent swarm for analysis tasks
   - Tools in `tools/` directory perform specialized analysis
   - Tool: Task with run_in_background: true for each analysis task
   - Agents: DependencyAnalyzer, StructureMapper, EntryPointFinder run simultaneously
   - Common tools: detect_framework, analyze_dependencies, analyze_structure, find_entry_points
   - Example: JavaScript project → Launch 3 parallel agents (dependencies, structure, entry points) → All complete in ~4s vs ~9s sequential

5. **Aggregate Results**

   - IF parallel execution used → Collect all agent results using TaskOutput
   - Combine data from all analysis tools
   - Generate formatted report with sections: overview, structure, dependencies, entry points
   - Keep comprehensive but concise (focus on what's important)
   - Example: Collect swarm results → Combine framework info + dependencies + structure → Complete context document with performance metrics

6. **Output Report**
   - IF OUTPUT_MODE is "display" OR user requested display: Show results in chat
   - IF OUTPUT_MODE is "save" OR user requested save: Write to OUTPUT_FILE
   - Example: "show me context" → Display in chat, "generate and save" → Write to .project-context.md

## Cookbook

### JavaScript/TypeScript Projects

- IF: The project has a `package.json` file AND `ENABLE_JAVASCRIPT` is true.
- THEN: Read and execute: `.claude/skills/project-context/cookbook/javascript.md`

### Python Projects

- IF: The project has `requirements.txt` or `pyproject.toml` AND `ENABLE_PYTHON` is true.
- THEN: Read and execute: `.claude/skills/project-context/cookbook/python.md`

### Unknown Project Type

- IF: No specific project type detected.
- THEN: Perform basic analysis using available built-in tools (Glob, Read).
- Report what can be detected and suggest adding Go or other language support.
