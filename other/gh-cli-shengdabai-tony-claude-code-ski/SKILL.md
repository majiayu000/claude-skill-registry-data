---
name: gh-cli
description: This skill should be used when working with GitHub CLI (gh) for any task including code search, workflow debugging, GitHub Pages deployment, or general GitHub operations. Use this skill for enhanced code search capabilities, analyzing failed workflow runs, managing GitHub Pages, or any gh command usage.
---

# GitHub CLI (gh)

## Overview

Provides specialized utilities for GitHub CLI operations with three powerful Python tools for common workflows, plus general guidance for effective gh command usage.

## Core Capabilities

### 1. Enhanced Code Search
Use `scripts/gh_code_search.py` for advanced GitHub code search with filtering, formatting, and sorting capabilities.

**Key features:** Multiple output formats, rate limiting handling, fork/private repo filtering, match count filtering

**Documentation:** `references/README_gh_code_search.md`

### 2. Workflow Failure Analysis
Use `scripts/gh_failed_run.py` to analyze GitHub Actions workflow failures and extract detailed error information.

**Key features:** Finds most recent failed run, extracts error patterns from logs, outputs structured JSON with run info and failed jobs

**Documentation:** `references/README_gh_failed_run.md`

### 3. GitHub Pages Management
Use `scripts/gh_pages_deploy.py` for GitHub Pages deployment automation including enabling Pages, status checks, and workflow generation.

**Key features:** Enable/configure Pages, check deployment status, trigger rebuilds, generate workflow templates

**Documentation:** `references/README_pages.md`

## General GitHub CLI Best Practices

When working with GitHub CLI:

- Prefer `gh` commands over raw `git` commands for GitHub-specific operations (issues, PRs, releases)
- Use `gh repo view` to quickly inspect repository details
- Leverage `gh pr create --web` or `gh issue create --web` for interactive workflows
- Check `gh --help` for discovering subcommands and capabilities
- Use `gh alias` to create shortcuts for frequently used command patterns

## Using the Python Utilities

All scripts accept `--help` for detailed usage information. Run them directly with Python 3:

```bash
python3 scripts/gh_code_search.py --help
python3 scripts/gh_failed_run.py --help
python3 scripts/gh_pages_deploy.py --help
```

Refer to the respective README files in `references/` for comprehensive documentation, examples, and troubleshooting guidance.
