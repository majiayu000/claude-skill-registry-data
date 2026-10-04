---
name: codacy-cloud-cli
description: Uses the Codacy Cloud CLI to query repositories, issues, security findings, pull requests, tools, and patterns on Codacy Cloud. Use whenever the user mentions Codacy, asks about code quality metrics, wants to check issues or findings in a repo, inspect a pull request analysis, browse security vulnerabilities, enable or disable tools, search patterns, trigger a reanalysis, or interact with any remote Codacy data — even if they don't say "Codacy CLI" explicitly.
license: MIT
metadata:
  author: Codacy
  version: 1.5.0
---

# Codacy Cloud CLI

> **Glossary:** See [glossary.md](../../references/glossary.md) for shared definitions of Codacy concepts (issues, findings, severity, coverage, tools, patterns, etc.).

The Codacy Cloud CLI (`codacy`) is the command-line interface for Codacy Cloud. Use it whenever the user wants to interact with remote Codacy data. This is a different tool from the Codacy Analysis CLI (`codacy-analysis`), which runs static analysis locally.

## Setup

```bash
# Install
npm install -g @codacy/codacy-cloud-cli

# Authenticate — 3 options:
# 1. Set the `CODACY_API_TOKEN` environment variable
export CODACY_API_TOKEN=<token>
# 2. Use the `codacy login` command (interactive login)
codacy login
# 3. Use the `codacy login` command (with token input)
codacy login --token <token>
# Obtain tokens: Codacy > My Account > Access Management > Account API Tokens (https://app.codacy.com/account/access-management)

# Verify
codacy info
```

**Shared session:** The Cloud CLI and the Analysis CLI (`codacy-analysis`) share the same credentials at `~/.codacy/credentials`. Logging in or out with either CLI applies to both — there is no need to authenticate separately.

## Getting help

The CLI is the authoritative source of truth. Always use `--help` to discover available commands, options, and current behavior:

```bash
codacy --help
codacy <command> --help
# e.g. codacy issues --help
```

Use `--output json` on any command for machine-readable output.

## Provider values

See the [Provider section in the glossary](../../references/glossary.md#provider) for the full table of CLI values (`gh`, `gl`, `bb`).

## Auto-detection of repository parameters

The CLI auto-detects the `provider`, `organization`, and `repository` from the git remote origin URL when run inside a repository. This means most commands work without specifying these parameters explicitly:

```bash
# Auto-detected (run inside the repo)
codacy issues
codacy repository
codacy pull-request 42

# Equivalent explicit form
codacy issues gh my-org my-repo
codacy repository gh my-org my-repo
codacy pull-request gh my-org my-repo 42
```

Auto-detection supports GitHub, GitLab, and Bitbucket remote URLs. If the remote cannot be parsed (e.g., non-standard hosting), pass the parameters explicitly. All examples in this document use the explicit form for clarity, but the short form is preferred when running inside a repo.

## How Codacy data works

- **Data reflects the HEAD commit** — issue lists, coverage, and security findings always show the state of the latest analyzed commit on the branch or pull request. There is no per-file or per-line historical view.
- **Configuration changes are not instant** — enabling/disabling tools or patterns, changing parameters, and ignoring issues only take effect after the next analysis. That means either triggering a reanalysis via `--reanalyze` or waiting for the next commit to be pushed.
- **Organization standards are enforced and cannot be overridden at repository level** — if a pattern is enforced by a Coding Standard at the organization level, its enabled/disabled state and parameters cannot be changed per-repository. To change it, the standard must be updated at the organization level.

### Reanalysis

Use `--reanalyze-and-wait` (`-w`) on the `repository` or `pull-request` commands to trigger reanalysis and block until it completes. The CLI captures a baseline, triggers reanalysis, polls every 10 seconds (up to 20 minutes), and reports issue deltas by pattern, severity, and category with timing information. Supports `--output json` for machine-readable delta reports.

```bash
# Trigger reanalysis and wait for results (preferred)
codacy repository gh my-org my-repo --reanalyze-and-wait
codacy repository gh my-org my-repo -w -o json    # JSON delta report

# Fire-and-forget reanalysis (no waiting)
codacy repository gh my-org my-repo --reanalyze
```

When using `--reanalyze` without `--and-wait`, check progress manually by re-running the command without `--reanalyze`:
- **Table output:** look at the "Analysis" field — `"Reanalysis in progress..."` means it is still running; `"Finished X ago"` means it is done
- **JSON output:** compare the `startedAnalysis` and `endedAnalysis` timestamps — complete when `startedAnalysis` > trigger time AND `endedAnalysis` > `startedAnalysis`

## Command reference

### Account & repositories

```bash
# Authenticated user and organizations
codacy info

# List repositories in an organization
codacy repositories <provider> <org>
codacy repositories gh my-org --search my-repo

# Repository dashboard (metrics, PRs, issues overview)
codacy repository gh my-org my-repo
codacy repository gh my-org my-repo --add       # add to Codacy
codacy repository gh my-org my-repo --remove    # remove from Codacy
codacy repository gh my-org my-repo --follow    # follow repository
codacy repository gh my-org my-repo --unfollow  # unfollow repository
codacy repository gh my-org my-repo --reanalyze            # trigger reanalysis (fire-and-forget)
codacy repository gh my-org my-repo --reanalyze-and-wait   # trigger and wait for completion with delta report
codacy repository gh my-org my-repo --link-standard <id>   # link a coding standard
codacy repository gh my-org my-repo --unlink-standard <id> # unlink a coding standard
```

### Issues (code quality)

```bash
# List issues with optional filters
codacy issues gh my-org my-repo
codacy issues gh my-org my-repo --branch main --severities Critical,High
codacy issues gh my-org my-repo --categories Security
codacy issues gh my-org my-repo --tools eslint,semgrep        # filter by detecting tool
codacy issues gh my-org my-repo --limit 500                    # fetch up to N results (default 100, max 1000)

# Overview: totals grouped by category/severity/language
codacy issues gh my-org my-repo --overview                     # short flag: -O
codacy issues gh my-org my-repo -O -o json                     # JSON — includes per-pattern issue counts and false positive counts
```

The `--overview` output includes:
- **False positive counts** per pattern — labeled as "Not a False Positive" / "Potential False Positive"
- **Suggested actions to reduce noise** — identifies patterns accounting for 10%+ of all issues or 3x the average per-pattern count, and generates ready-to-run `codacy pattern` disable commands for each. If a pattern is enforced by a coding standard or uses a config file, the suggestion adapts accordingly (e.g., suggests editing the coding standard or the config file instead)

```bash
# Full details for a single issue
codacy issue gh my-org my-repo <issueId>

# Ignore / unignore an issue
codacy issue gh my-org my-repo <issueId> --ignore
codacy issue gh my-org my-repo <issueId> --ignore --ignore-reason FalsePositive --ignore-comment "Not applicable here"
codacy issue gh my-org my-repo <issueId> --unignore

# Bulk-ignore all issues matching filters
codacy issues gh my-org my-repo --severities Minor --categories CodeStyle --ignore
```

Filters: `--branch`, `--patterns`, `--severities` (Critical,High,Medium,Minor), `--categories`, `--languages`, `--tools`, `--tags`, `--authors`

Ignore reasons: `AcceptedUse` (default) | `FalsePositive` | `NotExploitable` | `TestCode` | `ExternalCode`

### Security findings

```bash
# List findings
codacy findings gh my-org my-repo
codacy findings gh my-org                       # org-wide
codacy findings gh my-org my-repo --severities Critical,High
codacy findings gh my-org my-repo --statuses Overdue,DueSoon
codacy findings gh my-org my-repo --limit 500   # fetch up to N results (default 100, max 1000)

# Full details for a single finding (includes CVE data)
codacy finding gh my-org my-repo <findingId>

# Ignore / unignore a finding
codacy finding gh my-org my-repo <findingId> --ignore
codacy finding gh my-org my-repo <findingId> --ignore --ignore-reason FalsePositive --ignore-comment "Verified safe"
codacy finding gh my-org my-repo <findingId> --unignore
```

Filters: `--search`, `--severities` (Critical,High,Medium,Low), `--statuses` (Overdue,OnTrack,DueSoon,ClosedOnTime,ClosedLate,Ignored), `--categories`, `--scan-types`, `--dast-targets`

Ignore reasons: `AcceptedUse` (default) | `FalsePositive` | `NotExploitable` | `TestCode` | `ExternalCode`

### Pull requests

```bash
# PR summary (status, issues, coverage, changed files)
codacy pull-request gh my-org my-repo <prNumber>

# Annotated git diff with coverage and inline issues
codacy pull-request gh my-org my-repo <prNumber> --diff

# Full details for a specific issue within the PR
codacy pull-request gh my-org my-repo <prNumber> --issue <issueId>

# Ignore a specific issue in the PR
codacy pull-request gh my-org my-repo <prNumber> --ignore-issue <issueId>
codacy pull-request gh my-org my-repo <prNumber> --ignore-issue <issueId> --ignore-reason FalsePositive
codacy pull-request gh my-org my-repo <prNumber> --unignore-issue <issueId>

# Ignore all potential false positive issues in the PR at once
codacy pull-request gh my-org my-repo <prNumber> --ignore-all-false-positives

# Trigger reanalysis of PR HEAD commit
codacy pull-request gh my-org my-repo <prNumber> --reanalyze
codacy pull-request gh my-org my-repo <prNumber> --reanalyze-and-wait   # trigger and wait for completion
```

### Tools & patterns

```bash
# List all tools (enabled/disabled)
codacy tools gh my-org my-repo

# Enable or disable a tool
codacy tool gh my-org my-repo eslint --enable
codacy tool gh my-org my-repo eslint --disable
codacy tool gh my-org my-repo eslint --configuration-file true

# List patterns for a tool
codacy patterns gh my-org my-repo eslint
codacy patterns gh my-org my-repo eslint --enabled --categories Security
codacy patterns gh my-org my-repo pylint --search W0123

# Full details for a specific pattern (description, parameters, severity, category)
codacy pattern gh my-org my-repo eslint no-unused-vars

# Enable, disable, or configure a pattern
codacy pattern gh my-org my-repo eslint no-unused-vars --enable
codacy pattern gh my-org my-repo eslint no-unused-vars --disable
codacy pattern gh my-org my-repo eslint max-len --parameter max=120

# Enable or disable all patterns matching specific filters
codacy patterns gh my-org my-repo eslint --categories Security --severities Critical,High --enable-all
codacy patterns gh my-org my-repo pylint --categories CodeStyle --severities Minor --disable-all
```

**Configuration file and coding standard awareness:**
- When a tool uses a local configuration file (`--configuration-file true`), `codacy patterns` skips fetching managed patterns (they don't apply)
- When a pattern is enforced by a coding standard, `--enable`/`--disable` will refuse the operation with a message indicating which standard enforces it. Update the coding standard at the organization level instead, or unlink the standard from the repository first (`codacy repository ... --unlink-standard <id>`)

Pattern search tip: Codacy pattern IDs combine tool prefix and original ID. Use `--search` with the original ID to find them:
```bash
codacy patterns gh my-org my-repo semgrep --search HttpGetHTTPRequest
codacy patterns gh my-org my-repo pylint --search W0123
```

### Importing configuration

```bash
# Import tool and pattern configuration from a local config file
codacy tools gh my-org my-repo --import                          # imports from .codacy/codacy.config.json (default path)
codacy tools gh my-org my-repo --import ./custom-config.json     # imports from a custom path
codacy tools gh my-org my-repo --import -y                       # skip confirmation prompt
codacy tools gh my-org my-repo --import --force -y               # unlink coding standard first, then import
```

The `--import` flag reads a local `.codacy/codacy.config.json` (or a specified path) and applies the tool and pattern configuration to the Codacy Cloud repository. Use `-y` (`--skip-approval`) to skip the interactive confirmation. Use `--force` to unlink the repository from its Coding Standard before importing — this is required when org-level standards block pattern changes.

**Import behavior:**
- Preserves cloud-only tools during import — only tools supported locally are modified; cloud-only tools (e.g., SonarSharp, Codacy ScalaMeta Pro) keep their existing enabled/disabled state
- Handles config-file mode correctly — when a tool uses a local configuration file, the import skips resetting its managed patterns (they don't apply)
- Surfaces structured API error details on import failures, including which tools/patterns conflicted and why

**Note:** The `.codacy/codacy.config.json` file is for local analysis only. Committing it to the repository does NOT affect Codacy Cloud. The `--import` command is the only way to sync local config to Cloud.

## Common workflows

**Check critical security issues in a repo:**
```bash
codacy findings gh my-org my-repo --severities Critical,High
```

**Review what a PR introduced:**
```bash
codacy pull-request gh my-org my-repo 42
codacy pull-request gh my-org my-repo 42 --diff
```

**Understand a specific issue:**
```bash
codacy issue gh my-org my-repo <issueId>   # includes pattern docs and code context
```

**Trigger reanalysis and wait for results:**
```bash
codacy repository gh my-org my-repo --reanalyze-and-wait
codacy repository gh my-org my-repo -w -o json    # JSON delta report with issue changes by pattern/severity/category
```

**Identify and reduce noise:**
```bash
codacy issues gh my-org my-repo --overview        # see false positive counts and suggested actions to reduce noise
```
