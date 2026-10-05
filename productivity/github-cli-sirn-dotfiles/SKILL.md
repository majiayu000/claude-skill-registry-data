---
name: github-cli
type: reference
description: Reference for GitHub CLI (gh) - READ-ONLY operations only. ALWAYS read BEFORE using gh commands to ensure correct syntax and available flags.
---

## GitHub CLI Reference (gh)

**IMPORTANT**: This skill is for READ-ONLY operations only. DO NOT execute any commands that create, modify, or delete resources.

### Repository Identification

**Always be specific about which repository to use.**

| Method        | Command                      |
| ------------- | ---------------------------- |
| Use `-R` flag | `gh <command> -R owner/repo` |
| List remotes  | `git remote -v`              |

**Best Practice**: Use `-R owner/repo` explicitly instead of relying on the default repository to avoid ambiguity.

### Issues (Read-Only)

| Task             | Command                                      |
| ---------------- | -------------------------------------------- |
| List issues      | `gh issue list -R owner/repo`                |
| View issue       | `gh issue view <number> -R owner/repo`       |
| View issue (web) | `gh issue view <number> -R owner/repo --web` |
| Issue status     | `gh issue status -R owner/repo`              |

**List options**: `--state open|closed|all`, `--label bug`, `--assignee @me`, `--limit 10`

### Pull Requests (Read-Only)

| Task           | Command                               |
| -------------- | ------------------------------------- |
| List PRs       | `gh pr list -R owner/repo`            |
| View PR        | `gh pr view <number> -R owner/repo`   |
| View PR diff   | `gh pr diff <number> -R owner/repo`   |
| View PR checks | `gh pr checks <number> -R owner/repo` |
| PR status      | `gh pr status -R owner/repo`          |

**List options**: `--state open|closed|merged|all`, `--label enhancement`, `--draft`, `--limit 10`

### Repository (Read-Only)

| Task            | Command                         |
| --------------- | ------------------------------- |
| View repo info  | `gh repo view owner/repo`       |
| View repo (web) | `gh repo view owner/repo --web` |
| List your repos | `gh repo list`                  |
| List org repos  | `gh repo list <org>`            |

### GitHub Actions - Workflow Runs (Read-Only)

| Task         | Command                                    |
| ------------ | ------------------------------------------ |
| List runs    | `gh run list -R owner/repo`                |
| View run     | `gh run view <run-id> -R owner/repo`       |
| View run log | `gh run view <run-id> -R owner/repo --log` |
| Watch run    | `gh run watch <run-id> -R owner/repo`      |

**List options**: `--workflow <name>`, `--branch <branch>`, `--limit 10`, `--status completed|failed|in_progress`

### GitHub Actions - Workflows (Read-Only)

| Task               | Command                          |
| ------------------ | -------------------------------- | ------------------------- |
| List workflows     | `gh workflow list -R owner/repo` |
| View workflow      | `gh workflow view <name          | id> -R owner/repo`        |
| View workflow YAML | `gh workflow view <name          | id> -R owner/repo --yaml` |

### GitHub Actions - Cache (Read-Only)

| Task        | Command                       |
| ----------- | ----------------------------- |
| List caches | `gh cache list -R owner/repo` |

**List options**: `--limit 10`, `--sort size|created_at`, `--order asc|desc`

### Releases (Read-Only)

| Task          | Command                                  |
| ------------- | ---------------------------------------- |
| List releases | `gh release list -R owner/repo`          |
| View release  | `gh release view <tag> -R owner/repo`    |
| View latest   | `gh release view --latest -R owner/repo` |

### Search (Read-Only)

| Task           | Command                     |
| -------------- | --------------------------- |
| Search repos   | `gh search repos <query>`   |
| Search issues  | `gh search issues <query>`  |
| Search PRs     | `gh search prs <query>`     |
| Search code    | `gh search code <query>`    |
| Search commits | `gh search commits <query>` |

**Examples**:

```bash
gh search repos "language:go stars:>1000"
gh search issues "is:open label:bug repo:cli/cli"
gh search code "function main" --language=go
```

### Status (Read-Only)

| Task          | Command                                   |
| ------------- | ----------------------------------------- |
| View status   | `gh status`                               |
| Org status    | `gh status -o <org>`                      |
| Exclude repos | `gh status -e owner/repo1 -e owner/repo2` |

Shows assigned issues, PRs, review requests, mentions across your subscribed repositories.

### API (Read-Only GET Requests)

| Task           | Command                                      |
| -------------- | -------------------------------------------- |
| GET endpoint   | `gh api <endpoint> -R owner/repo`            |
| With jq filter | `gh api <endpoint> -R owner/repo --jq '.[]'` |
| Paginate       | `gh api <endpoint> -R owner/repo --paginate` |

**Examples**:

```bash
gh api repos/owner/repo/issues --paginate
gh api repos/owner/repo/pulls -q '.[] | {number, title}'
gh api graphql -f query='query { viewer { login } }'
```

### Common Output Options

| Goal | Flag | Example |
| --- | --- | --- | --- | --- |
| JSON output | `--json` | `gh issue list -R owner/repo --json number,title,state` |
| JSON fields | `--json <fields>` | `gh pr view 123 -R owner/repo --json headRefName,baseRefName` |
| Quiet (IDs only) | `--jq '.[] | .number'` | `gh issue list -R owner/repo --jq '.[] | .number'` |
| Web browser | `--web` | `gh issue view 123 -R owner/repo --web` |

### Identifying the Current Repository

Before running commands, determine the repository:

```bash
# From git remote
git remote -v

# From jj (if using Jujutsu)
jj git remote list
```

**Always use explicit `-R owner/repo`** to ensure you're querying the correct repository.
