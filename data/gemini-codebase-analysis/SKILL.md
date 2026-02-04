---
name: gemini-codebase-analysis
description: Analyze large codebases using Gemini CLI's massive context window. Use when analyzing entire codebases, comparing multiple large files, understanding project-wide patterns, verifying feature implementations, or when context limits are exceeded.
allowed-tools: Bash
---

# Gemini CLI for Large Codebase Analysis

Use the Gemini CLI with its massive context window to analyze large codebases or multiple files that might exceed context limits.

## Basic Syntax

```bash
gemini -p "@<path> <your question or prompt>"
```

The `@` syntax includes files and directories in your prompt. Paths are relative to your current working directory.

## File and Directory Inclusion

### Single file
```bash
gemini -p "@src/main.py Explain this file's purpose and structure"
```

### Multiple files
```bash
gemini -p "@package.json @src/index.js Analyze the dependencies used in the code"
```

### Entire directory
```bash
gemini -p "@src/ Summarize the architecture of this codebase"
```

### Multiple directories
```bash
gemini -p "@src/ @tests/ Analyze test coverage for the source code"
```

### Current directory and subdirectories
```bash
gemini -p "@./ Give me an overview of this entire project"
```

### Using --all_files flag
```bash
gemini --all_files -p "Analyze the project structure and dependencies"
```

## Implementation Verification Examples

### Check if a feature is implemented
```bash
gemini -p "@src/ @lib/ Has dark mode been implemented in this codebase? Show me the relevant files and functions"
```

### Verify authentication implementation
```bash
gemini -p "@src/ @middleware/ Is JWT authentication implemented? List all auth-related endpoints and middleware"
```

### Check for specific patterns
```bash
gemini -p "@src/ Are there any React hooks that handle WebSocket connections? List them with file paths"
```

### Verify error handling
```bash
gemini -p "@src/ @api/ Is proper error handling implemented for all API endpoints? Show examples of try-catch blocks"
```

### Check for rate limiting
```bash
gemini -p "@backend/ @middleware/ Is rate limiting implemented for the API? Show the implementation details"
```

### Verify caching strategy
```bash
gemini -p "@src/ @lib/ @services/ Is Redis caching implemented? List all cache-related functions and their usage"
```

### Check for security measures
```bash
gemini -p "@src/ @api/ Are SQL injection protections implemented? Show how user inputs are sanitized"
```

### Verify test coverage
```bash
gemini -p "@src/payment/ @tests/ Is the payment processing module fully tested? List all test cases"
```

## When to Use This Skill

- Analyzing entire codebases or large directories
- Comparing multiple large files
- Understanding project-wide patterns or architecture
- Current context window is insufficient for the task
- Working with files totaling more than 100KB
- Verifying if specific features, patterns, or security measures are implemented
- Checking for the presence of certain coding patterns across the entire codebase

## Important Notes

- Paths in `@` syntax are relative to your current working directory when invoking gemini
- The CLI will include file contents directly in the context
- No need for `--yolo` flag for read-only analysis
- Gemini's context window can handle entire codebases that would overflow Claude's context
- Be specific about what you're looking for to get accurate results
