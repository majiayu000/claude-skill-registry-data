---
name: serena-workflow
description: Best practices for activating and utilizing the Serena MCP toolset. Use this skill when working in a Serena-enabled project to ensure correct project activation (including WSL handling) and to leverage semantic tools for code navigation and editing.
metadata:
  short-description: Activate and use Serena MCP tools
---

# Serena Workflow Guidelines

This skill outlines the standard procedure for working with Serena MCP tools, ensuring consistent project activation and efficient code manipulation.

## 1. Project Activation

Before performing any code operations, you must activate the Serena project.

### WSL Environment Strategy
If you are operating in a WSL environment (paths starting with `/home/...`):
1.  **Primary Method**: Attempt activation using the UNC path format:
    `\\wsl$\Ubuntu<absolute_path>`
    (e.g., `\\wsl$\Ubuntu\home\user\repo`)
2.  **Fallback**: Use the standard Linux path only if the UNC path activation fails.

### Onboarding Check
Immediately after activation:
1.  Run `check_onboarding_performed`.
2.  If it returns `false`, you **MUST** run the `onboarding` tool before proceeding with any other tasks.

## 2. Serena-First Workflow

Prioritize Serena's semantic capabilities over standard file operations for code-related tasks.

- **Code Navigation**: Use semantic search tools to find symbols and references instead of `grep` or `find`.
- **Refactoring**: Leverage Serena's automated refactoring tools for safe code changes.
- **File Operations**: Reserve standard shell commands for non-code files or simple, non-semantic text processing.
