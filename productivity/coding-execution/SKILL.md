---
name: coding-execution
description: >
  Workflow for writing and executing code (bash, Python) to accomplish
  computation, data processing, and scripting tasks. Covers planning,
  dependency management, error handling, file organization, and result
  verification.
---

# Code Execution Skill

## Mission

Write and execute code (bash commands, Python scripts) to accomplish the
task. You have access to `bash` and `python_execute` tools for running
code, plus file tools for managing data.

## Workflow

1. **Plan before coding** — break the task into clear steps. Understand
   what input you need, what output is expected, and what tools to use.
2. **Execute code carefully**:
   - Write code to a file or run it directly via `bash` or `python_execute`.
   - **Dependency management**: Install any required packages before running
     code (e.g. `pip install <package>` via `bash`).
   - **Error handling**: If a command fails, examine the error message
     carefully. Fix the root cause — do NOT blindly retry the same command.
   - **File organization**: Use clear file names and absolute paths. Keep
     working files organized in a project directory.
   - **Verify results**: Always check that code ran successfully and the
     output is correct before reporting.
3. **Report results** — include the code you ran, its output, and any
   computed values or analysis results.

## Core Responsibilities

- **Code Execution**: Run code snippets, scripts, and commands to produce
  results.
- **Data Processing**: Download, parse, transform, and analyse data files
  (CSV, JSON, etc.).
- **Computation**: Perform numerical calculations, statistical analysis,
  or algorithmic processing.
- **File Operations**: Read, write, and manipulate files as needed.

## Best Practices

- **Environment Setup**: Before running code, ensure all necessary
  dependencies are installed. Use `pip install` for Python packages.
- **Error Handling**: If a command fails, carefully examine the error
  message to diagnose the problem. Do **not** blindly retry without
  addressing the underlying issue.
- **File Management**: Keep the file system organized. Use subdirectories
  for projects. Always use absolute paths when referencing files.
- **Data Analysis**: Use appropriate libraries (e.g. pandas, numpy for
  Python). Visualise data when necessary to gain insights.
- **Security**: Be cautious when running scripts from untrusted sources.
  Review code before execution.
- **Output Capture**: Always save or capture the output of executed code.
  If output is large, summarise key findings.
