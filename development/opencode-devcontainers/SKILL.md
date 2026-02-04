---
name: opencode-devcontainers
description: Concurrent branch development with devcontainers using clone-based isolation
---

# OpenCode DevContainers

When working on projects with devcontainers, use the `/devcontainer` command for concurrent branch development instead of git worktrees.

## Why Not Git Worktrees?

Git worktrees don't work inside devcontainers because:
- The `.git` file in a worktree references a path outside the mounted directory
- Devcontainers mount a single directory, breaking the worktree link

## Using /devcontainer in OpenCode

### Start Working on a New Branch

```
/devcontainer feature-x
```

This:
1. Creates a clone at `~/.cache/devcontainer-clones/myapp/feature-x/`
2. Uses `git clone --reference --dissociate` to save disk space
3. Checks out the branch (creates it if needed)
4. Assigns a unique port (13000-13099)
5. Starts the devcontainer with an override config
6. Routes subsequent commands to the container

### Managing Sessions

```
/devcontainer              # Show current status
/devcontainer feature-x    # Target feature-x branch
/devcontainer myapp/main   # Target specific repo/branch
/devcontainer off          # Disable, run commands on host
```

### Command Routing

When a devcontainer is targeted:
- Most commands run inside the container automatically
- Git commands still run on host (repo is mounted)
- Prefix with `HOST:` to force host execution

### Clone Directory Structure

```
~/.cache/devcontainer-clones/
  myapp/
    main/           # Clone for main branch
    feature-x/      # Clone for feature-x branch
    feature-y/      # Clone for feature-y branch
  other-repo/
    main/
```

### Port Assignments

Ports are tracked in `~/.cache/opencode-devcontainers/ports.json`:

```json
{
  "/Users/me/.cache/devcontainer-clones/myapp/main": {
    "port": 13000,
    "repo": "myapp",
    "branch": "main"
  },
  "/Users/me/.cache/devcontainer-clones/myapp/feature-x": {
    "port": 13001,
    "repo": "myapp",
    "branch": "feature-x"
  }
}
```

### Best Practices

1. **One branch per clone**: Each branch gets its own isolated environment
2. **Clean up after merge**: Use `/devcontainer off` when done with a branch
3. **Port range**: Default 13000-13099 supports up to 100 concurrent instances

### Integration with opencode-pilot

For automated issue processing, configure your `repos.yaml`:

```yaml
repos:
  myorg/myrepo:
    session:
      prompt_template: |
        /devcontainer issue-{number}

        {title}

        {body}
```

This starts an isolated devcontainer for each issue automatically.
