---
name: gitinjest
description: Convert GitHub repositories into LLM-friendly text. Use when you need to analyze external codebases, research unfamiliar libraries, understand third-party project structure, or ingest code from GitHub URLs (public/private, supports subdirectories).
---

# Gitingest

Convert GitHub repos into text format using the CLI - output streams to stdout by default.

# Gitingest CLI Commands for External Codebase Analysis

Key lesson: Always search broadly first (-i "*.ts" for TypeScript, -i "*.py" for Python, etc.) before narrowing down. The commands are powerful, but your search scope determines what you find.

## Installation

```bash
pipx install gitingest
```

## Default Usage (Streaming to stdout)

```bash
# Stream output directly (no file created)
gitingest https://github.com/username/repo -o -

# Capture in variable for processing
output=$(gitingest https://github.com/username/repo -o -)
```

## Private Repositories

```bash
# Set token as environment variable
export GITHUB_TOKEN=github_pat_...
gitingest https://github.com/username/private-repo -o -

# Or pass directly
gitingest https://github.com/username/private-repo --token github_pat_... -o -
```

## Subdirectories

```bash
# Analyze only specific part of repo
gitingest https://github.com/user/repo/tree/main/src -o -
```

## Basic Usage

- `gitingest https://github.com/user/repo -o -` - Get full repo overview (stdout)
- `gitingest https://github.com/user/repo --include-submodules -o -` - Include submodules

## File/Content Search

- `gitingest https://github.com/user/repo -i "pattern" -o -` - Search files containing pattern
- `gitingest https://github.com/user/repo -i "*filename*" -o -` - Find files by name/glob
- `gitingest https://github.com/user/repo -i "path/to/file" -o -` - Get specific file content

## Filtering

- `gitingest https://github.com/user/repo -e "pattern" -o -` - Exclude files matching pattern
- `gitingest https://github.com/user/repo -i "*.ts" -e "node_modules/*" -o -` - Include TS files, exclude node_modules


## Key Options

- `-o -` or `--output -`: Stream to stdout (no temp file)
- `--token` or `-t`: GitHub token for private repos
- `--include-submodules`: Include git submodules
- `--include-gitignored`: Include files normally ignored by .gitignore

## Output Structure

The CLI returns formatted text with:
- Summary: File count, size, token count
- Tree: Directory visualization
- Content: All code combined and formatted