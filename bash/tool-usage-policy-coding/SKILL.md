---
name: tool-usage-policy-coding
description: >
  Tool usage guidelines for code execution tasks. Covers bash and Python
  execution, dependency management, error handling, file organization,
  data analysis, and security best practices.
---

# Tool Usage Policy — Coding

## Primary Tools

- **bash**: Run shell commands, install packages, manage files.
- **python_execute**: Run Python scripts for computation and data analysis.
- **read_file / edit_file**: Read and modify source files and data.
- **calculator**: Use for arithmetic — NEVER calculate mentally.

## Core Responsibilities

- **Code Execution**: Run code snippets, scripts, and commands to produce
  results.
- **Data Processing**: Download, parse, transform, and analyse data files
  (CSV, JSON, etc.).
- **Computation**: Perform numerical calculations, statistical analysis,
  or algorithmic processing.
- **File Operations**: Read, write, and manipulate files as needed.

## Best Practices

1. **Plan before coding** — break the task into clear steps. Understand
   what input you need and what output is expected.
2. **Dependency management** — install required packages before running
   code (e.g., `pip install <package>` via `bash`). Verify installation
   with `python -c "import <module>"`.
3. **Error handling** — if a command fails, examine the error message
   carefully. Fix the root cause — do NOT blindly retry the same command.
4. **File organization** — use clear file names and absolute paths. Keep
   working files organized in a project directory.
5. **Verify results** — always check that code ran successfully and the
   output is correct before reporting.
6. **Security** — be cautious when running scripts from untrusted sources.
   Review code before execution.
7. **Output capture** — save or capture output of executed code. If output
   is large, summarise key findings.

## Do NOT

- Do NOT calculate mentally — always use `calculator` or `python_execute`.
- Do NOT blindly retry failed commands without fixing the underlying issue.
- Do NOT run resource-intensive processes without justification.
- Do NOT leave large temporary files behind — clean up after yourself.
