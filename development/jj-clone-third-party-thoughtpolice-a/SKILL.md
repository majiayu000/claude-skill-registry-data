---
name: jj-clone-third-party
description: Clone external repositories into work/ directory for examination and source code research. Use when needing to understand third-party dependency implementations, debug upstream issues, or research API usage patterns. (project)
---

# Jj Clone Third Party

## Overview

Clone external repositories into the `work/` directory for examination without affecting the main repository. This workflow enables source code research, dependency exploration, and upstream debugging while keeping external code isolated and gitignored.

## When to Use

Use this skill when:
- Understanding how a third-party dependency implements a feature
- Researching API usage patterns or behavior in upstream libraries
- Debugging issues that might originate in dependencies
- Examining source code of tools or libraries used in the project
- Exploring alternative libraries before adding them as dependencies

## Workflow

### 1. Identify the Repository

Determine the Git URL for the repository to examine. Common sources:
- GitHub: `https://github.com/owner/repo`
- GitLab: `https://gitlab.com/owner/repo`
- Package registries often link to source repositories

### 2. Clone into work/ Directory

Use `jj git clone` to clone the repository into `work/`:

```bash
jj git clone <repository-url> work/<descriptive-name>
```

**Examples:**
```bash
# Clone tokio to understand async runtime internals
jj git clone https://github.com/tokio-rs/tokio work/tokio

# Clone serde to examine serialization implementation
jj git clone https://github.com/serde-rs/serde work/serde

# Clone Buck2 to understand build system behavior
jj git clone https://github.com/facebook/buck2 work/buck2
```

**Important:** The clone is completely isolated from the main repository's history. It's stored under `work/` which is gitignored, so it won't affect version control.

### 3. Examine the Code

Navigate into the cloned directory and use standard tools:

```bash
cd work/<repo-name>

# Search for specific functions or patterns
rg "pattern" .

# Read specific files
cat path/to/file

# Explore directory structure
tree -L 2
```

Alternatively, use absolute paths from the repository root:

```bash
# Search without changing directory
rg "pattern" work/<repo-name>

# Read files using absolute paths
cat work/<repo-name>/path/to/file
```

### 4. Clean Up When Done

Remove the cloned repository when the examination is complete:

```bash
rm -rf work/<repo-name>
```

The repository is not tracked by version control, so deletion won't affect the main repository.

## Best Practices

### Use Descriptive Names

Choose clear directory names that indicate the purpose:
- `work/tokio` - Good: immediately clear what it contains
- `work/async-research` - Better if examining multiple async libraries
- `work/temp` - Poor: unclear purpose

### Navigate Efficiently

Prefer absolute paths from the repository root over changing directories:
```bash
# Preferred: stay in repo root
rg "Runtime::new" work/tokio/tokio/src

# Alternative: change directory
cd work/tokio && rg "Runtime::new" tokio/src
```

### Leverage Existing Tools

Use Read, Grep, and Glob tools to examine cloned code efficiently:
- Grep for searching patterns across files
- Read for viewing specific files
- Glob for finding files by pattern

### Document Findings

When examining third-party code to solve a problem, document key findings before cleanup:
- Note relevant file paths and line numbers
- Copy important code snippets into notes or comments
- Record insights about how the dependency works

## Limitations

- **No version control integration:** The clone is a separate jj repository, not integrated with the main repo's history
- **Manual cleanup required:** The repository remains in `work/` until manually deleted
- **Not suitable for modifications:** For testing patches to upstream, use the `jj-graft-third-party` skill instead

## Related Skills

- `jj-graft-third-party` - For integrating third-party repos to test patches
- `jj-workspace-experiments` - For creating isolated workspaces to test changes
