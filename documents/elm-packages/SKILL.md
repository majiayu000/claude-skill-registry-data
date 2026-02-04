---
name: elm-packages
description: >
  Look up Elm package documentation, list project dependencies, search the
  Elm package registry, and read module exports. Use when working with Elm
  projects, elm.json files, or needing information about Elm packages.
allowed-tools: Read, Bash, Glob
---

# Capabilities

All capabilities are exposed as bash scripts in the `scripts/` directory relative to this skill.

If scripts fail, see ./TROUBLESHOOTING.md for diagnosis and installation help.

```bash
# List installed packages (elm.json dependencies)
./scripts/list-installed-packages.sh

# Search the Elm package repository
./scripts/search-packages.sh "search query"

# Get README documentation for a package
./scripts/get-readme.sh {author} {name} {version}

# List package modules or module exports
./scripts/get-exports.sh {author} {name} {version}
./scripts/get-exports.sh {author} {name} {version} {ModuleName}

# Get full docs for a specific export
./scripts/get-export-docs.sh {author} {name} {version} {ModuleName} {exportName}
```

## Common Workflows

### Looking up docs for an installed package

1. Run `list-installed-packages.sh` to get author/name/version
2. Run `get-exports.sh` to list modules, then exports
3. Run `get-export-docs.sh` for full documentation on a specific export

### Discovering new packages

1. Run `search-packages.sh` with keywords to find packages
2. Run `get-readme.sh` for an overview
3. Run `get-exports.sh` to explore the API
