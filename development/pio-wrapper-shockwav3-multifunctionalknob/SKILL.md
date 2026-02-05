---
name: pio-wrapper
description: Filters PlatformIO output to reduce token usage in agentic tools. Returns success confirmation on successful builds and only error lines on failures instead of full logs. Use when agentic tools need to run PlatformIO commands to reduce context token consumption.
---

# PlatformIO Cli (pio) Wrapper

## Overview

This skill provides a transparent wrapper for PlatformIO (`pio`) commands that dramatically reduces token usage by filtering verbose build output. Instead of agentic tools receiving entire build logs, this wrapper returns:

- **On success**: A simple confirmation message
- **On error**: Only the relevant error lines, not the full log

This keeps your token budget for more important context while still providing agentic tools with actionable error information for debugging.

## How It Works

The wrapper script (`scripts/pio-wrapper.py`) intercepts all PlatformIO commands and:

1. Runs the `pio` command with all provided arguments
2. Captures both stdout and stderr
3. Checks the exit code
4. Filters and returns appropriate output

### Success Case

When a PlatformIO command completes successfully (exit code 0), agentic tools receive:

```
✓ PlatformIO command succeeded
```

This confirms the operation worked without wasting tokens on verbose success output.

### Error Case

When a command fails, the wrapper extracts only error-related lines that contain:
- Keywords like "error", "failed" (case insensitive)
- ANSI color codes indicating red text (typical error formatting)

Example error output:

```
✗ PlatformIO command failed. Errors:
In file included from src/main.cpp:5:
include/config.h:12:10: error: 'UNDEFINED_CONSTANT' was not declared in this scope
  int val = UNDEFINED_CONSTANT;
           ^
```

## Usage

When using this skill, agentic tools should call the wrapper script instead of running `pio` directly:

```bash
/path/to/skill/scripts/pio-wrapper.py run -e use_nimble
```

The wrapper accepts all the same arguments as the standard `pio` command and transparently filters the output.

## Token Savings

For a typical failed PlatformIO build:
- **Standard output**: 2000-5000 tokens (entire build log)
- **Wrapped output**: 50-200 tokens (error lines only)

This 10-50x reduction keeps your context window available for actual implementation work.
