---
name: setup-tagpr
description: Set up tagpr for automated release management in a repository. tagpr automatically creates and updates pull requests for unreleased items, tags them when merged, and creates GitHub Releases. Use this skill when users want to (1) introduce tagpr to their repository, (2) set up automated releases with tagpr, (3) configure tagpr with goreleaser for Go projects, (4) enable immutable releases with tagpr, or (5) set up release workflow for TypeScript/Node.js projects.
---

# Setup tagpr

This skill guides you through setting up [tagpr](https://github.com/Songmu/tagpr) for automated release management.

## What is tagpr?

tagpr is a GitHub Actions tool that:
- Automatically creates pull requests for pending releases
- Suggests semantic version increments based on commit history
- Tags commits when PRs merge
- Creates GitHub Releases automatically

## Prerequisites

**GH_PAT (Personal Access Token)**: tagpr requires a GitHub Personal Access Token with `repo` and `workflow` permissions to push tags and trigger subsequent workflows. Create a PAT and add it as a repository secret named `GH_PAT`.

Why not `GITHUB_TOKEN`? The default token cannot trigger other workflows when pushing tags, which is required for release workflows.

## Setup Workflow

1. **Determine the project type**:
   - **Go project with goreleaser?** → See [references/goreleaser-integration.md](references/goreleaser-integration.md)
   - **TypeScript/Node.js project?** → Follow "TypeScript/Node.js workflow" below
   - **Other projects** → Follow "Standard workflow" below

2. **Standard workflow**:
   1. Create GH_PAT and add as repository secret
   2. Create `.tagpr` configuration file
   3. Create GitHub Actions workflow file

3. **TypeScript/Node.js workflow**:
   1. Create GH_PAT and add as repository secret
   2. Create `.tagpr` configuration file with `versionFile` and `command`
   3. Create GitHub Actions workflow with asset upload

## Configuration Files

### .tagpr Configuration

Create `.tagpr` file at the repository root.

**Standard configuration (version from git tags only):**
```gitconfig
[tagpr]
    releaseBranch = main
    versionFile = -
    vPrefix = true
    release = draft
```

**Go project with version.go:**
```gitconfig
[tagpr]
    releaseBranch = main
    versionFile = version.go
    vPrefix = true
    release = draft
```

**TypeScript/Node.js project (e.g., Obsidian plugin):**
```gitconfig
[tagpr]
    releaseBranch = main
    versionFile = manifest.json,package.json
    vPrefix = true
    changelog = true
    release = draft
    majorLabels = major
    minorLabels = minor
    command = npm run build
```

#### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `releaseBranch` | Target branch for releases | `main` |
| `versionFile` | File(s) containing semantic version. Use `-` for git tags only. Multiple files can be comma-separated | - |
| `vPrefix` | Whether tags include `v` prefix (e.g., `v1.2.3`) | `true` |
| `release` | GitHub Release creation: `true`, `draft`, or `false`. Use `draft` for immutable releases | `true` |
| `changelog` | Enable/disable changelog updates | `true` |
| `command` | Command to run before release (for build/file modifications) | - |
| `majorLabels` | Custom labels for major version increment | `tagpr:major` |
| `minorLabels` | Custom labels for minor version increment | `tagpr:minor` |
| `commitPrefix` | Customize commit message prefix | `[tagpr]` |

### GitHub Actions Workflow

See [references/workflow-templates.md](references/workflow-templates.md) for workflow templates.

### Goreleaser Integration

For Go projects using goreleaser, see [references/goreleaser-integration.md](references/goreleaser-integration.md).

## Version Determination

tagpr determines the next version using:

1. **Label-based**: If merged PRs have labels:
   - `tagpr:major` or `major` → Major version bump
   - `tagpr:minor` or `minor` → Minor version bump
   - No label → Patch version bump

2. **Manual override**: Edit the version file or apply labels to the tagpr PR

## Verification Steps

After setup, verify by:

1. Push a commit to the release branch
2. Check that tagpr creates a release PR
3. Merge the release PR
4. Verify that a tag and GitHub Release are created
