---
name: creating-makefile
description: Scaffold or review Makefiles following org conventions. Use when creating a new Makefile, auditing an existing one, or adding recipes to a project. Auto-detects project type from the working directory.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash
  argument-hint: "[project-type-or-makefile-path]"
  stability: stable
  content-hash: sha256:99b10f5578553e5aa4ded222da3c8955c843a3ab52aa3bcd8b007c40ac35a5a4
  last-verified-cc-version: 1.0.34
---

# Creating Makefiles

**Target**: $ARGUMENTS

Creates or reviews a **rigorous, consistent Makefile** following org conventions.

## References

- Required structure + patterns: `references/makefile-conventions.md`
- CI linter script: `references/lint-makefile.sh`
- Language-specific recipe templates: `references/scaffold-*.md`

## Required Structure (all project types)

Every Makefile must have these elements in order:

```makefile
# Header comment describing the project
# Run `make` to see all available recipes.

# GNU Make version guard
ifeq ($(filter oneshell,$(.FEATURES)),)
$(error GNU Make >= 3.82 required (.ONESHELL). macOS ships 3.81 — install via: brew install make, then use gmake)
endif

.SILENT:
.ONESHELL:
.PHONY: \
    recipe_a recipe_b \
    help
.DEFAULT_GOAL := help

# -- config --
VERBOSE ?= 0
ifeq ($(VERBOSE),0)
  # quiet flags per tool
endif
```

## Conventions

- **snake_case** for all recipe names
- **`## description`** comment on every public recipe (for help output)
- **`# MARK: SECTION`** to group related recipes
- **`setup_*`** prefix for installation recipes (never bare `install`)
- **`validate`** chains `lint` + `test` (when both exist)
- **Idempotent setup**: `command -v X >/dev/null || install X`
- **No hardcoded paths** — use variables at top of file
- **`VERBOSE ?= 0`** with conditional quiet flags per tool
- **Zero-sudo installs** — use `~/.local/bin` or `~/.local/share/<tool>`, never `sudo apt/dnf`
- **`export PATH=...`** inside recipes that invoke tools installed to a non-default prefix (e.g. user-local npm)

## Approach

1. **Detect** what kind of project this is — look at build files, dependency manifests, and source file types in the working directory. If `$ARGUMENTS` names a type, use that instead.
2. **Find a scaffold** — list `references/scaffold-*.md` in this skill's directory. If one matches the detected project type, read it for language-specific recipe templates. If none matches, build recipes from first principles using the conventions above.
3. **Merge** the scaffold's recipes with the required structure (version guard, .SILENT, .ONESHELL, .PHONY, help, config variables). The scaffold provides the MARK sections and recipe bodies; the required structure wraps them.
4. **Check** if a Makefile already exists — if yes, review it against conventions and the scaffold. If no, create one from the merged template.
5. **Lint** with `references/lint-makefile.sh` — fix any failures.
6. **Verify** `make help` renders all recipes, `make validate` (or `make lint`) runs clean.

The scaffold files shipped with this skill are **starting points, not an exhaustive list**. For a project type without a matching scaffold, apply the same conventions and recipe structure — the patterns (setup, dev, help) are universal.

## Help Recipe (include in every Makefile)

```makefile
help:  ## Show available recipes grouped by section
    echo "Usage: make [recipe]"
    echo ""
    awk '/^# MARK:/ { \
        section = substr($$0, index($$0, ":")+2); \
        printf "\n\033[1m%s\033[0m\n", section \
    } \
    /^[a-zA-Z0-9_-]+:.*?##/ { \
        helpMessage = match($$0, /## (.*)/); \
        if (helpMessage) { \
            recipe = $$1; \
            sub(/:/, "", recipe); \
            printf "  \033[36m%-22s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH) \
        } \
    }' $(MAKEFILE_LIST)
```

## Quality Gates

- [ ] GNU Make version guard present
- [ ] `.SILENT`, `.ONESHELL`, `.DEFAULT_GOAL := help` set
- [ ] Full `.PHONY` list up front
- [ ] Every recipe has `## description` comment
- [ ] `# MARK:` sections group related recipes
- [ ] `snake_case` recipe names only
- [ ] `help` recipe with standard awk pattern
- [ ] `VERBOSE ?= 0` with quiet mode support
- [ ] No `sudo` in setup recipes (user-local installs only)
- [ ] `lint-makefile.sh` passes
