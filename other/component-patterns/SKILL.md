---
name: component-patterns
description: Per-component-type verification approaches. Use when generating verification scripts for different component types.
user-invocable: false
allowed-tools:
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Component Patterns

## Purpose

Provide verification strategies for different component types. This skill defines how to
test real behavior for CLIs, servers, parsers, processes, databases, and external APIs.

## When to Use

Load this skill when:
- Generating verification scripts via bulwark-verify skill
- Determining how to test a specific component type
- Implementing test-audit Step 7 rewrites

---

## Component Type Detection

Analyze the code to determine component type based on these indicators:

| Indicators | Component Type | Pattern Reference |
|------------|----------------|-------------------|
| Imports `child_process`, has `spawn`/`exec`/`execSync` | Process Spawner | `references/pattern-process-spawner.md` |
| Imports `http`/`https`/`express`/`fastify`/`koa`, has `listen()` | HTTP Server | `references/pattern-http-server.md` |
| Imports `fs`, reads/parses files, has parse functions | File Parser | `references/pattern-file-parser.md` |
| Has CLI argument parsing (`process.argv`, `yargs`, `commander`, `argparse`) | CLI Command | `references/pattern-cli-command.md` |
| Imports database driver (`pg`, `mysql`, `mongoose`, `sqlite`, `prisma`) | Database | `references/pattern-database.md` |
| Makes outbound HTTP calls (`fetch`, `axios`, `got`, `requests`) | External API | `references/pattern-external-api.md` |

---

## Pattern Reference Files

Each pattern reference contains:
- **Strategy**: High-level approach for testing the component type
- **Templates**: Ready-to-use verification script templates in Bash, Node/Jest, and Python/pytest
- **Placeholders**: Variables to substitute with component-specific values

### Available Patterns

| Pattern | File | Languages |
|---------|------|-----------|
| CLI Command | `references/pattern-cli-command.md` | Bash, Node, Python |
| HTTP Server | `references/pattern-http-server.md` | Bash, Node (supertest), Python |
| File Parser | `references/pattern-file-parser.md` | Bash, Node, Python |
| Process Spawner | `references/pattern-process-spawner.md` | Bash, Node |
| Database | `references/pattern-database.md` | Node, Python, Bash (SQLite) |
| External API | `references/pattern-external-api.md` | Node (MSW), Python (responses) |

---

## Usage Instructions

### Step 1: Detect Component Type

Analyze the target component code using the detection table above.

### Step 2: Load Pattern Reference

Read the appropriate pattern file from `references/`:

```
Read skills/component-patterns/references/pattern-{type}.md
```

### Step 3: Select Template

Choose the template that matches the project language:
- **Node projects** (`package.json` present): Use Node/Jest template
- **Python projects** (`pyproject.toml` or `setup.py` present): Use Python/pytest template
- **Generic/Other**: Use Bash template

### Step 4: Substitute Placeholders

Replace all `{placeholder}` values with component-specific information:

| Common Placeholders | Description |
|---------------------|-------------|
| `{component_name}` | Name of the component being tested |
| `{component_path}` | Import path to the module |
| `{port}` | Network port (for servers/processes) |
| `{expected_value}` | Expected output to verify |

---

## Quick Reference: Component to Pattern

| Component Type | Verification Strategy | Key Assertion |
|----------------|----------------------|---------------|
| CLI Command | Spawn, capture stdout/stderr | Exit code + output text |
| HTTP Server | Start, HTTP request, verify response | Status code + response body |
| File Parser | Create input, parse, check structure | Parsed fields + values |
| Process Spawner | Spawn, check port/pid, verify behavior | Process alive + responds |
| Database | Setup DB, execute ops, query state | Records exist/modified |
| External API | MSW intercept, real fetch, check result | Response data matches |

---

## Key Principle: Real Verification

All patterns follow the same principle: **verify observable output, not mock calls**.

| Anti-Pattern | Real Pattern |
|--------------|--------------|
| `expect(spawn).toHaveBeenCalled()` | `expect(await checkPort(8080)).toBe(true)` |
| `expect(fs.writeFile).toHaveBeenCalled()` | `expect(fs.existsSync(path)).toBe(true)` |
| `expect(fetch).toHaveBeenCalledWith(url)` | `const resp = await fetch(url); expect(resp.status).toBe(200)` |
| `expect(db.save).toHaveBeenCalled()` | `const found = await db.find(id); expect(found).toBeDefined()` |

---

## Diagnostic Output

Write diagnostic output to `logs/diagnostics/component-patterns-{YYYYMMDD-HHMMSS}.yaml`:

```yaml
skill: component-patterns
timestamp: {ISO-8601}
diagnostics:
  component_type_detected: cli|http|file-parser|process|database|api
  pattern_applied: "CLI Command Verification"
  template_language: bash|node|python
  files_analyzed: 1
  completion_status: success
```
